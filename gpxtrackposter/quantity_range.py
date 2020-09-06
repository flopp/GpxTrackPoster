# Copyright 2016-2020 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import typing

import pint  # type: ignore


class QuantityRange:
    def __init__(self) -> None:
        self._lower: typing.Optional[pint.quantity.Quantity] = None
        self._upper: typing.Optional[pint.quantity.Quantity] = None

    @classmethod
    def from_pair(cls, value1: pint.quantity.Quantity, value2: pint.quantity.Quantity) -> "QuantityRange":
        r = cls()
        r.extend(value1)
        r.extend(value2)
        return r

    def clear(self) -> None:
        self._lower = None
        self._upper = None

    def is_valid(self) -> bool:
        return self._lower is not None

    def lower(self) -> typing.Optional[pint.quantity.Quantity]:
        return self._lower

    def upper(self) -> typing.Optional[pint.quantity.Quantity]:
        return self._upper

    def diameter(self) -> pint.quantity.Quantity:
        if self.is_valid():
            assert self._upper is not None
            assert self._lower is not None
            return self._upper - self._lower
        return 0

    def contains(self, value: pint.quantity.Quantity) -> bool:
        if not self.is_valid():
            return False

        assert self._upper is not None
        assert self._lower is not None
        return self._lower <= value <= self._upper

    def extend(self, value: pint.quantity.Quantity) -> None:
        if not self.is_valid():
            self._lower = value
            self._upper = value
        else:
            assert self._upper is not None
            assert self._lower is not None
            self._lower = min(self._lower, value)
            self._upper = max(self._upper, value)

    def interpolate(self, relative: float) -> pint.quantity.Quantity:
        if not self.is_valid():
            raise ValueError("Cannot interpolate invalid QuantityRange")
        assert self._lower is not None
        assert self._upper is not None
        return self._lower + relative * (self._upper - self._lower)

    def relative_position(self, value: pint.quantity.Quantity) -> float:
        if not self.is_valid():
            raise ValueError("Cannot get relaitive_position for invalid QuantityRange")
        assert self._lower is not None
        assert self._upper is not None
        if value <= self._lower:
            return 0.0
        if value >= self._upper:
            return 1.0
        diff = self._upper - self._lower
        if diff == 0:
            return 0.0
        return ((value - self._lower) / diff).magnitude
