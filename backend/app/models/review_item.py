from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


# Enum for the three states of a review item; unseen, learning, and reviewing
class ReviewState(Enum):
    # item is totally new
    Unseen = auto()

    # item is being previewed; this is a special state for before the learning phase. gives person time to get familiar with the item.
    Previewing = auto()

    # item is being learned, e.g. reviewing in increasing intervals, but without penalty for failure
    Learning = auto()

    # item is being reviewed. difficulty factor updates now, can be "penalized" for failing.
    Reviewing = auto()


# Class to represent a reviewable item and its associated scheduler parameters
class ReviewItem(BaseModel):
    # Current state of the review item
    state: ReviewState = Field(ReviewState.Unseen, description="review state")

    # Current learning step index
    learning_index: int = Field(0, ge=0, description="current learning index")

    # Learning steps for the item (in minutes)
    # default steps from recommended settings of https://ankiweb.net/shared/info/1250336138 (A ear training Anki deck)
    learning_steps: list[float] = Field(
        default_factory=lambda: [1 / 12, 5 / 12, 2, 10, 60, 300],
        description="learning steps, in minutes",
    )

    # ReviewItem content
    content: str = Field(..., description="content of the review item")

    # Last review time (minutes delta since collection's epoch)
    last_review: Optional[int] = Field(
        description="last review time. minutes delta since collection epoch."
    )

    # Ease-factor / difficulty of the item, captured as a float. No dimensions.
    # Initialized to 2.3. Some initial testing with Super Ear in a real-ish setting, average Ease fell to 230%.
    ease_factor: float = Field(
        2.3, description="ease factor. estimates difficulty of the item"
    )

    # The current interval, in days
    current_interval: Optional[float] = Field(description="current interval, in days")

    # Number of times the item has been *pre*viewed
    n_previews: int = Field(
        0, description="number of times the item has been previewed"
    )

    # Note: No time delta is used here because the scheduler will be
    # responsible and calculate it during each review session

    # equality comparisons are based on the content,
    # not the scheduler parameters
    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return self.__str__()
