import sys,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('medium',compute_type='int8')
s,_=m.transcribe(np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768,vad_filter=False,word_timestamps=True,language='en')
for x in s:
  print(round(x.start,2),round(x.end,2),x.text); print(' '.join('%s@%.2f-%.2f'%(w.word.strip(),w.start,w.end) for w in x.words))
