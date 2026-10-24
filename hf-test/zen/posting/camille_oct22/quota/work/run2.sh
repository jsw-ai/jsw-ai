cd /workspace/hf-test/zen/posting/camille_oct22/quota
while pgrep -f work/run_all.sh >/dev/null; do sleep 15; done
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
for k in P4 P3 P5; do w; /workspace/.face-venv/bin/python ../work/vgate.py raw/$k.mp4 0.1 qc/vg_raw_$k.json 2>/dev/null | head -1; done
echo DONE2
