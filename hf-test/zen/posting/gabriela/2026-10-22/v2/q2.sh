cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while pgrep -f "v2/q1.sh" >/dev/null; do sleep 15; done
for k in T1 T2 T3; do bash work/waitmem.sh; python3 v2/build_v3.py $k; done
bash work/gateq.sh final/gabriela_tiktok_20261022_paulistanos-thursday_v3.mp4 final/gabriela_tiktok_20261022_spvsmiami-ep1_v2.mp4 final/gabriela_tiktok_20261022_fan-reveal_v3.mp4
for k in Y1 REEL; do bash work/waitmem.sh; python3 v2/build_v3.py $k; done
bash work/gateq.sh final/gabriela_yt_20261022_caipirinha-kiss_v2.mp4 final/gabriela_igreel_20261022_spvsmiami-ep1_v3.mp4
bash work/waitmem.sh; python3 v2/clink_v7.py; bash work/gateq.sh collab/gabriela_collab_oktoberfest_clink_v7_silent.mp4
echo Q2DONE
