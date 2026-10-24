import numpy as np,subprocess,sys
def env(f):
    sr=22050;a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(sr),'-f','s16le','-']),np.int16).astype(float)
    h=512;n=len(a)//h;fr=a[:n*h].reshape(n,h);e=np.log1p(np.abs(np.fft.rfft(fr*np.hanning(h),axis=1)))
    o=np.maximum(0,np.diff(e,axis=0)).sum(1);o=o-np.convolve(o,np.ones(16)/16,'same');return np.maximum(o,0),sr/h,len(a)/sr
def tempo(f):
    o,fps,d=env(f);ac=np.correlate(o,o,'full')[len(o)-1:]
    lags=np.arange(int(fps*60/170),int(fps*60/85));L=lags[np.argmax(ac[lags])];bpm=60*fps/L
    per=60/bpm;best=max(np.arange(0,per,0.01),key=lambda p:sum(o[int((p+k*per)*fps)] for k in range(int((d-p)/per)) if int((p+k*per)*fps)<len(o)))
    return bpm,best,d
if __name__=='__main__':
    for f in sys.argv[1:]: print(f,'bpm %.1f phase %.2f dur %.1f'%tempo(f))
