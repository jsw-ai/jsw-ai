import sys,subprocess,os,json,glob
for c in sys.argv[1:]:
    src=f'clips/{c}.mp4'; d=os.path.abspath(f'qc/raw_{c}'); os.makedirs(d,exist_ok=True)
    for f in glob.glob(d+'/*'): os.remove(f)
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
    fs=[]
    for i in range(12):
        t=round(dur*(i+0.5)/12,2); p=f'{d}/f{i:02d}_{t}.jpg'; subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',src,'-frames:v','1','-q:v','2',p]); fs.append(p)
    subprocess.run(['/workspace/.face-venv/bin/python','/workspace/hf-test/zen/posting/identity_gate.py','img','--model','charlotte','--source','seedream','--no-ocr','--json',d+'/g.json']+fs,capture_output=True,cwd='/workspace/hf-test')
    g=json.load(open(d+'/g.json')); out=[]
    for f in fs:
        k=[v for kk,v in g.items() if kk.endswith(os.path.basename(f))]; out.append((k[0].get('score_centroid') or 0) if k else 0)
    print(c,'min %.3f'%min(out),' '.join('%.2f'%s for s in out))
