cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss
P=../caipirinha_kiss_PROGRESS.md
while pgrep -f "bash work/finq5.sh" | grep -v $$ >/dev/null; do sleep 30; done
bash work/waitok.sh; python3 work/finish_v4C.py v14_linenset v15_mididress v16_denim v17_crewtee v18_turtleneck v19_kaftan v20_blazer v21_shirtdress && echo "- $(date +%R) v14-v21 finish_v4C done" >> $P
bash work/waitok.sh; /workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model gabriela --source seedream --body --json qc/stills_gate5.json fin/v1[4-9]*_v4C.jpg fin/v2*_v4C.jpg && echo "- $(date +%R) v14-v21 still gate -> qc/stills_gate5.json" >> $P
echo P6DONE
