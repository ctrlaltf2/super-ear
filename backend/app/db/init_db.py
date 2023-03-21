from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.user import User


async def init() -> None:
    print("Initializing to MongoDB @", settings.MONGODB_URI)

    client = AsyncIOMotorClient(str(settings.MONGODB_URI))

    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User],
    )
