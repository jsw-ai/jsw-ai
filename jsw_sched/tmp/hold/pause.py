import json,requests,sys,time;sys.path.insert(0,'/workspace')
from ayr_sienna import H
B='https://api.ayrshare.com/api'; CUT='2026-10-23T04:00:00Z'
M=['sienna','camille','charlotte','madison','gabriela','valentina']
def hd(m,x):
  h=dict(H(x))
  if m!='sienna': h['Profile-Key']=open(f'/home/box/agent-data/secrets/JSW-{m}-ayrshare-profile-key.txt').read().strip()
  return h
def pend(m):
  L=requests.get(B+'/history?lastRecords=300',headers=hd(m,False)).json(); L=L['history'] if isinstance(L,dict) else L
  return [p for p in L if p.get('status')=='pending' and p.get('scheduleDate','')>=CUT]
save={}
for m in M:
  save[m]=[]
  for p in pend(m):
    g=requests.get(B+'/post/'+p['id'],headers=hd(m,False)).json()
    save[m].append({'history':p,'full':g})
json.dump(save,open('/workspace/jsw_sched/pause_1022_pulled.json','w'),indent=1,default=str,ensure_ascii=False)
print({m:len(v) for m,v in save.items()},flush=True)
res={}
for m in M:
  for e in save[m]:
    p=e['history']; x='twitter' in p['platforms']
    r=requests.delete(B+'/post',headers=hd(m,x),json={'id':p['id']}).json()
    res[p['id']]={'model':m,'platforms':p['platforms'],'scheduleDate':p['scheduleDate'],'post':(p.get('post') or '')[:50],'del':r}
    if r.get('status')!='success': print('FAIL',m,p['id'],r,flush=True)
json.dump(res,open('/workspace/jsw_sched/pause_1022_delete_results.json','w'),indent=1,default=str,ensure_ascii=False)
time.sleep(5)
print('remaining',{m:[p['id'] for p in pend(m)] for m in M})
