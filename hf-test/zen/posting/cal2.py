import sys,glob,json,os,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
R='/workspace/hf-test/'; Z=R+'zen/posting/'
refs=sorted(glob.glob(Z+'sienna_refs/*.jpg'))
def emb(p):
    im=cv2.imread(p); f,_=g.faces(im)
    return None if not f else max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding
E={p:emb(p) for p in refs}
def sc(e,excl=()):
    A=np.array([v for k,v in E.items() if k not in excl]); c=A.mean(0);c/=np.linalg.norm(c); return float(c@e),float((A@e).max())
loo={os.path.basename(p):sc(E[p],(p,)) for p in refs}
neg={}
for p in sorted(glob.glob(R+'posting_oct14/retrain/raw/*')): 
    e=emb(p); neg['retrain/'+os.path.basename(p)]=sc(e) if e is not None else None
others={}
for m in ['camille','charlotte','madison','gabriela','valentina']:
    for p in sorted(glob.glob(R+f'keepers/{m}_*')):
        if p.endswith(('.png','.webp')):
            e=emb(p); 
            if e is not None: others[os.path.basename(p)]=sc(e)
oldkeep={}
for n in ['sienna_face_keeper.png','sienna_bikini1.png','sienna_bikini2.png','sienna_cover.png','sienna_face_close.png']:
    e=emb(R+'keepers/'+n); oldkeep[n]=sc(e) if e is not None else None
frames={}
for p in sorted(glob.glob('/tmp/fr/*.png')): 
    e=emb(p); frames[os.path.basename(p)]=sc(e,[x for x in refs if 'T1_wan' in x]) if e is not None else None
json.dump(dict(loo=loo,neg=neg,others=others,oldkeep=oldkeep,frames_heldout_video=frames),open('/tmp/cal2.json','w'),indent=1)
for k,v in json.load(open('/tmp/cal2.json')).items():
    print('==',k)
    for a,b in v.items(): print(' ',a,None if b is None else [round(x,3) for x in b])
