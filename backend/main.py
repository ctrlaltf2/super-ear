import asyncio
import logging

import tornado.options
import tornado.web

import tornado.httpserver
import tornado.ioloop
from tornado.options import define

from app.super_ear import SuperEarApplication
from app.db.init_db import init, bootstrap_db


tornado.options.define(
    "demo",
    default=False,
    help="Demo mode for the application. Disables authentication, assumes you're the demo user.",
)

tornado.options.define(
    "assume_username",
    default="",
    help="Assume this username for the application. Disables authentication, assumes you're the this user.",
)

define("debug", default=False, help="Debug mode for the application")

define("dsp-port", default=8081, help="TCP port to listen on for the DSP")


logger = logging.getLogger(__name__)


async def main():
    tornado.options.parse_command_line()

    print(tornado.options.options.demo, tornado.options.options.assume_username)
    # setup DB
    await init()
    await bootstrap_db()

    # Setup main app
    app = SuperEarApplication()

    # setup HTTP server
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)

    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
