import json,requests,hashlib,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
A='https://api.ayrshare.com/api'
L=requests.get(A+'/history?lastRecords=300',headers=H(True)).json(); L=L['history'] if isinstance(L,dict) else L
for p in sorted([p for p in L if p.get('status')=='pending'],key=lambda p:p['scheduleDate']): print('PENDING',p['id'],p['platforms'],p['scheduleDate'],len(p.get('mediaUrls') or []),(p.get('post') or '')[:30],flush=True)
for p in L:
  if (p.get('scheduleDate') or p.get('created',''))>='2026-10-20':
    for u in p.get('mediaUrls') or []:
      if u.endswith('.mp4'):
        m=hashlib.md5(requests.get(u,timeout=90).content).hexdigest()
        print('MD5',p['id'],p['status'],p['platforms'],m,'WHIPPAN' if m.startswith('b01847e1') else '',flush=True)
