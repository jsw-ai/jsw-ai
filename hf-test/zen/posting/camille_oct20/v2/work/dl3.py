import re,sys,subprocess,os
M={'30':'D6_t1','31':'D6_t2','32':'D6_t3','33':'D6_t4','20':'D6a','21':'D6b','12':'D5_t1','13':'D5_t2','14':'D4_t1','15':'D4_t2','16':'FL2h_t1','17':'FL2h_t2'}
t=open(sys.argv[1]).read()
rows=re.findall(r'(\d+),[0-9a-f-]{36},(\w+),\w+,\S+?,"?(https[^",\s]+)?',t)+[(a,b,c) for a,b,c in re.findall(r'index: (\d+)\n\s+job_id: \S+\n\s+status: (\w+)\n(?:.*\n){2}\s+result_url: "([^"]+)"',t)]
for i,st,u in rows:
    o='raw/%s.mp4'%M.get(i,i)
    if st=='completed' and u and not os.path.exists(o): subprocess.run(['curl','-s','-o',o,u]); print('got',o)
print(re.findall(r'(?:index: )?(\d+)[,\n]\s*(?:job_id: )?[0-9a-f-]{36}[,\n]\s*(?:status: )?(\w+)',t))
