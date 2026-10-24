import json,re
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo
ET=ZoneInfo('America/Detroit')
TZ={'sienna':'Australia/Brisbane','camille':'Europe/Paris','charlotte':'Europe/Berlin','gabriela':'America/New_York','madison':'America/Chicago','valentina':'America/New_York'}
D=json.load(open('details.json'))
rows=[]
for k,p in D.items():
    m,pid=k.split(':')
    sd=datetime.fromisoformat(p['scheduleDate'].replace('Z','+00:00'))
    rows.append((m,sd,pid,p))
rows.sort(key=lambda r:(r[0],r[1]))
for m,sd,pid,p in rows:
    et=sd.astimezone(ET); loc=sd.astimezone(ZoneInfo(TZ[m]))
    pl=p.get('platforms'); cap=p.get('post') or ''
    iss=[]
    if 2<=et.hour<6: iss.append('ET2-6AM')
    if 'tiktok' in pl:
        if not (p.get('tikTokOptions') or {}).get('isAIGenerated'): iss.append('TT-noAI')
        if loc.hour<7: iss.append('TT-local<7')
    if 'instagram' in pl and not (p.get('instagramOptions') or {}).get('isAIGenerated'): iss.append('IG-noAI')
    if 'youtube' in pl:
        yo=p.get('youTubeOptions') or {}
        if not yo.get('thumbNail'): iss.append('YT-nothumb')
        if yo.get('visibility') not in (None,'public'): iss.append('YT-vis:'+str(yo.get('visibility')))
    if 'twitter' in pl:
        urls=re.findall(r'https?://\S+',cap)
        if [u for u in urls if 'music.apple.com' not in u]: iss.append('X-URL')
        if not p.get('mediaUrls') and '?' not in cap: iss.append('X-textonly')
    if re.search(r'fanvue',cap,re.I): iss.append('FANVUE')
    if re.search(r'\bAI\b|artificial',cap): iss.append('AI-in-cap')
    keys=sorted(set(p.keys())-{'post','platforms','scheduleDate','id','mediaUrls','status','created','refId','profileTitle','type','user','postIds','scheduleTime','approved','mediaUrlsWithMetaData','isVideo','notes','shortenLinks','urls','profileKeyPrefix','profileKey'})
    print(f"{m:9} {pid} {et:%a %H:%M}ET loc{loc:%H:%M} {','.join(pl):22} media={len(p.get('mediaUrls') or [])} {iss} | {cap[:70]!r} {keys}")
