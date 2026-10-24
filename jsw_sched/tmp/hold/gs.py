import json,requests,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-gabriela-ayrshare-profile-key.txt').read().strip()}
L=requests.get('https://api.ayrshare.com/api/history?lastRecords=300',headers=h).json(); L=L['history'] if isinstance(L,dict) else L
for p in L:
  if p.get('scheduleDate','')>='2026-10-24T00' and p.get('status')!='deleted': print(p['id'],p['status'],p['platforms'],p['scheduleDate'])
