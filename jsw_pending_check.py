import requests,json
S='/home/box/agent-data/secrets/'
K=open(S+'JSW-ayrshare-api-key.txt').read().strip()
out={}
for m in ['sienna','charlotte','madison','valentina','gabriela','camille']:
    h={'Authorization':'Bearer '+K}
    if m!='sienna': h['Profile-Key']=open(S+f'JSW-{m}-ayrshare-profile-key.txt').read().strip()
    r=requests.get('https://api.ayrshare.com/api/history',headers=h,params={'status':'pending','lastDays':0},timeout=60)
    try: d=r.json()
    except: d=r.text
    items=d if isinstance(d,list) else d.get('history',d) if isinstance(d,dict) else d
    print('==',m,r.status_code)
    if isinstance(items,list):
        for p in items:
            if p.get('status') in ('pending','scheduled') or 'scheduleDate' in p:
                print(' ',p.get('id'),p.get('status'),p.get('scheduleDate'),p.get('platforms'),len(p.get('mediaUrls') or []),repr((p.get('post') or '')[:90]))
    else: print(str(items)[:300])
