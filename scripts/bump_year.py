#!/usr/bin/env python

# Copyright 2018-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import re
import sys

THIS_YEAR = str(datetime.datetime.now().year)
re_year = re.compile(r"\s(\d\d\d\d) Florian Pigorsch")
re_year_range = re.compile(r"\s(\d\d\d\d)-(\d\d\d\d) Florian Pigorsch")


def bump_year(file_name: str) -> None:
    lines = []
    with open(file_name, "r", encoding="utf8") as f:
        for line in f.readlines():
            m = re_year.search(line)
            if m and (m.group(1) != THIS_YEAR):
                start, end = m.span(1)
                lines.append(f"{line[:end]}-{THIS_YEAR}{line[end:]}")
                continue

            m = re_year_range.search(line)
            if m and (m.group(2) != THIS_YEAR):
                start, end = m.span(2)
                lines.append(f"{line[:start]}{THIS_YEAR}{line[end:]}")
                continue

            lines.append(line)

    with open(file_name, "w", encoding="utf8") as f:
        f.writelines(lines)


for arg in sys.argv:
    bump_year(arg)
