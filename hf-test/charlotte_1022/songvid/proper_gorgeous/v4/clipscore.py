#!/workspace/.face-venv/bin/python
# per-frame identity scores of raw clips after the same 9:16 cover crop as build3 (720x1280), all frames
import sys,json,os,subprocess,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
refs,cent=g.get_refs('charlotte')
for p in sys.argv[1:]:
    k=os.path.basename(p)[:-4]; o=f'clipscores/{k}.json'
    if os.path.exists(o): continue
    fps=eval(subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=r_frame_rate','-of','csv=p=0',p]).decode().strip())
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-vf','scale=-2:1280:flags=lanczos,crop=720:1280','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,1280,720,3); res=[]
    for i,f in enumerate(fr):
        if i%2: continue
        F,_=g.faces(np.ascontiguousarray(f)); F=[x for x in F if x.det_score>=0.55]
        s=None if not F else round(float(cent@max(F,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding),4)
        res.append((round(i/fps,3),s))
    json.dump(dict(file=p,fps=fps,per_frame=res),open(o,'w')); v=[s for _,s in res if s]
    print(k,len(res),round(float(np.median(v)),4),min(v),flush=True)
