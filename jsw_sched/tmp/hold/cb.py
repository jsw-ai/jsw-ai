import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-camille-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'; D='/workspace/hf-test/zen/posting/camille_oct22/quota/platform/'
S=[('ig_story1_Q1_lane.jpg','70ffdada9eede6abf31233a31c1c4b6e','instagram','13:30',None),
('reddit1_Q2r_market.jpg','60f30e0ced28391ea9e188b507169fd0','reddit','15:00','Saturday mornings at the market in Nice ☀️'),
('ig_story2_Q4_bakery.jpg','799c7f4562e8732767cfdce3246686bf','instagram','17:00',None),
('reddit2_Q3_promenade.jpg','c08526b82765e76ba151fc9856d14da4','reddit','21:00','Sea breeze and no plans on the Promenade 🌊'),
('ig_story3_Q5_rooftop.jpg','6831d2f6059a9308898137e549c70ebd','instagram','00:30',None)]
out=[]
for f,m,pl,t,title in S:
  b=open(D+f,'rb').read(); assert hashlib.md5(b).hexdigest()==m
  u=requests.post(B+'/media/upload',headers=h,json={'file':'data:image/jpeg;base64,'+base64.b64encode(b).decode(),'fileName':f},timeout=200).json()['url']
  assert u
  day='2026-10-24' if t=='00:30' else '2026-10-23'
  body={'post':title or ' ','platforms':[pl],'mediaUrls':[u],'scheduleDate':f'{day}T{t}:00Z'}
  if pl=='instagram': body['instagramOptions']={'stories':True,'isAIGenerated':True}; body['post']=''
  else: body['redditOptions']={'title':title,'subreddit':'u_Pristine_Culture_693'}
  r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
  pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(2)
  g=requests.get(B+'/post/'+str(pid),headers=h).json()
  gm=[hashlib.md5(requests.get(x).content).hexdigest() for x in g.get('mediaUrls') or []]
  print(f,pid,g.get('status'),g.get('scheduleDate'),gm==[m],r.get('errors') or '',flush=True)
  out.append({'file':f,'body':body,'resp':r,'get':g})
json.dump(out,open('/workspace/jsw_sched/camille_stills_1023.json','w'),indent=1,default=str,ensure_ascii=False)
