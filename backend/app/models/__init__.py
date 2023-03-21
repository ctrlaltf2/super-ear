from .review_item import ReviewItem
from .track import Track
from .collection import Collection
from app.core.srs.spn import SPN


# -- Default collections
class DefaultCollections:
    # Standard tuning, guitar, 6-string. 21 notes
    _GuitarStandard = Collection(
        tracks=[
            Track.from_list(
                [
                    ReviewItem(content=repr(SPN.from_str("E4") + offset))
                    for offset in range(0, 21 + 1)
                ],
                "String 1",
            ),
            Track.from_list(
                [
                    ReviewItem(content=repr(SPN.from_str("B3") + offset))
                    for offset in range(0, 21 + 1)
                ],
                "String 2",
            ),
            Track.from_list(
                [
                    ReviewItem(content=repr(SPN.from_str("G3") + offset))
                    for offset in range(0, 21 + 1)
                ],
                "String 3",
            ),
            Track.from_list(
                [
                    ReviewItem(content=repr(SPN.from_str("D3") + offset))
                    for offset in range(0, 21 + 1)
                ],
                "String 4",
            ),
            Track.from_list(
                [
                    ReviewItem(content=repr(SPN.from_str("A2") + offset))
                    for offset in range(0, 21 + 1)
                ],
                "String 5",
            ),
            Track.from_list(
                [
                    ReviewItem(content=repr(SPN.from_str("E2") + offset))
                    for offset in range(0, 21 + 1)
                ],
                "String 6",
            ),
        ]
    )

    @staticmethod
    def get(name: str):
        from copy import deepcopy

        if name == "GuitarStandard":
            return deepcopy(DefaultCollections._GuitarStandard)

        raise ValueError(f"Collection {name} not found.")
