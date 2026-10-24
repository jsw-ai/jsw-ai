cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while pgrep -f "gateq.sh v2/k/kf_t1" >/dev/null; do sleep 20; done
bash work/waitmem.sh; /workspace/.face-venv/bin/python ../../identity_gate.py img fin/fx2b_v4C.jpg fin/fs1b_v4C.jpg fin/frd2b_v4C.jpg fin/ft3b_v4C.jpg --model gabriela --source seedream --body --no-ocr --json v2/gate_fri_b.json
echo Q13DONE
