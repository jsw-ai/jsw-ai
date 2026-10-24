import json,requests,sys,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
A='https://api.ayrshare.com/api'
S=json.load(open('/workspace/jsw_sched/sienna_hold_1022.json'))['posts']
KEEP=['post','platforms','mediaUrls','isVideo','scheduleDate','instagramOptions','tikTokOptions','youTubeOptions','twitterOptions','redditOptions','shortenLinks']
res=[]
for v in S:
  body={k:v[k] for k in KEEP if v.get(k) is not None}
  if v['id']=='5F9QcKUXY0RKL3klxSKn': body['scheduleDate']='2026-10-23T01:25:00Z'
  if not body.get('mediaUrls') and v['id']!='DEJYQh6NWCR7bHD2rDaz': res.append({"old":v['id'],"skipped":"empty media"}); continue
  x='twitter' in body['platforms']
  r=requests.post(A+'/post',headers={**H(x),'Content-Type':'application/json'},data=json.dumps(body,ensure_ascii=False).encode()).json()
  nid=r.get('id') or (r.get('posts') or [{}])[0].get('id')
  vv=requests.get(f'{A}/post/{nid}',headers=H(x)).json() if nid else {}
  res.append({"old":v['id'],"new":nid,"platforms":body['platforms'],"scheduleDate":body['scheduleDate'],"status":vv.get('status'),"media_ok":vv.get('mediaUrls')==body.get('mediaUrls'),"request":body,"response":r})
  print(v['id'],'->',nid,body['platforms'],body['scheduleDate'],vv.get('status'),'media',len(vv.get('mediaUrls') or []),'' if nid else str(r)[:300],flush=True)
json.dump(res,open('/workspace/jsw_sched/sienna_hold_1022_recreate.json','w'),ensure_ascii=False,indent=2)
