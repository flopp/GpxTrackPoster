# Copyright 2020-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import s2sphere  # type: ignore
from dateutil import parser, tz

from gpxtrackposter.timezone_adjuster import TimezoneAdjuster


def test_adjust() -> None:
    tza = TimezoneAdjuster()

    time = parser.parse("2020-09-06T14:34:01.029Z")

    freiburg = s2sphere.LatLng.from_degrees(47.998933, 7.841819)
    time_freiburg = tza.adjust(time, freiburg)
    assert time_freiburg.hour == 16

    newyork = s2sphere.LatLng.from_degrees(40.711344, -74.005382)
    time_newyork = tza.adjust(time, newyork)
    assert time_newyork.hour == 10


def test_adjust_with_utc_returns_time() -> None:
    tza = TimezoneAdjuster()

    tzinfos = {"CDT": tz.gettz("US/Central")}
    time = parser.parse("2020-09-06T14:34:01.029 CDT", tzinfos=tzinfos)

    freiburg = s2sphere.LatLng.from_degrees(47.998933, 7.841819)
    time_freiburg = tza.adjust(time, freiburg)
    assert time_freiburg.hour == 14

    newyork = s2sphere.LatLng.from_degrees(40.711344, -74.005382)
    time_newyork = tza.adjust(time, newyork)
    assert time_newyork.hour == 14
