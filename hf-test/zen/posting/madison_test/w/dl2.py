import re,sys,subprocess,os
out=sys.argv[1]
for f in sys.argv[2:]:
    t=open(f).read()
    for m in re.finditer(r'(\d+)[, ]+[0-9a-f-]{36}[, ]+completed[^"\n]*?"?(https://\S+?\.png)"?\s',t.replace('\n    ',' ').replace('index: ','').replace('job_id: ','').replace('status: ','').replace('result_url: ','').replace('type: image model: seedream_v5_pro','')):
        i,u=m.group(1),m.group(2)
        p=f'{out}/w{i}.png'
        if not os.path.exists(p): subprocess.call(['curl','-s','-o',p,u])
