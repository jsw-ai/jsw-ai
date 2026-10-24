#!/bin/bash
# wait until >=3 GB available, then run the given command
while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 20; done
echo "start avail=$(free -g | awk '/Mem:/{print $7}')G $(date +%T)"; "$@"
