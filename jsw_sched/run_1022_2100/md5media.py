import json,hashlib,requests,os,collections
D=json.load(open('details.json'))
cache={}
os.makedirs('media',exist_ok=True)
groups=collections.defaultdict(list)
out={}
for k,p in D.items():
    for u in p.get('mediaUrls') or []:
        if u not in cache:
            r=requests.get(u,timeout=120); cache[u]=hashlib.md5(r.content).hexdigest()
        groups[cache[u]].append((k,p['platforms'],p['scheduleDate']))
        out.setdefault(k,[]).append(cache[u])
json.dump({'by_post':out,'groups':groups},open('media_md5.json','w'),indent=1)
for h,v in groups.items():
    if len(v)>1 or any(len(x[1])>1 for x in v): print(h,v)
