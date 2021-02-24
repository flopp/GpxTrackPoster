#!/usr/bin/env python

# Copyright 2018-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import re
import sys


def has_valid_copyright(file_name: str) -> bool:
    re_copyright = re.compile(rf"{datetime.datetime.now().year} Florian Pigorsch")
    re_copyright_bad_year = re.compile(r"\d\d\d\d Florian Pigorsch")

    ok = True
    empty = True
    copyright_found = False
    copyright_bad_year_found = False

    with open(file_name, "r") as f:
        for line in f.readlines():
            empty = False
            if re_copyright.search(line):
                copyright_found = True
                break
            if re_copyright_bad_year.search(line):
                copyright_bad_year_found = True
                break

    if not empty:
        if copyright_bad_year_found:
            print(f"{file_name}: copyright with bad year")
            ok = False
        elif not copyright_found:
            print(f"{file_name}: no copyright")
            ok = False

    return ok


if not all([has_valid_copyright(file_name) for file_name in sys.argv]):
    sys.exit(1)

sys.exit(0)
