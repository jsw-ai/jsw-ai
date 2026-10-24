cd /workspace/hf-test/zen/posting
while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done
/workspace/.face-venv/bin/python identity_gate.py img camille_oct22/quota/platform/*.jpg --model camille_v3 --no-ocr --json camille_oct22/quota/qc/gate_platform.json > camille_oct22/quota/qc/run7.log 2>&1
echo "- $(date +%-I:%M\ %p) platform stills gated -> qc/gate_platform.json" >> camille_oct22/PROGRESS_QUOTA_1022.md; echo DONE7 >> camille_oct22/quota/qc/run7.log
