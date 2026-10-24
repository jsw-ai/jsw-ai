import cv2,numpy as np,sys
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(1024,1024))
def facebox(img):
    fs=app.get(img)
    if not fs: return None
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));return f.bbox
def process(img,strength=1.0):
    h,w=img.shape[:2];b=facebox(img)
    if b is None: return img
    cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2;bw,bh=b[2]-b[0],b[3]-b[1]
    m=np.zeros((h,w),np.float32);cv2.ellipse(m,(int(cx),int(cy-bh*0.05)),(int(bw*0.62),int(bh*0.75)),0,0,360,1,-1)
    # skin mask
    ycc=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb);cr,cb=ycc[...,1].astype(int),ycc[...,2].astype(int)
    sk=((cr>135)&(cr<185)&(cb>85)&(cb<135)).astype(np.float32);sk=cv2.GaussianBlur(sk,(0,0),5)
    m=cv2.GaussianBlur(m,(0,0),bw*0.08)*sk*strength
    lab=cv2.cvtColor(img,cv2.COLOR_BGR2LAB).astype(np.float32);L=lab[...,0]
    # local reference: heavy blur of L within face -> highlights = L above local mean
    base=cv2.GaussianBlur(L,(0,0),bw*0.12)
    hi=np.clip(L-(base+8),0,None)
    # also compress absolute highlights
    L2=L-hi*0.65*m
    # soften low-frequency sheen blobs slightly (frequency blend): replace mid-freq of L with its smoothed within mask
    mid=cv2.GaussianBlur(L2,(0,0),bw*0.025)
    L2=L2*(1-0.25*m)+mid*(0.25*m)+ (L2-mid)*0*m
    # keep high-frequency pore texture
    lo=cv2.GaussianBlur(L,(0,0),1.5);tex=L-lo
    L2=L2+tex*0.0
    lab[...,0]=np.clip(L2,0,255)
    # slight desat in highlights region
    lab[...,1:]=128+(lab[...,1:]-128)*(1-0.0*m[...,None])
    out=cv2.cvtColor(lab.astype(np.uint8),cv2.COLOR_LAB2BGR)
    return out
if __name__=='__main__':
    for n in sys.argv[1:]:
        for src,dst in ((f'raw/g{n}.png',f'raw/pp_g{n}.png'),(f'../stills/camille_s{n}.jpg',f'raw/pp_orig{n}.png')):
            img=cv2.imread(src);cv2.imwrite(dst,process(img));print(dst)
