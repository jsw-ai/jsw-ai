#!/bin/bash
# g.sh clip fps -> qc/<name>.json + summary
v=$1; n=$(basename $v .mp4); fps=${2:-10}; d=qc/${n}_fr; rm -rf $d; mkdir -p $d
ffmpeg -loglevel error -y -i $v -vf fps=$fps -q:v 2 $d/f%04d.jpg
/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model charlotte --source seedream --no-ocr --json qc/$n.json $d/*.jpg >/dev/null 2>&1
python3 summ.py qc/$n.json
