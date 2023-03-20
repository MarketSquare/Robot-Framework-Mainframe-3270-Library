#!/bin/sh
Xvfb :1 -screen 0 1152x900x8 -nolisten tcp -nolisten unix &
export DISPLAY=:1.0

exec "$@"