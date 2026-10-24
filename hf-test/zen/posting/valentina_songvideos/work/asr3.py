from faster_whisper import WhisperModel
import json,subprocess,numpy as np
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-ss","0","-t","80","-i","/workspace/music/distrokid/valentina/02_fuego_lento.wav","-af","highpass=f=150,lowpass=f=6000","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe(a,word_timestamps=True,vad_filter=True,initial_prompt="Lights down low and the bass hits deep. Poquito a poco, más lento. Fuego lento, slow fire.")
out=[[w.start,w.end,w.word] for s in segs for w in s.words]
json.dump(out,open("words3.json","w")); print(info.language,len(out)); print(''.join(x for _,_,x in out))
