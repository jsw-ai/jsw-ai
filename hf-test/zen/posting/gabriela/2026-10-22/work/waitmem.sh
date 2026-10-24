#!/bin/bash
for i in $(seq 1 36); do a=$(free -g|awk '/Mem/{print $7}'); [ "$a" -ge 3 ] && exit 0; echo "$(date +%T) avail=${a}G waiting"; sleep 300; done; exit 1
