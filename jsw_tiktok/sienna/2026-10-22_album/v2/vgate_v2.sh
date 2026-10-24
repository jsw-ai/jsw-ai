#!/bin/bash
# usage: vgate_v2.sh clip.mp4 tag  -> identity at 2 fps, frames for eye check at 5 fps
c=$1; t=$2; D=/workspace/jsw_tiktok/sienna/2026-10-22_album/v2/fr_$t; mkdir -p $D/id $D/eye; rm -f $D/id/* $D/eye/*
ffmpeg -v error -i $c -vf fps=${GFPS:-2} $D/id/f_%03d.png
ffmpeg -v error -i $c -vf fps=5 $D/eye/e_%03d.png
/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model sienna --source seedream $D/id/*.png > $D/gate_raw.txt 2>&1
grep -E "PASS|FAIL" $D/gate_raw.txt | sed -E "s/.*f_([0-9]+)\.png.*score_centroid': ([0-9.]+).*/\1 \2/" | grep -E "^[0-9]+ [0-9.]+$" | sort -n > $D/gate.txt
n=$(ls $D/id|wc -l); s=$(wc -l < $D/gate.txt); p=$(awk '$2>=0.78' $D/gate.txt|wc -l)
echo "$t frames=$n scored=$s pass78=$p pct=$(awk -v p=$p -v s=$s "BEGIN{printf \"%.1f\",100*p/s}") min=$(sort -k2 -n $D/gate.txt|head -1) below60=$(awk '$2<0.6' $D/gate.txt|wc -l)"
