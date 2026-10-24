import json,requests,subprocess,sys,os;sys.path.insert(0,'/workspace')
from ayr_sienna import H
A='https://api.ayrshare.com/api';S='/home/box/agent-data/secrets/'
for m in ['madison','gabriela','valentina','camille','sienna']:
  h=H(True)
  if m!='sienna': h['Profile-Key']=open(S+f'JSW-{m}-ayrshare-profile-key.txt').read().strip()
  L=requests.get(A+'/history?lastRecords=300',headers=h).json(); L=L['history'] if isinstance(L,dict) else L
  for p in L:
    if p.get('status')!='pending': continue
    pl=p.get('platforms',[]); io=p.get('instagramOptions') or {}; yo=p.get('youTubeOptions') or {}
    kinds=[k for k,c in [('TikTok','tiktok' in pl),('Reel','instagram' in pl and not io.get('stories') and any(u.endswith('.mp4') for u in p.get('mediaUrls') or [])),('Short','youtube' in pl and yo.get('shorts'))] if c]
    if not kinds: continue
    for u in p.get('mediaUrls') or []:
      d=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',u],capture_output=True,text=True).stdout.strip()
      try: f=float(d)
      except: f=None
      print(m,p['id'],'/'.join(kinds),p['scheduleDate'],d,'UNDER 7s' if f is not None and f<7 else ('NO DURATION' if f is None else ''),flush=True)
    if not p.get('mediaUrls'): print(m,p['id'],kinds,'NO MEDIA',flush=True)
