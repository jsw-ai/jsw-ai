cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
bash work/gateq.sh v2/k/kv2_beco.mp4 v2/k/kv2_wynwood.mp4 v2/k/kv2_ibira.mp4 v2/k/kv2_beachbar.mp4 v2/k/kv2_havana.mp4 v2/k/kv2_keybis.mp4 v2/k/kv2_clink7.mp4
bash work/waitmem.sh; python3 work/finish_v4C.py v2rdfoot v2rdarp
bash work/waitmem.sh; /workspace/.face-venv/bin/python ../../identity_gate.py img fin/v2rdfoot_v4C.jpg fin/v2rdarp_v4C.jpg --model gabriela --source seedream --body --no-ocr --json v2/gate_stills_v2rd.json
echo Q1DONE
