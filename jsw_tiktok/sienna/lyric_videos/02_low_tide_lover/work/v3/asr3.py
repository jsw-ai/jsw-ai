from faster_whisper import WhisperModel
import json,subprocess,numpy as np
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","/workspace/music/distrokid/sienna/02_low_tide_lover.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=8)
rows=json.load(open("../timings.json"))
out=[]
for s,e,t in rows:
  seg=a[int(max(0,s-0.6)*16000):int((e+0.6)*16000)]
  r=[]
  for beam in (5,):
    ss,_=m.transcribe(seg,language="en",beam_size=beam,condition_on_previous_text=False,word_timestamps=True,vad_filter=False)
    ws=[(round(w.start+s-0.6,2),w.word,round(w.probability,2)) for x in ss for w in x.words]
  out.append([s,t,''.join(w[1] for w in ws),ws]); print(f"{s:7.2f} | {t}\n        > {''.join(w[1] for w in ws)}",flush=True)
json.dump(out,open("asr3.json","w"))
