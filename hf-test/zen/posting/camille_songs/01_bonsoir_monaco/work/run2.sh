cd /workspace/hf-test/zen/posting/camille_songs/01_bonsoir_monaco
g(){ while pgrep -f "identity_gate|vgate|fgate" >/dev/null || [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 15; done; }
m(){ while [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 15; done; }
g; (cd /workspace/hf-test/zen/posting && /workspace/.face-venv/bin/python identity_gate.py --model camille_v3 --no-ocr --json camille_songs/01_bonsoir_monaco/qc/gate_M09h.json img camille_songs/01_bonsoir_monaco/fin/M09_lights_h_v4C.jpg 2>&1 | tail -2)
for c in hook x yt; do m; python3 work/build.py $c || echo FAIL $c; done
g; /workspace/.face-venv/bin/python work/vgate_multi.py out/camille_bonsoir_monaco_hook_21s_silent.mp4 out/camille_bonsoir_monaco_x_24s_silent.mp4 out/camille_bonsoir_monaco_youtube_21s_silent.mp4
echo ALL_DONE
