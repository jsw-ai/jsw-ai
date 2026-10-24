#!/bin/bash
cd /workspace/jsw_tiktok/sienna/2026-10-22_daily/fc_v2
for n in "$@"; do [ -f gate/v_$n.json ] && continue; [ -f kl/$n.mp4 ] || continue
 . ./waitfree.sh; echo "$(date +%T) free=$(free -g|awk '/Mem/{print $7}')G start $n" >> qc/vq.log
 ./vg.py kl/$n.mp4 2>/dev/null | head -1 >> qc/vq.log
 python3 -c "
import json;d=json.load(open('gate/v_$n.json'));print('$n',''.join('.' if (x[1] is not None and x[1]>=0.78) else 'x' for x in d['per_frame']))" >> qc/vq.log
done
