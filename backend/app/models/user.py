import uuid


from beanie import Document
from pydantic import UUID4
from pydantic.fields import Field
from tornado.options import options

from app.models import Collection, DefaultCollections


class User(Document):
    uuid: UUID4 = Field(default_factory=uuid.uuid4, description="The user's UUID")

    username: str = Field(
        ..., description="The user's username", max_length=32, min_length=3
    )

    hashed_password: str = Field(..., description="The user's hashed password. bcrypt")

    collection: Collection = Field(
        default_factory=lambda: DefaultCollections.get(
            "GuitarTester" if options.demo else "GuitarStandard"
        ),
        description="The collection of the user. Future: Will support multiple.",
    )

    class Settings:
        use_state_management = True  # ez keep objects in sync
