cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss
while pgrep -f runasr.sh >/dev/null; do sleep 30; done
for i in $(seq 1 200); do a=$(free -g|awk '/Mem/{print $7}'); g=$(pgrep -af "python.*(fgate|vgate2|identity_gate|pf_gate)"|grep -ci gabriela); [ "$a" -ge 3 ] && [ "$g" -eq 0 ] && break; echo "$(date +%T) avail=$a gates=$g"; sleep 60; done
/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model gabriela --source seedream --body --json qc/stills_gate.json fin/*_v4C.jpg
echo SGDONE
