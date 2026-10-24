set -u
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
G="/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py"
cut(){ ffmpeg -v error -y -ss $3 -to $4 -i $2 -an -c:v libx264 -crf 12 qc/rev_v3/$1.mp4; }
F=final
cut T1_a $F/gabriela_tiktok_20261022_paulistanos-thursday_v3.mp4 0 2.8
cut T1_b $F/gabriela_tiktok_20261022_paulistanos-thursday_v3.mp4 2.8 6.3
cut T2_a $F/gabriela_tiktok_20261022_spvsmiami-ep1_v2.mp4 0 2.6
cut T2_b $F/gabriela_tiktok_20261022_spvsmiami-ep1_v2.mp4 2.6 6.0
cut T3_a $F/gabriela_tiktok_20261022_fan-reveal_v3.mp4 0 1.0
cut T3_b $F/gabriela_tiktok_20261022_fan-reveal_v3.mp4 1.0 4.6
cut Y1_a $F/gabriela_yt_20261022_caipirinha-kiss_v2.mp4 0 1.2
cut Y1_b $F/gabriela_yt_20261022_caipirinha-kiss_v2.mp4 1.2 2.4
cut Y1_c $F/gabriela_yt_20261022_caipirinha-kiss_v2.mp4 2.4 7.4
cut Y1_d $F/gabriela_yt_20261022_caipirinha-kiss_v2.mp4 7.4 12.4
cut R_a $F/gabriela_igreel_20261022_spvsmiami-ep1_v3.mp4 0 2.7
cut R_b $F/gabriela_igreel_20261022_spvsmiami-ep1_v3.mp4 2.7 6.1
cp collab/gabriela_collab_oktoberfest_clink_v8_silent.mp4 qc/rev_v3/CL.mp4
waitfree(){ while pgrep -f identity_gate.py >/dev/null; do sleep 10; done; }
for s in T1_a T1_b T2_a T2_b T3_a T3_b Y1_a Y1_b Y1_c Y1_d R_a R_b CL; do waitfree; echo "== $s"; $G video --model gabriela --no-ocr --json qc/rev_v3/$s.json qc/rev_v3/$s.mp4 2>&1 | tail -4; done
waitfree; echo "== stills"; $G img --model gabriela --source seedream --no-ocr --json qc/rev_v3/stills.json final/stories_v3/*.jpg final/gabriela_x_20261022_paodequeijo_v3.jpg final/gabriela_reddit_20261023_foot_b_v3.jpg 2>&1 | tail -12
echo DONE
