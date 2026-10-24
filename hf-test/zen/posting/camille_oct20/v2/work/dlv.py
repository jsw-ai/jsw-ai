import re,sys,subprocess,os
N=['GA2_t1','GA2_t2','GB2_t1','GB2_t2','E3_t1','E3_t2','E4_t1','E4_t2','D3_t1','D3_t2','FL2_t1','FL2_t2']
off=int(sys.argv[2]) if len(sys.argv)>2 else 0
t=open(sys.argv[1]).read()
for i,st,url in re.findall(r'index: (\d+)\n\s+job_id: \S+\n\s+status: (\w+)\n(?:.*\n){2}\s+result_url: "([^"]+)"',t):
    n=N[int(i)-off] if int(i)-off<len(N) else 'x'+i
    o='raw/%s.mp4'%n
    if st=='completed' and not os.path.exists(o): subprocess.run(['curl','-s','-o',o,url]); print('got',n)
print(re.findall(r'index: (\d+)\n\s+job_id: \S+\n\s+status: (\w+)',t))
