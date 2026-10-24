import json,base64,sys,requests
sys.path.append('/workspace')
from ayr import *
import ayr_sienna as AS
D=json.load(open('details.json'))
def HX(m):
    h=H(m); h.update({k:v for k,v in AS.H(True).items() if k.startswith('X-Twitter')}); return h
log={}
# 1) Madison X VmVX -> 22:30Z with OAuth1 ; qY19 -> same time with OAuth1
for pid,new in [('VmVXX7FRgEMAi13l6tew','2026-10-22T22:30:00Z'),('qY19ktL2DJnFVOIDDA2l','2026-10-23T13:00:00Z')]:
    p=D['madison:'+pid]
    body={"post":p['post'],"platforms":["twitter"],"scheduleDate":new}
    if p.get('mediaUrls'): body["mediaUrls"]=p['mediaUrls']
    r=delete('madison','/post',{"id":pid}); log[pid+'_delete']=[r.status_code,r.json().get('status')]
    r=requests.post(A+'/post',headers=HX('madison'),json=body,timeout=120); log[pid+'_new']=[r.status_code,r.json(),body]
# 2) Madison YT Lz16 with thumbnail
b64=base64.b64encode(open('madison_fit_rating_v2_thumb.jpg','rb').read()).decode()
r=post('madison','/media/upload',{"file":"data:image/jpeg;base64,"+b64,"fileName":"madison_fit_rating_v2_thumb.jpg"}); up=r.json(); log['thumb_upload']=[r.status_code,up]
turl=up.get('url') or up.get('accessUrl')
p=D['madison:Lz161mIOJUow7UbcKvhE']
yo=dict(p['youTubeOptions']); yo['thumbNail']=turl; yo['containsSyntheticMedia']=True; yo['madeForKids']=False
body={"post":p['post'],"platforms":["youtube"],"mediaUrls":p['mediaUrls'],"isVideo":True,"scheduleDate":p['scheduleDate'],"youTubeOptions":yo}
if turl:
    r=delete('madison','/post',{"id":"Lz161mIOJUow7UbcKvhE"}); log['Lz16_delete']=[r.status_code,r.json().get('status')]
    r=post('madison','/post',body); log['Lz16_new']=[r.status_code,r.json(),body]
json.dump(log,open('fix_1522.json','w'),indent=1,ensure_ascii=False)
for k,v in log.items(): print(k, json.dumps(v,ensure_ascii=False)[:600])
