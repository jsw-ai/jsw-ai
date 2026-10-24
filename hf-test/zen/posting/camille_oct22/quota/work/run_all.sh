cd /workspace/hf-test/zen/posting/camille_oct22/quota
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
w; /workspace/.face-venv/bin/python ../work/vgate.py raw/K3r.mp4 0.1 qc/vg_raw_K3r.json 2>/dev/null | head -1
w; python3 work/export.py work/spec_YT1_promenade.json
for k in TT1_baguette TT2_album_lane TT3_bluehour YT1_promenade X1_rooftop_slow X2_lane_reverse X3_baguette_cut; do
 w; /workspace/.face-venv/bin/python ../work/vgate.py final/camille_oct22q_${k}_silent.mp4 0.1 qc/gate_final_$k.json 2>/dev/null | head -1
done
echo ALLDONE
