import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
A=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);A.prepare(ctx_id=-1,det_size=(640,640))
c=np.load('centroid.npy');v=sys.argv[1];out=sys.argv[2]
cap=cv2.VideoCapture(v);fps=cap.get(5);n=int(cap.get(7));sc=[];faces=[];bodies=[]
for i in range(0,n,3):
    cap.set(1,i);ok,im=cap.read()
    if not ok:break
    f=A.get(im)
    if not f: sc.append((i/fps,0));continue
    f=max(f,key=lambda x:x.bbox[2]-x.bbox[0]);s=float(f.normed_embedding@c);sc.append((i/fps,s))
    if abs((i/fps*2)-round(i/fps*2))<0.06:
        x1,y1,x2,y2=f.bbox;w=x2-x1;cx,cy=(x1+x2)/2,(y1+y2)/2;r=w*1.1
        fc=cv2.resize(im[max(0,int(cy-r)):int(cy+r),max(0,int(cx-r)):int(cx+r)],(200,200))
        cv2.putText(fc,'%.1fs %.2f'%(i/fps,s),(4,18),0,0.55,(0,0,255),2);faces.append(fc)
        if round(i/fps*2)%4==0: bodies.append(cv2.resize(im,(240,int(240*im.shape[0]/im.shape[1]))))
s=np.array([x[1] for x in sc]);print(v,'min %.3f med %.3f max %.3f frac>=.70 %.2f'%(s.min(),np.median(s),s.max(),(s>=.70).mean()))
print(' '.join('%.1f:%.2f'%x for x in sc[::4]))
refs=[cv2.imread('/workspace/hf-test/zen/posting/valentina_test2/fin/%s_v4C.jpg'%k) for k in ['s5_a','s2_b','s1_a']]
rf=[]
for im in refs:
    f=max(A.get(im),key=lambda x:x.bbox[2]-x.bbox[0]);x1,y1,x2,y2=f.bbox;w=x2-x1;cx,cy=(x1+x2)/2,(y1+y2)/2;r=w*1.1
    rf.append(cv2.resize(im[max(0,int(cy-r)):int(cy+r),max(0,int(cx-r)):int(cx+r)],(200,200)))
rows=[np.hstack(rf+faces[i:i+5]+[np.zeros((200,200,3),np.uint8)]*(5-len(faces[i:i+5]))) for i in range(0,len(faces),5)]
F=np.vstack(rows)
rb=cv2.resize(refs[0],(240,int(240*refs[0].shape[0]/refs[0].shape[1])))
h=bodies[0].shape[0];rb=cv2.resize(rb,(int(rb.shape[1]*h/rb.shape[0]),h))
B=np.hstack([rb]+bodies)
W=max(F.shape[1],B.shape[1])
pad=lambda x:np.hstack([x,np.full((x.shape[0],W-x.shape[1],3),255,np.uint8)])
cv2.imwrite(out,np.vstack([pad(F),pad(B)]),[cv2.IMWRITE_JPEG_QUALITY,85])
