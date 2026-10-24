cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while pgrep -f "v2/q4.sh" >/dev/null; do sleep 20; done
bash work/waitmem.sh; python3 work/finish_v4C.py v3rdfoot v3rdarp
bash work/waitmem.sh; /workspace/.face-venv/bin/python ../../identity_gate.py img fin/v3rdfoot_v4C.jpg fin/v3rdarp_v4C.jpg --model gabriela --source seedream --body --no-ocr --json v2/gate_stills_v3rd.json
echo Q5DONE
