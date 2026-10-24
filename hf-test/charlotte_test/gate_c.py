#!/workspace/.face-venv/bin/python
"""Identity + basic QA gate for model content.  Verification, not generation.
Usage:
  identity_gate.py img   --model sienna a.png b.jpg ...      (stills)
  identity_gate.py video --model sienna clip.mp4 [--frames 8]
  options: --json out.json  --log rejects.jsonl  --verbose
Exit code 0 only if every input passes.  Thresholds in THRESH (calibrated, see MODEL_CONTENT_PROCESS.md).
"""
import sys, os, json, argparse, subprocess, tempfile, time, glob
import numpy as np, cv2
from insightface.app import FaceAnalysis

ROOT = '/workspace/hf-test'
sys.path.insert(0,'/workspace/hf-test/zen/posting')
PACKS = '/workspace/hf-test/charlotte_test/gate_pack.json'
THRESH = dict(centroid=0.72, best_ref=0.74, video_centroid=0.55, video_best_ref=0.52, video_median=0.58, video_floor=0.50, min_det=0.55, edge_margin=0.02, headroom=0.03,
              min_face_frac=0.06, seedream_centroid=0.78, second_face_ratio=0.25, video_pass_frac=0.80)
_app = None
def app():
    global _app
    if _app is None:
        _app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        _app.prepare(ctx_id=-1, det_size=(640, 640))
    return _app

def faces(im):
    """Robust detection: downscale big images, retry with padding for huge close-up faces."""
    h, w = im.shape[:2]; s = 1.0
    if max(h, w) > 1280: s = 1280 / max(h, w); im = cv2.resize(im, (int(w*s), int(h*s)))
    f = app().get(im); off = (0, 0); H, W = im.shape[:2]
    if not f:
        px, py = W//2, H//2
        pad = cv2.copyMakeBorder(im, py, py, px, px, cv2.BORDER_CONSTANT, value=(127, 127, 127))
        f = app().get(pad); off = (px, py)
        if f:
            for x in f: x.bbox = x.bbox - np.array([px, py, px, py]); x.kps = x.kps - np.array([px, py])
    return f, (W, H)

def load_embs(paths):
    out = []
    for p in paths:
        im = cv2.imread(os.path.join(ROOT, p) if not os.path.isabs(p) else p)
        if im is None: continue
        f, _ = faces(im)
        if f: out.append(max(f, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding)
    return np.array(out)

def get_refs(model, exclude=()):
    packs = json.load(open(PACKS)); E = load_embs([p for p in packs[model]['face_refs'] if p not in exclude])
    if len(E) == 0: raise SystemExit(f'no usable face refs for {model}')
    c = E.mean(0); c /= np.linalg.norm(c); return E, c

def ocr_text(im):
    try:
        from rapidocr_onnxruntime import RapidOCR
        r, _ = RapidOCR()(im)
        return [t[1] for t in (r or []) if float(t[2]) > 0.75 and len(t[1].strip()) >= 4]
    except Exception: return []

def check_image(im, refs, cent, T=THRESH, ocr=True, video=False, source=None, body=False):
    r = dict(pass_=False, reasons=[], score_centroid=None, score_best=None)
    f, (W, H) = faces(im)
    f = [x for x in f if x.det_score >= T['min_det']]
    if not f: r['reasons'].append('no_face_detected'); return r
    f.sort(key=lambda x: -(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    a = lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])
    if len(f) > 1 and a(f[1]) > T['second_face_ratio']*a(f[0]): r['reasons'].append('multiple_people')
    m = f[0]; x0, y0, x1, y1 = m.bbox
    mx, my = T['edge_margin']*W, T['edge_margin']*H
    if x0 < mx or x1 > W-mx or y1 > H-my: r['reasons'].append('face_cut_by_frame')
    if y0 < T['headroom']*H: r['reasons'].append('no_headroom_top_cropped')
    if (y1-y0)/H < T['min_face_frac']: r['reasons'].append('face_too_small')
    sims = refs @ m.normed_embedding
    r['score_centroid'] = float(cent @ m.normed_embedding); r['score_best'] = float(sims.max())
    if source == 'seedream' and r['score_centroid'] < T['seedream_centroid']: r['reasons'].append('identity_centroid_low_seedream')  # per-source: Seedream copies one ref's face; see §0c
    if r['score_centroid'] < T['video_centroid' if video else 'centroid']: r['reasons'].append('identity_centroid_low')
    if r['score_best'] < T['video_best_ref' if video else 'best_ref']: r['reasons'].append('identity_best_ref_low')
    if body:
        import body_check as bc
        b = bc.verdict(bc.measure(im))
        r['body'] = {k: v for k, v in b.items() if k != 'pass_'}; r['body_pass'] = b['pass_']; r['body_measurable'] = b['measurable']
        r['reasons'] += [x for x in b['reasons'] if not x.startswith('body_unmeasurable')]
        r['visual_check_required'] = 'MANDATORY visual body+face check vs approved body refs (numeric body check is a coarse proxy)'
    if ocr:
        t = ocr_text(im)
        if t: r['reasons'].append('text_in_image:' + '|'.join(t)[:60])
    r['pass_'] = not r['reasons']; return r

def sample_frames(path, n):
    d = tempfile.mkdtemp(); cap = cv2.VideoCapture(path); tot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); out = []
    for i in np.linspace(0, max(tot-1, 0), n).astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i)); ok, fr = cap.read()
        if ok: out.append((int(i), fr))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('mode', choices=['img', 'video']); ap.add_argument('--model', required=True)
    ap.add_argument('--frames', type=int, default=8); ap.add_argument('--json'); ap.add_argument('--log'); ap.add_argument('--no-ocr', action='store_true')
    ap.add_argument('--source', choices=['soul', 'seedream', 'other'], default='other'); ap.add_argument('--body', action='store_true', help='add silhouette/pose body check (still images)')
    ap.add_argument('--exclude', nargs='*', default=[]); ap.add_argument('files', nargs='+'); a = ap.parse_args()
    refs, cent = get_refs(a.model, a.exclude); res = {}; ok_all = True
    for p in a.files:
        if a.mode == 'img':
            im = cv2.imread(p)
            r = check_image(im, refs, cent, ocr=not a.no_ocr, source=a.source, body=a.body) if im is not None else dict(pass_=False, reasons=['unreadable'])
        else:
            fr = sample_frames(p, a.frames); rs = [check_image(f, refs, cent, ocr=False, video=True) for _, f in fr]
            sc = [x['score_centroid'] for x in rs if x['score_centroid'] is not None]
            frac = sum(x['pass_'] for x in rs)/max(len(rs), 1); reasons = sorted({q for x in rs for q in x['reasons']})
            floor_bad = bool(sc) and (min(sc) < THRESH['video_floor'] or float(np.median(sc)) < THRESH['video_median'])
            ok = frac >= THRESH['video_pass_frac'] and not floor_bad and len(rs) > 0
            r = dict(pass_=ok, frames=len(rs), frame_pass_frac=frac, min_centroid=min(sc) if sc else None, reasons=([] if ok else reasons or ['video_frames_fail']))
        res[p] = r; ok_all &= r['pass_']
        print(('PASS ' if r['pass_'] else 'FAIL ') + os.path.basename(p), {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k != 'pass_'})
        if a.log and not r['pass_']:
            open(a.log, 'a').write(json.dumps(dict(ts=time.strftime('%F %T'), model=a.model, file=os.path.abspath(p), **{k: v for k, v in r.items() if k != 'pass_'})) + '\n')
    if a.json: json.dump(res, open(a.json, 'w'), indent=1)
    sys.exit(0 if ok_all else 1)
if __name__ == '__main__': main()
