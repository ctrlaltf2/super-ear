from typing import Callable

import tornado.websocket
import tornado.escape


class GameSessionSocketHandler(tornado.websocket.WebSocketHandler):
    # on_open is a function callback
    cb_on_open: Callable

    # on_close is a function callback
    cb_on_close: Callable

    # socket for this connection. what's in the tuple depends on what the socket is.
    sock: tuple

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

        # call parent ctor
        super().__init__(*args, **kwargs)

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

        self.cb_on_open(self.sock, self)

    def on_close(self) -> None:
        print("WebSocket closed")
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
