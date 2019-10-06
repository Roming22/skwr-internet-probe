#!/bin/bash
set -e
BIN_DIR=`cd $(dirname $0); pwd`

# Let SKWR know that the container is up and running
echo "[`hostname -s`] Started"

python3 -u $BIN_DIR/probe.py
