import numpy as np,subprocess,sys
def load(p): return np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',p,'-ar','16000','-ac','1','-f','s16le','-']),np.int16).astype(float)/32768
def f0(x):
    out=[];sp=[]
    for i in range(0,len(x)-800,320):
        fr=x[i:i+800]
        if np.sqrt((fr**2).mean())<0.02: continue
        fr=fr-fr.mean(); ac=np.correlate(fr,fr,'full')[799:]
        lo,hi=int(16000/350),int(16000/70); k=ac[lo:hi].argmax()+lo
        if ac[k]/ac[0]>0.4: out.append(16000/k)
        S=np.abs(np.fft.rfft(fr*np.hanning(800))); sp.append((S*np.arange(len(S))*20).sum()/S.sum())
    return np.median(out),np.percentile(out,[10,90]),np.median(sp)
for p in sys.argv[1:]: print(p.split('/')[-1],f0(load(p)))
