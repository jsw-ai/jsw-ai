cd /workspace/hf-test/charlotte_1022/songvid/proper_gorgeous/v3
P=/workspace/.face-venv/bin/python
for c in ytshorts hook x; do
 n=$(python3 -c "import json;print(json.load(open('cfg_$c.json'))['name'])")
 bash gw.sh python3 build3.py cfg_$c.json && bash gw.sh $P pershot.py $n && $P sbs.py $n
 echo "STEP_DONE $c"; echo "- $(date +%H:%M) v3 $c built+gated" >> ../../progress.md
done; echo CHAIN_DONE
