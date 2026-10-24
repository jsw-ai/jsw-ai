import json,requests,sys,base64,time,hashlib;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(False),'Profile-Key':open('/home/box/agent-data/secrets/JSW-gabriela-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'; f='/workspace/hf-test/zen/posting/gabriela/2026-10-22/collab/gabriela_collab_oktoberfest_clink_v9_silent.mp4'
v=requests.post(B+'/media/upload',headers=h,json={'file':'data:video/mp4;base64,'+base64.b64encode(open(f,'rb').read()).decode(),'fileName':f.split('/')[-1]},timeout=300).json()['url']
body={'post':'São Paulo: saúde! 🍻 with @charlottehayes240','platforms':['tiktok'],'mediaUrls':[v],'isVideo':True,'scheduleDate':'2026-10-24T16:30:00Z','tikTokOptions':{'isAIGenerated':True}}
r=requests.post(B+'/post',headers=h,json=body,timeout=120).json()
pid=r.get('id') or (r.get('posts') or [{}])[0].get('id'); time.sleep(3)
g=requests.get(B+'/post/'+pid,headers=h).json()
json.dump({'body':body,'resp':r,'get':g},open('/workspace/jsw_sched/gabriela_tt_clink_v9_1024.json','w'),indent=1,default=str)
b=requests.get(g['mediaUrls'][0]).content; open('t.mp4','wb').write(b)
print(pid,g.get('status'),g.get('scheduleDate'),hashlib.md5(b).hexdigest(),g.get('post'),g.get('tikTokOptions'))
