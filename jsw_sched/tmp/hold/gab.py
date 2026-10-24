import json,requests,subprocess,hashlib,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
from datetime import datetime,timedelta,timezone
h={**H(True),'Profile-Key':open('/home/box/agent-data/secrets/JSW-gabriela-ayrshare-profile-key.txt').read().strip()}
L=requests.get('https://api.ayrshare.com/api/history?lastRecords=300',headers=h).json(); L=L['history'] if isinstance(L,dict) else L
for p in sorted([p for p in L if p.get('status')=='pending'],key=lambda p:p['scheduleDate']):
  et=(datetime.fromisoformat(p['scheduleDate'].replace('Z','+00:00'))-timedelta(hours=4)).strftime('%a %m/%d %I:%M %p ET')
  for u in p.get('mediaUrls') or [None]:
    info='no media'
    if u:
      b=requests.get(u,timeout=90).content; m=hashlib.md5(b).hexdigest()
      open('g.tmp','wb').write(b)
      d=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,format_name','-of','csv=p=0','g.tmp'],capture_output=True,text=True).stdout.strip()
      info=f"{u.split('/')[-1]} md5 {m[:8]} {d}"
    print(p['id'],p['platforms'],et,'|',(p.get('post') or '')[:45].replace('\n',' '),'|',info,'|',json.dumps(p.get('redditOptions') or p.get('instagramOptions') or ''),flush=True)
