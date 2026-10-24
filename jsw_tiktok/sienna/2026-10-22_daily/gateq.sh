#!/bin/bash
# usage: gateq.sh NAME... ; finishes + gates stills not yet gated; appends to qc/gateq.log
cd /workspace/jsw_tiktok/sienna/2026-10-22_daily; export PATH=/tmp/bin:$PATH
for n in "$@"; do
  [ -f raw/$n.png ] || continue
  grep -q "reasons\|centroid" gate/$n.txt 2>/dev/null && continue
  [ -f fin/${n}_v4C.jpg ] || /workspace/.face-venv/bin/python finish_v4C.py $n >/dev/null 2>&1
  while [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 10; done
  /workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model sienna --source seedream --body fin/${n}_v4C.jpg > gate/$n.txt 2>/dev/null
  echo "$n $(grep -oE "PASS|FAIL" gate/$n.txt|head -1) $(grep -oE "centroid'?: ?[0-9.]+" gate/$n.txt|head -1) $(grep -oE "reasons': \[[^]]*\]" gate/$n.txt|head -1)" >> qc/gateq.log
done
