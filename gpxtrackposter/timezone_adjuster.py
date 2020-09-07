# Copyright 2016-2020 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import typing

import pytz
import s2sphere  # type: ignore
import timezonefinder  # type: ignore


class TimezoneAdjuster:
    _timezonefinder: typing.Optional[timezonefinder.TimezoneFinder] = None

    def __init__(self) -> None:
        if not TimezoneAdjuster._timezonefinder:
            TimezoneAdjuster._timezonefinder = timezonefinder.TimezoneFinder()

    @classmethod
    def adjust(cls, time: datetime.datetime, latlng: s2sphere.LatLng) -> datetime.datetime:
        # If a timezone is set, there's nothing to do.
        if time.utcoffset():
            return time
        assert cls._timezonefinder
        tz_name = cls._timezonefinder.timezone_at(lat=latlng.lat().degrees, lng=latlng.lng().degrees)
        if tz_name is None:
            return time
        tz = pytz.timezone(tz_name)
        tz_time = time.astimezone(tz)
        return tz_time
