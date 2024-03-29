import logging

from typing import Iterator

from pydantic import BaseModel
from pydantic.fields import Field

from app.models.review_item import ReviewItem

logger = logging.getLogger(__name__)


# A track is a collection of review items that are related to each other
# For example, a track can be the set of notes on the high E string of a guitar
# Track acts like an ordered list of review items
class Track(BaseModel):
    # Name for the track
    name: str = Field(..., description="Name of the track")

    # The review items in this track
    review_items: list[ReviewItem] = Field(..., description="Review items in the track")

    # Python, collections API []
    # O(1)
    def __getitem__(self, item: int) -> ReviewItem:
        return self.review_items[item]

    # O(n)
    def __contains__(self, item: ReviewItem) -> bool:
        return item in self.review_items

    def __iter__(self) -> Iterator[ReviewItem]:
        # Pass through to the review items list
        return iter(self.review_items)

    def __reversed__(self):
        # Pass through to the review items list
        return reversed(self.review_items)

    def __len__(self) -> int:
        return len(self.review_items)

    def append(self, item: ReviewItem):
        if item in self.review_items:
            logger.warning("Item already in track, adding anyways.")

        self.review_items.append(item)

    @staticmethod
    def from_list(items: list[ReviewItem], name: str) -> "Track":
        return Track(review_items=items, name=name)

    def __repr__(self):
        return (
            f"Track(\n\tname={self.name},\n\treview_items={str(self.review_items)}\n)"
        )
