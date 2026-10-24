cd /workspace/hf-test/zen/posting/camille_oct22
k=$1; python3 work/export.py work/spec_$k.json && /workspace/.face-venv/bin/python work/vgate.py final/camille_oct22_${k}_silent.mp4 0.1 qc/vg/final_$k.json 2>/dev/null | head -1 > qc/vg/final_$k.txt
