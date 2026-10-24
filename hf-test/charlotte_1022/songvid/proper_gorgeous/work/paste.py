import json,subprocess,cv2,numpy as np,sys,os
J=json.load(open('hz.json'))
for k,v in J.items():
    o=f'hz/{k}_op.png'
    if not os.path.exists(o): subprocess.run(['curl','-s','-o',o,f'https://d8j0ntlcm91z4.cloudfront.net/user_3FVNMIClbGzn2xUkyZYSkvCyeX9/hf_20261022_{v}.png'])
    big=cv2.imread(o); src=cv2.imread(f'hz/{k}_top.jpg')
    H,W=big.shape[:2]; h,w=src.shape[:2]; s=H/h
    sr=cv2.resize(src,(round(w*s),H),interpolation=cv2.INTER_CUBIC)
    r=cv2.matchTemplate(big[:, :],sr[20:-20,20:-20],cv2.TM_CCOEFF_NORMED); _,mv,_,ml=cv2.minMaxLoc(r)
    x=ml[0]-20; y=ml[1]-20
    m=np.zeros(sr.shape[:2],np.float32); m[:, :]=1; f=24
    ramp=np.linspace(0,1,f); m[:, :f]*=ramp; m[:, -f:]*=ramp[::-1]; m=m[...,None]
    out=big.astype(np.float32); x0=max(0,x); x1=min(W,x+sr.shape[1])
    reg=out[:, x0:x1]; s2=sr[:, x0-x:x1-x].astype(np.float32); mm=m[:, x0-x:x1-x]
    out[:, x0:x1]=reg*(1-mm)+s2*mm
    cv2.imwrite(f'hz/{k}_16x9.jpg',out.astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
    print(k,W,H,'match',round(mv,3),'x',x)
