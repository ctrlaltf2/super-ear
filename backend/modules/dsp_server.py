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
    # Callback functions called when user connects
    on_connect: list[Callable[[tuple, DSPSession], None]]

    # Callback functions called when a socket is confirmed to be a DSP device
    on_confirm: list[Callable[[tuple], None]]

    # Callback functions called when user disconnects
    on_disconnect: list[Callable[[tuple], None]]

    # Keep track of connections
    connections: dict[tuple, IOStream]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = {}

        self.on_connect = []
        self.on_confirm = []
        self.on_disconnect = []

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

        confirmed = False

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

                # If the data is empty, ignore it
                if len(decoded_data) == 0:
                    continue

                # Ideally confirmation is cryptographically based, like a credit card (DSP is the credit card),
                # but because this is a ~12 week project, we'll just use a simple string. Security by obscurity, but good enough.
                if not confirmed:
                    # If the data is a identification message, call the confirm callbacks
                    if decoded_data == "SUPEREAR":
                        print(
                            f"Received confirmation from DSP at {address}. Beginning DSP session."
                        )
                        confirmed = True

                        for cb in self.on_confirm:
                            cb(address)

                        continue  # don't call recv_message on first time
                    else:
                        print(
                            f"Received invalid confirmation from TCP socket at {address}. Disconnecting."
                        )
                        break  # disconnect the stream, it's not a DSP

                if confirmed:  # delegate to the DSPSession the message
                    # Call the session's recv_message function
                    session.recv_message(decoded_data)
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

    def register_confirm_cb(self, cb):
        assert callable(cb)
        self.on_confirm.append(cb)
