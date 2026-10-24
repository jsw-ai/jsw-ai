import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-madison-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'; f='/workspace/madison_oct22/cuts2120/madison_1022_pickleball_igreel_8s_v2.mp4'
b=open(f,'rb').read(); assert hashlib.md5(b).hexdigest()=='3af86c6b7218412633aebc51f071838f'
v=requests.post(B+'/media/upload',headers=h,json={'file':'data:video/mp4;base64,'+base64.b64encode(b).decode(),'fileName':f.split('/')[-1]},timeout=300).json()['url']; assert v
body={'post':'here for the paddle twirl, not the score. what sport should i embarrass myself in next? 🏓 #pickleball #resortlife link in bio','platforms':['instagram'],'mediaUrls':[v],'isVideo':True,'scheduleDate':'2026-10-23T10:30:00Z','instagramOptions':{'reels':True,'shareReelsFeed':True,'isAIGenerated':True}}
r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(3)
g=requests.get(B+'/post/'+pid,headers=h).json()
json.dump({'body':body,'resp':r,'get':g},open('/workspace/jsw_sched/madison_igreel_pickleball_v2_1023.json','w'),indent=1,default=str,ensure_ascii=False)
print(pid,g.get('status'),g.get('scheduleDate'),[hashlib.md5(requests.get(x).content).hexdigest() for x in g['mediaUrls']],g.get('instagramOptions'))
