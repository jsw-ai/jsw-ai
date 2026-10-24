import sys,cv2,numpy as np,subprocess,json
from insightface.app import FaceAnalysis
vid,wav=sys.argv[1],sys.argv[2]
app=FaceAnalysis(name='buffalo_l',allowed_modules=['detection','landmark_2d_106'],providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
cap=cv2.VideoCapture(vid);fps=cap.get(5);m=[]
while True:
  ok,f=cap.read()
  if not ok:break
  fs=app.get(f)
  if not fs: m.append(np.nan);continue
  l=max(fs,key=lambda x:x.bbox[2]-x.bbox[0]).landmark_2d_106
  # inner lip: use distance between upper/lower lip landmarks 
  up=l[[71,62,63,64]].mean(0) if False else None
  ys=l[52:72,1]; xs=l[52:72,0]
  h=(l[:,1].max()-l[:,1].min())
  m.append((np.ptp(l[52:72][:,1]))/h)
m=np.array(m);m=np.nan_to_num(m,nan=np.nanmean(m))
a=subprocess.run(['ffmpeg','-v','error','-i',wav,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
a=np.frombuffer(a,np.int16).astype(np.float32);hop=int(16000/fps)
e=np.array([np.sqrt((a[i*hop:(i+1)*hop]**2).mean()+1e-9) for i in range(len(m))])
z=lambda x:(x-x.mean())/(x.std()+1e-9)
r={lag:float(np.mean(z(m[max(0,lag):len(m)+min(0,lag)])*z(e[max(0,-lag):len(e)-max(0,lag)]))) for lag in range(-30,31)}
np.save('qc/mouth_'+vid.split('/')[-1]+'.npy',m);print(json.dumps({'zero_lag':round(r[0],3),'best':max(r.items(),key=lambda x:x[1])}))
