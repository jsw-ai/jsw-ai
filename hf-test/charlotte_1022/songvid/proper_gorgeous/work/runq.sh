#!/bin/bash
# wait for >=3GB avail and no other gate process (max 25 min then only mem rule)
s=$(date +%s)
while true; do
  a=$(free -g | awk '/Mem:/{print $7}'); n=$(pgrep -f 'gate' | grep -v $$ | wc -l)
  if [ "$a" -ge 3 ] && { [ "$n" -eq 0 ] || [ $(( $(date +%s)-s )) -gt 1500 ]; }; then break; fi
  sleep 20
done
echo "start $(date) avail=$a others=$n"
exec "$@"
