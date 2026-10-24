import json,sys,requests,time

import importlib.util as _u; _s=_u.spec_from_file_location("AS","/workspace/ayr_sienna.py"); AS=_u.module_from_spec(_s); _s.loader.exec_module(AS)
from jswayr import *
log=[]
def L(x): log.append(x); print(json.dumps(x,ensure_ascii=False)[:400])
det=json.load(open('details.json'))
# 1 move Sienna TikTok jWfKag97 out of quiet hours (3 AM AEST) to 23:00Z (9 AM AEST Fri)
r=requests.patch(A+'/post',headers=H('sienna'),json={"id":"jWfKag97exWuKHsyRQ5N","scheduleDate":"2026-10-22T23:00:00Z"},timeout=60)
L({"a":"patch jWfKag97 ->23:00Z","code":r.status_code,"r":r.json()})
# 2 move Sienna X DEJYQh6N 01:00Z -> 02:00Z (2h spacing after 00:00Z post)
r=requests.patch(A+'/post',headers=AS.H(True),json={"id":"DEJYQh6NWCR7bHD2rDaz","scheduleDate":"2026-10-23T02:00:00Z"},timeout=60)
L({"a":"patch DEJYQh6N ->02:00Z","code":r.status_code,"r":r.json()})
# 3 Camille YT Short M5xpQ2oI 02:00Z (4 AM Nice) -> 21:00Z (11 PM Nice late-night slot)
r=requests.patch(A+'/post',headers=H('camille'),json={"id":"M5xpQ2oIvKC5bQbytFOU","scheduleDate":"2026-10-22T21:00:00Z"},timeout=60)
L({"a":"patch M5xpQ2oI ->21:00Z","code":r.status_code,"r":r.json()})
# 4 pull Sienna IG jt9omvi (caption 'full song: search' failed REV-155 logic)
old=det['sienna:jt9omvicoFT03cVXCY8P']; json.dump(old,open('pulled_sienna_ig_jt9omvi.json','w'),ensure_ascii=False,indent=1)
r=requests.delete(A+'/post',headers=H('sienna'),json={"id":"jt9omvicoFT03cVXCY8P"},timeout=60)
L({"a":"delete jt9omvi","code":r.status_code,"r":r.json()})
# 5 recreate Sienna X posts created 10/21 11:06 AM ET without OAuth1 headers
new={}
for i in ["cTvF9tyDTc7uXbDLyscS","2MdJxzQvX2yHkQkY6Qwc","tsT7yJjyHm011Qxw0ok7","i0KOrG4oHeuR2GftWQyt","rZBaKTzo2JNe1NCxZEw0"]:
    o=det['sienna:'+i]
    body={"post":o['post'],"platforms":["twitter"],"scheduleDate":o['scheduleDate'],"shortenLinks":False}
    if o.get('mediaUrls'): body["mediaUrls"]=o['mediaUrls']
    d=requests.delete(A+'/post',headers=AS.H(True),json={"id":i},timeout=60)
    L({"a":"delete "+i,"code":d.status_code,"r":d.json()})
    if d.status_code!=200: continue
    time.sleep(2)
    c=requests.post(A+'/post',headers=AS.H(True),json=body,timeout=120)
    L({"a":"recreate "+i,"code":c.status_code,"body":body,"r":c.json()})
    try: new[i]=c.json()['posts'][0]['id']
    except Exception: new[i]=None
json.dump({"log":log,"new":new},open('act_log.json','w'),ensure_ascii=False,indent=1)
print(new)
