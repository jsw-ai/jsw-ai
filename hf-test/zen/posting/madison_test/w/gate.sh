cd /workspace/hf-test && /workspace/.face-venv/bin/python zen/posting/identity_gate.py img --model madison --source seedream --body --log zen/posting/reject_log.jsonl --json $1 "${@:2}" >/dev/null 2>&1
python3 - $1 <<'P'
import json,sys
d=json.load(open(sys.argv[1]))
items=d.items() if isinstance(d,dict) else [(x.get('file'),x) for x in d]
for k,v in items:
    b=v.get('body') or {}
    print(v.get('pass', v.get('ok')), k.split('/')[-1], v.get('score_centroid'), v.get('score_best'), [r for r in v.get('reasons',[]) if 'seedream' not in r], 'bust',b.get('bust_w'),'thigh',b.get('thigh_w'))
P
