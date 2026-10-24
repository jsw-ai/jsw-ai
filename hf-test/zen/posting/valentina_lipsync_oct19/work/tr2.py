import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
m=WhisperModel(sys.argv[2] if len(sys.argv)>2 else 'medium',compute_type='int8')
s,i=m.transcribe(a,language='en',word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
for x in s:
    print(' '.join('%s@%.1f'%(w.word.strip(),w.start) for w in x.words))
