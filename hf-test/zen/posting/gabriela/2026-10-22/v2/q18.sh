cd /workspace/hf-test/zen/posting/gabriela/2026-10-22

bash work/waitmem.sh; python3 v2/build_v5.py T1 T2 REEL; python3 v2/build_fri.py FT1 FT2 FY1 FY2
bash work/gateq.sh final/*_v5.mp4 final/gabriela_tiktok_20261023_studio-warmup_v2.mp4 final/gabriela_tiktok_20261023_miami-pier_v3.mp4 final/gabriela_yt_20261023_studio-day_v2.mp4 final/gabriela_yt_20261023_rooftop-night_v2.mp4
echo Q18DONE
