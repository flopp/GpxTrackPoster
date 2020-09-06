#!/bin/bash

set -euo pipefail

for FIT in "$@" ; do
    GPX="${FIT}.gpx"
    if [ -f "${GPX}" ] ; then
        continue
    fi

    echo "${FIT}"
    gpsbabel -i garmin_fit -f "${FIT}" -o gpx -F "${GPX}"
done