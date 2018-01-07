#!/usr/bin/env python

# Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys

#
# Replace 'Usage' code section in README.md file (argv[1]) with actual usage text from stdin.
#

readme_file = sys.argv[1]
readme = []
with open(readme_file, 'r') as f:
    readme = f.readlines()

with open(readme_file, 'w') as f:
    state = 0
    for line in readme:
        if state == 0:
            f.write(line)
            if line.startswith('## Usage'):
                state = 1
        elif state == 1:
            f.write(line)
            if line.startswith('```'):
                state = 2
                # insert actual usage message from stdin
                f.write(sys.stdin.read())
        elif state == 2:
            if line.startswith('```'):
                f.write(line)
                state = 3
        else:
            f.write(line)
