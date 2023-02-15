from abc import ABC, abstractmethod
from typing import Optional

from modules.srs.collection import Collection
from modules.srs.review_item import ReviewItem

# Generic interface for spaced-repetition schedulers
# Will be used to test out different scheduling algorithms


class Scheduler(ABC):
    # Retrieves the next item to review
    @staticmethod
    @abstractmethod
    def get_next_note(collection: Collection) -> Optional[ReviewItem]:
        pass

    # Gets the next set of unseen items.
    @staticmethod
    @abstractmethod
    def get_next_unseen_items(collection: Collection) -> Optional[list[ReviewItem]]:
        pass

    # Gets the set of items that are due for review
    @staticmethod
    @abstractmethod
    def get_due_items(collection: Collection) -> Optional[list[ReviewItem]]:
        pass

    # Reviews an item, modifying it in-place
    @staticmethod
    @abstractmethod
    def review(item: ReviewItem, note_distance: int, ms_elapsed: int):
        pass
