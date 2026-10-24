#!/bin/bash
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -qE "Q4DONE" work/gateq4.log; do sleep 20; done
bash work/waitmem.sh && /workspace/.face-venv/bin/python ../../identity_gate.py img --model gabriela --source seedream --body --no-ocr --json qc/gate_stills_b4.json fin/padaria_e_v4C.jpg fin/padaria_f_v4C.jpg
bash work/gateq.sh final/gabriela_tiktok_20261022_fan-reveal_v2.mp4; echo Q5DONE
