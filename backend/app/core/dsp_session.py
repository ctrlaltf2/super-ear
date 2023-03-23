from __future__ import annotations

import logging

from tornado.iostream import IOStream

# python moment: https://www.stefaanlippens.net/circular-imports-type-hints-python.html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.game_session import GameSessionSocketHandler


logger = logging.getLogger(__name__)


# lifecycle managed automatically for each TCP Socket session, i.e. object created when DSP connects, destroyed when DSP disconnects
# socket is a confirmed DSP device
class DSPSession:
    # Underlying IOStream for the socket connection
    stream: IOStream

    # Paired game session
    game_session: GameSessionSocketHandler | None

    # Called on creation of the TCP socket session
    def __init__(self, stream: IOStream):
        self.stream = stream
        self.game_session = None

    # Called on deletion of the TCP socket session
    def __del__(self):
        # TODO: Signal unpair to game session?
        return

    def _send_to_game_session(self, tp: str, data):
        if self.game_session is None:
            print("tried to send to game session, it was none")
            return

        self.game_session.send_frontend_message(tp, data)

    # Sends a message to the DSP
    def send_message(self, msg: str):
        # ensure newline at end
        if not msg.endswith("\n"):
            msg += "\n"

        # convert to bytes
        msg_b = msg.encode("utf-8")

        self.stream.write(msg_b)

    # Called when a message is received from the DSP
    async def recv_message(self, msg: str):
        logger.debug(f"DSPSession Received message: {msg}")

        typ, _, payload = msg.strip().partition(" ")

        valid_typ = ["play"]

        if typ not in valid_typ:
            self.send_message(f"error invalid message type {typ}")
            return

        match typ:
            case "play":
                await self._handle_play(payload)
                return

        assert False, f"forgot to handle case {typ}"

    async def _handle_play(self, payload: str):
        print("DSPSession::_handle_play")
        logger.debug(f"DSPSession::_handle_play({payload})")

        if self.game_session is None:
            self.send_message("error no game session")
            return

        try:
            payload_as_float = float(payload)
        except ValueError:
            self.send_message("error invalid payload (should be float)")
            return

        lolwhat = self.game_session._process_message("play", payload_as_float)
        print("type lolwhat = ", type(lolwhat))
        await lolwhat

    def pair(self, game_session: GameSessionSocketHandler):
        assert self.game_session is None
        self.game_session = game_session
        self._send_to_game_session("info", "Hello from DSP session")

    def unpair(self):
        self.game_session = None
