set -u
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
G="/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py"
waitfree(){ while pgrep -f identity_gate.py >/dev/null; do sleep 0.5; done; }
for s in T3_a T3_b CL Y1_a Y1_b Y1_c Y1_d; do waitfree; echo "== $s"; $G video --model gabriela --no-ocr --json qc/rev_v3/$s.json qc/rev_v3/$s.mp4 2>&1 | tail -2; done
waitfree; echo "== stills"; $G img --model gabriela --source seedream --no-ocr --json qc/rev_v3/stills.json final/stories_v3/*.jpg final/gabriela_x_20261022_paodequeijo_v3.jpg final/gabriela_reddit_20261023_foot_b_v3.jpg 2>&1 | tail -12
echo DONE
