import asyncio
import logging

import tornado.web

import tornado.httpserver
import tornado.ioloop
from tornado.options import define

from app.super_ear import SuperEarApplication
from app.db.init_db import init, bootstrap_db


define("debug", default=False, help="Debug mode for the application")

logger = logging.getLogger(__name__)


async def main():
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
