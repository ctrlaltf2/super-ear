import tornado.web

from tornado.options import options

from modules.dsp import DSPServer
from modules.frontend import FrontendHandler


class SuperEarApplication(tornado.web.Application):
    # TCP server used for DSP
    tcp_server: DSPServer

    def __init__(self, *args, **kwargs):
        super(SuperEarApplication, self).__init__(*args, **kwargs)
        self.tcp_server = DSPServer()
        self.tcp_server.listen(options.dsp_port)
        self.tcp_server.register_pluck_cb(self.on_pluck)
        print("Main id(self):", id(self))

        self.add_handlers(
            r"^.*$",
            [
                (r"/", FrontendHandler),
            ],
        )

    def on_pluck(self, data: float, address: tuple):
        print("String pluck: ", data * 2, "from", address)
        print(f"id(self): {id(self)}")
