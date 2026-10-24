import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-charlotte-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'; D='/workspace/hf-test/charlotte_1022/quota2/final/'
def up(f,mt):
  b=open(D+f,'rb').read(); return hashlib.md5(b).hexdigest(),requests.post(B+'/media/upload',headers=h,json={'file':f'data:{mt};base64,'+base64.b64encode(b).decode(),'fileName':f},timeout=300).json()['url']
m,v=up('charlotte_youtube_20261022_tegernsee-jetty-reset_v5_music.mp4','video/mp4'); assert m=='1907d9eeae3b5b6efb17e5241fe59382' and v
_,t=up('charlotte_youtube_20261022_tegernsee-jetty-reset_v4_thumb.jpg','image/jpeg')
C='Tried a football-free day at Lake Tegernsee after the 2-2. Lasted 4 minutes. 🎵 Proper Gorgeous out now on Apple Music https://music.apple.com/us/album/proper-gorgeous/6825712667 #Shorts #Arsenal #Munich #Tegernsee'
body={'post':C,'platforms':['youtube'],'mediaUrls':[v],'isVideo':True,'scheduleDate':'2026-10-23T03:00:00Z','youTubeOptions':{'title':'Tried a football-free day at Lake Tegernsee after the 2-2.','visibility':'public','shorts':True,'thumbNail':t,'containsSyntheticMedia':True}}
r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(3)
g=requests.get(B+'/post/'+pid,headers=h).json()
json.dump({'body':body,'resp':r,'get':g},open('/workspace/jsw_sched/charlotte_yt_jetty_v5_1022.json','w'),indent=1,default=str,ensure_ascii=False)
print(pid,g.get('status'),g.get('scheduleDate'),[hashlib.md5(requests.get(x).content).hexdigest() for x in g['mediaUrls']],g.get('youTubeOptions'),r.get('errors') or '')
