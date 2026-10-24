import sys,json,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting/valentina_oct22/work'); import vgate
for p in sys.argv[1:]:
    r=vgate.run(p,2); s=[x for _,x in r if x is not None]
    res=dict(file=p,frames=len(r),scored=len(s),median=float(np.median(s)),min=float(min(s)),below70=sum(x<.7 for x in s),per_frame=r)
    res['PASS']=res['median']>=.78 and res['min']>=.70
    json.dump(res,open(p[:-4]+'_gate.json','w'))
    op=[x for t,x in r if t<1.6 and x]; 
    print(p,'med %.3f min %.3f <.70 %d scored %d/%d opener med %.3f min %.3f'%(res['median'],res['min'],res['below70'],len(s),len(r),np.median(op),min(op)),'PASS' if res['PASS'] else 'FAIL',flush=True)
