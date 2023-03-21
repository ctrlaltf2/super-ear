import asyncio
import logging

import tornado.web

import tornado.httpserver
import tornado.ioloop
from tornado.options import options, define

from app.super_ear import SuperEarApplication
from app.db.init_db import init


define("debug", default=False, help="Debug mode for the application")
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    options.parse_command_line()

    # setup DB
    asyncio.get_event_loop().run_until_complete(init())

    # Setup main app
    app = SuperEarApplication()

    # setup HTTP server
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)

    # run
    tornado.ioloop.IOLoop.current().start()
