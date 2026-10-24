cd /workspace/hf-test/zen/posting/camille_songs/01_bonsoir_monaco
g(){ while pgrep -f "identity_gate|vgate|fgate" >/dev/null || [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 15; done; }
g; cd /workspace/hf-test/zen/posting && /workspace/.face-venv/bin/python identity_gate.py --model camille_v3 --no-ocr --json camille_songs/01_bonsoir_monaco/qc/gate_M09h.json camille_songs/01_bonsoir_monaco/fin/M09_lights_h_v4C.jpg | tail -2; cd -
g; /workspace/.face-venv/bin/python work/vgate_multi.py raw/K_*.mp4
echo GATE_DONE
