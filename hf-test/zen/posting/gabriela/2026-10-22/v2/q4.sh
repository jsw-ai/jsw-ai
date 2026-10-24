while pgrep -f "gateq.sh final/gabriela_tiktok_20261022_paulistanos" >/dev/null; do sleep 20; done
bash work/waitmem.sh; python3 v2/build_v3.py T3
bash work/waitmem.sh; python3 v2/clink_v8.py
bash work/gateq.sh final/gabriela_tiktok_20261022_fan-reveal_v3.mp4 collab/gabriela_collab_oktoberfest_clink_v8_silent.mp4
echo Q4DONE
