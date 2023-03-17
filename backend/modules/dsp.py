import logging

from typing import Callable

from tornado import gen
from tornado.iostream import IOStream, StreamClosedError
from tornado.options import define, options
from tornado.tcpserver import TCPServer
from modules.dsp_session import DSPSession

# Main class used to listen and communicate with the DSP
# Will listen on port 8081 by default for information being sent from the DSP module
define("dsp-port", default=8081, help="TCP port to listen on for the DSP")
logger = logging.getLogger(__name__)


class DSPServer(TCPServer):
    # Callback functions to be called when a new guitar string pluck message is received
    on_pluck: list[Callable[[float, tuple], None]]

    # Callback functions called when user connects
    on_connect: list[Callable[[tuple, DSPSession], None]]

    # Callback functions called when user disconnects
    on_disconnect: list[Callable[[tuple], None]]

    # Keep track of connections
    connections: dict[tuple, IOStream]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = {}

        self.on_connect = []
        self.on_disconnect = []
        self.on_pluck = []

    @gen.coroutine
    def handle_stream(self, stream, address):
        # Store connection
        assert address not in self.connections  # Shouldn't happen but just in case
        self.connections[address] = stream

        # Start a session for this connection
        session = DSPSession(stream)

        # Call all connect callbacks
        for cb in self.on_connect:
            cb(address, session)

        while True:
            try:
                # Protocol messages are delimited by newlines (future; null bytes)
                # It's up to the DSPSession to handle the rest
                data = yield stream.read_until(b"\n")

                # Attempt to decode a UTF-8 string from the data
                try:
                    decoded_data = data.decode("utf-8").strip()
                except UnicodeError:
                    logger.warning(f"Received invalid UTF-8 data: 0x{data.hex()}")
                    continue  # TODO: send structured error message to DSP?

                # Call the session's recv_message function
                session.recv_message(decoded_data)

                continue

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
                elif command == "INJECT" and (options.debug == True):
                    (socket_address, _, payload) = payload.partition(" ")
                    (ip, _, port) = socket_address.partition(":")

                    lookup_address = (ip, int(port))
                    logger.debug(f"Injecting data to {lookup_address}: '{payload}'")

                    # Make sure connection is being looked up/tracked correctly & exists
                    if lookup_address not in self.connections:
                        yield stream.write(b"ERROR: No connection to that address\n")
                        continue

                    # Forward the data on that stream as bytes, decoded from utf-8
                    yield self.connections[lookup_address].write(
                        payload.encode("utf-8")
                    )
                    logger.debug(f"Sent data to {lookup_address}.")
                else:
                    logger.warning(f"Received unknown command: {command}")
                    yield stream.write(b"UNKNOWN " + command.encode("utf-8") + b"\n")
                    continue  # TODO: send structured error message to DSP?

                # Echo back an acknowledgement
                yield stream.write(b"ACK " + data)

            except StreamClosedError:
                logger.warning(f"Lost client at host {address[0]}:{address[1]}")

                # Exit receive loop
                break
            except Exception as e:
                print(f"Uncaught exception in DSPServer: '{e}'")

                # Exit receive loop
                break

        # Remove from connections
        assert address in self.connections  # Should be there but assumption of course
        del self.connections[address]

        # Call disconnect callbacks
        for cb in self.on_disconnect:
            cb(address)

    # Add a callback function to be called when a user connects. Takes full address and IOStream
    def register_connect_cb(self, cb):
        assert callable(cb)
        self.on_connect.append(cb)

    # Add a callback function to be called when a user disconnects. Takes full address of socket
    def register_disconnect_cb(self, cb):
        assert callable(cb)
        self.on_disconnect.append(cb)
