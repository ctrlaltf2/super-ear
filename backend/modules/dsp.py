import logging

from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.options import define
from tornado.tcpserver import TCPServer

# Main class used to listen and communicate with the DSP
# Will listen on port 8081 by default for information being sent from the DSP module
define("dsp-port", default=8081, help="TCP port to listen on for the DSP")
logger = logging.getLogger(__name__)


class DSPServer(TCPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_recv = []
        # self.on_note_schedule = on_note_schedule

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

                yield stream.write(data)

            except StreamClosedError:
                logger.warning(f"Lost client at host {address[0]}:{address[1]}")
                break
            except Exception as e:
                print(e)
