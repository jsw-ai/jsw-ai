import json
from ayr import *
out={}
for m in ['sienna','camille','charlotte','gabriela','madison','valentina']:
    d=json.load(open(f'sched_{m}.json'))
    posts=d['history'] if isinstance(d,dict) else d
    ids=[p['id'] for p in posts if p.get('status') in ('pending','error') and (p.get('scheduleDate') or '')>='2026-10-22T13']
    for i in ids+(['DN5DSGpTbjyi6lArcoE7'] if m=='madison' else []):
        r=get(m,f'/post/{i}')
        out[f'{m}:{i}']=r.json()
    u=get(m,'/user')
    j=u.json()
    out[f'{m}:user']={k:j.get(k) for k in ['activeSocialAccounts','displayNames','title']}
json.dump(out,open('details.json','w'),indent=1,ensure_ascii=False)
