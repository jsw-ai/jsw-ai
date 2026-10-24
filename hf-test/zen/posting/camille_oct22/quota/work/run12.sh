cd /workspace/hf-test/zen/posting/camille_oct22/quota
while pgrep -f work/run11.sh >/dev/null; do sleep 15; done
for n in T2a1 T2a2 T2b2 T31 T32; do python3 work/skin_local.py raw/$n.png raw/${n}_tex.png; done
cd ..; python3 quota/work/finish_v4C.py T2a1 T2a2 T2b2 T31 T32; cd /workspace/hf-test/zen/posting
while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done
/workspace/.face-venv/bin/python identity_gate.py img camille_oct22/quota/fin/T2a1_v4C.jpg camille_oct22/quota/fin/T2a2_v4C.jpg camille_oct22/quota/fin/T2b2_v4C.jpg camille_oct22/quota/fin/T31_v4C.jpg camille_oct22/quota/fin/T32_v4C.jpg --model camille_v3 --no-ocr --json camille_oct22/quota/qc/gate_T.json
echo "- $(date +%-I:%M\ %p) T stills finished+gated -> qc/gate_T.json" >> camille_oct22/PROGRESS_QUOTA_1022.md; echo DONE12
