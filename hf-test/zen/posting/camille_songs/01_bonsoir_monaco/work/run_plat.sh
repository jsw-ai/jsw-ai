cd /workspace/hf-test/zen/posting/camille_songs/01_bonsoir_monaco
P=/workspace/hf-test/zen/posting/camille_oct22/PROGRESS_SONGS.md
m(){ while [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 15; done; }
for p in tiktok igreel fb reddit ytshorts; do
 m; python3 work/build_v2.py $p && echo "- render $p done $(date +%H:%M)" >> $P
 m; r=$(/workspace/.face-venv/bin/python work/vgate_multi.py out/camille_bonsoir_monaco_${p}_21s_v2_silent.mp4 2>&1 | rg med); echo "- gate $p: $r" >> $P; echo "$r"
done; echo ALL_DONE
