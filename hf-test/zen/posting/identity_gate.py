#!/opt/jsw/.venv/bin/python
"""Identity + basic QA gate for model content.  Verification, not generation.
Usage:
  identity_gate.py img   --model sienna a.png b.jpg ...      (stills)
  identity_gate.py video --model sienna clip.mp4 [--frames N]   (default: every frame)
  options: --json out.json  --log rejects.jsonl  --verbose
Exit code 0 only if every input passes.  Thresholds in THRESH: Hard Rules s4 (10/21) = 0.78 centroid on
every scored face frame, stills and video; frames with no face are skipped (e.g. whip pans).
"""
import sys, os, json, argparse, subprocess, tempfile, time, glob
import numpy as np, cv2
from insightface.app import FaceAnalysis

ROOT = os.environ.get('JSW_REF_ROOT', '/opt/jsw-data/hf-test')  # refs from grok-vm /workspace/hf-test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PACKS = os.environ.get('JSW_PACKS', '/opt/jsw-data/identity_packs.json')
PACK_ALIAS = {'camille': 'camille_v3'}  # camille pack RETIRED 2026-10-21, replaced by camille_v3
THRESH = dict(centroid=0.78, best_ref=0.74, video_centroid=0.78, min_det=0.55, edge_margin=0.02, headroom=0.03,
              min_face_frac=0.06, seedream_centroid=0.78, second_face_ratio=0.25)
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
    packs = json.load(open(PACKS)); pack = packs[PACK_ALIAS.get(model, model)]
    st = str(pack.get('status', ''))
    if st.upper().startswith(('DRAFTED', 'RETIRED')): raise SystemExit(f'{model} pack is {st}: not gateable')
    E = load_embs([p for p in pack['face_refs'] if p not in exclude])
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
    if not video and r['score_best'] < T['best_ref']: r['reasons'].append('identity_best_ref_low')
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

def sample_frames(path, n=0):
    """n=0: every frame (Hard Rules: every scored face frame). n>0: n evenly spaced frames."""
    cap = cv2.VideoCapture(path); tot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); out = []
    if n <= 0:
        i = 0
        while True:
            ok, fr = cap.read()
            if not ok: break
            out.append((i, fr)); i += 1
        return out
    for i in np.linspace(0, max(tot-1, 0), n).astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i)); ok, fr = cap.read()
        if ok: out.append((int(i), fr))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('mode', choices=['img', 'video']); ap.add_argument('--model', required=True)
    ap.add_argument('--frames', type=int, default=0); ap.add_argument('--json'); ap.add_argument('--log'); ap.add_argument('--no-ocr', action='store_true')
    ap.add_argument('--source', choices=['soul', 'seedream', 'other'], default='other'); ap.add_argument('--body', action='store_true', help='add silhouette/pose body check (still images)')
    ap.add_argument('--exclude', nargs='*', default=[]); ap.add_argument('files', nargs='+'); a = ap.parse_args()
    refs, cent = get_refs(a.model, a.exclude); res = {}; ok_all = True
    for p in a.files:
        if a.mode == 'img':
            im = cv2.imread(p)
            r = check_image(im, refs, cent, ocr=not a.no_ocr, source=a.source, body=a.body) if im is not None else dict(pass_=False, reasons=['unreadable'])
        else:
            fr = sample_frames(p, a.frames); rs = [check_image(f, refs, cent, ocr=False, video=True) for _, f in fr]
            scored = [x for x in rs if x['score_centroid'] is not None]; sc = [x['score_centroid'] for x in scored]
            low = sum(s < THRESH['video_centroid'] for s in sc)
            notes = sorted({q for x in scored for q in x['reasons'] if not q.startswith('identity_')})  # framing: info only, as in the 10/22 per-frame gate
            ok = bool(sc) and low == 0
            r = dict(pass_=ok, frames=len(rs), frames_scored=len(sc), frames_no_face=len(rs)-len(sc), frames_below_bar=low,
                     median_centroid=float(np.median(sc)) if sc else None, min_centroid=min(sc) if sc else None,
                     frame_notes=notes, reasons=([] if ok else ['identity_frame_below_0.78'] if sc else ['no_face_frames']))
        res[p] = r; ok_all &= r['pass_']
        print(('PASS ' if r['pass_'] else 'FAIL ') + os.path.basename(p), {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k != 'pass_'})
        if a.log and not r['pass_']:
            open(a.log, 'a').write(json.dumps(dict(ts=time.strftime('%F %T'), model=a.model, file=os.path.abspath(p), **{k: v for k, v in r.items() if k != 'pass_'})) + '\n')
    if a.json: json.dump(res, open(a.json, 'w'), indent=1)
    sys.exit(0 if ok_all else 1)
if __name__ == '__main__': main()
