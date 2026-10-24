# dl.py <jobs_wait output file> : downloads completed jobs by job id using work/jobs_v3.txt names -> raw/<name>.mp4
import re,sys,subprocess,os
B='/workspace/hf-test/zen/posting/camille_oct20/v3/'
names={l.split()[2]:l.split()[0] for l in open(B+'work/jobs_v3.txt') if len(l.split())>=3 and re.match(r'[0-9a-f]{8}-',l.split()[2])}
t=open(sys.argv[1]).read()
for jid,st,url in re.findall(r'job_id: (\S+)\n\s+status: (\w+)\n(?:\s+\w+: .*\n)*?\s+result_url: "?([^"\s]+)',t):
    n=names.get(jid)
    o=B+'raw/'+n+'.mp4'
    if st=='completed' and n and not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
for jid,st,url in re.findall(r'\d+,([0-9a-f-]{36}),(\w+),\w+,\w+,"?(https[^",\s]+)',t):
    n=names.get(jid); o=B+'raw/'+str(n)+'.mp4'
    if st=='completed' and n and not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
print(re.findall(r'status: (\w+)',t))
