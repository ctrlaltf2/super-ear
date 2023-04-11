import datetime
import pytz

from pydantic import BaseModel
from pydantic.fields import Field

from app.models.track import Track


# Class to represent a set of learning tracks
class Collection(BaseModel):
    # List of the tracks
    tracks: list[Track] = Field(
        ..., description="list of tracks that make up this collection"
    )

    # Index of the active track
    active_track_index: int = Field(0, ge=0, description="index of the active track")

    # Epoch for the collection (UTC)
    epoch: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=pytz.utc),
        description="epoch for the collection (UTC)",
    )

    # Day of most recent review. epoch.to_local_time() + datetime.timedelta(days=last_review_day).
    most_recent_review: int = Field(
        -1,
        description="day of most recent review. days since epoch. Local time # days..",
    )

    # Number of new seen on last_review_day
    n_recently_reviewed: int = Field(
        0, description="number of new seen on most_recent_review"
    )

    n_recently_new: int = Field(
        0, description="number of new seen on most_recent_review"
    )

    # -- collection settings
    max_card_previews: int = Field(
        3, description="maximum number of times a card can be previewed", ge=0
    )

    # Maximum number of new items to study per day
    max_new_per_day: int = Field(
        6, description="maximum number of new items to study per day", ge=0
    )

    # Maximum number of items to study per day. # of cards, not # of reviews.
    max_reviews_per_day: int = Field(
        100, description="maximum number of items to study per day", ge=0
    )

    # If should mix review and new items together
    do_mix_new_review: bool = Field(
        False, description="if should mix review and new items together"
    )

    # learn ahead interval, in hours
    # if a card is learning
    learn_ahead_interval: float = Field(
        20 / 60, description="learn ahead interval, in hours", ge=0.0, lt=24.0
    )

    # time zone for the collection. Affects what is defined as "today".
    timezone: str = Field("US/Eastern", description="time zone for the collection")

    # next day start time. n_hours past 00:00 of current date
    next_day_start_hours: float = Field(
        4.0,
        description="number of hours past midnight to start the next day",
        ge=0.0,
        le=23.0,
    )

    def add(self, item: Track):
        self.tracks.append(item)

    def __repr__(self):
        return f"Collection(\n\ttracks={str(self.tracks)}\n)"

    def get_active_track(self) -> Track:
        return self.tracks[self.active_track_index]

    def set_active_track(self, identifier: str | int):
        if type(identifier) is str:
            # Find the track with the matching name
            for i, track in enumerate(self.tracks):
                if track.name == identifier:
                    self.active_track_index = i
                    break
            else:
                raise ValueError(f"Track with name {identifier} not found")
        elif type(identifier) is int:
            self.active_track_index = identifier

    def get_epoch(self) -> datetime.datetime:
        # makes epoch into a timezone-aware object because why is it not Already
        return self.epoch.replace(tzinfo=pytz.utc)
