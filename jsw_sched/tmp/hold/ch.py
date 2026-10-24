import json,requests,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
from datetime import datetime,timedelta
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-charlotte-ayrshare-profile-key.txt').read().strip()}
L=requests.get('https://api.ayrshare.com/api/history?lastRecords=300',headers=h).json(); L=L['history'] if isinstance(L,dict) else L
for p in L:
  if 'youtube' in p.get('platforms',[]) and p.get('scheduleDate','')>='2026-10-23':
    print(p['id'],p['status'],p['scheduleDate'],(p.get('post') or '')[:40])
