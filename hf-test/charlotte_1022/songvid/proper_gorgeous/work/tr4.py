import subprocess,numpy as np,json
from faster_whisper import WhisperModel
raw=subprocess.run(['ffmpeg','-v','quiet','-i','/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=3)
P="Mirror in the loo, I'm checking my face. Lashes on point. Walk in, heads turn, yeah. Proper gorgeous, proper gorgeous. Walking in like I'm a fortress. Can't afford this, but I adore this. Oi, oi, look at her go."
segs,_=m.transcribe(x,language='en',word_timestamps=True,initial_prompt=P,condition_on_previous_text=False)
W=[]
for s in segs:
    print(round(s.start,2),round(s.end,2),s.text,flush=True)
    for w in s.words: W.append([round(float(w.start),2),round(float(w.end),2),w.word])
json.dump(W,open('t4.json','w'))
