import numpy as np, wave, subprocess, os
sr=44100; bpm=120; dur=14.0
t=np.arange(int(sr*dur))/sr; a=np.zeros_like(t)
beat=60/bpm
rng=np.random.default_rng(1)
for i in range(int(dur/beat)):
    s=int(i*beat*sr); n=int(0.25*sr); tt=np.arange(n)/sr
    k=np.sin(2*np.pi*(50+90*np.exp(-tt*30))*tt)*np.exp(-tt*12)
    a[s:s+n]+=0.7*k[:len(a[s:s+n])]
    h=int((i*beat+beat/2)*sr); n=int(0.05*sr)
    a[h:h+n]+=0.12*rng.standard_normal(n)[:len(a[h:h+n])]*np.exp(-np.arange(n)/sr*80)[:len(a[h:h+n])]
    if i%2==1:
        n=int(0.12*sr); sn=rng.standard_normal(n)*np.exp(-np.arange(n)/sr*30)
        a[s:s+n]+=0.25*sn[:len(a[s:s+n])]
for f,g in [(220,.06),(277.2,.05),(329.6,.05)]:
    a+=g*np.sin(2*np.pi*f*t)*(0.7+0.3*np.sin(2*np.pi*t/beat/4))
a*=np.minimum(1,(dur-t)/0.4); a=a/np.max(np.abs(a))*0.8
w=wave.open('beat.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
w.writeframes((a*32767).astype(np.int16).tobytes());w.close()
