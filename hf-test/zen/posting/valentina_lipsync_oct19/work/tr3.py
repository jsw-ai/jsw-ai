import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
for name in sys.argv[2:]:
  m=WhisperModel(name,compute_type='int8')
  s,i=m.transcribe(a,language='en',beam_size=5,word_timestamps=True,vad_filter=True,vad_parameters=dict(min_silence_duration_ms=300))
  s=list(s); print(name,' | '.join('%.2f-%.2f %s'%(x.start,x.end,x.text) for x in s))
