# mouth.py clip.mp4 -> per-frame mouth opening (inner lip gap / face height), audio RMS, best lag correlation, and frames with extreme wide-open mouth
import sys,cv2,numpy as np,subprocess,insightface
from insightface.app import FaceAnalysis
app=FaceAnalysis(allowed_modules=['detection','landmark_2d_106'],providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1,det_size=(640,640))
f=sys.argv[1]; cap=cv2.VideoCapture(f); fps=cap.get(5); op=[]
while True:
    ok,im=cap.read()
    if not ok: break
    fs=app.get(cv2.resize(im,(540,960)))
    if not fs: op.append(np.nan); continue
    L=max(fs,key=lambda x:x.bbox[2]-x.bbox[0]).landmark_2d_106
    # 106-pt: inner lips upper 71..? use mouth points 52-71; opening = vertical spread of inner mouth pts / face height
    mo=L[52:72]; fh=np.ptp(L[:,1])
    op.append((np.ptp(mo[:,1]))/fh)
op=np.array(op)
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',f,'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)
hop=int(16000/fps); r=np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)+1e-9) for i in range(len(op))])
ok=~np.isnan(op); o=op.copy(); o[~ok]=np.nanmean(op)
def c(l):
    x=o[max(0,l):len(o)+min(0,l)]; y=r[max(0,-l):len(r)+min(0,-l)]; return np.corrcoef(x,y)[0,1]
cs={l:c(l) for l in range(-6,7)}; bl=max(cs,key=cs.get)
print(f,'fps',fps,'corr@0 %.2f best lag %d frames (%.2f) '%(cs[0],bl,cs[bl]))
thr=np.nanpercentile(op,95)
print('p50 %.3f p95 %.3f max %.3f'%(np.nanmedian(op),thr,np.nanmax(op)))
print('per 0.25s max open:',' '.join('%.2f:%.3f'%(i/4,np.nanmax(op[int(i*fps/4):int((i+1)*fps/4)])) for i in range(int(len(op)/fps*4))))
