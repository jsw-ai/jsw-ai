cd /workspace/hf-test/zen/posting/camille_oct22/quota
while pgrep -f work/run8.sh >/dev/null; do sleep 15; done
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
w; r=$(/workspace/.face-venv/bin/python ../work/vgate.py raw/L2r.mp4 0.2 qc/vg_raw_L2r.json 2>/dev/null | head -1); echo "$r"; echo "- $(date +%-I:%M\ %p) raw gate $r" >> ../PROGRESS_QUOTA_1022.md; echo DONE9
