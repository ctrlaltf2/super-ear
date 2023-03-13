import tornado.websocket


class GameSessionSocketHandler(tornado.websocket.WebSocketHandler):
    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        print("WebSocket opened")

    def on_close(self):
        print("WebSocket closed")

    def on_message(self, message):
        print("WebSocket message:", message)
