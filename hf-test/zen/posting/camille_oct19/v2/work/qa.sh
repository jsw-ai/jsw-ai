# usage: qa.sh name mp4 start
set -e; cd /workspace/hf-test/zen/posting/camille_oct19/v2
N=$1; M=$2; S=$3; G=/workspace/.face-venv/bin/python; GATE=/workspace/hf-test/zen/posting/identity_gate.py
python3 work/sbs.py $N $M $S
$G $GATE video --model camille_v3_draft --frames 10 --json work/gate_${N}_video.json $M 2>/dev/null | tail -2 || true
$G $GATE img --model camille_v3_draft --json work/gate_${N}_frames.json $(python3 -c "import json;print(' '.join(json.load(open('frames/$N/list.json'))))") 2>/dev/null | rg -o "^(PASS|FAIL).*" || true
$G ../work/eyes.py $M 2>/dev/null | rg -c CLOSED || true
