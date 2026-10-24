import sys,json,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting/valentina_oct22/work'); import vgate
for p in sys.argv[1:]:
    r=vgate.run(p,2); s=[x for _,x in r if x is not None]
    res=dict(file=p,frames=len(r),scored=len(s),median=float(np.median(s)) if s else 0,min=float(min(s)) if s else 0,below70=sum(x<.7 for x in s),per_frame=r)
    res['PASS']=bool(s) and len(s)==len(r) and res['median']>=.78 and res['min']>=.70
    json.dump(res,open(p[:-4]+'_gate.json','w'))
    print(p,'med %.3f min %.3f <.70 %d scored %d/%d'%(res['median'],res['min'],res['below70'],len(s),len(r)),'PASS' if res['PASS'] else 'FAIL',flush=True)
