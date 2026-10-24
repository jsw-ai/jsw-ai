# dl.py resultfile idx=name ...  downloads completed results
import re,sys,subprocess
t=open(sys.argv[1]).read(); N=dict(a.split('=') for a in sys.argv[2:])
for i,jid,st,url in re.findall(r'  (\d+),([0-9a-f-]{36}),(\w+),\w+,\S+?,"([^"]+)"',t):
    if i in N and st=='completed':
        ext=url.rsplit('.',1)[1]; subprocess.run(['curl','-s','-o',f'raw/{N[i]}.{ext}',url]); print('got',N[i])
print(re.findall(r'  (\d+),[0-9a-f-]{36},(\w+)',t))
