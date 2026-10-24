import sys,wave,numpy as np
from faster_whisper import WhisperModel
w=wave.open(sys.argv[1]);a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
m=WhisperModel('base',compute_type='int8')
s,i=m.transcribe(a,word_timestamps=True,language=None)
print(i.language)
for x in s: print(x.text,[(w.word,round(w.start,2),round(w.end,2)) for w in x.words])
