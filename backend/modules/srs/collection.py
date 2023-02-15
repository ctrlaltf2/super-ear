from modules.srs.track import Track


# Class to represent a set of learning tracks
class Collection:
    tracks: list[Track]

    def __init__(self, tracks: list[Track]):
        self.tracks = tracks

    def add(self, item: Track):
        self.tracks.append(item)

    def __repr__(self):
        return f"Collection(\n\ttracks={str(self.tracks)}\n)"
