from tornado.iostream import IOStream


class DSPSession:
    # Underlying IOStream for the socket connection
    stream: IOStream

    def __init__(self, stream: IOStream):
        self.stream = stream

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
