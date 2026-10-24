import re,subprocess,json,sys
f,d=sys.argv[1],sys.argv[2]
ids=json.load(open('man/media_ids.json'))
for l in open(f):
    m=re.match(r"- (\S+): .*@(\S+) '(\S+)'",l)
    if not m: continue
    mid,fn,url=m.groups()
    ct='video/mp4' if fn.endswith('mp4') else 'image/jpeg'
    for k in range(3):
        r=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-X','PUT','-H','Content-Type: '+ct,'-H','If-None-Match: *','--data-binary','@'+d+'/'+fn,url],capture_output=True,text=True).stdout
        if r=='200': break
    ids[fn]=mid; print(fn,mid,r)
json.dump(ids,open('man/media_ids.json','w'),indent=1)
