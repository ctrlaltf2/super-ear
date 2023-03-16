import logging
import tornado.web

from tornado.options import options
from tornado.iostream import IOStream
from tornado.web import StaticFileHandler, RedirectHandler

from modules.dsp import DSPServer
from modules.game_session import GameSessionSocketHandler
from modules.srs import SPN

logger = logging.getLogger(__name__)


class SuperEarApplication(tornado.web.Application):
    # TCP server used for DSP
    tcp_server: DSPServer

    # Active DSP connections list. socket.peername tuple -> stream
    dsp_connections: dict[tuple, IOStream]

    # Active game sessions, socket.peername tuple -> game session
    game_sessions: dict[tuple, GameSessionSocketHandler]

    def __init__(self, *args, **kwargs):
        super(SuperEarApplication, self).__init__(*args, **kwargs)

        self.tcp_server = DSPServer()
        self.tcp_server.listen(options.dsp_port)

        # Register callbacks for DSP
        self.tcp_server.register_pluck_cb(self.on_dsp_pluck)
        self.tcp_server.register_connect_cb(self.on_dsp_connect)
        self.tcp_server.register_disconnect_cb(self.on_dsp_disconnect)

        self.dsp_connections = {}
        self.game_sessions = {}

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
                ),
            ],
        )

    def on_game_session_open(self, socket: tuple, session: GameSessionSocketHandler):
        assert socket not in self.game_sessions

        self.game_sessions[socket] = session
        print(f"Opened GS::{socket}")

    def on_game_session_close(self, socket: tuple):
        assert socket in self.game_sessions

        if socket in self.game_sessions:
            del self.game_sessions[socket]

        print(f"Closed GS::{socket}")

    def on_game_session_message(self, socket: tuple, message: str):
        assert socket in self.game_sessions

        print(f"Message from GS::{socket}: {message}")

    # Callback for when a DSP sends a pluck message
    def on_dsp_pluck(self, string_frequency: float, address: tuple):
        print(
            f"String pluck with frequency {string_frequency} (multiplied by two is {2*string_frequency}) from {address}"
        )
        note_played = SPN.from_freq(string_frequency)
        dist = abs(SPN.from_str("A4") - note_played)
        print(
            f"Note was a {SPN.from_freq(string_frequency)} which is {dist} semitones from {SPN.from_str('A4')}."
        )

    # Callback function for when a DSP connects
    def on_dsp_connect(self, address: tuple, stream: IOStream):
        logger.info(f"New DSP connection from {address}")

        assert (
            address not in self.dsp_connections
        )  # Assumption made, shouldn't happen I think

        self.dsp_connections[address] = stream

    # Callback function for when a DSP disconnects
    def on_dsp_disconnect(self, address: tuple):
        logger.info(f"Disconnected DSP from {address}")

        assert (
            address in self.dsp_connections
        )  # Assumption made, again shouldn't happen I think

        del self.dsp_connections[address]
