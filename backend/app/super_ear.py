import logging
import random

import tornado.web

from bidict import (
    bidict,
    ValueDuplicationError,
    KeyDuplicationError,
)
from collections import deque

from tornado.options import options
from tornado.web import StaticFileHandler, RedirectHandler, OutputTransform

from app.core.dsp_server import DSPServer
from app.core.game_session import GameSessionSocketHandler
from app.core.dsp_session import DSPSession
from app.core.srs.spn import SPN

logger = logging.getLogger(__name__)


# Responsible for managing the lifecycle of DSP sessions and game sessions, and pairing management
class SuperEarApplication(tornado.web.Application):
    # TCP server used for DSP
    tcp_server: DSPServer

    # Active DSP connections list. socket.peername tuple -> stream
    dsp_sessions: dict[tuple, DSPSession]

    # Active game sessions, socket.peername tuple -> game session
    game_sessions: dict[tuple, GameSessionSocketHandler]

    # mapping, dsp address <-> game session address
    pairings: bidict[tuple, tuple]

    # unpaired DSPs. FIFO queue until pairing is worked out
    unpaired_dsp: deque[tuple]

    # DSPServer must first confirm that the TCP socket connection is in fact a DSP.
    # This is the set of unconfirmed DSPs.
    unconfirmed_dsps: set[tuple]

    # unpaired game sessions. FIFO queue until pairing is worked out
    unpaired_game_sessions: deque[tuple]

    # Generate an open string sequence used for pairing
    def _generate_openstring_sequence(self) -> list[int]:
        # Generate a random list of numbers 1-6 with replacement
        pair_code = [random.randint(1, 6) for _ in range(5)]

        return pair_code

    # Convert to SPN, mapping numbers to the corresponding guitar string in standard tuning
    def _openstring_id_to_SPN(self, openstring_id: int) -> SPN:
        str_to_note = {
            1: "E4",
            2: "B3",
            3: "G3",
            4: "D3",
            5: "A2",
            6: "E2",
        }

        return SPN.from_str(str_to_note[openstring_id])

    # attempt pairing of a DSP and a game session. returns true if successful
    async def _pair(self, dsp_address: tuple, game_session_address: tuple) -> bool:
        print("SuperEarApplication::_pair()")
        try:
            self.pairings[dsp_address] = game_session_address

            game_session = self.game_sessions[game_session_address]
            dsp_session = self.dsp_sessions[dsp_address]

            await game_session.pair(dsp_session)
            dsp_session.pair(game_session)
        except KeyDuplicationError:
            logger.warning(
                f"Unexpected duplicate mapping from {dsp_address}, one to {game_session_address}"
            )
            raise
        except ValueDuplicationError:
            logger.warning(
                f"Unexpected duplicate mapping to {game_session_address}, one from {dsp_address}"
            )
            raise
        except Exception as e:
            logger.warning(f"Unexpected exception {type(e)}")
            raise

        return True

    def _is_paired(self, socket: tuple) -> bool:
        return socket in self.pairings or socket in self.pairings.inverse

    # get the paired game session, if it exists
    def get_paired_game_session(
        self, dsp_address: tuple
    ) -> GameSessionSocketHandler | None:
        if dsp_address in self.pairings:
            return self.game_sessions[self.pairings[dsp_address]]
        else:
            return None

    # get the paired DSP for a game session, if it exists
    def get_paired_dsp_session(self, game_session_address: tuple) -> DSPSession | None:
        if game_session_address in self.pairings.inverse:
            return self.dsp_sessions[self.pairings.inverse[game_session_address]]
        else:
            return None

    def __init__(self, *args, **kwargs):
        super(SuperEarApplication, self).__init__(*args, **kwargs)

        self.tcp_server = DSPServer()
        self.tcp_server.listen(options.dsp_port)

        # Register callbacks for DSP
        self.tcp_server.register_connect_cb(self.on_dsp_connect)
        self.tcp_server.register_confirm_cb(self.on_dsp_confirm)
        self.tcp_server.register_disconnect_cb(self.on_dsp_disconnect)

        self.dsp_sessions = {}
        self.game_sessions = {}
        self.pairings = bidict()

        self.unpaired_dsp = deque()
        self.unpaired_game_sessions = deque()
        self.unconfirmed_dsps = set()

        class WhyDoYouSendServerTokens(OutputTransform):
            def transform_first_chunk(self, status_code, headers, chunk, _):
                headers.pop("Server")
                return status_code, headers, chunk

        super().__init__([], transforms=[WhyDoYouSendServerTokens])

        self.add_handlers(
            r"^.*$",
            [
                (
                    r"/game_session",
                    GameSessionSocketHandler,
                    {
                        "on_open": self.on_game_session_open,
                        "on_close": self.on_game_session_close,
                        "on_message": self.on_game_session_message,
                    },
                ),
                (r"/play", RedirectHandler, {"url": "/"}),
                (
                    r"/(.*)",
                    StaticFileHandler,
                    {"path": "/super-ear/srv", "default_filename": "index.html"},
                ),  # TODO: basic login handler here on the static side, sets a cookie. Cookie used in GameSessionSocketHandler
            ],
        )

    async def on_game_session_open(
        self, socket: tuple, session: GameSessionSocketHandler
    ):
        assert (
            socket not in self.game_sessions
        ), "game session already exists (duplicate call or duplicate socket?)"

        self.game_sessions[socket] = session

        self.unpaired_game_sessions.appendleft(socket)
        await self.attempt_pairings()

        print(f"Opened GS::{socket}")

    def on_game_session_message(self, socket: tuple, message: dict):
        assert (
            socket in self.game_sessions
        ), "game session does not exist (race condition?)"

        print(f"Message from GS::{socket}: {message}")

    async def on_game_session_close(self, socket: tuple):
        assert (
            socket in self.game_sessions
        ), "game session does not exist, (duplicate call, socket, or race condition?)"

        if socket in self.game_sessions:
            del self.game_sessions[socket]

        if socket in self.unpaired_game_sessions:
            self.unpaired_game_sessions.remove(socket)

        # unpair if necessary
        if socket in self.pairings.inverse:
            dsp_sock = self.pairings.inverse[socket]

            # alert the paired dsp that it's been unpaired
            if dsp_sock in self.dsp_sessions:
                self.dsp_sessions[dsp_sock].unpair()

            assert (
                dsp_sock not in self.unconfirmed_dsps
            ), "DSP was unpaired but still unconfirmed"

            # Set it back into pairing mode (TODO: If sequence-based pair implemented, this will need to be changed)
            self.unpaired_dsp.appendleft(dsp_sock)

            del self.pairings.inverse[socket]

        await self.attempt_pairings()
        print(f"Closed GS::{socket}")

    # Callback function for when a DSP connects
    def on_dsp_connect(self, socket: tuple, session: DSPSession):
        logger.info(f"New DSP connection from {socket}")

        assert (
            socket not in self.dsp_sessions
        ), "duplicate DSP socket detected"  # Assumption made, shouldn't happen I think

        self.dsp_sessions[socket] = session

        self.unconfirmed_dsps.add(socket)

        print(f"Opened TCP::{socket}")

    # called when the DSPServer confirms (to the best of its ability) that a TCP socket is a DSP
    async def on_dsp_confirm(self, socket: tuple):
        print("SE::DSP confirmed")
        # Remove from the unconfirmed set
        assert (
            socket in self.unconfirmed_dsps
        ), "DSP was double-confirmed or wasn't added to unconfirmed list"
        self.unconfirmed_dsps.remove(socket)

        # Add it to the unpaired one
        self.unpaired_dsp.appendleft(socket)

        # and try pairings
        await self.attempt_pairings()

    # Callback function for when a DSP disconnects
    async def on_dsp_disconnect(self, socket: tuple):
        logger.info(f"Disconnected DSP from {socket}")

        assert (
            socket in self.dsp_sessions
        ), "Possible double-remove detected, or dsp_session didn't track socket"  # Assumption made, again shouldn't happen I think

        if socket in self.dsp_sessions:
            del self.dsp_sessions[socket]

        if socket in self.unconfirmed_dsps:
            self.unconfirmed_dsps.remove(socket)

        if socket in self.unpaired_dsp:
            self.unpaired_dsp.remove(socket)

        # unpair if necessary
        if socket in self.pairings:
            game_session_sock = self.pairings[socket]

            # alert the paired game session that it's been unpaired
            if game_session_sock in self.game_sessions:
                await self.game_sessions[game_session_sock].unpair()

            # Set it back into pairing mode (TODO: If sequence-based pair implemented, this will need to be changed)
            self.unpaired_game_sessions.appendleft(game_session_sock)

            del self.pairings[socket]

        await self.attempt_pairings()
        print(f"Closed DSP::{socket}")

    async def attempt_pairings(self):
        print("Attempting pairings")
        print(self.unpaired_dsp, self.unpaired_game_sessions)
        # Pair on a FIFO basis
        while len(self.unpaired_dsp) > 0 and len(self.unpaired_game_sessions) > 0:
            dsp_sock = self.unpaired_dsp.pop()
            game_session_sock = self.unpaired_game_sessions.pop()

            print("Pairing", dsp_sock, game_session_sock)

            paired = await self._pair(dsp_sock, game_session_sock)
            assert paired, "Pairing failed"
            print(f"Paired DSP::{dsp_sock} with GS::{game_session_sock}")
