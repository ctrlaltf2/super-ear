import datetime
import logging
import random

import pytz

from abc import ABC, abstractmethod
from collections import defaultdict
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
    def review(
        collection: Collection, item: ReviewItem, note_distance: int, ms_elapsed: int
    ) -> bool:
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
        # Get all items first
        review_items = _collection.get_active_track().review_items

        # Split into new/learning/review items
        items_by_state: defaultdict[ReviewState, list[OrderedReviewItem]] = defaultdict(
            list
        )

        # add all due items to the dict
        for review_item in review_items:
            due_date = V1.get_due_date(_collection, review_item)

            if V1.is_due(_collection, review_item, due_date):
                items_by_state[review_item.state].append(
                    OrderedReviewItem(review_item, due_date)
                )

        all_new_items = (
            items_by_state[ReviewState.Previewing] + items_by_state[ReviewState.Unseen]
        )

        new_items_today = all_new_items[: _collection.max_new_per_day]
        for item in new_items_today:
            item.item.state = ReviewState.Previewing

        # For learning/review, get items due before the learn cutoff
        learning_items_today = [item for item in items_by_state[ReviewState.Learning]]

        reviewing_items_today = [item for item in items_by_state[ReviewState.Reviewing]]

        # TODO: Restrict max learning/reiew items/day here
        queue = new_items_today + learning_items_today + reviewing_items_today

        # shuffle the queue
        random.shuffle(queue)

        return queue

    # get if a item is due
    @staticmethod
    def is_due(_collection: Collection, _item: ReviewItem, due_date: datetime.datetime):
        if _item.state == ReviewState.Unseen:
            return True
        elif _item.state == ReviewState.Previewing:
            return True
        elif _item.state == ReviewState.Learning:
            return due_date < V1._learn_cutoff(_collection)
        elif _item.state == ReviewState.Reviewing:
            return due_date <= V1.get_today_start(_collection)

    # Get the timestamp for the start of the current study day.
    @staticmethod
    def get_today_start(_collection: Collection) -> datetime.datetime:
        tz_str = _collection.timezone

        try:
            tz = pytz.timezone(tz_str)
        except pytz.exceptions.UnknownTimeZoneError:
            logger.error(f"Unknown timezone '{tz_str}'")
            raise

        global_now = datetime.datetime.now(datetime.timezone.utc)

        # *danger zone starts playing*

        loc_now = tz.normalize(global_now.astimezone(tz))

        # very hacky yet easy to understand because getting datetime code right is like
        # trying to reverse engineer a JavaScript applicatoin by only using voltages and a multimeter on the CPU that runs it

        # goal: round now() to the nearest (start of a day + next_day_start_hours)
        yester_yesterday_start = loc_now.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        yester_yesterday_start = tz.normalize(
            yester_yesterday_start
            + datetime.timedelta(days=-2, hours=_collection.next_day_start_hours)
        )

        yesterday_start = loc_now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = tz.normalize(
            yesterday_start
            + datetime.timedelta(days=-1, hours=_collection.next_day_start_hours)
        )

        today_start = loc_now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_start = tz.normalize(
            today_start + datetime.timedelta(hours=_collection.next_day_start_hours)
        )

        # now, calculate and store the differences
        yester_yesterday_diff = loc_now - yester_yesterday_start
        yesterday_diff = loc_now - yesterday_start
        today_diff = loc_now - today_start

        # throw them into an array and sort it to lazily find the smallest difference
        diffs = sorted(
            [
                (
                    yester_yesterday_diff / datetime.timedelta(hours=1.0),
                    yester_yesterday_start,
                ),
                (yesterday_diff / datetime.timedelta(hours=1.0), yesterday_start),
                (today_diff / datetime.timedelta(hours=1.0), today_start),
            ]
        )

        # Then get the first dt that is not in the future.
        rounded_datetime = None

        for _, dt in diffs:
            if dt > loc_now:
                continue
            else:
                rounded_datetime = dt
                break

        assert rounded_datetime is not None

        # *danger zone stops playing*

        # and normalize it back to UTC
        global_today_start = rounded_datetime.astimezone(pytz.utc)

        return global_today_start

    @staticmethod
    def get_due_date(_collection: Collection, _item: ReviewItem) -> datetime.datetime:
        if _item.last_review is not None:  # triggers for learning and reviewing items
            last_review_date = _collection.epoch + datetime.timedelta(
                days=_item.last_review
            )

            return last_review_date + V1._calculate_interval(_item)
        else:  # triggers for unseen items
            return V1.get_today_start(_collection)

    # get the last review time (global) for an item
    @staticmethod
    def _last_review_time(
        _collection: Collection, _item: ReviewItem
    ) -> datetime.datetime | None:
        if _item.last_review is not None:
            return _collection.epoch + datetime.timedelta(days=_item.last_review)
        else:
            return None

    # get the learning ahead cutoff time (global)
    @staticmethod
    def _learn_cutoff(_collection: Collection) -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            hours=_collection.learn_ahead_interval
        )

    # helper to map numbers from one range to another proportionally
    # cf. arduino map
    @staticmethod
    def _map_range(x, c_in, c_out):
        in_min, in_max = c_in
        out_min, out_max = c_out
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Reviews an item, returning a reviewed copy
    # not pure / side effects- modifies ease factor and last review time, last interval
    # returns: True if should review again this session
    @staticmethod
    def review(
        _collection: Collection, item: ReviewItem, note_distance: int, ms_elapsed: int
    ) -> bool:
        # ref: SM-2 algorithm, http://super-memory.com/english/ol/sm2.htm
        # modifications made to above for better usability
        err = float(note_distance)
        err = max(0, min(5, err))  # clamp note distance to 0-5

        # update review time
        if item.state != ReviewState.Unseen:
            diff = V1.get_today_start(_collection).date() - _collection.epoch.date()
            item.last_review = diff.days

        match item.state:
            case ReviewState.Unseen:
                print("Item is new")
                item.state = ReviewState.Previewing
                return True
            case ReviewState.Previewing:
                print("Item is previewing")
                was_correct = note_distance <= 0.001

                if was_correct:
                    print("Item was correct")
                    item.n_previews += 1
                else:
                    print("Item was incorrect")
                    # increment n_previews with a 50% chance
                    if random.random() < 0.5:
                        item.n_previews += 1

                if item.n_previews >= _collection.max_card_previews:
                    print("Item graduated from previewing")
                    item.state = ReviewState.Learning
                    return False  # for now, don't put back into the learning queue.
                else:
                    return True

            case ReviewState.Learning:
                print("Item is learning")
                was_correct = note_distance <= 0.001

                if was_correct:
                    print("Item was correct")
                else:
                    print("Item was incorrect")

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

    @staticmethod
    def _calculate_interval(_item: ReviewItem) -> datetime.timedelta:
        match _item.state:
            case ReviewState.Unseen:
                return V1._unseen_interval(_item)
            case ReviewState.Previewing:
                return V1._unseen_interval(_item)
            case ReviewState.Learning:
                return V1._learning_interval(_item)
            case ReviewState.Reviewing:
                return V1._reviewing_interval(_item)

    @staticmethod
    def _unseen_interval(_item: ReviewItem, mx=8) -> datetime.timedelta:
        # Add a random number of seconds to add some jitter to the due date for unseen items
        return datetime.timedelta(seconds=random.random() * 2 * mx - mx)

    @staticmethod
    def _learning_interval(_item: ReviewItem) -> datetime.timedelta:
        return datetime.timedelta(minutes=_item.learning_steps[_item.learning_index])

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
