# skinfx.py in.mp4 out.mp4 [strength]  -- per-frame matte + natural texture pass on skin only (no blur on the image)
# skin mask (YCrCb) minus edges (eyes/lips/hair) ; specular roll-off (matte) ; boost existing fine detail (pores/freckles) ; fine luma grain on skin
import cv2,numpy as np,sys,subprocess
src,dst=sys.argv[1:3]; k=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
cap=cv2.VideoCapture(src); fps=cap.get(5); W=int(cap.get(3)); H=int(cap.get(4))
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-i',src,'-map','0:v','-map','1:a?','-c:a','copy','-c:v','libx264','-crf','13','-preset','fast','-pix_fmt','yuv420p',dst],stdin=subprocess.PIPE)
rng=np.random.default_rng(7); s=W/1080.0
while True:
    ok,f=cap.read()
    if not ok: break
    ycc=cv2.cvtColor(f,cv2.COLOR_BGR2YCrCb).astype(np.float32); Y,Cr,Cb=ycc[...,0],ycc[...,1],ycc[...,2]
    m=((Cr>135)&(Cr<180)&(Cb>80)&(Cb<130)&(Y>55)).astype(np.float32)
    m=cv2.GaussianBlur(m,(0,0),4*s)
    e=cv2.GaussianBlur(np.abs(Y-cv2.GaussianBlur(Y,(0,0),2*s)),(0,0),3*s)
    m*=np.clip(1-(e-5)/7,0,1)
    L=cv2.GaussianBlur(Y,(0,0),10*s)
    spec=np.clip(Y-L-6,0,None); Y=Y-0.45*k*spec*m                      # flatten shiny highlights (matte)
    hi=np.clip(Y-215,0,None); Y=Y-0.4*k*hi*m                            # roll off hot skin
    b1=cv2.GaussianBlur(Y,(0,0),0.9*s); b2=cv2.GaussianBlur(Y,(0,0),3.0*s)
    Y=Y+(0.9*k*np.clip(Y-b1,-8,8)+0.55*k*np.clip(b1-b2,-10,6))*m        # pores + freckle contrast
    g=cv2.GaussianBlur(rng.normal(0,2.2,Y.shape).astype(np.float32),(0,0),0.5*s)
    Y=Y+g*m*k
    ycc[...,0]=np.clip(Y,0,255)
    p.stdin.write(cv2.cvtColor(ycc.astype(np.uint8),cv2.COLOR_YCrCb2BGR).tobytes())
p.stdin.close(); p.wait(); print('ok',dst)
