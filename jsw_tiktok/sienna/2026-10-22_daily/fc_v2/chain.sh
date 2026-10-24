#!/bin/bash
cd /workspace/jsw_tiktok/sienna/2026-10-22_daily/fc_v2
while pgrep -f "vg.py kl/" >/dev/null; do sleep 5; done
./gq.sh GA_1 GA_2 GA_3 GA_4 GB_1 GB_2 GB_3 GB_4
STEP=2 ./vq.sh vB_4 vB_5 vB_6 vC_4 vC_5 vC_6
