import logging

from typing import Callable

from tornado import gen
from tornado.iostream import IOStream, StreamClosedError
from tornado.options import define, options
from tornado.tcpserver import TCPServer

# Main class used to listen and communicate with the DSP
# Will listen on port 8081 by default for information being sent from the DSP module
define("dsp-port", default=8081, help="TCP port to listen on for the DSP")
logger = logging.getLogger(__name__)


class DSPServer(TCPServer):
    # Callback functions to be called when a new guitar string pluck message is received
    on_pluck: list[Callable[[float, tuple], None]]

    # Callback functions called when user connects
    on_connect: list[Callable[[tuple, IOStream], None]]

    # Callback functions called when user disconnects
    on_disconnect: list[Callable[[tuple], None]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_pluck = []
        self.on_connect = []
        self.on_disconnect = []

    @gen.coroutine
    def handle_stream(self, stream, address):
        # Call all connect callbacks
        for cb in self.on_connect:
            cb(address, stream)

        while True:
            try:
                # Implementation-defined algorithm begins here
                data = yield stream.read_until(b"\n")

                # Attempt to decode a UTF-8 string from the data
                try:
                    print("trying")
                    decoded_data = data.decode("utf-8").strip()
                except UnicodeError:
                    logger.warning(f"Received invalid UTF-8 data: 0x{data.hex()}")
                    continue  # TODO: send structured error message to DSP?

                # Parse command & payload
                (command, _, payload) = decoded_data.partition(" ")

                if command == "PLUCK":
                    try:
                        frequency = float(payload)
                    except ValueError:
                        logger.warning(f"Received invalid frequency: {payload}")
                        continue  # TODO: send structured error message to DSP?

                    # call the callback functions for plucking
                    for cb in self.on_pluck:
                        cb(frequency, address)
                else:
                    logger.warning(f"Received unknown command: {command}")
                    yield stream.write(b"UNKNOWN " + command.encode("utf-8") + b"\n")
                    continue  # TODO: send structured error message to DSP?

                # Echo back an acknowledgement
                yield stream.write(b"ACK " + data)

            except StreamClosedError:
                logger.warning(f"Lost client at host {address[0]}:{address[1]}")

                # Call disconnect callbacks
                for cb in self.on_disconnect:
                    cb(address)

                # Exit receive loop
                break
            except Exception as e:
                print(f"Uncaught exception in DSPServer: '{e}'")

    # Add a callback function to be called when a new guitar string pluck message is received
    def register_pluck_cb(self, cb):
        self.on_pluck.append(cb)

    # Add a callback function to be called when a user connects. Takes full address and IOStream
    def register_connect_cb(self, cb):
        self.on_connect.append(cb)

    # Add a callback function to be called when a user disconnects. Takes full address of socket
    def register_disconnect_cb(self, cb):
        self.on_disconnect.append(cb)
