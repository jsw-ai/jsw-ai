import sys,subprocess,numpy as np,json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="float32")
for f in sys.argv[1:]:
    raw=subprocess.run(["ffmpeg","-v","quiet","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(a,language="en",vad_filter=True)
    out=[(round(s.start,1),round(s.end,1),s.text.strip()) for s in segs]
    name=f.split('/')[-1]
    json.dump(out,open(name+'.json','w'),indent=0)
    print(name,flush=True)
