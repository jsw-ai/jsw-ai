#!/bin/bash
# usage: waitmem.sh cmd...   waits until available >=3GB, then runs
while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done
echo "start $(date +%T) avail $(free -g | awk '/Mem:/{print $7}')G"; "$@"
