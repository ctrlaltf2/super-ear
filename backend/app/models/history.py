from typing import Dict, List

from beanie import Document
from pydantic import UUID4
from pydantic.fields import Field

from app.models.history_event import HistoryEvent


class ReviewHistory(Document):
    user_uuid: UUID4 = Field(..., description="The user who reviewed the notes")

    events: Dict[str, List[HistoryEvent]] = Field(
        default_factory=dict,
        description="The events that happened during the review. str(track (string) number + SPN name) -> events",
    )

    class Settings:
        use_state_management = True
