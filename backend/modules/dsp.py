import logging

from typing import Callable

from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.options import define
from tornado.tcpserver import TCPServer

# Main class used to listen and communicate with the DSP
# Will listen on port 8081 by default for information being sent from the DSP module
define("dsp-port", default=8081, help="TCP port to listen on for the DSP")
logger = logging.getLogger(__name__)


class DSPServer(TCPServer):
    # Callback function to be called when a new guitar string pluck message is received
    on_pluck: list[Callable[[str, tuple], None]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_pluck = []

    @gen.coroutine
    def handle_stream(self, stream, address):
        ## Do a simple echo back
        while True:
            try:
                # Implementation-defined algorithm begins here
                data = yield stream.read_until(b"\n")

                # Force a newline at the end
                if not data.endswith(b"\n"):
                    data = data + b"\n"

                # Attempt to decode a UTF-8 string from the data
                try:
                    decoded_data = data.decode("utf-8").strip()
                except UnicodeError:
                    logger.warning(f"Received invalid UTF-8 data: 0x{data.hex()}")
                    continue  # TODO: send error message to DSP?

                # Assume that the data is a guitar string pluck message and call the callback functions
                for cb in self.on_pluck:
                    cb(decoded_data, address)

                # Echo back an acknowledgement
                yield stream.write(b"ACK " + data)

            except StreamClosedError:
                logger.warning(f"Lost client at host {address[0]}:{address[1]}")
                break
            except Exception as e:
                print(e)

    # Add a callback function to be called when a new guitar string pluck message is received
    def register_pluck_cb(self, cb):
        self.on_pluck.append(cb)
