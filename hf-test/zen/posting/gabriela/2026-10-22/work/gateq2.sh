#!/bin/bash
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -qE "QDONE|TIMEOUT" work/gateq1.log; do sleep 20; done
bash work/gateq.sh work/k2_miamisway_s.mp4 collab/gabriela_collab_oktoberfest_saude_v2_silent.mp4
bash work/waitmem.sh && /workspace/.face-venv/bin/python ../../identity_gate.py img --model gabriela --source seedream --body --no-ocr --json qc/gate_stills_b3.json fin/okt_a_v4C.jpg fin/padaria_d_v4C.jpg
echo Q2DONE
