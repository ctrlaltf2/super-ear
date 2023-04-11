import datetime

import pytz

from pydantic import BaseModel
from pydantic.fields import Field

from app.models.review_item import ReviewState


class HistoryEvent(BaseModel):
    time: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=pytz.utc),
        description="The time the event happened",
    )

    answer: str = Field(..., description="The answer the user gave")

    ease_factor: float = Field(..., description="The ease factor of the review item")

    review_offset: float = Field(
        ...,
        description="The offset from the last review in hours. This is the time between the review and the due date. negative is late.",
    )

    state: ReviewState = Field(..., description="The state of the review item")
