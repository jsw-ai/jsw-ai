import re,sys,subprocess,os
B='/workspace/hf-test/zen/posting/camille_oct21/'
names={l.split()[2]:l.split()[0] for l in open(B+'work/jobs.txt') if len(l.split())>=3}
t=open(sys.argv[1]).read()
for jid,st,url in re.findall(r'job_id: (\S+)\n\s+status: (\w+)\n(?:\s+\w+: .*\n)*?\s+result_url: "?([^"\s]+)',t):
    n=names.get(jid); ext=url.rsplit('.',1)[1]
    o=B+'raw/'+str(n)+'.'+ext
    if st=='completed' and n and not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
for jid,st,url in re.findall(r'\d+,([0-9a-f-]{36}),(\w+),\w+,\w+,"?(https[^",\s]+)',t):
    n=names.get(jid); ext=url.rsplit('.',1)[1]; o=B+'raw/'+str(n)+'.'+ext
    if st=='completed' and n and not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
