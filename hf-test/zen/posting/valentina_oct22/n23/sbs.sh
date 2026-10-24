#!/bin/bash
# sbs.sh video out times...
v=$1; o=$2; shift 2; d=$(mktemp -d); i=0
for t in "$@"; do ffmpeg -loglevel error -y -ss $t -i $v -frames:v 1 -vf scale=-2:640 $d/f$i.png; i=$((i+1)); done
ffmpeg -loglevel error -y -i /workspace/hf-test/zen/posting/valentina_test2/fin/s2_b_v4C.jpg -vf scale=-2:640 $d/ref.png
ffmpeg -loglevel error -y $(for f in $d/ref.png $d/f*.png; do echo -i $f; done) -filter_complex "hstack=inputs=$((i+1))" $o
