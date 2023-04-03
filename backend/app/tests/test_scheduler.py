import datetime

import freezegun
import pytest
import pytz

from app.core.srs.scheduler import V1
from app.models import DefaultCollections
from app.models.collection import Collection
from app.models.review_item import ReviewItem, ReviewState


class TestSchedulerV1:
    class TestGenerateReviewingQueue:
        pass

    class TestGetTodayStart:
        col: Collection = DefaultCollections.get("GuitarStandard")

        @pytest.mark.parametrize(
            "loc_time, expected_loc",
            [
                ("2023-01-01 00:00:00", "2022-12-31 04:00:00"),
                ("2023-01-01 00:00:01", "2022-12-31 04:00:00"),
                ("2023-01-01 23:59:59", "2023-01-01 04:00:00"),
                ("2023-01-01 03:59:59", "2022-12-31 04:00:00"),
                ("2023-01-01 04:00:00", "2023-01-01 04:00:00"),
                ("2023-01-01 04:01:01", "2023-01-01 04:00:00"),
                ("2023-01-02 00:00:00", "2023-01-01 04:00:00"),
                ("2023-01-02 00:00:01", "2023-01-01 04:00:00"),
                ("2023-01-02 23:59:59", "2023-01-02 04:00:00"),
            ],
        )
        def test_get_today_start(self, loc_time, expected_loc):
            self.col.next_day_start_hours = 4  # force to 4am
            self.col.timezone = "US/Eastern"

            # TODO: (only half kidding) test the test code
            tz = pytz.timezone(self.col.timezone)
            loc_time_dt = tz.normalize(
                tz.localize(datetime.datetime.fromisoformat(loc_time))
            )

            assert (
                loc_time_dt.date() == datetime.datetime.fromisoformat(loc_time).date()
            )

            global_time_dt = loc_time_dt.astimezone(pytz.utc)

            with freezegun.freeze_time(global_time_dt):
                calculated_start_global = V1.get_today_start(self.col)
                calculated_start_loc = calculated_start_global.astimezone(tz)

                expected_loc = datetime.datetime.fromisoformat(expected_loc)

                assert calculated_start_loc.date() == expected_loc.date()
                assert calculated_start_loc.time() == expected_loc.time()

    def test_basic_queue_building(self):
        with freezegun.freeze_time("2023-01-01 00:00:00") as freezer:
            # Initial test: a new collection
            col: Collection = DefaultCollections.get("GuitarStandard")
            q = V1.generate_reviewing_queue(col)

            # to start, collection size should be == new per day
            assert len(q) == col.max_new_per_day

            # all should be previwing to start
            for item in q:
                assert item.item.state == ReviewState.Previewing

            max_previews = col.max_card_previews

            # preview all cards
            for i in range(max_previews):
                for item in q:
                    should_reinsert = V1.review(col, item.item, 0, 0)

                    # after max previews, shouldn't resinert and should be learning
                    if i == max_previews - 1:
                        assert not should_reinsert
                        assert item.item.state == ReviewState.Learning

            # pass a day
            freezer.move_to("2023-01-02 00:00:00")
            q = V1.generate_reviewing_queue(col)

            assert len(q) == col.max_new_per_day * 2

            # pass another day, without reviewing anything in the last (should yield unchanged queue)
            freezer.move_to("2023-01-03 00:00:00")
            q = V1.generate_reviewing_queue(col)

            assert len(q) == col.max_new_per_day * 2

            # TODO: many more cases to be checked here:
            # - max review per day
            # - proper due checking
