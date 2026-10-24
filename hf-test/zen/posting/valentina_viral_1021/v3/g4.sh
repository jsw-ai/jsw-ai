#!/bin/bash
# g4.sh clip tag step -> per-time gate
v=$1;t=$2;s=${3:-0.25}; mkdir -p fr_$t; rm -f fr_$t/*
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $v)
for ts in $(python3 -c "import numpy as n;print(' '.join('%.2f'%x for x in n.arange(0.05,$d-0.02,$s)))"); do ffmpeg -v error -y -ss $ts -i $v -frames:v 1 fr_$t/f_$ts.png; done
/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model valentina --source seedream fr_$t/*.png 2>&1 | grep -E "PASS|FAIL" | sed -E "s/.*f_([0-9.]+)\.png.*score_centroid': ([0-9.]+).*/\1 \2/" | sort -n | tr '\n' ' '; echo
