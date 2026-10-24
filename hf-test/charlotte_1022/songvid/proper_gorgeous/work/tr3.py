import subprocess,numpy as np,json
from faster_whisper import WhisperModel
a0=95
raw=subprocess.run(['ffmpeg','-v','quiet','-ss',str(a0),'-t','72','-i','/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2)
segs,_=m.transcribe(x,language='en',word_timestamps=True,vad_filter=False)
W=[]
for s in segs:
    for w in s.words: W.append([round(w.start+a0,2),round(w.end+a0,2),w.word]); print(W[-1],flush=True)
json.dump(W,open('t3.json','w'))
