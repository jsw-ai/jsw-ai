. work/w.sh
for m in tiktok igreel fb x reddit; do
 [ $m = x ] && n=x_24s_v4 || n=${m}_21s_v4; f=out/camille_bonsoir_monaco_$n.mp4
 [ -f $f ] || { w; python3 work/build_v4.py $m; }
 w; /workspace/.face-venv/bin/python work/vgate_multi.py ${f%.mp4}_silent.mp4
 ffmpeg -v error -y -i $f -vf "fps=0.6,scale=270:-1,tile=7x2" -frames:v 1 qc/sheet_$n.jpg
 echo "- $(date +%H:%M) v4 $n md5 $(md5sum $f|cut -c1-32) size $(stat -c%s $f) $(rg med work/run_v4.log | tail -1)" >> PROGRESS_SONGS.md
done; echo ALLDONE
