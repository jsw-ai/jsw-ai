#!/bin/bash
cd /workspace/jsw_tiktok/sienna/2026-10-22_daily/fc_v2; export PATH=/tmp/bin:$PATH
for n in "$@"; do
  [ -f raw/$n.png ] || continue
  grep -q "centroid" gate/$n.txt 2>/dev/null && continue
  [ -f fin/${n}_v4C.jpg ] || /workspace/.face-venv/bin/python finish_v4C.py $n >/dev/null 2>&1
  . ./waitfree.sh; echo "$(date +%T) free=$(free -g|awk '/Mem/{print $7}')G start $n" >> qc/gq.log
  /workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model sienna --source seedream --body fin/${n}_v4C.jpg > gate/$n.txt 2>/dev/null
  echo "$n $(grep -oE "centroid'?: ?[0-9.]+" gate/$n.txt|head -1) $(grep -oE "reasons': \[[^]]*\]" gate/$n.txt|head -1)" >> qc/gq.log
done
