import tornado.web


class FrontendHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
