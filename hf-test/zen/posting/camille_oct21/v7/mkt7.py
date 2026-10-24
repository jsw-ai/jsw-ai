import cv2,numpy as np,subprocess
src='/workspace/hf-test/zen/posting/camille_oct21/raw/PB2.mp4'; a=0.0; b=0.8
cap=cv2.VideoCapture(src)
W,H=1080,1920; Z=1.12; cx,cy=585,820
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
# elliptical distance from subject core (face+hair+torso center), normalized
fx,fy=W/2,H*0.42
d=np.sqrt(((xx-fx)/(W*0.40))**2+((yy-fy)/(H*0.36))**2)
# body column below face stays sharp
body=np.clip((yy-H*0.55)/(H*0.1),0,1)*np.exp(-((xx-W/2)/(W*0.42))**8)
d=np.minimum(d,np.where(body>0,1-body*0.6+ (d-1)*0 ,d))
w=np.clip((d-0.85)/0.55,0,1); w=w*w*(3-2*w)   # smoothstep falloff, no hard edge
w=cv2.GaussianBlur(w,(0,0),40)[...,None]
dark=1-0.35*w
M=np.float32([[Z,0,W/2-cx*Z],[0,Z,H/2-cy*Z]])
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','24','-i','-','-c:v','libx264','-crf','10','-preset','fast','-pix_fmt','yuv420p','/workspace/hf-test/zen/posting/camille_oct21/v7/mkt7.mp4'],stdin=subprocess.PIPE)
for i in range(int(round((b-a)*24))):
    ok,f=cap.read()
    f=cv2.warpAffine(f,M,(W,H),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    b1=cv2.GaussianBlur(f,(0,0),8); b2=cv2.GaussianBlur(f,(0,0),22)
    # progressive: sharp -> b1 -> b2
    w1=np.clip(w*2,0,1); w2=np.clip(w*2-1,0,1)
    o=(f*(1-w1)+b1*w1)*(1-w2)+b2*w2
    o*=dark
    p.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
cv2.imwrite('/workspace/hf-test/zen/posting/camille_oct21/v7/wmap.png',(w[...,0]*255).astype(np.uint8))
