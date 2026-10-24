import json,requests,subprocess,hashlib,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
A='https://api.ayrshare.com/api'
S=json.load(open('/workspace/jsw_sched/sienna_hold_1022.json'))['posts']
rep=[]
for v in S:
  r={"id":v['id'],"platforms":v['platforms'],"sd":v['scheduleDate'],"text":(v.get('post') or '')[:40],"media":[]}
  for u in v.get('mediaUrls') or []:
    b=requests.get(u,timeout=60).content; fn=u.split('/')[-1]; open(fn,'wb').write(b)
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,format_name','-of','csv=p=0',fn],capture_output=True,text=True).stdout.strip()
    r['media'].append({"url":u,"bytes":len(b),"md5":hashlib.md5(b).hexdigest(),"probe":p})
  rep.append(r); print(json.dumps(r,ensure_ascii=False),flush=True)
json.dump(rep,open('media_check.json','w'),indent=1)
L=requests.get(A+'/history?lastRecords=300',headers=H(True)).json(); L=L['history'] if isinstance(L,dict) else L
json.dump(L,open('hist_now.json','w'))
print('== pending now',[ (p['id'],p['platforms']) for p in L if p.get('status')=='pending'])
print('== today live/err')
for p in L:
  s=p.get('scheduleDate') or p.get('created') or ''
  if s>='2026-10-22T04:00' and p.get('status') in('success','error'):
    print(p['id'],p['status'],s[:16],p['platforms'],'media:',len(p.get('mediaUrls') or []),[ (x.get('platform'),x.get('postUrl')) for x in p.get('postIds') or []],(p.get('post') or '')[:35])
  if '2113330066578878826' in json.dumps(p): print('TWEET MATCH',p['id'],p.get('status'))
