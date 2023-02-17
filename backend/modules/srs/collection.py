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

    def __init__(self, tracks: list[Track], **kwargs):
        self.tracks = tracks

        self.active_track_index = kwargs.get("active_track_index", 0)
        self.epoch = kwargs.get("epoch", datetime.datetime.now())

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
