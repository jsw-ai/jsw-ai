import subprocess, numpy as np, json
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2)
raw=subprocess.run(['ffmpeg','-v','error','-i','/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32)
segs,_=m.transcribe(a,word_timestamps=True,initial_prompt="Proper gorgeous, walking in like I'm a fortress. Can't afford this, but I adore this. Walk in, heads turn, yeah.",language='en',beam_size=1)
out=[]
for s in segs:
    out.append({'s':s.start,'e':s.end,'t':s.text,'w':[(w.start,w.end,w.word) for w in s.words]}); print(round(s.start,1),round(s.end,1),s.text,flush=True)
json.dump(out,open('t2.json','w'),indent=0)
