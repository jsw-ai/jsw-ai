import json
from ayr import *
out={}
for m in ['sienna','camille','charlotte','gabriela','madison','valentina']:
    d=json.load(open(f'sched_{m}.json'))
    posts=d['history'] if isinstance(d,dict) else d
    for p in posts:
        if p.get('status')=='pending':
            out[f'{m}:{p["id"]}']=get(m,f'/post/{p["id"]}').json()
json.dump(out,open('details.json','w'),indent=1,ensure_ascii=False)
