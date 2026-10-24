cd /workspace/hf-test/zen/posting/camille_oct22/quota
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
for k in TT1_baguette YT1_promenade TT3_bluehour X3_baguette_cut X1_rooftop_slow; do
 w; python3 work/export_light.py work/spec_$k.json
 w; /workspace/.face-venv/bin/python ../work/vgate.py final/camille_oct22q_${k}_silent.mp4 0.1 qc/gate_final_$k.json 2>/dev/null | head -1
done; echo DONE3
