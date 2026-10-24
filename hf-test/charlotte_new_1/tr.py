import sys,numpy as np,subprocess
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv.pop(1),compute_type='int8')
for f in sys.argv[1:]:
    a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',f,'-vn','-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
    s,i=m.transcribe(a,language='en',vad_filter=False)
    print(f,[ (round(x.start,1),round(x.end,1),x.text) for x in s],flush=True)
