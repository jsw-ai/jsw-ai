import json,requests,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
from datetime import datetime,timedelta
L=requests.get('https://api.ayrshare.com/api/history?lastRecords=300',headers=H(False)).json(); L=L['history'] if isinstance(L,dict) else L
for p in sorted(L,key=lambda p:p.get('scheduleDate','')):
  if p.get('status') in('pending','success') and p.get('scheduleDate','')>='2026-10-22T04':
    et=(datetime.fromisoformat(p['scheduleDate'].replace('Z','+00:00'))-timedelta(hours=4)).strftime('%a %m/%d %H:%M')
    print(p['id'],p['status'],p['platforms'],et,(p.get('post') or '')[:30].replace('\n',' '))
