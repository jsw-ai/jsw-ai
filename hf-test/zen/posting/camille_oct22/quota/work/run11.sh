cd /workspace/hf-test/zen/posting/camille_oct22/quota
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
for k in $@; do
 w; python3 work/export_crop.py work/spec_$k.json
 w; r=$(/workspace/.face-venv/bin/python ../work/vgate.py final/camille_oct22q_${k}_silent.mp4 0.1 qc/gate_final_$k.json 2>/dev/null | head -1); echo "$r"
 echo "- $(date +%-I:%M\ %p) FINAL $k gate: $r" >> ../PROGRESS_QUOTA_1022.md
done; echo DONE10 $@
