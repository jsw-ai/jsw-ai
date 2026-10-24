import json,sys,numpy as np
def win(f):
    d=json.load(open(f)); t=[r[0] for r in d]; s=np.array([r[1] if r[1] is not None else np.nan for r in d],float)
    med=np.array([np.nanmedian(s[max(0,i-1):i+2]) for i in range(len(s))])
    best=(0,0,0)
    for i in range(len(s)):
        for j in range(i,len(s)):
            seg=s[i:j+1];m=med[i:j+1]
            if np.isnan(seg).any() or seg.min()<0.72 or m.min()<0.78: break
            if j-i>best[1]-best[0]: best=(i,j,0)
    i,j,_=best; return t[i],t[j],(s[i:j+1].min() if j>i else None),(med[i:j+1].min() if j>i else None)
for f in sys.argv[1:]: print(f, win(f))
