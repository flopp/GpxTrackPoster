# Copyright 2016-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import typing

import pint  # type: ignore


class Units:
    _instance = None

    def __init__(self) -> None:
        if not Units._instance:
            Units._instance = pint.UnitRegistry()

    def __getattr__(self, name: str) -> typing.Any:
        return getattr(Units._instance, name)
