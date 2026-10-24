import re,sys,subprocess,os
t=open(sys.argv[1]).read(); J=dict(l.split() for l in open('jobs.txt') if l.strip())
for u in re.findall(r'https://[^"\s,]+\.(?:png|mp4|jpg|jpeg|webp)',t):
    for jid,n in J.items():
        if jid in u:
            out=('kl/'+n+'.mp4') if u.endswith('mp4') else ('raw/'+n+'.png')
            if not os.path.exists(out): subprocess.run(['curl','-s','-o',out,u]); print(out)
