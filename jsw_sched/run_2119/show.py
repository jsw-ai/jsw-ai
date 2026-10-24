import json,sys
for m in sys.argv[1:]:
    for k in ['sched','hist']:
        d=json.load(open(f'{k}_{m}.json'))
        if isinstance(d,dict) and 'history' not in d: print(m,k,str(d)[:300]); continue
        posts=d['history'] if isinstance(d,dict) else d
        print(f'== {m} {k}: {len(posts)}')
        for p in posts:
            t=p.get('post') or ''
            if isinstance(t,dict): t=json.dumps(t)
            print(' ',p.get('id'),p.get('status'),p.get('scheduleDate') or p.get('created'),p.get('platforms'),t[:60].replace('\n',' '),
              [ (x.get('platform'),x.get('status'),x.get('postUrl')) for x in p.get('postIds',[]) ] if p.get('postIds') else '', p.get('errors') and str(p.get('errors'))[:200])
