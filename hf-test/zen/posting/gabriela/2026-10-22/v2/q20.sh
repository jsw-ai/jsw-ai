cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -q Q19DONE v2/q19.log; do sleep 30; done
bash work/waitmem.sh; python3 v2/build_v6.py T2; bash work/gateq.sh final/gabriela_tiktok_20261022_spvsmiami-ep1_v6.mp4; echo Q20DONE
