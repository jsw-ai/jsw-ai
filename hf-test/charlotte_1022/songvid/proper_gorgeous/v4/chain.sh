cd /workspace/hf-test/charlotte_1022/songvid/proper_gorgeous/v4
P=/workspace/.face-venv/bin/python
for c in x hook ytshorts; do
 n=$(python3 -c "import json;print(json.load(open('cfg_$c.json'))['name'])")
 python3 build3.py cfg_$c.json && echo "- $(date +%H:%M) v4 $c encoded" >> ../v2/progress.md && bash gw.sh $P pershot.py $n && $P sbs.py $n
 echo "STEP_DONE $c"; echo "- $(date +%H:%M) v4 $c gated: $(python3 -c "import json;print('PASS' if json.load(open('qc/${n}_gate.json'))['pass_'] else 'FAIL')")" >> ../v2/progress.md
done; echo CHAIN_DONE
