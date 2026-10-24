import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-madison-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'; D='/workspace/madison_songs_1022/out/'
def up(f,mt):
  b=open(D+f,'rb').read(); return hashlib.md5(b).hexdigest(),requests.post(B+'/media/upload',headers=h,json={'file':f'data:{mt};base64,'+base64.b64encode(b).decode(),'fileName':f},timeout=300).json()['url']
m,v=up('madison_iced_coffee_girl_ytshort_21s_9x16_v3.mp4','video/mp4'); assert m=='c90978fc2f6ca02eaacb365d3b578378' and v
_,t=up('madison_iced_coffee_girl_ytshort_21s_9x16_v3_thumb.jpg','image/jpeg')
C='Madison Cole – Iced Coffee Girl ☕🤠 from my album Iced Coffee & Heartbreak, out now. #icedcoffee #countrypop #shorts'
body={'post':C,'platforms':['youtube'],'mediaUrls':[v],'isVideo':True,'scheduleDate':'2026-10-23T19:00:00Z','youTubeOptions':{'title':'Madison Cole – Iced Coffee Girl ☕🤠','visibility':'public','shorts':True,'thumbNail':t,'containsSyntheticMedia':True}}
r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(3)
g=requests.get(B+'/post/'+pid,headers=h).json()
json.dump({'body':body,'resp':r,'get':g},open('/workspace/jsw_sched/madison_yt_icedcoffee_v3_1023.json','w'),indent=1,default=str,ensure_ascii=False)
print(pid,g.get('status'),g.get('scheduleDate'),[hashlib.md5(requests.get(x).content).hexdigest() for x in g['mediaUrls']],g.get('youTubeOptions'),r.get('errors') or '')
