import numpy as np, wave, sys
sr=44100
def make(name,bpm,root,seed,prog,dur=24):
    rng=np.random.default_rng(seed); n=int(sr*dur); out=np.zeros(n)
    beat=60/bpm; t=np.arange(n)/sr
    def add(sig,start):
        s=int(start*sr); e=min(n,s+len(sig))
        if s<n: out[s:e]+=sig[:e-s]
    k=np.arange(int(.35*sr))/sr
    kick=np.sin(2*np.pi*(50*np.exp(-k*18)+45)*k*1.0)*np.exp(-k*9)
    kick=np.sin(2*np.pi*np.cumsum(45+90*np.exp(-k*30))/sr)*np.exp(-k*8)
    h=np.arange(int(.08*sr))/sr; hat=rng.standard_normal(len(h))*np.exp(-h*60); hat=np.diff(hat,prepend=0)
    c=np.arange(int(.2*sr))/sr; clap=rng.standard_normal(len(c))*np.exp(-c*25)
    nb=int(dur/beat)
    for b in range(nb):
        tt=b*beat
        if b%4 in (0,2) or b%8==7: add(kick*.9,tt)
        if b%4 in (1,3): add(clap*.35,tt)
        add(hat*.25,tt); add(hat*.18,tt+beat/2)
    for bar in range(int(nb/4)+1):
        ch=prog[bar%len(prog)]
        tt=bar*4*beat
        for q in range(4):
            qs=tt+q*beat
            f=root*2**(ch[0]/12)
            L=int(beat*sr*0.95); x=np.arange(L)/sr
            bass=np.sin(2*np.pi*f/2*x)*np.exp(-x*3)*.5
            add(bass,qs)
            # chords on offbeats
            for off in (0.5,):
                pad=np.zeros(L)
                for iv in ch:
                    ff=root*2**(iv/12)*2
                    pad+=np.sin(2*np.pi*ff*x)+.4*np.sin(4*np.pi*ff*x)
                pad*=np.exp(-x*5)*.07
                add(pad,qs+off*beat)
        # arpeggio
        for q in range(8):
            ff=root*2**(ch[q%len(ch)]/12)*4; L=int(beat/2*sr); x=np.arange(L)/sr
            add(np.sin(2*np.pi*ff*x)*np.exp(-x*9)*.08,tt+q*beat/2)
    # lowpass-ish smoothing
    k2=np.ones(4)/4; out=np.convolve(out,k2,'same')
    out/=np.abs(out).max(); out*=.8
    fade=int(sr*1.0); out[-fade:]*=np.linspace(1,0,fade)
    st=np.stack([out,np.roll(out,40)],1)
    w=wave.open(f'tracks/{name}.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
make('gab_track_120bpm_sunset',120,196,21,[(0,4,7),(9,12,16),(5,9,12),(7,11,14)],dur=16)
make('gab_track_100bpm_soft',100,220,22,[(0,3,7),(8,12,15),(5,8,12),(10,14,17)],dur=16)
