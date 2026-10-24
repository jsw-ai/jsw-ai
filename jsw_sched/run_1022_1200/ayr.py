import json,requests
S='/home/box/agent-data/secrets/'
A='https://app.ayrshare.com/api'
KEY=open(S+'JSW-ayrshare-api-key.txt').read().strip()
def H(m):
    h={"Authorization":"Bearer "+KEY}
    if m!='sienna': h["Profile-Key"]=open(S+f'JSW-{m}-ayrshare-profile-key.txt').read().strip()
    return h
def get(m,path,**kw): return requests.get(A+path,headers=H(m),timeout=60,**kw)
def post(m,path,body): return requests.post(A+path,headers=H(m),json=body,timeout=120)
def delete(m,path,body): return requests.delete(A+path,headers=H(m),json=body,timeout=60)
def put(m,path,body): return requests.put(A+path,headers=H(m),json=body,timeout=120)
