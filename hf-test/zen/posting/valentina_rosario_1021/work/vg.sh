#!/bin/bash
# usage: vg.sh clip.mp4 tag  -> 10 frames gate
v=$1; t=$2; mkdir -p fr_$t; rm -f fr_$t/*
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $v)
for i in $(seq 0 9); do ts=$(python3 -c "print(round(($i+0.5)*$d/10,2))"); ffmpeg -v error -y -ss $ts -i $v -frames:v 1 fr_$t/f_$ts.png; done
/workspace/.face-venv/bin/python ../../identity_gate.py img --model valentina --source seedream ${@:3} fr_$t/*.png 2>&1 | grep -E "PASS|FAIL"
