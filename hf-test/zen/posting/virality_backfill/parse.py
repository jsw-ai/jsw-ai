import re,json,sys,subprocess,os
B='https://d8j0ntlcm91z4.cloudfront.net/user_3FVNMIClbGzn2xUkyZYSkvCyeX9/'
out={}
for l in open('jobs.tsv'):
  v,j,n=l.split()
  h=v+'.html'
  if not os.path.exists(h): subprocess.run(['curl','-s','-o',h,B+n+'.html'])
  t=open(h).read()
  m=re.search(r'"scores":(\{[^}]*\})',t); s=json.loads(m.group(1)) if m else {}
  g=re.search(r'"global_scores_by_frame":\[([^\]]*)\]',t); fr=[float(x) for x in g.group(1).split(',')] if g else []
  out[v]=dict(s,frames=fr)
json.dump(out,open('scores.json','w'),indent=1)
for v,s in sorted(out.items()): print(v,{k:s.get(k) for k in ['overall_score','hook_score','viral_potential','brain_engagement','sustain','peak_second']})
