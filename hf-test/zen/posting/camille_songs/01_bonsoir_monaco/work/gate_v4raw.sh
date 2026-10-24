. work/w.sh
for f in raw/K4_*.mp4; do b=$(basename $f .mp4); ffmpeg -v error -y -i $f -vf "fps=2,scale=160:-1,tile=10x1" -frames:v 1 qc/feet_$b.jpg; done
w; /workspace/.face-venv/bin/python work/vgate_multi.py raw/K4_*.mp4; echo GDONE
