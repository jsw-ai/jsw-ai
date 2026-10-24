cd /workspace/hf-test/zen/posting/camille_oct22/quota
while pgrep -f work/run5.sh >/dev/null; do sleep 15; done
w(){ while [ $(free -g | awk '/Mem:/{print $7}') -lt 3 ]; do sleep 10; done; }
for f in platform/*.jpg platform/*.png; do [ -f "$f" ] || continue; w
 r=$(cd /workspace/hf-test/zen/posting && /workspace/.face-venv/bin/python identity_gate.py camille_oct22/quota/$f --model camille_v3 --no-ocr --json 2>/dev/null | tr -d '\n' | head -c 400)
 echo "$f $r"; echo "- $(date +%-I:%M\ %p) still gate $f: $(echo $r | grep -o '"[a-z_]*score[a-z_]*": *[0-9.]*' | head -2 | tr '\n' ' ')" >> ../PROGRESS_QUOTA_1022.md
done; echo DONE6
