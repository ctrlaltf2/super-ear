import logging

import tornado.web

import tornado.httpserver
import tornado.ioloop
from tornado.options import options, define

from app.super_ear import SuperEarApplication
from app.core.dsp_server import DSPServer


define("debug", default=False, help="Debug mode for the application")
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
