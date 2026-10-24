cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while pgrep -f "v2/q9.sh" >/dev/null; do sleep 20; done
true
bash work/waitmem.sh; /workspace/.face-venv/bin/python ../../identity_gate.py img fin/fx1_v4C.jpg fin/fx2_v4C.jpg fin/fx3_v4C.jpg fin/fs1_v4C.jpg fin/fs2_v4C.jpg fin/fs3_v4C.jpg fin/frd2_v4C.jpg fin/ft1_v4C.jpg fin/ft2_v4C.jpg fin/ft3_v4C.jpg fin/fyt1_v4C.jpg fin/fyt2_v4C.jpg --model gabriela --source seedream --body --no-ocr --json v2/gate_fri.json
echo Q10DONE
