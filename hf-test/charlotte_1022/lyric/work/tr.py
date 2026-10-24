import subprocess, numpy as np, json, sys
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2)
for f,tag,p in [('01_night_bus_diaries.wav','t1','Night bus diaries, write it down. Glitter in my hair all over town.'),('02_proper_gorgeous.wav','t2','Proper gorgeous, walking in like I\'m a fortress. Can\'t afford this, but I adore this.')]:
    raw=subprocess.run(['ffmpeg','-v','error','-i','/workspace/music/distrokid/charlotte/'+f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.float32)
    segs,_=m.transcribe(a,word_timestamps=True,initial_prompt=p,language='en',vad_filter=False)
    out=[{'s':s.start,'e':s.end,'t':s.text,'w':[(w.start,w.end,w.word) for w in s.words]} for s in segs]
    json.dump(out,open(tag+'.json','w'),indent=0)
    for s in out: print(tag,round(s['s'],1),round(s['e'],1),s['t'])
