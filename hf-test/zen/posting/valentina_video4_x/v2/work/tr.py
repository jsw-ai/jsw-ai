import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
m=WhisperModel('medium',compute_type='int8')
s,i=m.transcribe(a,language='en',word_timestamps=True,vad_filter=False,initial_prompt="Miami woman flirting.")
for x in s:
    print(round(x.start,1),round(x.end,1),x.text)
