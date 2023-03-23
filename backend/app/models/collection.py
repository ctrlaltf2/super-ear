import datetime

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

    # Epoch for the collection
    epoch: datetime.datetime = Field(
        default_factory=datetime.datetime.now, description="epoch for the collection"
    )

    # Day of most recent review. Days since epoch.
    last_review_day: int = Field(
        0, description="day of most recent review. days since epoch."
    )

    # -- collection settings

    # Maximum number of new items to study per day
    max_new_per_day: int = Field(
        3, description="maximum number of new items to study per day", ge=0
    )

    # Maximum number of items to study per day. # of cards, not # of reviews.
    max_reviews_per_day: int = Field(
        75, description="maximum number of items to study per day", ge=0
    )

    # If should mix review and new items together
    do_mix_new_review: bool = Field(
        False, description="if should mix review and new items together"
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
