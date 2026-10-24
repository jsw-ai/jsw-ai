cd /workspace/hf-test/zen/posting/camille_oct22/quota
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
for k in L4 L1 L5 L2 L3 L6; do w; r=$(/workspace/.face-venv/bin/python ../work/vgate.py raw/$k.mp4 0.2 qc/vg_raw_$k.json 2>/dev/null | head -1); echo "$r"; echo "- $(date +%-I:%M\ %p) raw gate $r" >> ../PROGRESS_QUOTA_1022.md; done; echo DONE8
