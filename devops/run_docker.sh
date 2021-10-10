#!/bin/bash

SCRIPT_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd );
PROJECT_BASE=$(realpath ${SCRIPT_PATH}/..);
PUID=$(id -u);
PGID=$(id -g);

CMD="docker run -ti --rm --name=fbposter \
    -p 4444:4444 \
    -p 5000:5000 \
    -p 5678:5678 \
    -p 5900:5900 \
    -p 7900:7900 \
    # -v $PWD/fb_poster:/install \
    -e PUID=${PUID} \
    -e PGID=${PGID} \
    gitcuppajoe/fbposter:latest bash"

echo "${CMD}"
bash -c "${CMD}"