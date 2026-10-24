cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss
while pgrep -f "finish_v4C.py v09" >/dev/null; do sleep 20; done
bash work/waitok.sh; /workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model gabriela --source seedream --body --json qc/stills_gate3.json fin/v09_*_v4C.jpg fin/v1[0-3]_*_v4C.jpg > work/sg3.log 2>&1
bash work/waitok.sh; cd work; OMP_NUM_THREADS=2 /workspace/.whisper-venv/bin/python asr.py > asr.log 2>&1; echo P1DONE
