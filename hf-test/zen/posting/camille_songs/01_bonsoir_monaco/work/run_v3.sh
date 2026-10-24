. work/w.sh
for m in hook x tiktok igreel fb reddit ytshorts; do
 case $m in hook) n=hook_21s_v3;; x) n=x_24s_v3;; *) n=${m}_21s_v3;; esac
 f=out/camille_bonsoir_monaco_$n.mp4
 [ -f $f ] || { w; python3 work/build_v3.py $m; }
 echo "ok $f $(md5sum $f|cut -c1-32) $(stat -c%s $f)"
 w; /workspace/.face-venv/bin/python work/vgate_multi.py ${f%.mp4}_silent.mp4
 ffmpeg -v error -y -i $f -vf "fps=0.6,scale=270:-1,tile=7x2" -frames:v 1 qc/sheet_$n.jpg
 echo "- $(date +%H:%M) v3 $n md5 $(md5sum $f|cut -c1-32) $(tail -1 work/run_v3.log | rg med)" >> /workspace/hf-test/zen/posting/camille_oct22/PROGRESS_SONGS.md
done; echo ALLDONE
