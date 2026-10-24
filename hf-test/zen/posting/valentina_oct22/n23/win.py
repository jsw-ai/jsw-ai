import json,sys,numpy as np
for f in sys.argv[1:]:
  pf=json.load(open(f))['per_frame']; best=None
  for i in range(len(pf)):
    for j in range(i+1,len(pf)+1):
      s=[x for _,x in pf[i:j]]
      if None in s or min(s)<.70: break
      if np.median(s)>=.78 and (best is None or j-i>best[1]-best[0]): best=(i,j,np.median(s),min(s))
  if best: print(f,'window %.2f-%.2f s med %.3f min %.3f'%(pf[best[0]][0],pf[best[1]-1][0],best[2],best[3]))
  else: print(f,'no window')
