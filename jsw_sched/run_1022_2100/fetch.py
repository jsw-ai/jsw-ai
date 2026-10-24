import json,requests
S='/home/box/agent-data/secrets/'
A='https://app.ayrshare.com/api'
key=open(S+'JSW-ayrshare-api-key.txt').read().strip()
for m in ['sienna','camille','charlotte','gabriela','madison','valentina']:
    h={"Authorization":"Bearer "+key}
    if m!='sienna': h["Profile-Key"]=open(S+f'JSW-{m}-ayrshare-profile-key.txt').read().strip()
    for kind,params in [('hist',{'lastDays':2}),('sched',{'status':'scheduled'})]:
        r=requests.get(A+'/history',headers=h,params=params,timeout=60)
        json.dump(r.json(),open(f'{kind}_{m}.json','w'),indent=1)
