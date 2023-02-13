import logging

import tornado.web

import tornado.httpserver
import tornado.ioloop
from tornado.options import options

from modules.super_ear import SuperEarApplication
from modules.dsp import DSPServer


logger = logging.getLogger(__name__)


def tcpServer():
    server = DSPServer()
    server.listen(options.dsp_port)
    return server


if __name__ == "__main__":
    options.parse_command_line()
    app = SuperEarApplication()

    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
