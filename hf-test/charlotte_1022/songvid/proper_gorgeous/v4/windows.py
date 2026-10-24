import json,glob,numpy as np,sys
MED=float(sys.argv[1]) if len(sys.argv)>1 else .795; MN=.72; MINLEN=0.8
for f in sorted(glob.glob('clipscores/*.json')):
    d=json.load(open(f)); pf=d['per_frame']; best=[]
    n=len(pf)
    for i in range(n):
        for j in range(n-1,i,-1):
            w=[s for _,s in pf[i:j+1]]
            if None in w or min(w)<MN: continue
            L=pf[j][0]-pf[i][0]
            if L<MINLEN: break
            if np.median(w)>=MED: best.append((round(L,2),pf[i][0],pf[j][0],round(float(np.median(w)),4),min(w))); break
    best.sort(reverse=True)
    # greedy non-overlapping
    sel=[]
    for b in best:
        if all(b[2]<=s[1] or b[1]>=s[2] for s in sel): sel.append(b)
    print(f.split('/')[-1][:-5], sel[:3])
