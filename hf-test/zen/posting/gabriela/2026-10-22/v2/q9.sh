cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while pgrep -f "Q8DONE" >/dev/null; do sleep 20; done
bash work/gateq.sh v2/k/kv4_reel2.mp4
bash work/waitmem.sh; python3 v2/build_v4.py REEL
bash work/gateq.sh final/gabriela_igreel_20261022_spvsmiami-ep1_v4.mp4
echo Q9DONE
