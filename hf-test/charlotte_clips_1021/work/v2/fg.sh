#!/bin/bash
# usage: fg.sh NAME=URL ...
cd /workspace/hf-test/charlotte_clips_1021/work
F=()
for a in "$@"; do n=${a%%=*}; u=${a#*=}; curl -s -o raw/$n.png "$u"; F+=(fin/${n}_v4C.jpg); N+=($n); done
python3 finish_v4C.py "${N[@]}" >/dev/null
cd /workspace/hf-test && /workspace/.face-venv/bin/python zen/posting/identity_gate.py img --model charlotte --source seedream --body "${F[@]/#/charlotte_clips_1021/work/}" 2>/dev/null | grep -E "^(PASS|FAIL)" | sed -E "s/'body'.*//"
cd charlotte_clips_1021/work && python3 - "${F[@]}" <<'P'
import sys;from PIL import Image
f=sys.argv[1:];ims=[Image.open(x).convert('RGB').resize((300,533)) for x in f]
s=Image.new('RGB',(300*len(f),533));[s.paste(im,(i*300,0)) for i,im in enumerate(ims)];s.save('v2/sheet_last.jpg',quality=85)
P
