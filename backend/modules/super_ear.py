import logging
import tornado.web

from tornado.options import options
from tornado.iostream import IOStream

from modules.dsp import DSPServer
from modules.frontend import FrontendHandler

logger = logging.getLogger(__name__)


class SuperEarApplication(tornado.web.Application):
    # TCP server used for DSP
    tcp_server: DSPServer

    # Active DSP connections list. socket tuple -> stream
    dsp_connections: dict[tuple, IOStream]

    def __init__(self, *args, **kwargs):
        super(SuperEarApplication, self).__init__(*args, **kwargs)

        self.tcp_server = DSPServer()
        self.tcp_server.listen(options.dsp_port)

        # Register callbacks
        self.tcp_server.register_pluck_cb(self.on_dsp_pluck)
        self.tcp_server.register_connect_cb(self.on_dsp_connect)
        self.tcp_server.register_disconnect_cb(self.on_dsp_disconnect)

        self.dsp_connections = {}

        self.add_handlers(
            r"^.*$",
            [
                (r"/", FrontendHandler),
            ],
        )

    # Callback for when a DSP sends a pluck message
    def on_dsp_pluck(self, string_frequency: float, address: tuple):
        print(
            f"String pluck with frequency {string_frequency} (multiplied by two is {2*string_frequency}) from {address}"
        )

    # Callback function for when a DSP connects
    def on_dsp_connect(self, address: tuple, stream: IOStream):
        logger.info(f"New DSP connection from {address}")

        assert (
            address not in self.dsp_connections
        )  # Assumption made, shouldn't happen I think

        self.dsp_connections[address] = stream

    # Callback function for when a DSP disconnects
    def on_dsp_disconnect(self, address: tuple):
        logger.info(f"Disconnected DSP from {address}")

        assert (
            address in self.dsp_connections
        )  # Assumption made, again shouldn't happen I think

        del self.dsp_connections[address]
