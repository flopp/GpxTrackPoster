#!/usr/bin/env python

# Copyright 2018-2020 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys

USAGE = sys.stdin.read()
readme_md_file_name = sys.argv[0]

if not USAGE.startswith("usage: create_poster"):
    raise RuntimeError("Bad usage info from stdin")

# replace usage in README.md
with open(readme_md_file_name, "r") as f:
    lines = f.readlines()
    with open(readme_md_file_name, "w") as f:
        STATE = 0
        for line in lines:
            if STATE == 0:
                f.write(line)
                if line.startswith("## Usage"):
                    STATE = 1
            elif STATE == 1:
                f.write(line)
                if line.startswith("```"):
                    STATE = 2
                    f.write(USAGE)
            elif STATE == 2:
                if line.startswith("```"):
                    f.write(line)
                    STATE = 3
            else:
                f.write(line)
