import json,requests,sys,base64,time;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-charlotte-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'; D='/workspace/hf-test/charlotte_1022/rb2/final/'
def up(f,mt):
  r=requests.post(B+'/media/upload',headers=h,json={'file':f'data:{mt};base64,'+base64.b64encode(open(D+f,'rb').read()).decode(),'fileName':f},timeout=300).json()
  return r['url']
v=up('charlotte_yt_20261022_matchday-vs-recovery_v10.mp4','video/mp4'); t=up('YT1_thumb_v10.jpg','image/jpeg')
T='matchday me. recovery me 🧖‍♀️ #shorts #arsenal #gunners'
body={'post':T,'platforms':['youtube'],'mediaUrls':[v],'isVideo':True,'scheduleDate':'2026-10-23T19:30:00Z',
 'youTubeOptions':{'title':T,'visibility':'public','shorts':True,'thumbNail':t,'containsSyntheticMedia':True}}
r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
pid=r.get('id') or (r.get('posts') or [{}])[0].get('id')
time.sleep(3); g=requests.get(B+'/post/'+pid,headers=h).json()
json.dump({'body':body,'resp':r,'get':g},open('/workspace/jsw_sched/charlotte_yt_v10_1023.json','w'),indent=1,default=str)
import hashlib;m=hashlib.md5(requests.get(g['mediaUrls'][0]).content).hexdigest()
print(pid,g.get('status'),g.get('scheduleDate'),m,json.dumps(g.get('youTubeOptions')))
