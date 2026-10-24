import sys,glob,numpy as np,cv2
from insightface.app import FaceAnalysis
A=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);A.prepare(ctx_id=-1,det_size=(640,640))
def emb(p):
    im=cv2.imread(p) if isinstance(p,str) else p
    h,w=im.shape[:2];s=min(1,1280/max(h,w));im=cv2.resize(im,(int(w*s),int(h*s)))
    f=A.get(im)
    if not f: return None
    f=max(f,key=lambda x:(x.bbox[2]-x.bbox[0]));e=f.normed_embedding;return e
R=[emb(p) for p in sorted(glob.glob('/workspace/hf-test/zen/posting/valentina_test2/fin/s[1245678]_[ab]_v4C.jpg'))]
c=np.mean(R,0);c/=np.linalg.norm(c)
np.save('centroid.npy',c)
for p in sys.argv[1:]:
    e=emb(p);print(p, None if e is None else round(float(e@c),3))
