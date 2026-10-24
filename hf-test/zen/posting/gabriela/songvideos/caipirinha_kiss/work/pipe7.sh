cd /workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss
while [ -z "$(grep ALLDONE work/finq6.log 2>/dev/null)" ]; do sleep 30; done
for c in v14_linenset v15_mididress v16_denim v20_blazer; do [ -f kl/${c}_pf.json ] && continue; bash work/waitok.sh; GFPS=12 /workspace/hf-test/zen/posting/gabriela/2026-10-22/work/pf_gate.py kl/$c.mp4 2>/dev/null && echo "- $(date +%R) clip gate $c: $(python3 -c "import json;d=json.load(open('kl/${c}_pf.json'));print(d['median'],d['min'])")" >> ../caipirinha_kiss_PROGRESS.md; done
echo P7DONE
