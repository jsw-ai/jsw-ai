cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while pgrep -f "gateq.sh work/k2_miamisway" >/dev/null; do sleep 10; done
bash work/waitmem.sh; python3 work/finish_v4C.py v2ibira v2beco v2wynwood v2beachbar v2havana v2keybis v2s1 v2s2 v2s3
cd fin; for n in ibira beco wynwood beachbar havana keybis s1 s2 s3; do bash ../work/waitmem.sh; /workspace/.face-venv/bin/python ../../../identity_gate.py v2${n}_v4C.jpg --model gabriela --source seedream --body --no-ocr --json > ../v2/gate_v2${n}.json 2>/dev/null; python3 -c "import json;d=json.load(open('../v2/gate_v2${n}.json'));d=d[0] if isinstance(d,list) else d;print('$n',d.get('pass_'),d.get('score_centroid'),d.get('body_pass'))"; done; echo FGDONE
