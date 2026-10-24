import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[1],compute_type='int8')
for f in sys.argv[2:]:
  a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',f,'-vn','-af','highpass=f=80,loudnorm','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
  s,i=m.transcribe(a,language='en',beam_size=5,temperature=0,condition_on_previous_text=False,vad_filter=True)
  print(f,' | '.join('%.2f-%.2f %s'%(x.start,x.end,x.text) for x in s),flush=True)
