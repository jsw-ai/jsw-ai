cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
bash work/waitmem.sh; /workspace/.face-venv/bin/python ../../identity_gate.py img fin/fx2b_v4C.jpg fin/fs1b_v4C.jpg fin/frd2b_v4C.jpg fin/ft3b_v4C.jpg --model gabriela --source seedream --body --no-ocr --json v2/gate_fri_b.json
bash work/waitmem.sh; python3 v2/build_fri.py FT1 FT2 FY1 FY2
bash work/gateq.sh final/gabriela_tiktok_20261023_studio-warmup_v1.mp4 final/gabriela_tiktok_20261023_miami-pier_v1.mp4 final/gabriela_yt_20261023_studio-day_v1.mp4 final/gabriela_yt_20261023_rooftop-night_v1.mp4
echo Q14DONE
