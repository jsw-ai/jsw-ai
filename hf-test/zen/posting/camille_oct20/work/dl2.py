import re,sys,subprocess,os
t=open(sys.argv[1]).read(); N=dict(a.split('=') for a in sys.argv[2:])
for blk in re.split(r'\n  - ',t):
    i=re.search(r'index: (\d+)',blk); st=re.search(r'status: (\w+)',blk); u=re.search(r'result_url: "([^"]+)"',blk)
    if not i: continue
    i=i.group(1); print(i,N.get(i),st.group(1) if st else '?')
    if u and i in N and not os.path.exists(f'raw/{N[i]}.mp4'): subprocess.run(['curl','-s','-o',f'raw/{N[i]}.mp4',u.group(1)])
