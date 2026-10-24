import sys,json,cv2,numpy as np
sys.path.insert(0,'..')
import identity_gate as g
ms=g.load_embs(['/workspace/hf-test/zen/posting/madison_test/refs/m_face.jpg']); 
E,c=g.get_refs('camille')
res={}
for n in range(1,7):
    im=cv2.imread(f'raw/r2_{n}.png'); f,(W,H)=g.faces(im)
    if not f: print(n,'noface');continue
    # faces() may downscale; use same scale
    s=1280/max(im.shape[:2]) if max(im.shape[:2])>1280 else 1
    im2=cv2.resize(im,None,fx=s,fy=s) if s<1 else im
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    b=x.bbox.astype(int); x0,y0,x1,y1=[max(0,v) for v in b]
    crop=cv2.cvtColor(im2[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY)
    lap=cv2.Laplacian(crop,cv2.CV_64F).var()
    e=x.normed_embedding
    print(n,'face_frac_h %.2f'%((y1-y0)/H),'lap %.0f'%lap,'cos_camille_centroid %.2f'%float(e@c),'max_ref %.2f'%float((E@e).max()),'cos_madison %.2f'%float((ms@e).max()))
