set -x
F=final
if ! ffprobe -v error $F/charlotte_yt_20261022_matchday-vs-recovery_v5.mp4 2>/dev/null; then python3 v5/enc2.py v5/yt1.json && echo "- YT1 v5 encoded $(date +%T)" >> progress.md; fi
if ! ffprobe -v error $F/charlotte_x_20261022_pilates-vs-icebath_v5.mp4 2>/dev/null; then python3 v5/enc2.py v5/x2.json && echo "- X2 v5 encoded $(date +%T)" >> progress.md; fi
python3 v5/enc2.py v5/collab.json
for v in yt1:charlotte_yt_20261022_matchday-vs-recovery_v5 x2:charlotte_x_20261022_pilates-vs-icebath_v5 collab:charlotte_collab_20261022_oktoberfest-stein-clink_v5; do k=${v%%:*}; f=${v#*:}
 [ -f v5/qc/${k}_v5_scores.json ] && continue
 bash gw.sh python3 ../rb/vgate.py $F/$f.mp4 10 v5/qc/${k}_v5.json > v5/qc/${k}_v5_gate.log 2>&1; echo "- gate $k: $(sed -n 2p v5/qc/${k}_v5_gate.log | cut -d' ' -f2-)" >> progress.md
done
echo ALLDONE
