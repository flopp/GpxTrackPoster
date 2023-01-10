"""
Several tests for YearRange
"""
# Copyright 2021-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from datetime import datetime
from typing import Optional

import pytest

from gpxtrackposter.year_range import YearRange


def test_init_returns_invalid_instance() -> None:
    """YearRange object is initialised with None values"""
    year_range = YearRange()
    assert year_range.from_year is None
    assert year_range.to_year is None


@pytest.mark.parametrize(
    "string, from_year, to_year",
    [("all", None, None), ("2016", 2016, 2016), ("2018", 2018, 2018), ("2016-2018", 2016, 2018)],
)
def test_parse_with_valid_strings_sets_values_returns_true(
    string: str, from_year: Optional[int], to_year: Optional[int]
) -> None:
    """parse with valid strings returns True"""
    year_range = YearRange()
    assert year_range.parse(string)
    assert from_year == year_range.from_year
    assert to_year == year_range.to_year


@pytest.mark.parametrize(
    "invalid_string",
    ["20xx", "20xx-2018", "2016:2018"],
)
def test_parse_with_invalid_strings_returns_false(invalid_string: str) -> None:
    """parse with invalid strings returns False"""
    year_range = YearRange()
    assert not year_range.parse(invalid_string)


def test_parse_with_wrong_order_returns_false() -> None:
    """parse with wrong order of years returns False"""
    invalid_string = "2018-2016"
    year_range = YearRange()
    assert not year_range.parse(invalid_string)


@pytest.mark.parametrize(
    "valid_string",
    ["2016", "2018", "2016-2018"],
)
def test_clear_returns_empty_instance(valid_string: str) -> None:
    """clear returns empty instance of YearRange"""
    year_range = YearRange()
    assert year_range.parse(valid_string)
    assert year_range.from_year is not None
    assert year_range.to_year is not None
    year_range.clear()
    assert year_range.from_year is None
    assert year_range.to_year is None


@pytest.mark.parametrize(
    "valid_string, added, from_year, to_year",
    [
        ("all", datetime(2015, 1, 1), 2015, 2015),
        ("2016", datetime(2015, 1, 1), 2015, 2016),
        ("2016", datetime(2019, 1, 1), 2016, 2019),
        ("2016-2018", datetime(2015, 1, 1), 2015, 2018),
        ("2016-2018", datetime(2019, 1, 1), 2016, 2019),
    ],
)
def test_add_increases_year_range(valid_string: str, added: datetime, from_year: int, to_year: int) -> None:
    """add with higher/lower values increases YearRange"""
    year_range = YearRange()
    assert year_range.parse(valid_string)
    year_range.add(added)
    assert from_year == year_range.from_year
    assert to_year == year_range.to_year


@pytest.mark.parametrize(
    "string, value",
    [
        ("all", datetime(2015, 1, 1)),
        ("2016", datetime(2016, 1, 1)),
        ("2016-2018", datetime(2016, 1, 1)),
        ("2016-2018", datetime(2017, 1, 1)),
        ("2016-2018", datetime(2018, 1, 1)),
    ],
)
def test_contains_returns_true(string: str, value: datetime) -> None:
    """contains returns True"""
    year_range = YearRange()
    assert year_range.parse(string)
    assert year_range.contains(value)


@pytest.mark.parametrize(
    "string, value",
    [
        ("2016", datetime(2015, 1, 1)),
        ("2016", datetime(2017, 1, 1)),
        ("2016-2018", datetime(2015, 1, 1)),
        ("2016-2018", datetime(2019, 1, 1)),
    ],
)
def test_contains_returns_false(string: str, value: datetime) -> None:
    """contains returns False"""
    year_range = YearRange()
    assert year_range.parse(string)
    assert not year_range.contains(value)


def test_count_with_empty_year_range_returns_zero() -> None:
    """count with empty year range returns 0"""
    year_range = YearRange()
    assert 0 == year_range.count()


@pytest.mark.parametrize(
    "string, expected_value",
    [
        ("2016", 1),
        ("2016-2018", 3),
        ("2015-2019", 5),
    ],
)
def test_count_returns_value(string: str, expected_value: int) -> None:
    """count returns value"""
    year_range = YearRange()
    assert year_range.parse(string)
    assert expected_value == year_range.count()


def test_iter_with_empty_year_range_returns() -> None:
    """iter with empty year range returns"""
    year_range = YearRange()
    list_of_years = []
    for year in year_range.iter():
        list_of_years.append(year)
    assert not list_of_years


@pytest.mark.parametrize(
    "string, expected_values",
    [
        ("2016", [2016]),
        ("2016-2018", [2016, 2017, 2018]),
        ("2015-2019", [2015, 2016, 2017, 2018, 2019]),
    ],
)
def test_iter_returns_values(string: str, expected_values: list) -> None:
    """iter returns YearRange values"""
    year_range = YearRange()
    assert year_range.parse(string)
    list_of_years = []
    for year in year_range.iter():
        list_of_years.append(year)
    assert expected_values == list_of_years
