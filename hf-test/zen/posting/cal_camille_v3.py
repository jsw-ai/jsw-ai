"""camille_v3 calibration 2026-10-22, same method as calibrate_gate.py/cal3.py (Sienna) + madison note:
pack LOO (centroid + best-ref), positives = approved pack refs + oct22 gated finals (stills + ~10 frames/clip),
negatives = other models' pack face refs. Run: /workspace/.face-venv/bin/python cal_camille_v3.py"""
import sys,glob,json,os,cv2,numpy as np,subprocess,tempfile
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
R='/workspace/hf-test/'; Z=R+'zen/posting/'; P=json.load(open(g.PACKS))
def emb(im):
    f,_=g.faces(im); return None if not f else max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding
rd=lambda p:cv2.imread(p if os.path.isabs(p) else R+p)
pack=P['camille_v3']['face_refs']; E={p:emb(rd(p)) for p in pack}
def sc(e,ex=()):
    A=np.array([v for k,v in E.items() if k not in ex and v is not None]); c=A.mean(0); c/=np.linalg.norm(c); return round(float(c@e),3),round(float((A@e).max()),3)
out={'loo':{},'stills':{},'clips':{},'neg':{}}
for p in pack: out['loo'][os.path.basename(p)]=sc(E[p],(p,))
for p in sorted(glob.glob(Z+'camille_oct22/fin/*.jpg')):
    e=emb(rd(p)); out['stills'][os.path.basename(p)]=sc(e) if e is not None else None
for m in sorted(glob.glob(Z+'camille_oct22/final/*_manifest.json')):
    v=m.replace('_manifest.json','_silent.mp4')
    if not os.path.exists(v): v=m.replace('_manifest.json','.mp4')
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v]))
    s=[]
    for i in range(10):
        t=d*(i+0.5)/10; tf=tempfile.mktemp(suffix='.png')
        subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',v,'-frames:v','1',tf]); im=cv2.imread(tf)
        if im is not None:
            e=emb(im)
            if e is not None: s.append(sc(e)[0])
            os.remove(tf)
    out['clips'][os.path.basename(v)]=dict(n=len(s),min=min(s) if s else None,med=float(np.median(s)) if s else None)
for m,v in P.items():
    if m.startswith('camille') or not isinstance(v,dict): continue
    for p in v.get('face_refs',[]):
        im=rd(p)
        if im is None: continue
        e=emb(im)
        if e is not None: out['neg'][m+'/'+os.path.basename(p)]=sc(e)
json.dump(out,open(Z+'camille_oct22/qc/calib_camille_v3_1022.json','w'),indent=1); print(json.dumps(out,indent=1))
