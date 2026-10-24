import sys,subprocess,numpy as np
from faster_whisper import WhisperModel
raw=subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32)
m=WhisperModel('medium',compute_type='int8')
s,i=m.transcribe(a,word_timestamps=True,language='en',initial_prompt="Okay, I'm not saying I told you so. Miami woman.")
for x in s: print(x.text,[(w.word,round(w.start,2),round(w.end,2)) for w in x.words])
