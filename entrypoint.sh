#!/bin/sh

Xvfb :1 -screen 0 1152x900x8&
export DISPLAY=:1.0

if [ ! -z $1 ]
then
   singleTest="--test $1"
fi
robot $singleTest --logLevel TRACE:INFO /tests 