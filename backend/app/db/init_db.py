from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.user import User

_initiated = False


async def init() -> None:
    global _initiated

    print("Initializing to MongoDB @", settings.MONGODB_URI)

    client = AsyncIOMotorClient(str(settings.MONGODB_URI))

    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User],
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
    demo_user = User(username="demo")
    await demo_user.insert()
