import json,hashlib,requests,os,collections,subprocess
D=json.load(open('details.json'))
os.makedirs('media',exist_ok=True)
cache={};groups=collections.defaultdict(list);out={}
for k,p in D.items():
    for u in p.get('mediaUrls') or []:
        if u not in cache:
            r=requests.get(u,timeout=180); h=hashlib.md5(r.content).hexdigest()
            fn='media/'+h+os.path.splitext(u)[1]; open(fn,'wb').write(r.content)
            dur=None
            if fn.endswith('.mp4') or fn.endswith('.mov'):
                dur=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn],capture_output=True,text=True).stdout.strip()
            cache[u]=(h,dur,len(r.content),r.status_code)
        groups[cache[u][0]].append((k,p['platforms'],p['scheduleDate']))
        out.setdefault(k,[]).append([u]+list(cache[u]))
json.dump({'by_post':out,'groups':groups},open('media_md5.json','w'),indent=1)
for k,v in out.items(): print(k,[(x[1][:10],x[2],x[3],x[4]) for x in v])
print('--- shared files')
for h,v in groups.items():
    if len(v)>1 or any(len(x[1])>1 for x in v): print(h,v)
