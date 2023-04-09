import bcrypt

import tornado.escape
import tornado.ioloop
import tornado.web

from app.models.user import User


class BaseAuthHandler(tornado.web.RequestHandler):
    async def prepare(self):
        user_id = self.get_secure_cookie("user")

        if user_id:
            self.user_id = user_id


class AuthCreateHandler(BaseAuthHandler):
    @tornado.web.authenticated
    async def post(self):
        # must be logged in to create users
        if not self.user_id:
            self.set_status(401)
            return

        staged_username = tornado.escape.utf8(self.get_argument("username"))

        # check not already created
        user = await User.find_one(User.username == staged_username)

        if user is not None:
            self.set_status(400)
            return

        # create user
        password = tornado.escape.utf8(self.get_argument("password"))
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User(
            username=tornado.escape.to_unicode(staged_username),
            hashed_password=tornado.escape.to_unicode(hashed_password),
        )

        await user.insert()


class AuthLoginHandler(BaseAuthHandler):
    async def post(self):
        username = tornado.escape.utf8(self.get_argument("username"))
        password = tornado.escape.utf8(self.get_argument("password"))

        user = await User.find_one(User.username == username)

        if user is None:
            self.set_status(401)
            return

        if not bcrypt.checkpw(password, tornado.escape.utf8(user.hashed_password)):
            self.set_status(401)
            return

        self.set_secure_cookie("user", tornado.escape.to_unicode(user.username))


class AuthLogoutHandler(BaseAuthHandler):
    async def post(self):
        self.clear_cookie("user")
