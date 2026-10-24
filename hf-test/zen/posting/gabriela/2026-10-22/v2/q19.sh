cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -q Q18DONE v2/q18.log; do sleep 30; done
bash work/waitmem.sh; python3 v2/build_fan.py; bash work/gateq.sh final/gabriela_tiktok_20261022_fan-reveal_v4.mp4; echo Q19DONE
