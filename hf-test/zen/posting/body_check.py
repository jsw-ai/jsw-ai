#!/workspace/.face-venv/bin/python
"""Body-proportion check (proxy, NOT a substitute for the visual check). RTMPose-m keypoints (rtmlib) + u2net_human_seg silhouette.
Measures silhouette widths along the shoulder->hip axis, normalised by torso length T.  See MODEL_CONTENT_PROCESS.md §0c."""
import os, sys, json, numpy as np, cv2, onnxruntime as ort
_sess = None; _body = None
SEG = '/workspace/models/u2net_human_seg.onnx'
def _models():
    global _sess, _body
    if _body is None:
        from rtmlib import Body
        _body = Body(mode='balanced', backend='onnxruntime', device='cpu', to_openpose=False)
        _sess = ort.InferenceSession(SEG, providers=['CPUExecutionProvider'])
    return _body, _sess
def seg_mask(im):
    _, s = _models(); h, w = im.shape[:2]
    x = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2RGB), (320, 320)).astype(np.float32) / 255.
    x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
    o = s.run(None, {s.get_inputs()[0].name: x})[0][0, 0]; o = (o - o.min()) / (o.max() - o.min() + 1e-8)
    return cv2.resize(o, (w, h)) > 0.5
def span(m, y, cx):
    y = int(np.clip(y, 0, m.shape[0]-1)); row = m[y]; x = int(np.clip(cx, 0, len(row)-1))
    if not row[x]: return 0.0
    a = x
    while a > 0 and row[a-1]: a -= 1
    b = x
    while b < len(row)-1 and row[b+1]: b += 1
    return float(b-a+1)
def measure(im, face_h=None):
    """Features in units of FACE HEIGHT (buffalo bbox height; pass face_h, else measured here via identity_gate.faces).
    Returns dict; keys missing/None = not measurable in this framing."""
    body, _ = _models(); h, w = im.shape[:2]
    if max(h, w) > 1280: s = 1280/max(h, w); im = cv2.resize(im, (int(w*s), int(h*s))); h, w = im.shape[:2]; face_h = face_h*s if face_h else None
    if face_h is None:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import identity_gate as g
        fc, _ = g.faces(im)
        if not fc: return dict(error='no_face_for_scale')
        m0 = max(fc, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); face_h = float(m0.bbox[3]-m0.bbox[1])
    k, sc = body(im)
    if len(k) == 0: return dict(error='no_person')
    i = int(np.argmax(sc.mean(1))); k, sc = k[i], sc[i]
    if min(sc[5], sc[6]) < 0.4: return dict(error='shoulders_not_visible')
    S = (k[5]+k[6])/2; hips_ok = min(sc[11], sc[12]) > 0.4 and max(k[11][1], k[12][1]) < h
    m = seg_mask(im); U = face_h; d = dict(error=None, sh_w=float(abs(k[5][0]-k[6][0])/U))
    # upper-torso silhouette width: widest row between 15% and 45% of the way shoulder->hip (hips ok) or shoulder line +0..0.9 face heights
    if hips_ok:
        H = (k[11]+k[12])/2; ys = [(S + f*(H-S)) for f in (0.15, 0.25, 0.35, 0.45)]
        d['torso_T_face'] = float(np.linalg.norm(S-H)/U)
    else: ys = [S + np.array([0, f*U]) for f in (0.3, 0.6, 0.9)]
    d['bust_w'] = float(max(span(m, q[1], q[0]) for q in ys)/U)
    d['mask_sh'] = float(span(m, S[1]+0.15*U, S[0])/U / max(d['sh_w'], 1e-6))   # silhouette width just below shoulder line / shoulder keypoint width (mask sanity)
    if hips_ok:
        for n, a, b, fr in (('thigh_w', 11, 13, 0.4),):
            v = [span(m, (k[a+j]+fr*(k[b+j]-k[a+j]))[1], (k[a+j]+fr*(k[b+j]-k[a+j]))[0])/U for j in (0, 1) if min(sc[a+j], sc[b+j]) > 0.4]
            d[n] = float(np.mean(v)) if v else None
    return d
# calibration (face-height units), see MODEL_CONTENT_PROCESS.md §0c
BT = dict(bust_w_min=1.40, thigh_w_min=0.90, max_yaw_sh=0.90, min_sh=0.60, min_mask_sh=1.05)
def verdict(d, T=BT):
    r = dict(measurable=False, reasons=[], pass_=True, **{k: (round(v, 2) if isinstance(v, float) else v) for k, v in d.items() if k != 'error'})
    if d.get('error'): r['reasons'].append('body_unmeasurable:' + d['error']); return r
    if d['sh_w'] < T['min_sh'] or d['mask_sh'] < T['min_mask_sh']: r['reasons'].append('body_unmeasurable:pose_or_mask_unreliable'); return r
    if d['sh_w'] < T['max_yaw_sh']: r['reasons'].append('body_slim_or_turned:shoulder_width_%.2f' % d['sh_w']); r['pass_'] = False
    if d.get('bust_w') is not None and d['bust_w'] < T['bust_w_min']: r['reasons'].append('body_bust_width_low:%.2f<%.2f' % (d['bust_w'], T['bust_w_min'])); r['pass_'] = False
    if d.get('thigh_w') is not None and d['thigh_w'] < T['thigh_w_min']: r['reasons'].append('body_thigh_thin:%.2f<%.2f' % (d['thigh_w'], T['thigh_w_min'])); r['pass_'] = False
    r['measurable'] = True; return r
if __name__ == '__main__':
    for p in sys.argv[1:]:
        r = verdict(measure(cv2.imread(p))); print(('PASS ' if r['pass_'] else 'FAIL ') + os.path.basename(p)[:24].ljust(24), {k: v for k, v in r.items() if k != 'pass_'})
