from faster_whisper import WhisperModel
import json,subprocess,numpy as np
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","/workspace/music/distrokid/valentina/02_fuego_lento.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=2)
segs,_=m.transcribe(a,word_timestamps=True,language="en",vad_filter=False,condition_on_previous_text=False)
out=[[w.start,w.end,w.word] for s in segs for w in s.words]
json.dump(out,open("words.json","w")); print(len(out))
