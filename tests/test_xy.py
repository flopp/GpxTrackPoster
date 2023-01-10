"""
Several tests for XY
"""
# Copyright 2021-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from typing import Union

import pytest

from gpxtrackposter.xy import XY


@pytest.mark.parametrize(
    "other, expected",
    [
        (10.0, (500.0, 1000.0)),
        (10, (500.0, 1000.0)),
        (0.5, (25.0, 50.0)),
        (-5.0, (-250.0, -500.0)),
        (XY(10.0, 5.0), (500.0, 500.0)),
        (XY(-10.0, 5.0), (-500.0, 500.0)),
        (XY(0.5, -5.0), (25.0, -500.0)),
    ],
)
def test_multiplication(other: Union[float, XY], expected: XY) -> None:
    """Test multiplication"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == (test_object * other).tuple()


@pytest.mark.parametrize(
    "other, expected",
    [
        (10.0, (500.0, 1000.0)),
        (10, (500.0, 1000.0)),
        (0.5, (25.0, 50.0)),
        (-5.0, (-250.0, -500.0)),
        (XY(10.0, 5.0), (500.0, 500.0)),
        (XY(-10.0, 5.0), (-500.0, 500.0)),
        (XY(0.5, -5.0), (25.0, -500.0)),
    ],
)
def test_right_multiplication(other: Union[float, XY], expected: XY) -> None:
    """Test right multiplication"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == (other * test_object).tuple()


@pytest.mark.parametrize(
    "other, expected",
    [
        (10.0, (5.0, 10.0)),
        (10, (5.0, 10.0)),
        (0.5, (100.0, 200.0)),
        (-5.0, (-10.0, -20.0)),
        (XY(10.0, 5.0), (5.0, 20.0)),
        (XY(-10.0, 5.0), (-5.0, 20.0)),
        (XY(0.5, -5.0), (100.0, -20.0)),
    ],
)
def test_division(other: Union[float, XY], expected: XY) -> None:
    """Test division"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == (test_object / other).tuple()


@pytest.mark.parametrize(
    "other, expected",
    [
        (10.0, (60.0, 110.0)),
        (10, (60.0, 110.0)),
        (0.5, (50.5, 100.5)),
        (-5.0, (45.0, 95.0)),
        (XY(10.0, 5.0), (60.0, 105.0)),
        (XY(-10.0, 5.0), (40.0, 105.0)),
        (XY(0.5, -5.0), (50.5, 95.0)),
    ],
)
def test_addition(other: Union[float, XY], expected: XY) -> None:
    """Test addition"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == (test_object + other).tuple()


@pytest.mark.parametrize(
    "other, expected",
    [
        (10.0, (60.0, 110.0)),
        (10, (60.0, 110.0)),
        (0.5, (50.5, 100.5)),
        (-5.0, (45.0, 95.0)),
        (XY(10.0, 5.0), (60.0, 105.0)),
        (XY(-10.0, 5.0), (40.0, 105.0)),
        (XY(0.5, -5.0), (50.5, 95.0)),
    ],
)
def test_right_addition(other: Union[float, XY], expected: XY) -> None:
    """Test right addition"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == (other + test_object).tuple()


@pytest.mark.parametrize(
    "other, expected",
    [
        (10.0, (40.0, 90.0)),
        (10, (40.0, 90.0)),
        (0.5, (49.5, 99.5)),
        (-5.0, (55.0, 105.0)),
        (XY(10.0, 5.0), (40.0, 95.0)),
        (XY(-10.0, 5.0), (60.0, 95.0)),
        (XY(0.5, -5.0), (49.5, 105.0)),
    ],
)
def test_subtraction(other: Union[float, XY], expected: XY) -> None:
    """Test subtraction"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == (test_object - other).tuple()


def test_representation() -> None:
    """Test representation"""
    test_object: XY = XY(50.0, 100.0)
    assert "XY: 50.0/100.0" == str(test_object)


@pytest.mark.parametrize(
    "this, other",
    [
        (XY(10.0, 10.0), XY(10, 10)),
        (XY(10.54321, 10.12345), XY(10.5432100001, 10.1234500001)),
    ],
)
def test_equality_returns_true(this: XY, other: XY) -> None:
    """Test equality"""
    assert this == other


@pytest.mark.parametrize(
    "this, other",
    [
        (XY(10.0, 10.0), 10.0),
        (XY(10.0, 10.0), XY(11, 11)),
        (XY(10.54321, 10.12345), XY(10.543215, 10.123455)),
    ],
)
def test_equality_returns_false(this: XY, other: Union[float, XY]) -> None:
    """Test equality"""
    assert not this == other


def test_tuple() -> None:
    """Test tuple"""
    test_object: XY = XY(50.0, 100.0)
    assert (50.0, 100.0) == test_object.tuple()


def test_to_int() -> None:
    """Test to_int"""
    test_object: XY = XY(50.12345, 100.98765)
    assert (50, 100) == test_object.to_int().tuple()


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, (50.0, 101.0)),
        (1, (50.1, 101.0)),
        (2, (50.12, 100.99)),
        (3, (50.123, 100.988)),
        (4, (50.1234, 100.9877)),
        (5, (50.12345, 100.98765)),
        (None, (50.0, 101.0)),
    ],
)
def test_round(n: int, expected: XY) -> None:
    """Test round"""
    test_object: XY = XY(50.12345, 100.98765)
    assert expected == test_object.round(n).tuple()


@pytest.mark.parametrize(
    "test_object, expected",
    [
        (XY(12.5, 25.0), 25.0),
        (XY(25.0, 12.5), 25.0),
        (XY(12.5, -25.0), 12.5),
        (XY(-25.0, 12.5), 12.5),
        (XY(12, 25), 25),
        (XY(25, 12), 25),
    ],
)
def test_get_max(test_object: XY, expected: float) -> None:
    """Test get_max"""
    assert expected == test_object.get_max()


@pytest.mark.parametrize(
    "test_object, expected",
    [
        (XY(12.5, 25.0), 12.5),
        (XY(25.0, 12.5), 12.5),
        (XY(12.5, -25.0), -25.0),
        (XY(-25.0, 12.5), -25.0),
        (XY(12, 25), 12),
        (XY(25, 12), 12),
    ],
)
def test_get_min(test_object: XY, expected: float) -> None:
    """Test get_min"""
    assert expected == test_object.get_min()


@pytest.mark.parametrize(
    "max_value, expected",
    [
        (25.0, (12.5, 25.0)),
        (50.0, (25.0, 50.0)),
        (200.0, (100.0, 200.0)),
        (-50.0, (-25.0, -50.0)),
    ],
)
def test_scale_to_max_value_with_good_values(max_value: float, expected: XY) -> None:
    """Test scale_to_max_value"""
    test_object: XY = XY(50.0, 100.0)
    assert expected == test_object.scale_to_max_value(max_value).tuple()


@pytest.mark.parametrize(
    "max_value, expected",
    [
        (25.0, (25.0, 12.5)),
        (-50.0, (25.0, -50.0)),
        (-50.0, (-25.0, 50.0)),
    ],
)
def test_scale_to_max_value_with_bad_values(max_value: float, expected: XY) -> None:
    """Test scale_to_max_value"""
    test_object: XY = XY(50.0, 100.0)
    assert not expected == test_object.scale_to_max_value(max_value).tuple()


@pytest.mark.parametrize(
    "max_value, expected",
    [
        (25.0, (25.0, 12.5)),
        (50.0, (50.0, 25.0)),
        (200.0, (200.0, 100.0)),
        (-50.0, (-50.0, -25.0)),
    ],
)
def test_scale_to_max_value_with_x_gt_y_with_good_values(max_value: float, expected: XY) -> None:
    """Test scale_to_max_value_with_x_gt_y"""
    test_object: XY = XY(100.0, 50.0)
    assert expected == test_object.scale_to_max_value(max_value).tuple()


@pytest.mark.parametrize(
    "max_value, expected",
    [
        (25.0, (12.5, 25.0)),
        (-50.0, (50.0, -25.0)),
        (-50.0, (-50.0, 25.0)),
    ],
)
def test_scale_to_max_value_with_x_gt_y_with_bad_values(max_value: float, expected: XY) -> None:
    """Test scale_to_max_value_with_x_gt_y"""
    test_object: XY = XY(100.0, 50.0)
    assert not expected == test_object.scale_to_max_value(max_value).tuple()
