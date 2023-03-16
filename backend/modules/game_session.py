from typing import Callable

import tornado.websocket


class GameSessionSocketHandler(tornado.websocket.WebSocketHandler):
    cb_on_open: Callable

    # onclose is a function callback
    cb_on_close: Callable

    # socket for this connection. what's in the tuple depends on what the socket is.
    sock: tuple

    def __init__(self, *args, **kwargs):
        print("GameSocket::__init__()")

        assert "on_open" in kwargs
        assert "on_close" in kwargs
        assert "on_message" in kwargs

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

    def open(self):
        print("WebSocket opened")

        assert self.ws_connection is not None
        assert self.ws_connection.stream is not None
        assert self.ws_connection.stream.socket is not None

        self.sock = self.ws_connection.stream.socket.getpeername()

        self.cb_on_open(self.sock, self)

    def on_close(self):
        print("WebSocket closed")
        self.cb_on_close(self.sock)

    def on_message(self, message):
        print("WebSocket message:", message)
        self.cb_on_message(self.sock, message)
