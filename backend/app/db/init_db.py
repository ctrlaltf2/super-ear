import bcrypt
import secrets
import string

import tornado.escape

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.user import User
from app.models.history import ReviewHistory

_initiated = False


async def init() -> None:
    global _initiated

    print("Initializing to MongoDB @", settings.MONGODB_URI)

    client = AsyncIOMotorClient(str(settings.MONGODB_URI))

    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User, ReviewHistory],
    )

    _initiated = True


# Temporary, bootstraps the DB with a user
async def bootstrap_db():
    if not _initiated:
        await init()

    # check for the demo user
    demo_user = await User.find_one(User.username == "demo")

    if demo_user is not None:
        print("Demo user already exists")
        return

    print("Bootstrapping DB with demo user")

    # make a demo user and insert into DB
    corpus = string.ascii_letters + string.digits
    password = "".join(secrets.choice(corpus) for _ in range(16))
    print(f"Demo user password: '{password}'")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    demo_user = User(
        username="demo",
        hashed_password=tornado.escape.to_unicode(hashed_password),
    )
    await demo_user.insert()
