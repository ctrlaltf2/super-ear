import asyncio

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("get")
        self.write("Hello, world")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ]
    )


async def main():
    app = make_app()
    app.listen(8000)
    await asyncio.Event().wait()


if __name__ == "__main__":
    print("Starting...")
    asyncio.run(main())
