from faster_whisper import WhisperModel
import json,subprocess,numpy as np,os
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","/workspace/music/distrokid/sienna/02_low_tide_lover.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
rows=json.load(open("../timings.json")); fn="asr5.jsonl"
done={json.loads(l)['i'] for l in open(fn)} if os.path.exists(fn) else set()
for i,(s,e,t) in enumerate(rows):
  if i in done: continue
  o=max(0,s-0.5); seg=a[int(o*16000):int((e+0.5)*16000)]
  ss,_=m.transcribe(seg,language="en",beam_size=5,condition_on_previous_text=False,word_timestamps=True,vad_filter=False,no_speech_threshold=None,log_prob_threshold=None,compression_ratio_threshold=None)
  ws=[(round(w.start+o,2),w.word,round(w.probability,2)) for x in ss for w in x.words]
  open(fn,"a").write(json.dumps({"i":i,"s":s,"lyric":t,"asr":''.join(w[1] for w in ws),"words":ws})+"\n"); print(i,flush=True)
