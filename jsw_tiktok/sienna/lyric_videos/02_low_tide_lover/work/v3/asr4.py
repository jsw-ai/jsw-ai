from faster_whisper import WhisperModel
import json,subprocess,numpy as np,os,sys
mname=sys.argv[1]
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","/workspace/music/distrokid/sienna/02_low_tide_lover.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel(mname,device="cpu",compute_type="int8",cpu_threads=4)
fn=f"asr4_{mname}.jsonl"; done=set()
if os.path.exists(fn): done={json.loads(l)['t0'] for l in open(fn)}
for t0 in range(8,150,12):
  if t0 in done: continue
  seg=a[t0*16000:(t0+16)*16000]
  ss,_=m.transcribe(seg,language="en",beam_size=5,condition_on_previous_text=False,word_timestamps=True,vad_filter=False)
  ws=[(round(w.start+t0,2),round(w.end+t0,2),w.word,round(w.probability,2)) for x in ss for w in x.words]
  open(fn,"a").write(json.dumps({"t0":t0,"words":ws})+"\n"); print(t0,''.join(w[2] for w in ws),flush=True)
