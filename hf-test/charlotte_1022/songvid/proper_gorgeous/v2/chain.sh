#!/bin/bash
cd /workspace/hf-test/charlotte_1022/songvid/proper_gorgeous/v2
for k in hook x ytshorts; do
  n=$(python3 -c "import json;print(json.load(open('cfg_$k.json'))['name'])")
  [ -f final/$n.mp4 ] || python3 build3.py cfg_$k.json || exit 1
  bash gw.sh ./pershot.py $n 2>&1 | grep -E "PASS|FAIL|Error"
  echo "- $(date +%H:%M) gated $n: $(grep -c . qc/${n}_perframe.csv) rows; see qc/${n}_gate.json" >> ../../progress.md
done
echo CHAIN_DONE
