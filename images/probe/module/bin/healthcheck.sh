#!/bin/bash

[ -e "/opt/module/data/logs.csv" ] || exit 1
ps -ef | grep module | grep -q probe.py || exit 1
