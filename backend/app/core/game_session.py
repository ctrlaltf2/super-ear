from __future__ import annotations

import json

from enum import Enum
from typing import Callable

import tornado.websocket
import tornado.escape

# python moment: https://www.stefaanlippens.net/circular-imports-type-hints-python.html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.dsp_session import DSPSession


class GameSessionSocketHandler(tornado.websocket.WebSocketHandler):
    class SessionState(Enum):
        WAITING_FOR_DSP = "waiting_for_dsp"
        PAIRED = "paired"

        def __str__(self):
            return self.value

    # on_open is a function callback
    cb_on_open: Callable

    # on_close is a function callback
    cb_on_close: Callable

    # socket for this connection. what's in the tuple depends on what the socket is.
    sock: tuple

    # Paired DSP session
    dsp_session: DSPSession | None

    # Pairing code, assigned by SuperEarApplication
    _pair_code: list[int] | None

    # State of the session
    _state: SessionState

    def __init__(self, *args, **kwargs):
        print("GameSocket::__init__()")

        assert "on_open" in kwargs
        assert callable(kwargs["on_open"])

        assert "on_close" in kwargs
        assert callable(kwargs["on_close"])

        assert "on_message" in kwargs
        assert callable(kwargs["on_message"])

        self.cb_on_open = kwargs["on_open"]
        self.cb_on_close = kwargs["on_close"]
        self.cb_on_message = kwargs["on_message"]

        # oops
        del kwargs["on_open"]
        del kwargs["on_close"]
        del kwargs["on_message"]

        self.dsp_session = None
        self._pair_code = None

        # call parent ctor
        super().__init__(*args, **kwargs)

    def _set_state(self, state: SessionState):
        self._state = state
        self.send_frontend_message("state", str(state))

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def set_default_headers(self) -> None:
        self.set_header("Server", "")

    def open(self) -> None:
        print("WebSocket opened")

        assert self.ws_connection is not None
        assert self.ws_connection.stream is not None
        assert self.ws_connection.stream.socket is not None

        self.sock = self.ws_connection.stream.socket.getpeername()

        self._set_state(self.SessionState.WAITING_FOR_DSP)
        assert (
            self._state == self.SessionState.WAITING_FOR_DSP
        ), "post: set state should set the state"

        self.cb_on_open(self.sock, self)

    def on_close(self) -> None:
        print("WebSocket closed")
        # TODO: Signal unpair to connected DSP
        self.cb_on_close(self.sock)

    def on_message(self, message: str) -> None:
        assert self.ws_connection is not None
        assert self.ws_connection.stream is not None
        assert self.ws_connection.stream.socket is not None
        assert (
            self.ws_connection.stream.socket.getpeername() == self.sock
        )  # should be turned off for prod

        # decode JSON message
        try:
            message = tornado.escape.json_decode(message)
        except ValueError:
            return

        print(f"Got message: {message}")

        # validate message
        if not isinstance(message, dict):
            return

        if "type" not in message:
            return

        if "payload" not in message:
            return

        self.cb_on_message(self.sock, message)

    def assign_pair_code(self, pair_code: list[int]):
        assert self._pair_code is None
        self._pair_code = pair_code

    def send_to_dsp(self, msg: str):
        print(f"Sending to DSP: {msg}")
        if self.dsp_session is None:
            return

        assert self._state == self.SessionState.PAIRED

        self.dsp_session.send_message(msg)

    def pair(self, dsp_session: DSPSession) -> None:
        assert self.dsp_session is None, "Already paired"
        self.dsp_session = dsp_session
        self._set_state(self.SessionState.PAIRED)

        assert (
            self._state == self.SessionState.PAIRED
        ), "post: set state should set the state"

    def unpair(self):
        self.dsp_session = None
        self._set_state(self.SessionState.WAITING_FOR_DSP)

        assert (
            self._state == self.SessionState.WAITING_FOR_DSP
        ), "post: set state should set the state"

    # Sends a message to the connected frontend client
    def send_frontend_message(self, type: str, data: float | int | str | list | dict):
        print("Sending message to frontend")
        msg = json.dumps({"type": type, "payload": data})
        self.write_message(msg)
