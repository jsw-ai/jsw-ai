cd /workspace/hf-test/zen/posting/camille_oct22/quota
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
for v in test/pad.mp4 test/crop.mp4 raw/P4.mp4; do w; /workspace/.face-venv/bin/python ../work/vgate.py $v 0.5 test/$(basename $v .mp4).json 2>/dev/null|head -1; done; echo TDONE
