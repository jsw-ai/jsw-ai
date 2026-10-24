import sys,cv2;sys.path.insert(0,'.');from fgate import score
for k in ['s2_b','B3a','rosB','H1','F1']:
  for v in [f'hraw/h_{k}.png',f'hraw/h_{k}_tex.png',f'hfin/h_{k}_v4C.jpg']:
    im=cv2.imread(v);H,W=im.shape[:2];out=[]
    for z in [1.0,1.3,1.6]:
      # crop centered on face region: find face via full score first
      w,h=int(W/z),int(H/z);x=(W-w)//2;y=max(0,int((H-h)*0.3))
      c=cv2.resize(im[y:y+h,x:x+w],(1920,1080));s=score(c);out.append(f'z{z}:{s and round(s,3)}')
    print(v,*out,flush=True)
