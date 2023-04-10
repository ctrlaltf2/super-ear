import datetime

import pytz

from pydantic import BaseModel
from pydantic.fields import Field


class HistoryEvent(BaseModel):
    time: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=pytz.utc),
        description="The time the event happened",
    )

    answer: str = Field(..., description="The answer the user gave")

    ease_factor: float = Field(..., description="The ease factor of the review item")

    review_offset: datetime.timedelta = Field(
        ...,
        description="The offset from the last review. This is the time between the review and the due date. negative is late.",
    )
