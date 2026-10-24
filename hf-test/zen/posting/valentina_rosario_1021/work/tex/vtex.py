# per-frame v4C-style finish for video: skin mask, tame specular highlights, pore-scale texture, light sharpen, sensor grain
import sys, subprocess, numpy as np, cv2
src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5); W=int(cap.get(3)); H=int(cap.get(4))
p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-crf','12','-pix_fmt','yuv420p',dst], stdin=subprocess.PIPE)
rng = np.random.default_rng(3); k=0
while True:
    ok, fr = cap.read()
    if not ok: break
    a = fr.astype(np.float32)
    ycc = cv2.cvtColor(fr, cv2.COLOR_BGR2YCrCb).astype(np.float32); Y,Cr,Cb = ycc[...,0],ycc[...,1],ycc[...,2]
    m = ((Cr>135)&(Cr<180)&(Cb>80)&(Cb<130)&(Y>60)).astype(np.float32)
    m = cv2.GaussianBlur(m,(0,0),5)
    e = cv2.GaussianBlur(np.abs(Y-cv2.GaussianBlur(Y,(0,0),2)),(0,0),3); prot = np.clip(1-(e-4)/6,0,1); mm = m*prot
    hl = np.clip((Y-195)/60,0,1)*m
    a -= (hl*16)[...,None]                                  # break up locked specular sheen
    n1 = cv2.GaussianBlur(rng.normal(0,1,Y.shape).astype(np.float32),(0,0),0.8)*7
    n2 = cv2.GaussianBlur(rng.normal(0,1,Y.shape).astype(np.float32),(0,0),3)*4
    a += ((n1*0.5+n2*0.35)*mm*(0.6+0.4*Y/255))[...,None]    # pore-scale texture on skin
    a += (a - cv2.GaussianBlur(a,(0,0),1.0))*0.3            # light sharpen
    a += cv2.GaussianBlur(rng.normal(0,2.2,Y.shape).astype(np.float32),(0,0),0.5)[...,None]  # sensor grain
    p.stdin.write(np.clip(a,0,255).astype(np.uint8).tobytes()); k+=1
p.stdin.close(); p.wait(); print('frames',k)
