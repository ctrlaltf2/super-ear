import datetime
import heapq
import logging
import random

from abc import ABC, abstractmethod
from typing import Any, Optional

from app.models.collection import Collection
from app.models.review_item import ReviewItem, ReviewState

# Generic interface for spaced-repetition schedulers
# Will be used to test out different scheduling algorithms

logger = logging.getLogger(__name__)


class Scheduler(ABC):
    # Builds a collection's reviewing queue. All cards sorted by due date. Up to scheduler to order them.
    @staticmethod
    @abstractmethod
    def generate_reviewing_queue(_collection: Collection) -> Optional[Any]:
        pass

    # Reviews an item, updating its scheduler parameters
    @staticmethod
    @abstractmethod
    def review(item: ReviewItem, note_distance: int, ms_elapsed: int) -> bool:
        pass

    # Gets the next due date for an item. Ideally, generate_reviewing_queue uses this.
    @staticmethod
    @abstractmethod
    def get_due_date(_collection: Collection, _item: ReviewItem) -> datetime.datetime:
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
    ) -> list[OrderedReviewItem]:
        # Store a current timestamp to assign to unseen items
        now = datetime.datetime.now(datetime.timezone.utc)
        # TODO: Time zone should match system time zone, conversion needed here
        tomorrow = datetime.datetime(
            year=now.year, month=now.month, day=now.day, tzinfo=datetime.timezone.utc
        ) + datetime.timedelta(days=1)

        # Get all items first
        review_items = _collection.get_active_track().review_items

        # Split into new/learning/review items
        all_new_items = [
            OrderedReviewItem(item, V1.get_due_date(_collection, item))
            for item in review_items
            if item.state == ReviewState.Unseen
        ]
        all_learning_items = [
            OrderedReviewItem(item, V1.get_due_date(_collection, item))
            for item in review_items
            if item.state == ReviewState.Learning
        ]
        all_reviewing_items = [
            OrderedReviewItem(item, V1.get_due_date(_collection, item))
            for item in review_items
            if item.state == ReviewState.Reviewing
        ]

        # TODO: Take into account the current day & the collections last review times to use the max review limits appropriately, to be per day and not per session
        new_items_today = all_new_items[: _collection.max_new_per_day]
        for item in new_items_today:
            item.item.state = ReviewState.Learning

        # For learning/review, get items due before EOD current day
        learning_items_today = [
            item for item in all_learning_items if item.due_date < tomorrow
        ]

        reviewing_items_today = [
            item for item in all_reviewing_items if item.due_date < tomorrow
        ]

        # Generate a priority queue of items sorted by due date
        # TODO: Restructure to make this take into account _collection.do_mix_new_review. Currently is implicit on the scheduler's due_dates, of which this sorts
        # Use a doubly-keyed sort? State then by due_date within that state.
        queue = new_items_today + learning_items_today + reviewing_items_today
        heapq.heapify(queue)

        return queue

    # pure
    @staticmethod
    def get_due_date(_collection: Collection, _item: ReviewItem) -> datetime.datetime:
        if _item.last_review is not None:  # triggers for learning and reviewing items
            last_review_date = _collection.epoch + datetime.timedelta(
                days=_item.last_review
            )

            return last_review_date + V1._calculate_interval(_item)
        else:  # triggers for unseen items
            return datetime.datetime.now(
                datetime.timezone.utc
            ) + V1._calculate_interval(_item)

    # helper to map numbers from one range to another proportionally
    # cf. arduino map
    @staticmethod
    def _map_range(x, c_in, c_out):
        in_min, in_max = c_in
        out_min, out_max = c_out
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Reviews an item, returning a reviewed copy
    # not pure / side effects- modifies ease factor and last review time, last interval
    @staticmethod
    def review(item: ReviewItem, note_distance: int, ms_elapsed: int) -> bool:
        # print(f"Reviewing item {item}")
        # Update ease factor
        # ref: SM-2 algorithm, http://super-memory.com/english/ol/sm2.htm
        err = float(note_distance)
        err = max(0, min(5, err))  # clamp note distance to 0-5

        match item.state:
            case ReviewState.Unseen:
                print("Item is new")
                item.state = ReviewState.Learning
                return True
            case ReviewState.Learning:
                print("Item is learning")
                was_correct = note_distance <= 0.001

                if was_correct:
                    print("Item was correct")
                    pass
                else:
                    print("Item was incorrect")
                    pass

                if was_correct:  # increment learning step // go to reviewing state
                    if (
                        item.learning_index >= len(item.learning_steps) - 1
                    ):  # graduated?
                        print("Item graduated")
                        item.state = ReviewState.Reviewing
                        item.learning_index = 0
                        item.current_interval = datetime.timedelta(
                            minutes=item.learning_steps[-1]
                        ) / datetime.timedelta(days=1)
                    else:  # move to next learning step
                        print("Item moved to next learning step")
                        item.learning_index += 1
                else:  # reset learning step
                    print("Item reset to first learning step")
                    item.learning_index = 0

                return (err - 5) < 4

            case ReviewState.Reviewing:
                print("Item is reviewing")
                # Map correctness into SM-2's interpretation of correctness
                if err > 0.001:  # mark as incorrect- [3,4,5]
                    err = V1._map_range(err, (1.0, 5.0), (3.0, 5.0))

                # quality response (0-5)
                q = 5 - err
                print(f"SM-2 quality of {q}")

                # step 6 of SM-2
                if q < 3:  # start reps from beginning, -> learning
                    print("SM-2 q < 3, resetting learning step")
                    item.state = ReviewState.Learning
                    item.learning_index = 0
                    item.current_interval = None

                # Update last interval
                last_interval = V1._calculate_interval(item)
                item.current_interval = last_interval / datetime.timedelta(
                    days=1
                )  # get # days as float

                print("Updating ease factor")
                item.ease_factor = max(
                    1.3,
                    item.ease_factor + (0.1 - err * (0.08 + err * 0.02)),
                )

                return q < 4

    # pure
    @staticmethod
    def _calculate_interval(_item: ReviewItem) -> datetime.timedelta:
        match _item.state:
            case ReviewState.Unseen:
                return V1._unseen_interval(_item)
            case ReviewState.Learning:
                return V1._learning_interval(_item)
            case ReviewState.Reviewing:
                return V1._reviewing_interval(_item)

    # pure
    @staticmethod
    def _unseen_interval(_item: ReviewItem, mx=8) -> datetime.timedelta:
        # Add a random number of seconds to add some jitter to the due date for unseen items
        return datetime.timedelta(seconds=random.random() * 2 * mx - mx)

    # pure
    @staticmethod
    def _learning_interval(_item: ReviewItem) -> datetime.timedelta:
        return datetime.timedelta(minutes=_item.learning_steps[_item.learning_index])

    # pure
    @staticmethod
    def _reviewing_interval(_item: ReviewItem) -> datetime.timedelta:
        # ref: http://super-memory.com/english/ol/sm2.htm because Anki's algo is a bit opaque (tech debt from supporting all its features)
        # SM-2 is the basis of Anki, so formulas are very similar
        last_interval: datetime.timedelta
        if _item.current_interval is None:
            last_interval = datetime.timedelta(minutes=_item.learning_steps[-1])
        else:
            last_interval = datetime.timedelta(days=_item.current_interval)

        n_days: float = last_interval / datetime.timedelta(days=1)
        days_ef: float = n_days * _item.ease_factor

        # max days is 90d
        days_ef = min(days_ef, 90)

        return datetime.timedelta(days=days_ef)


# Driver to help with scheduler API testing
class Driver:
    @staticmethod
    def main():
        # Simulates a user session
        # Realistically, this would be tracked asynchronously

        from app.models import DefaultCollections
        from app.core.srs.spn import SPN

        # session.state = initializing

        # Get the user's collection
        # TODO: Collection database retreival logic
        user_collection = DefaultCollections.get("GuitarStandard")

        scheduler: Any = V1

        # session -> generating_queue
        # queue is a priority queue of (due_date, item) sorted due_date ascending
        reviewing_queue = scheduler.generate_reviewing_queue(user_collection)

        # session.state = reviewing

        while not reviewing_queue.empty():
            # Get the next item to review
            next_item: ReviewItem = reviewing_queue.get()

            # session.state -> awaiting_response
            # Send a request to the user to review the item
            # TODO: Implement, this is on DSP server side

            # Assume user's response is present, they get one off
            response = SPN.from_str(next_item.content) + 1

            # session.state -> scoring
            note_distance = abs(response - next_item.content)

            scheduler.review(next_item, note_distance, 0)

            due_date = scheduler.get_due_date(next_item)
            if due_date < datetime.datetime.now(datetime.timezone.utc):
                reviewing_queue.put(OrderedReviewItem(next_item, due_date))

            # session.state -> reviewing

        # session over -> store collection
        # TODO: Store collection database
