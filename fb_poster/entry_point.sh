#!/bin/sh

RCol='\e[0m'    # Reset Color
Red='\e[0;31m'; # Red Text

# turn on bash's job control
set -m

echo "Setting up services..."

if [ $1 = "debug" ]; then
    echo "Debug mode selected."
    /opt/bin/entry_point.sh &
    echo "${Red}Flask not running. Debugger listening on port 5678. You must attach...${RCol}"
    python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run --host=0.0.0.0 # Listen on port 5678
else
    echo "Release mode selected"
    /opt/bin/entry_point.sh & # Start the primary process and put it in the background. This is the selenium entry point.
    python3 -m flask run --host=0.0.0.0 # Start the webhook process. In this instance, it is app.py.
    fg %1 # Now we bring the primary process back into the foreground and leave it there.
fi