cd /workspace/hf-test/charlotte_1022/rb2
while ! grep -q JETTY_DONE ../quota2/progress.md; do sleep 20; done
for c in vK2a vK2b; do ffmpeg -loglevel error -y -i v10/clips/$c.mp4 -vf "crop=623:1108:100:0,scale=1080:1920:flags=lanczos" -c:v libx264 -crf 14 -preset fast -threads 2 -pix_fmt yuv420p v10/clips/${c}_c.mp4; bash gw.sh /workspace/.face-venv/bin/python ../quota2/work/vgate.py v10/clips/${c}_c.mp4 10 v10/qc/raw_$c.json 2>&1 | tail -2 >> progress.md; done
echo COLLAB_GATES_DONE >> progress.md
