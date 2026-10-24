. work/w.sh
for f in raw/K_M02s_v.mp4 raw/K_M02t_v.mp4; do w; /workspace/.face-venv/bin/python work/vgate_multi.py $f; done
