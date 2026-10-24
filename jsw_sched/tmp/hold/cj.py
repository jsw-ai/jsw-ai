import json,requests,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
from datetime import datetime,timedelta
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-charlotte-ayrshare-profile-key.txt').read().strip()}
L=requests.get('https://api.ayrshare.com/api/history?lastRecords=300',headers=h).json(); L=L['history'] if isinstance(L,dict) else L
for p in sorted(L,key=lambda p:p.get('scheduleDate','')):
  s=json.dumps(p)
  if p.get('status')=='pending' or 'jetty' in s.lower() and 'youtube' in p.get('platforms',[]):
    et=(datetime.fromisoformat(p['scheduleDate'].replace('Z','+00:00'))-timedelta(hours=4)).strftime('%a %m/%d %H:%M')
    print(p['id'],p['status'],p['platforms'],et,(p.get('post') or '')[:40].replace('\n',' '),[x.get('postUrl') for x in p.get('postIds') or []])
