import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
a=np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',sys.argv[1],'-ar','16000','-ac','1','-f','s16le','-']),np.int16).astype(np.float32)/32768
m=WhisperModel('small',compute_type='int8')
s,i=m.transcribe(a,language='en',vad_filter=False)
print(i.language,i.language_probability)
for x in s: print(round(x.start,1),round(x.end,1),x.text)
