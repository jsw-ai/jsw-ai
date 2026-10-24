from faster_whisper import WhisperModel
import json,subprocess,numpy as np
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-ss","8","-t","24","-i","/workspace/music/distrokid/sienna/02_low_tide_lover.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(a,word_timestamps=True,language="en",vad_filter=False,condition_on_previous_text=False)
out=[[round(w.start+8,2),round(w.end+8,2),w.word] for s in segs for w in s.words]
json.dump(out,open("words_intro.json","w")); print(out)
