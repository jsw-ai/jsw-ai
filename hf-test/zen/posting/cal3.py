import sys,glob,json,os,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
R='/workspace/hf-test/'; Z=R+'zen/posting/'
refs=sorted(glob.glob(Z+'sienna_refs/*.jpg'))
def emb(p):
    im=cv2.imread(p); f,_=g.faces(im)
    return None if not f else max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding
E={os.path.basename(p):emb(p) for p in refs}
grp=lambda n:'x2' if n.startswith('x2_dawn') else ('vid' if n.startswith('T1') else n)
def sc(e,ex=()):
    A=np.array([v for k,v in E.items() if grp(k) not in ex]); c=A.mean(0);c/=np.linalg.norm(c); return float(c@e),float((A@e).max())
out={}
# strict group LOO (drop x2 pair together, drop all video refs together)
for k in E: out[k]=sc(E[k],(grp(k),))
for k,v in out.items(): print('LOO-group',k,[round(x,3) for x in v])
# held-out video frames vs stills-only pack
fr=[]
for p in sorted(glob.glob('/tmp/fr/*.png')): 
    e=emb(p); fr.append((os.path.basename(p),sc(e,('vid',))))
for a,b in fr: print('frame vs stills-only',a,[round(x,3) for x in b])
E2=None
json.dump(dict(loo=out,fr=fr),open('/tmp/cal3.json','w'))
