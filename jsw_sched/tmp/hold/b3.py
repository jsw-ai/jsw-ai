import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
B='https://api.ayrshare.com/api'; P='/workspace/hf-test/zen/posting/'
def k(m): return open(f'/home/box/agent-data/secrets/JSW-{m}-ayrshare-profile-key.txt').read().strip()
J=[('valentina','valentina_oct22/n23/cuts/valentina_tiktok_20261023_mami11_v5.mp4','4c81b39b01d3e6156059dc4c633de686','tiktok','2026-10-23T16:30:00Z',"mami said home by 11… it's 10:58 and I'm still dancing 💃🏽 link in bio #latina #miami #mamadice #fyp"),
('valentina','valentina_oct22/n23/cuts/valentina_tiktok_20261023_dance_v4.mp4','2059c0ba4928900af5977da0a2566f5b','tiktok','2026-10-23T13:00:00Z','learn this one before you ask me out 💃🏽 link in bio #latina #miami #dance #fyp'),
('camille','camille_oct22/quota/platform/x4b_Q8a_balcony.jpg','611df3d729e4fb68fa45e1c027462212','twitter','2026-10-23T19:00:00Z','Sea view, one record on repeat. Riviera Après Minuit is out now on Apple Music 🎶 https://music.apple.com/us/album/riviera-apr%C3%A8s-minuit/6825779566')]
out=[]
for m,f,md,pl,t,c in J:
  h={**H(pl=='twitter'),'Profile-Key':k(m)}
  b=open(P+f,'rb').read(); assert hashlib.md5(b).hexdigest()==md
  mt='video/mp4' if f.endswith('mp4') else 'image/jpeg'
  u=requests.post(B+'/media/upload',headers=h,json={'file':f'data:{mt};base64,'+base64.b64encode(b).decode(),'fileName':f.split('/')[-1]},timeout=300).json()['url']; assert u
  body={'post':c,'platforms':[pl],'mediaUrls':[u],'scheduleDate':t}
  if pl=='tiktok': body.update(isVideo=True,tikTokOptions={'isAIGenerated':True})
  r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
  pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(3)
  g=requests.get(B+'/post/'+str(pid),headers=h).json()
  gm=[hashlib.md5(requests.get(x).content).hexdigest() for x in g.get('mediaUrls') or []]
  print(m,f.split('/')[-1],pid,g.get('status'),g.get('scheduleDate'),gm==[md],g.get('post')==c,r.get('errors') or '',flush=True)
  out.append({'file':f,'body':body,'resp':r,'get':g})
json.dump(out,open('/workspace/jsw_sched/pass_1013_1023.json','w'),indent=1,default=str,ensure_ascii=False)
