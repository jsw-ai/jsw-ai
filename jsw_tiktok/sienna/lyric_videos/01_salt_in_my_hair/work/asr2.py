from faster_whisper import WhisperModel
import json,subprocess,numpy as np
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","/workspace/music/distrokid/sienna/01_salt_in_my_hair.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(a,word_timestamps=True,language="en",initial_prompt=open("lyrics.txt").read()[:800],condition_on_previous_text=False)
out=[[w.start,w.end,w.word] for s in segs for w in s.words]
json.dump(out,open("words_med.json","w")); print(len(out))
