import requests,base64,json
S='/home/box/agent-data/secrets/'; D='/workspace/xposts/madison_golf_reel_1021/v5/variants/'
K=open(S+'JSW-ayrshare-api-key.txt').read().strip()
h={'Authorization':'Bearer '+K,'Profile-Key':open(S+'JSW-madison-ayrshare-profile-key.txt').read().strip()}
log={'uploads':[]}; urls=[]
for f in ['ig_1_S2.jpg','ig_2_P2.jpg']:
    b='data:image/jpeg;base64,'+base64.b64encode(open(D+f,'rb').read()).decode()
    r=requests.post('https://api.ayrshare.com/api/media/upload',headers=h,json={'file':b,'fileName':f},timeout=120)
    j=r.json(); log['uploads'].append({'file':D+f,'status':r.status_code,'response':j}); urls.append(j['url'])
body={'post':open(D+'ig_caption.txt').read().rstrip('\n'),'platforms':['instagram'],'mediaUrls':urls,'scheduleDate':'2026-10-22T00:30:00Z','instagramOptions':{'isAIGenerated':True}}
r=requests.post('https://api.ayrshare.com/api/post',headers=h,json=body,timeout=120)
log['request']=body; log['status']=r.status_code; log['response']=r.json()
json.dump(log,open('/workspace/xposts/madison_golf_ig_1021.json','w'),indent=2,ensure_ascii=False)
print(r.status_code, json.dumps(log['response'])[:600])
