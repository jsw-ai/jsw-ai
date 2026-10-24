cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss
P=../caipirinha_kiss_PROGRESS.md
for c in hook x ig yt; do
 n=$(python3 -c "import json;print(json.load(open('work/cuts.json'))['$c']['name'])")
 if [ ! -f final/$n.mp4 ]; then bash work/waitok.sh; python3 work/build.py $c && echo "- $(date +%R) built final/$n.mp4" >> $P; fi
 if [ ! -f final/${n}_pf.json ]; then bash work/waitok.sh; GFPS=12 /workspace/hf-test/zen/posting/gabriela/2026-10-22/work/pf_gate.py final/$n.mp4 && echo "- $(date +%R) gated $n: $(python3 -c "import json;d=json.load(open('final/${n}_pf.json'));print(d['median'],d['min'],d['pass_'])")" >> $P; fi
done
echo ALLDONE
