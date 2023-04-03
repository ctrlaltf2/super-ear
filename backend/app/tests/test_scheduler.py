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
