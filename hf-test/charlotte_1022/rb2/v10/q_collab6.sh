cd /workspace/hf-test/charlotte_1022/rb2
while ! grep -q GATES3_DONE progress.md; do sleep 20; done
bash gw.sh ffmpeg -nostdin -loglevel error -y -i v10/clips/vK2b_c.mp4 -i v4/try_cat.mp4 -filter_complex "[0:v]trim=0:4.0,setpts=PTS-STARTPTS,fps=30,setsar=1[a];[1:v]fps=30,setsar=1,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" -c:v libx264 -crf 14 -preset fast -threads 2 -pix_fmt yuv420p v10/collab6_cat.mp4
timeout 1500 python3 v5/enc2.py v10/collab6.json >> progress.md 2>&1
bash gw.sh /workspace/.face-venv/bin/python ../quota2/work/vgate.py final/charlotte_collab_20261022_oktoberfest-stein-clink_v6.mp4 10 v10/qc/fin_collab6.json 2>&1 | tail -2 | head -1 >> progress.md
echo COLLAB6_DONE >> progress.md
