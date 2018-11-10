#!/usr/bin/env python

# Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import datetime
import re
import sys

re_copyright = re.compile(r'{} Florian Pigorsch'.format(datetime.datetime.now().year))
re_copyright_bad_year = re.compile(r'\d\d\d\d Florian Pigorsch')
errors = False

for file_name in sys.argv:
    empty = True
    copyright_found = False
    copyright_bad_year_found = False

    with open(file_name, 'r') as f:
        for line in f.readlines():
            empty = False
            if re_copyright.search(line):
                copyright_found = True
                break
            elif re_copyright_bad_year.search(line):
                copyright_bad_year_found = True
                break

    if not empty:
        if copyright_bad_year_found:
            print('{}: copyright with bad year'.format(file_name))
            errors = True
        elif not copyright_found:
            print('{}: no copyright'.format(file_name))
            errors = True

if errors:
    sys.exit(1)

sys.exit(0)
