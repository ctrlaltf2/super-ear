import datetime

from enum import Enum, auto
from typing import Any, Optional, Self


# Enum for the three states of a review item; unseen, learning, and reviewing
class ReviewState(Enum):
    Unseen = auto()
    Learning = auto()
    Reviewing = auto()


# Class to represent a reviewable item and its associated scheduler parameters
class ReviewItem:
    # Current state of the review item
    state: ReviewState

    # Current learning step
    learning_index: int

    # Learning steps for the item (in minutes)
    learning_steps: list[float]

    # ReviewItem content
    content: Any

    # Last review time (minutes delta since collection's epoch)
    last_review: Optional[int]

    # Ease-factor / difficulty of the item, captured as a float. No dimensions.
    # Initialized to 2.5, since that's the default in Anki & SM-2.
    ease_factor: float

    # The current interval, in days
    current_interval: Optional[float]

    # Note: No time delta is used here because the scheduler will be
    # responsible and calculate it during each review session

    def __init__(self, content: Any, **kwargs):
        self.state = kwargs.get("state", ReviewState.Unseen)
        self.learning_index = kwargs.get("learning_index", 0)
        self.learning_steps = kwargs.get(
            "learning_steps", [1 / 12, 5 / 12, 2, 10, 60, 300]
        )  # default steps from recommended settings of https://ankiweb.net/shared/info/1250336138 (A ear training Anki deck)
        self.content = content
        self.last_review = kwargs.get("last_review", None)
        self.ease_factor = kwargs.get("ease_factor", 2.5)
        self.current_interval = kwargs.get("current_interval", None)

    # equality comparisons are based on the content,
    # not the scheduler parameters
    def __eq__(self, other: Self) -> bool:
        return self.content == other.content

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return self.__str__()
