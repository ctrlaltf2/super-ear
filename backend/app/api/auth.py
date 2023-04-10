import bcrypt

import tornado.escape
import tornado.ioloop
import tornado.web

from app.models.user import User


class BaseAuthHandler(tornado.web.RequestHandler):
    async def prepare(self):
        print("auth prepare")
        user_id = self.get_secure_cookie("user")

        print(f"user_id: {user_id}")

        if user_id:
            self.user_id = user_id
        else:
            self.user_id = None


class AuthCreateHandler(BaseAuthHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

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
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    async def post(self):
        username = tornado.escape.to_unicode(self.get_argument("username"))
        password = tornado.escape.to_unicode(self.get_argument("password"))

        user = await User.find_one(User.username == username)

        if user is None:
            print(f"no user with name '{username}'")
            self.set_status(401)
            return

        if not bcrypt.checkpw(
            tornado.escape.utf8(password), tornado.escape.utf8(user.hashed_password)
        ):
            print(f"password '{password}' is bad")
            self.set_status(401)
            return

        self.set_secure_cookie("user", tornado.escape.to_unicode(user.username))


class AuthLogoutHandler(BaseAuthHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    async def post(self):
        self.clear_cookie("user")
