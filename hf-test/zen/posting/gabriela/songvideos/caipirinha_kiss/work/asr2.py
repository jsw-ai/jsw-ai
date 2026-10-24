from faster_whisper import WhisperModel
import json,subprocess,numpy as np
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-ss","40","-t","32","-i","/workspace/music/distrokid/gabriela/05_caipirinha_kiss.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(a,word_timestamps=True,language="en",condition_on_previous_text=False)
out=[[w.start+40,w.end+40,w.word] for s in segs for w in s.words]
json.dump(out,open("words2.json","w")); print(len(out))
