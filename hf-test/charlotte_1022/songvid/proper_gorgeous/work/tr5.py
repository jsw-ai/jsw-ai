import subprocess,numpy as np,json
from faster_whisper import WhisperModel
raw=subprocess.run(['ffmpeg','-v','quiet','-ss','28','-t','40','-i','/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav','-af','highpass=f=200,lowpass=f=4000','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32)
m=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2)
segs,_=m.transcribe(x,language='en',word_timestamps=True,condition_on_previous_text=False,vad_filter=False,no_speech_threshold=0.9)
W=[]
for s in segs:
    print(round(s.start+28,2),round(s.end+28,2),s.text,flush=True)
    for w in s.words: W.append([round(float(w.start)+28,2),round(float(w.end)+28,2),w.word])
json.dump(W,open('t5.json','w'))
