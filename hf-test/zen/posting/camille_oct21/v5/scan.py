import sys,subprocess,re,glob,os,numpy as np,cv2
for t in sys.argv[1:]:
    D=f'v5/scan_{t}'; os.makedirs(D,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'raw/{t}.mp4','-vf','fps=4','-start_number','0',D+'/f%03d.png'],check=True)
    fs=sorted(glob.glob(D+'/f*.png'))
    g=subprocess.run(['/workspace/.face-venv/bin/python','/workspace/hf-test/zen/posting/identity_gate.py','img','--no-ocr','--model','camille_v3_draft']+fs,capture_output=True,text=True).stdout
    sc={m.group(1):m.group(2) for m in re.finditer(r"(?:PASS|FAIL) (\S+) .*?score_centroid': ([0-9.]+|None)",g)}
    cap=cv2.VideoCapture(f'raw/{t}.mp4'); prev=None; mot=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        h,w=f.shape[:2]; r=cv2.cvtColor(f[:int(h*.4)],cv2.COLOR_BGR2GRAY).astype(float)
        if prev is not None: mot.append(np.abs(r-prev).mean())
        prev=r
    fps=cap.get(5); mot=np.array(mot)
    print(t,'fps',fps,' '.join(f"{i*.25:.2f}:{sc.get(os.path.basename(f))}" for i,f in enumerate(fs)))
    print('  hairmotion per 0.5s',' '.join(f"{mot[int(i*fps/2):int((i+1)*fps/2)].mean():.2f}" for i in range(int(len(mot)/fps*2))))
