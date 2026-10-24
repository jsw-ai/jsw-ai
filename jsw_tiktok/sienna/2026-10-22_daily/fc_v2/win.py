import json,glob
for f in sorted(glob.glob('gate/v_*.json')):
    d=json.load(open(f));pf=d['per_frame'];best=(0,0,0);s=None
    for i,(t,v) in enumerate(pf):
        ok=v is not None and v>=0.78
        if ok and s is None: s=i
        if (not ok or i==len(pf)-1) and s is not None:
            e=i if ok else i-1
            L=pf[e][0]-pf[s][0]
            if L>best[0]: best=(round(L,2),pf[s][0],pf[e][0])
            s=None
    print(f, 'med',round(d['median'],3),'best window',best)
