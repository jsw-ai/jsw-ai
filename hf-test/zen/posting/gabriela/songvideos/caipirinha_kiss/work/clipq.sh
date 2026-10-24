cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss
while pgrep -f pipe1.sh >/dev/null; do sleep 20; done
for k in $(seq 1 300); do
 f=$(for x in kl/*.mp4; do [ -f "${x%.mp4}_pf.json" ] || echo $x; done | head -1)
 [ -z "$f" ] && { [ -f work/clips_all_in ] && break; sleep 60; continue; }
 bash work/waitok.sh; echo "$(date +%T) gate $f"; GFPS=12 /workspace/hf-test/zen/posting/gabriela/2026-10-22/work/pf_gate.py "$f" 2>/dev/null
done; echo CQDONE
