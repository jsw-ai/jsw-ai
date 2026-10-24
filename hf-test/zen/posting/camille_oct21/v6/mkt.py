import cv2,numpy as np,subprocess,sys
import os; src="../raw/PB2.mp4"; a=float(os.environ["A"]); b=a+0.8; Z=float(os.environ.get("Z","1.15"))
cap=cv2.VideoCapture(src); cap.set(cv2.CAP_PROP_POS_MSEC,a*1000)
W,H=1080,1920; cx,cy=585,820
# static person mask in output coords (after zoom)
def zm(x,y): return int((x-cx)*Z+W/2), int((y-cy)*Z+H/2)
m=np.zeros((H,W),np.uint8)
c=zm(585,620); cv2.ellipse(m,c,(int(500*Z),int(540*Z)),0,0,360,255,-1)
torso=np.array([zm(x,y) for x,y in [(150,1050),(940,1050),(1080,1250),(1080,1920),(0,1920),(0,1250)]],np.int32)
cv2.fillPoly(m,[torso],255)
m=cv2.erode(m,np.ones((15,15),np.uint8)); mf=cv2.GaussianBlur(m,(0,0),35).astype(np.float32)/255; mf=mf[...,None]
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','24','-i','-','-c:v','libx264','-crf','10','-preset','fast','-pix_fmt','yuv420p','mkt.mp4'],stdin=subprocess.PIPE)
n=int(round((b-a)*24))
M=np.float32([[Z,0,W/2-cx*Z],[0,Z,H/2-cy*Z]])
for i in range(n):
    ok,f=cap.read()
    f=cv2.warpAffine(f,M,(W,H),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT)
    bg=cv2.GaussianBlur(f,(0,0),28).astype(np.float32)*0.55
    o=f*mf+bg*(1-mf)
    p.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
cv2.imwrite('mask.png',m)
