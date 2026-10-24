cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss/work
for i in $(seq 1 200); do a=$(free -g|awk '/Mem/{print $7}'); g=$(pgrep -af "python.*(fgate|vgate2|identity_gate|pf_gate)"|grep -ci gabriela); [ "$a" -ge 3 ] && [ "$g" -eq 0 ] && break; echo "$(date +%T) avail=$a gates=$g"; sleep 60; done
OMP_NUM_THREADS=2 /workspace/.whisper-venv/bin/python asr.py && /workspace/.whisper-venv/bin/python align.py
