cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -q Q14DONE v2/q14.log; do sleep 20; done
bash work/waitmem.sh; python3 v2/build_fri.py FT3; bash work/gateq.sh final/gabriela_tiktok_20261023_guarana-cheers_v1.mp4; echo Q15DONE
