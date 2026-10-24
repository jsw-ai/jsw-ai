import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("small",compute_type="int8")
import wave,numpy as np;W=wave.open(sys.argv[1]);a=np.frombuffer(W.readframes(W.getnframes()),np.int16).astype(np.float32)/32768;s,_=m.transcribe(a,word_timestamps=True,language="en")
out=[]
for seg in s:
  print(f"{seg.start:6.2f}-{seg.end:6.2f} {seg.text}")
  out+= [dict(w=w.word,s=w.start,e=w.end) for w in seg.words]
json.dump(out,open(sys.argv[2],'w'))
