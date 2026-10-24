import sys,subprocess,numpy as np,json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="float32")
for f,prompt in [(sys.argv[1],"Salt in my hair, sun on my skin. Ocean keeps calling, I keep diving in. And the wind's turning offshore."),(sys.argv[2],"Catching a flight to Bali. Sarong and a coconut, sorry, I'm free. Clouds below like whitewash foam.")]:
    raw=subprocess.run(["ffmpeg","-v","quiet","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(a,language="en",vad_filter=False,initial_prompt=prompt,condition_on_previous_text=False)
    out=[(round(s.start,1),round(s.end,1),s.text.strip()) for s in segs]
    json.dump(out,open(f.split('/')[-1]+'.v2.json','w'),indent=0)
    print(f,flush=True)
