# Video adaptation of finish_v4C.py: per-frame skin texture transfer (0.5) on YCrCb skin mask w/ edge protection,
# sharpen 0.3, luma grain sigma 3 (new seed per frame), matte highlight tame. Light, natural only.
import sys, numpy as np, cv2, subprocess
src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5)
W, H = 720, 1280
p = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-',
     '-c:v','libx264','-crf','12','-preset','slow','-pix_fmt','yuv420p',dst], stdin=subprocess.PIPE)
k = 0
def gb(x, s): return cv2.GaussianBlur(x, (0, 0), s)
while True:
    ok, fr = cap.read()
    if not ok: break
    fr = cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA) if fr.shape[:2] != (H, W) else fr
    a = fr.astype(np.float32)
    ycc = cv2.cvtColor(fr, cv2.COLOR_BGR2YCrCb).astype(np.float32); Y, Cr, Cb = ycc[...,0], ycc[...,1], ycc[...,2]
    m = ((Cr>135)&(Cr<180)&(Cb>80)&(Cb<130)&(Y>60)).astype(np.float32); m = gb(m, 5)
    e = gb(np.abs(Y-gb(Y, 2)), 3); prot = np.clip(1-(e-4)/6, 0, 1); mask = m*prot
    rt = np.random.default_rng(7)
    n = gb(rt.normal(0, 40, Y.shape).astype(np.float32), 0.9)*0.18 + gb(rt.normal(0, 40, Y.shape).astype(np.float32), 4)*0.10
    rng = np.random.default_rng(100 + k)
    Yt = Y + n*(0.6+0.4*Y/255) - np.clip((Y-200)/55, 0, 1)*m*14
    hp = np.clip(Yt-gb(Yt, 1.6), -6, 6); lo = np.clip(gb(Yt, 6)-gb(Y, 6), -8, 4)
    b = a + ((hp+lo*0.5)*mask*0.5)[..., None]
    b = b + (b-gb(b, 1.0))*0.3
    b = b + gb(rng.normal(0, 3.0, Y.shape).astype(np.float32), 0.4)[..., None]
    p.stdin.write(np.clip(b, 0, 255).astype(np.uint8).tobytes()); k += 1
p.stdin.close(); p.wait(); print('frames', k, 'fps', fps)
