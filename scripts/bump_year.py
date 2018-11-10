#!/usr/bin/env python

# Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import re
import sys

this_year = str(datetime.datetime.now().year)
re_year = re.compile(r'\s(\d\d\d\d) Florian Pigorsch')
re_year_range = re.compile(r'\s(\d\d\d\d)-(\d\d\d\d) Florian Pigorsch')


def bump_year(file_name):
    lines = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            m = re_year.search(line)
            if m and (m.group(1) != this_year):
                start, end = m.span(1)
                lines.append('{}-{}{}'.format(line[:end], this_year, line[end:]))
                continue

            m = re_year_range.search(line)
            if m and (m.group(2) != this_year):
                start, end = m.span(2)
                lines.append('{}{}{}'.format(line[:start], this_year, line[end:]))
                continue

            lines.append(line)

    with open(file_name, 'w') as f:
        f.writelines(lines)


for arg in sys.argv:
    bump_year(arg)
