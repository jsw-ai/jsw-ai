# fetch_qa.sh name url start hook
set -e; cd /workspace/hf-test/zen/posting/camille_oct19/v2
curl -s -o raw/$1.mp4 "$2"; ./work/qa.sh $1 raw/$1.mp4 "$3" > work/qa_$1.txt 2>&1
bash work/export_pad.sh raw/$1.mp4 work/tt_$1.mp4 "$4"
/workspace/.face-venv/bin/python ../../identity_gate.py video --model camille_v3_draft --frames 10 --no-ocr --json work/gate_tt_$1.json work/tt_$1.mp4 2>/dev/null | rg "PASS|FAIL" >> work/qa_$1.txt
