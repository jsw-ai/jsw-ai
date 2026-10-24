import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
for sz in ['small','medium']:
    m=WhisperModel(sz,compute_type='int8')
    s,i=m.transcribe(a,language='en',word_timestamps=True,initial_prompt="Hiya. British woman chatting.")
    print(sz,[(w.word,round(w.start,2)) for x in s for w in x.words])
