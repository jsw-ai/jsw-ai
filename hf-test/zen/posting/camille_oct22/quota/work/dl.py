import re,sys,subprocess,os
names=dict(l.split()[:2][::-1] for l in open('work/jobs.txt'))
t=open(sys.argv[1]).read()
for jid,st,url in re.findall(r'job_id: (\S+)\n\s+status: (\w+)\n(?:\s+\w+: .*\n)*?\s+result_url: "?([^"\s]+)',t):
    n=names.get(jid)
    if n and st=='completed':
        o='raw/'+n+'.'+url.rsplit('.',1)[1]
        if not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
