import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h=H(True); B='https://api.ayrshare.com/api'
f='/workspace/jsw_tiktok/sienna/2026-10-22_daily/thirdpass/sienna_x_20261022_x_tease_sunrise_bikini_v4.jpg'
b=open(f,'rb').read(); assert hashlib.md5(b).hexdigest()=='02361f4c7a4ae1c772b85df4db701a08'
u=requests.post(B+'/media/upload',headers=h,json={'file':'data:image/jpeg;base64,'+base64.b64encode(b).decode(),'fileName':f.split('/')[-1]},timeout=200).json()['url']; assert u
C='first light, salt water, nobody else awake yet 🌅 the rest is in my bio'
body={'post':C,'platforms':['twitter'],'mediaUrls':[u],'scheduleDate':'2026-10-23T10:30:00Z','twitterOptions':{'possiblySensitive':True}}
r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(3)
g=requests.get(B+'/post/'+pid,headers=h).json()
json.dump({'body':body,'resp':r,'get':g},open('/workspace/jsw_sched/sienna_x_tease_v4_1023.json','w'),indent=1,default=str,ensure_ascii=False)
print(pid,g.get('status'),g.get('scheduleDate'),[hashlib.md5(requests.get(x).content).hexdigest() for x in g['mediaUrls']],g.get('post')==C,g.get('twitterOptions'),r.get('errors') or '')
