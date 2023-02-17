import datetime
import random

from abc import ABC, abstractmethod
from copy import deepcopy
from queue import PriorityQueue
from random import shuffle
from typing import Any, Optional

from modules.srs.collection import Collection
from modules.srs.review_item import ReviewItem, ReviewState
from modules.srs.spn import SPN

# Generic interface for spaced-repetition schedulers
# Will be used to test out different scheduling algorithms
# Takes a mostly functional design with no side effects


class Scheduler(ABC):
    # Builds a collection's reviewing queue. All cards sorted by due date. Up to scheduler to order them.
    @staticmethod
    @abstractmethod
    def generate_reviewing_queue(_collection: Collection) -> Optional[Any]:
        pass

    # Retrieves the next item to review
    @staticmethod
    @abstractmethod
    def get_next_note(_collection: Collection) -> Optional[ReviewItem]:
        pass

    # Gets the next set of unseen items.
    @staticmethod
    @abstractmethod
    def get_next_unseen_items(_collection: Collection) -> Optional[list[ReviewItem]]:
        pass

    # Gets the set of items that are due for review
    @staticmethod
    @abstractmethod
    def get_due_items(_collection: Collection) -> Optional[list[ReviewItem]]:
        pass

    # Reviews an item, returning a reviewed copy
    @staticmethod
    @abstractmethod
    def review(_item: ReviewItem, note_distance: int, ms_elapsed: int) -> ReviewItem:
        pass


# A review item associated with a timestamp (due_date). Used to sort items by due date in priority queue
class OrderedReviewItem:
    # Reference to the item being reviewed
    item: ReviewItem

    # Timestamp of when the item is due for review
    due_date: datetime.datetime

    def __init__(self, item: ReviewItem, due_date: datetime.datetime):
        self.item = item
        self.due_date = due_date

    def __repr__(self):
        return f"OrderedReviewItem(\n\titem={str(self.item)},\n\tdue_date={str(self.due_date)}\n)"

    def __lt__(self, other):
        return self.due_date < other.due_date

    def __eq__(self, other):
        return self.item == other.item


# V1 of the scheduler, adapted from Anki's algorithm
# Only accounts for note distance currently
class V1(Scheduler):
    @staticmethod
    def generate_reviewing_queue(
        _collection: Collection,
    ) -> PriorityQueue[OrderedReviewItem]:
        # Store a current timestamp to assign to unseen items
        now = datetime.datetime.now(datetime.timezone.utc)

        # Get all items first
        review_items = _collection.get_active_track().review_items

        # Generate a priority queue of items sorted by due date
        queue: PriorityQueue[OrderedReviewItem] = PriorityQueue()

        for item in review_items:
            # Compute the due date. If the item is unseen, use the current timestamp
            if item.last_review is None:
                due_date = now
            else:
                due_date = (
                    V1.calculate_interval(item)
                    + item.last_review
                    + datetime.timedelta(
                        seconds=random.random() * 4 - 2
                    )  # Add some jitter
                )

            queue.put(OrderedReviewItem(item, due_date))

        return queue

    @staticmethod
    def calculate_interval(_item: ReviewItem) -> datetime.timedelta:
        match _item.state:
            case ReviewState.Unseen:
                return V1._unseen_interval(_item)
            case ReviewState.Learning:
                return V1._learning_interval(_item)
            case ReviewState.Reviewing:
                return V1._reviewing_interval(_item)

    @staticmethod
    def _unseen_interval(_item: ReviewItem) -> datetime.timedelta:
        pass

    @staticmethod
    def _learning_interval(_item: ReviewItem) -> datetime.timedelta:
        return datetime.timedelta(minutes=_item.learning_steps[_item.learning_index])

    @staticmethod
    def _reviewing_interval(_item: ReviewItem) -> datetime.timedelta:
        pass

    # Retrieves the next item to review
    @staticmethod
    def get_next_note(_collection: Collection) -> Optional[ReviewItem]:
        if _collection.learning_queue is None:
            raise ValueError("Learning queue is uninitialized")

        if len(_collection.learning_queue) == 0:
            raise ValueError("Learning queue is empty")

        return _collection.learning_queue[0]

    # Gets the next set of unseen items.
    @staticmethod
    def get_next_unseen_items(_collection: Collection) -> Optional[list[ReviewItem]]:
        # Get the active track
        _track = _collection.get_active_track()

        # Get the unseen items
        unseen_items = list(
            filter(  # Filter out items that are not in the unseen state
                lambda review_item: review_item.state == ReviewState.Unseen,
                _track.review_items,
            )
        )

        # If there are no unseen items, return None
        if len(unseen_items) == 0:
            return None

        # Get the number of unseen items to return
        # If the number of unseen items is less than the number of items to return,
        # return all of the unseen items
        num_items_to_return = min(len(unseen_items), V1.n_new_items_today(_collection))

        # Return the first num_items_to_return unseen items
        return unseen_items[:num_items_to_return]

    # Returns the number of unseen items that can be studied at this time (day)
    @staticmethod
    def n_new_items_today(_collection: Collection) -> int:
        return 3  # TODO: Implement

    # Gets the set of items that are due for review
    @staticmethod
    def get_due_items(_collection: Collection) -> Optional[list[ReviewItem]]:
        pass

    # Reviews an item, returning a reviewed copy
    @staticmethod
    def review(_item: ReviewItem, note_distance: int, ms_elapsed: int) -> ReviewItem:
        pass


# Driver to help with scheduler API testing
class Driver:
    @staticmethod
    def main():
        # Simulates a user session
        # Realistically, this would be tracked asynchronously

        from modules.srs import DefaultCollections

        # session.state = initializing

        # Get the user's collection
        # TODO: Collection database retreival logic
        user_collection = DefaultCollections.get("GuitarStandard")

        scheduler: Any = V1

        # session -> generating_queue
        # queue is a priority queue of (due_date, item) sorted due_date ascending
        reviewing_queue = scheduler.generate_reviewing_queue(user_collection)

        # session.state = reviewing

        while len(reviewing_queue) > 0:
            # Get the next item to review
            next_item: ReviewItem = scheduler.get_next_item(user_collection)

            # session.state -> awaiting_response
            # Send a request to the user to review the item
            # TODO: Implement, this is on DSP server side

            # Assume user's response is present, they get one off
            response = next_item.content + 1

            # session.state -> scoring
            note_distance = abs(response - next_item.content)

            next_interval = scheduler.calculate_interval(next_item, note_distance, 0)

            # Update last review time
            next_item.last_review = None  # TODO: current time UTC

            # put into learning queue
            # TODO: priority queue insert

            reviewing_queue = scheduler.generate_reviewing_queue(user_collection)

            # session.state -> reviewing

        # session over -> store collection
        # TODO: Store collection database
