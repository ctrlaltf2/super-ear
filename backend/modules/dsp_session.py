from __future__ import annotations

from tornado.iostream import IOStream

from enum import Enum

# python moment: https://www.stefaanlippens.net/circular-imports-type-hints-python.html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.game_session import GameSessionSocketHandler


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
        print(f"Sending to game session: {tp} {data}")
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
    def recv_message(self, msg: str):
        print(f"DSPSession Received message: {msg}")

    def pair(self, game_session: GameSessionSocketHandler):
        print("DSPSession::pair()")
        assert self.game_session is None
        self.game_session = game_session
        self._send_to_game_session("info", "Hello from DSP session")

    def unpair(self):
        self.game_session = None
