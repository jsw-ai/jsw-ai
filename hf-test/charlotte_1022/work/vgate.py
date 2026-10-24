# usage: vgate.py video fps outjson  -> per-frame centroid scores
import sys,subprocess,os,json,glob,tempfile
v,fps,out=sys.argv[1],sys.argv[2],sys.argv[3]
d=out+'_frames'; os.makedirs(d,exist_ok=True)
for f in glob.glob(d+'/*'): os.remove(f)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',v,'-vf',f'fps={fps}','-q:v','2',d+'/f%04d.jpg'],check=True)
fs=sorted(glob.glob(d+'/*.jpg'))
subprocess.run(['/workspace/.face-venv/bin/python','/workspace/hf-test/zen/posting/identity_gate.py','img','--model','charlotte','--source','seedream','--no-ocr','--json',out]+fs,capture_output=True)
g=json.load(open(out)); sc=[]
for f in fs:
    k=[x for kk,x in g.items() if kk.endswith(os.path.basename(f))]
    s=k[0].get('score_centroid') if k else None
    sc.append(s)
vals=[s for s in sc if s is not None]
import statistics
print(os.path.basename(v),'n=%d scored=%d median=%.3f min=%.3f below70=%d below78=%d'%(len(sc),len(vals),statistics.median(vals),min(vals),sum(s<0.70 for s in vals),sum(s<0.78 for s in vals)))
print(' '.join('%.2f'%s if s is not None else '--' for s in sc))
json.dump({'scores':sc},open(out.replace('.json','_scores.json'),'w'))
