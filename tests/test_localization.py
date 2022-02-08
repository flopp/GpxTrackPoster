"""
Several tests for Localization
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import locale

import pytest

from gpxtrackposter.localization import localized_day_of_week_name


@pytest.mark.parametrize(
    "invalid_day",
    [-10, -1, 7, 10],
)
def test_localized_with_invalid_raises_exception(invalid_day: int) -> None:
    """method with invalid value returns False"""
    with pytest.raises(AssertionError):
        assert not localized_day_of_week_name(invalid_day, True)
        assert not localized_day_of_week_name(invalid_day, False)


def test_localized_returns_expected_value() -> None:
    """method with valid values returns expected value"""
    locale.setlocale(category=locale.LC_ALL, locale=["de_DE", "UTF-8"])
    assert "Montag" == localized_day_of_week_name(0, False)
    assert "Samstag" == localized_day_of_week_name(5, False)
    assert "Sonntag" == localized_day_of_week_name(6, False)
    assert "M" == localized_day_of_week_name(0, True)
    assert "S" == localized_day_of_week_name(5, True)
    assert "S" == localized_day_of_week_name(6, True)
    locale.setlocale(category=locale.LC_ALL, locale=["en_US", "UTF-8"])
    assert "Monday" == localized_day_of_week_name(0, False)
    assert "Saturday" == localized_day_of_week_name(5, False)
    assert "Sunday" == localized_day_of_week_name(6, False)
    assert "M" == localized_day_of_week_name(0, True)
    assert "S" == localized_day_of_week_name(5, True)
    assert "S" == localized_day_of_week_name(6, True)
    locale.setlocale(category=locale.LC_ALL, locale=["zh_CN", "UTF-8"])
    assert "星期一" == localized_day_of_week_name(0, False)
    assert "星期六" == localized_day_of_week_name(5, False)
    assert "星期日" == localized_day_of_week_name(6, False)
    assert "一" == localized_day_of_week_name(0, True)
    assert "六" == localized_day_of_week_name(5, True)
    assert "日" == localized_day_of_week_name(6, True)
