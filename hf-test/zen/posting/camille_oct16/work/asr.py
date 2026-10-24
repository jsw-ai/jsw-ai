import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
a=np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',sys.argv[1],'-ar','16000','-ac','1','-f','s16le','-']),np.int16).astype(np.float32)/32768
m=WhisperModel('small',compute_type='int8')
ip=sys.argv[2] if len(sys.argv)>2 else None
for lang in (None,'en','fr'):
    s,i=m.transcribe(a,language=lang,initial_prompt=ip,vad_filter=False,word_timestamps=True)
    print('lang',lang,i.language,round(i.language_probability,2))
    for x in s: print(' ',round(x.start,1),round(x.end,1),x.text)
