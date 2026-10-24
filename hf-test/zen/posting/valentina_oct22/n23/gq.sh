#!/bin/bash
# gate queue: waits for >=3 GB available before each gate
cd /workspace/hf-test/zen/posting/valentina_oct22/n23
for f in "$@"; do
  while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 15; done
  echo "$(date +%H:%M) avail=$(free -g | awk '/Mem:/{print $7}')G gating $f"
  /workspace/.face-venv/bin/python vg.py $f 2>&1 | grep mp4
done
