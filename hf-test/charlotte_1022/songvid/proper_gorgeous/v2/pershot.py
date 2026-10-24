#!/workspace/.face-venv/bin/python
# usage: pershot.py name [name...]  -> qc/<name>_gate.json + csv; every 2nd frame, per-shot windows from manifest
import sys,json,cv2,numpy as np,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
refs,cent=g.get_refs('charlotte')
def sc(fr):
    fr=cv2.resize(fr,(720,1280)); f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if not f: return None
    m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); return round(float(cent@m.normed_embedding),4)
for n in sys.argv[1:]:
    man=json.load(open(f'final/{n}_manifest.json')); cap=cv2.VideoCapture(f'final/{n}.mp4'); res=[]; i=0
    while True:
        ok,fr=cap.read()
        if not ok: break
        if i%2==0: res.append((round(i/30,3),sc(fr)))
        i+=1
    open(f'qc/{n}_perframe.csv','w').write('t,score\n'+''.join(f'{t},{s}\n' for t,s in res))
    shots=[]
    for k,s in enumerate(man['shots']):
        v=[x for t,x in res if s['t0']<=t<s['t1']]; nf=sum(x is None for x in v); v=[x for x in v if x is not None]
        d=dict(shot=k,t0=s['t0'],t1=s['t1'],still=os.path.basename(s['source_still']),frames=len(v),no_face=nf,median=round(float(np.median(v)),4) if v else None,min=min(v) if v else None)
        d['pass']=bool(v) and d['median']>=0.78 and d['min']>=0.70 and nf==0; shots.append(d)
    allv=[x for _,x in res if x is not None]
    out=dict(file=man['file'],frames=len(res),median=round(float(np.median(allv)),4),min=min(allv),no_face=len(res)-len(allv),shots=shots,pass_=all(s['pass'] for s in shots))
    json.dump(out,open(f'qc/{n}_gate.json','w'),indent=1)
    print(n,'PASS' if out['pass_'] else 'FAIL',out['median'],out['min'],[(s['shot'],s['median'],s['min'],s['pass']) for s in shots],flush=True)
