import re,subprocess,os,sys
names=dict(l.split()[:2][::-1] for l in open('work/jobs.txt'))
t=open(sys.argv[1]).read()
for jid,st in re.findall(r'([0-9a-f-]{36}),(\w+)',t): print(names.get(jid),st)
for jid,url in re.findall(r'([0-9a-f-]{36}),completed,\w+,[\w.-]+,"?(https[^",\s]+)',t):
    n=names[jid]; o='raw/'+n+'.'+url.rsplit('.',1)[1]
    if not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
