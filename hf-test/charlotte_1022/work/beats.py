import sys, librosa, numpy as np, json
out={}
for name in sys.argv[1:]:
    y,sr=librosa.load(f'/workspace/music/charlotte/mp3/{name}.mp3',sr=22050,mono=True)
    tempo,beats=librosa.beat.beat_track(y=y,sr=sr); bt=librosa.frames_to_time(beats,sr=sr)
    rms=librosa.feature.rms(y=y)[0]; t=librosa.frames_to_time(np.arange(len(rms)),sr=sr)
    # loudest 12 s window starting on a beat, after 20 s
    best=None
    for b in bt:
        if b<20 or b+12>t[-1]: continue
        m=rms[(t>=b)&(t<b+12)].mean()
        if best is None or m>best[1]: best=(b,m)
    out[name]={'tempo':float(np.atleast_1d(tempo)[0]),'start':float(best[0]),'beats':[float(x) for x in bt if best[0]<=x<best[0]+14]}
    print(name, out[name]['tempo'], out[name]['start'])
json.dump(out,open('beats.json','w'))
