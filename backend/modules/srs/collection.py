import datetime

from typing import Any, Optional

from modules.srs.track import Track


# Class to represent a set of learning tracks
class Collection:
    # List of the tracks
    tracks: list[Track]

    # Index of the active track
    active_track_index: int = 0

    # Epoch for the collection
    epoch: datetime.datetime

    # Day of most recent review. Days since epoch.
    last_review_day: int = 0

    # Number of new items left to study on current day (epoch + last_review_day)
    n_new_items_today: int

    # Number of reviewing items left to study on current day (epoch + last_review_day)
    n_review_items_today: int

    # -- collection settings

    # Maximum number of new items to study per day
    max_new_per_day: int = 3

    # Maximum number of items to study per day. # of cards, not # of reviews.
    max_reviews_per_day: int = 75

    # If should mix review and new items together
    do_mix_new_review: bool = False

    def __init__(self, tracks: list[Track], **kwargs):
        self.tracks = tracks

        # Pull in configuration
        self.active_track_index = kwargs.get("active_track_index", 0)
        self.epoch = kwargs.get("epoch", datetime.datetime.now())
        self.max_new_per_day = kwargs.get("max_new_per_day", 3)
        self.max_reviews_per_day = kwargs.get("max_reviews_per_day", 75)
        self.do_mix_new_review = kwargs.get("do_mix_new_review", False)
        self.last_review_day = kwargs.get("last_review_day", 0)

    def add(self, item: Track):
        self.tracks.append(item)

    def __repr__(self):
        return f"Collection(\n\ttracks={str(self.tracks)}\n)"

    def get_active_track(self) -> Track:
        return self.tracks[self._active_track_index]

    def set_active_track(self, identifier: str | int):
        if type(identifier) is str:
            # Find the track with the matching name
            for i, track in enumerate(self.tracks):
                if track.name == identifier:
                    self._active_track_index = i
                    break
        elif type(identifier) is int:
            self._active_track_index = identifier
