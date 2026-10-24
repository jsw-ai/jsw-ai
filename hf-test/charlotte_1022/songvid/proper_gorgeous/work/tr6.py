import subprocess,numpy as np,json
from faster_whisper import WhisperModel
a0=116
raw=subprocess.run(['ffmpeg','-v','quiet','-ss',str(a0),'-t','36','-i','/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32)
m=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
segs,_=m.transcribe(x,language='en',word_timestamps=True,vad_filter=False,initial_prompt="Walk in, heads turn, yeah. Proper gorgeous, proper gorgeous. Walking in like I'm a fortress. Can't afford this, but I adore this.")
W=[]
for s in segs:
    print(round(s.start+a0,2),round(s.end+a0,2),s.text,flush=True)
    for w in s.words: W.append([round(w.start+a0,2),round(w.end+a0,2),w.word])
json.dump(W,open('t6.json','w'))
