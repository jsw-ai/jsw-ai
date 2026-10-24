# Original procedural instrumentals (no samples, no vocals). synth.py name bpm bars style
import numpy as np, sys, scipy.signal as ss, scipy.io.wavfile as wf
name,bpm,bars,style=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
SR=44100; beat=60/bpm; N=int(SR*beat*4*bars); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(3)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*g*(1-pan)/1; R[i:i+n]+=sig[:n]*g*(1+pan)/1
def env(n,a,d): t=np.arange(n)/SR; e=np.minimum(t/a,1)*np.exp(-t/d); return e
def kick():
    n=int(.4*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7)*1.0
def hat(o=False):
    n=int((.18 if o else .05)*SR); x=rng.normal(0,1,n); b,a=ss.butter(4,7000/(SR/2),'high'); return ss.lfilter(b,a,x)*env(n,.001,.06 if o else .015)*.25
def clap():
    n=int(.25*SR); x=rng.normal(0,1,n); b,a=ss.butter(2,[900/(SR/2),3000/(SR/2)],'band'); return ss.lfilter(b,a,x)*env(n,.002,.08)*.5
def nf(m): return 440*2**((m-69)/12)
def keys(notes,dur,bright):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for m in notes:
        f=nf(m); s+=np.sin(2*np.pi*f*t+0.6*np.sin(2*np.pi*f*t)*np.exp(-t*3))*0.9+0.25*np.sin(4*np.pi*f*t)*np.exp(-t*4)
    e=np.minimum(t/.01,1)*np.exp(-t/(dur*0.6 if bright<1 else dur*0.35)); s=s*e/len(notes)
    b,a=ss.butter(2,(2500 if bright<1 else 4000)/(SR/2)); return ss.lfilter(b,a,s)*.55
def bass(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; f=nf(m); s=ss.sawtooth(2*np.pi*f*t)*0.6+np.sin(2*np.pi*f*t)
    b,a=ss.butter(2,400/(SR/2)); return ss.lfilter(b,a,s)*np.minimum(t/.005,1)*np.exp(-t/(dur*.8))*.45
# progression: Fmaj9 - Em7 - Dm9 - Cmaj7 (Riviera-ish), one chord per bar
prog=[([53,57,60,64,67],41),([52,55,59,62],40),([50,53,57,60,64],38),([48,52,55,59],36)]
for bar in range(bars):
    ch,root=prog[bar%4]; t0=bar*4*beat
    for b4 in range(4):
        tb=t0+b4*beat
        if not (style=='lounge' and bar==0 and b4<2): add(kick(),tb,0,0.9 if style=='house' else 0.7)
        add(hat(True),tb+beat/2,0.3,1.0 if style=='house' else 0.6)
        if style=='house': add(hat(),tb+beat/4,-0.3); add(hat(),tb+3*beat/4,-0.3)
        if b4 in (1,3): add(clap(),tb,0,0.8 if style=='house' else 0.45)
        # bass offbeat pumping
        add(bass(root,beat*0.45),tb+beat/2,0,1.0)
    if style=='house':
        for s16 in (0,3,6,10,12):  # syncopated chord stabs
            add(keys(ch,beat*0.5,1),t0+s16*beat/4,0.15*((s16%2)*2-1),0.9)
    else:
        add(keys(ch,beat*3.5,0.5),t0,0,1.1); add(keys([n+12 for n in ch[:2]],beat*1,0.5),t0+2.5*beat,0.4,0.5)
# sidechain pump
t=np.arange(N)/SR; ph=(t%beat)/beat; pump=0.55+0.45*np.minimum(ph/0.35,1)
mix=np.stack([L,R],1); mix[:,0]*=pump; mix[:,1]*=pump
# simple room reverb (multi-tap)
rev=np.zeros_like(mix)
for d,g in ((0.031,.3),(0.047,.25),(0.071,.2),(0.113,.15),(0.17,.1)):
    k=int(d*SR); rev[k:]+=mix[:-k][:,::-1]*g
mix=mix+rev*0.6; mix=np.tanh(mix/np.abs(mix).max()*1.6)*0.85
wf.write(f'{name}.wav',SR,(mix*32767).astype(np.int16)); print(name,N/SR)
