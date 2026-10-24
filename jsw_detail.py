import requests
S='/home/box/agent-data/secrets/'
K=open(S+'JSW-ayrshare-api-key.txt').read().strip()
for m,ids in [('madison',['EInWuetM55Bg99oOyNwg']),('gabriela',['UWKTZb7NgGAwqCLB2UjB']),('valentina',['VQIhVBY5OkURy1C4iBDr'])]:
    h={'Authorization':'Bearer '+K,'Profile-Key':open(S+f'JSW-{m}-ayrshare-profile-key.txt').read().strip()}
    d=requests.get('https://api.ayrshare.com/api/history',headers=h,params={'status':'pending'},timeout=60).json()
    for p in d if isinstance(d,list) else d.get('history',[]):
        if p.get('id') in ids: print(m,p.get('id'),p.get('created'),p.get('mediaUrls'),p.get('tikTokOptions'),p.get('instagramOptions'),repr(p.get('post')))
