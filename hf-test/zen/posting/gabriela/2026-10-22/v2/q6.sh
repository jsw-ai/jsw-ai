cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
bash work/waitmem.sh; python3 work/finish_v4C.py v4t1a v4reel v4t2sp v4t2mia v4s1 v4s2
bash work/waitmem.sh; /workspace/.face-venv/bin/python ../../identity_gate.py img fin/v4t1a_v4C.jpg fin/v4reel_v4C.jpg fin/v4t2sp_v4C.jpg fin/v4t2mia_v4C.jpg fin/v4s1_v4C.jpg fin/v4s2_v4C.jpg --model gabriela --source seedream --body --no-ocr --json v2/gate_stills_v4.json
echo Q6DONE
