import cv2,numpy as np,sys,subprocess
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(480,480))
def run(src,dst,strength=0.8):
    cap=cv2.VideoCapture(src);w=int(cap.get(3));h=int(cap.get(4));fps=cap.get(5)
    tmp=dst+'.noaudio.mp4'
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    box=None;i=0;det=0
    while True:
        ok,fr=cap.read()
        if not ok: break
        if i%2==0:
            s=480/w;sm=cv2.resize(fr,(480,int(h*s)));fs=app.get(sm)
            if fs:
                f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox/s
                if (b[2]-b[0])>w*0.08:
                    box=b if box is None else 0.5*box+0.5*b;det+=1
                else: box=None
            else: box=None
        out=fr
        if box is not None:
            bw,bh=box[2]-box[0],box[3]-box[1];cx,cy=(box[0]+box[2])/2,(box[1]+box[3])/2
            x0,y0=int(max(0,cx-bw*.9)),int(max(0,cy-bh*.95));x1,y1=int(min(w,cx+bw*.9)),int(min(h,cy+bh*.95))
            roi=fr[y0:y1,x0:x1];m=np.zeros(roi.shape[:2],np.float32)
            cv2.ellipse(m,(int(cx-x0),int(cy-bh*.05-y0)),(int(bw*.62),int(bh*.75)),0,0,360,1,-1)
            ycc=cv2.cvtColor(roi,cv2.COLOR_BGR2YCrCb);cr,cb=ycc[...,1].astype(int),ycc[...,2].astype(int)
            sk=cv2.GaussianBlur(((cr>135)&(cr<185)&(cb>85)&(cb<135)).astype(np.float32),(0,0),3)
            m=cv2.GaussianBlur(m,(0,0),bw*.08)*sk*strength
            lab=cv2.cvtColor(roi,cv2.COLOR_BGR2LAB).astype(np.float32);L=lab[...,0]
            base=cv2.GaussianBlur(L,(0,0),bw*.12);hi=np.clip(L-(base+8),0,None)
            lab[...,0]=np.clip(L-hi*0.6*m,0,255)
            out=fr.copy();out[y0:y1,x0:x1]=cv2.cvtColor(lab.astype(np.uint8),cv2.COLOR_LAB2BGR)
        p.stdin.write(out.tobytes());i+=1
    p.stdin.close();p.wait()
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',tmp,'-i',src,'-map','0:v','-map','1:a?','-c:v','copy','-c:a','copy','-map_metadata','-1',dst]);
    import os;os.remove(tmp);print(src,'frames',i,'detected',det)
if __name__=='__main__': run(sys.argv[1],sys.argv[2],float(sys.argv[3]) if len(sys.argv)>3 else 0.8)
