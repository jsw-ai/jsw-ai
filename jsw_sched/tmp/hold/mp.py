import json,requests,sys,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
from datetime import datetime,timedelta
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-madison-ayrshare-profile-key.txt').read().strip()}
L=requests.get('https://api.ayrshare.com/api/history?lastRecords=300',headers=h).json(); L=L['history'] if isinstance(L,dict) else L
for p in sorted(L,key=lambda p:p.get('scheduleDate','')):
  if p.get('status')=='pending' or p.get('scheduleDate','')>='2026-10-23T04':
    et=(datetime.fromisoformat(p['scheduleDate'].replace('Z','+00:00'))-timedelta(hours=4)).strftime('%a %m/%d %H:%M')
    ms=[hashlib.md5(requests.get(u).content).hexdigest() for u in (p.get('mediaUrls') or [])]
    print(json.dumps(p.get('instagramOptions')),p['id'],p['status'],p['platforms'],et,'|',(p.get('post') or '')[:40].replace('\n',' '),'|',ms)
