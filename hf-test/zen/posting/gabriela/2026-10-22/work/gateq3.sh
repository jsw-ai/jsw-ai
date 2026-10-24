#!/bin/bash
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
export GFPS=12
for f in collab/gabriela_collab_oktoberfest_saude_v2_silent.mp4 final/gabriela_tiktok_20261022_spvsmiami-ep1_v1.mp4 final/gabriela_tiktok_20261022_paulistanos-thursday_v2.mp4 final/gabriela_tiktok_20261022_fan-reveal_v1.mp4 final/gabriela_yt_20261022_caipirinha-kiss_v1.mp4; do
  bash work/waitmem.sh || { echo TIMEOUT; exit 1; }; echo "$(date +%T) gate $f"; work/pf_gate.py "$f" || echo "FAILRUN $f"; done
bash work/waitmem.sh && /workspace/.face-venv/bin/python ../../identity_gate.py img --model gabriela --source seedream --body --no-ocr --json qc/gate_stills_b3.json fin/okt_a_v4C.jpg fin/padaria_d_v4C.jpg
echo Q3DONE
