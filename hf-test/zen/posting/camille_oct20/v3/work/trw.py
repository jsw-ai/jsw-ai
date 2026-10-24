import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
m=WhisperModel('small',compute_type='float32')
for f in sys.argv[1:]:
  a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',f,'-vn','-af','highpass=f=80,loudnorm','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
  s,i=m.transcribe(a,language='en',beam_size=5,temperature=0,condition_on_previous_text=False,vad_filter=True,word_timestamps=True)
  print(f); [print(' '.join('%.2f:%s'%(w.start,w.word) for w in x.words)) for x in s]
