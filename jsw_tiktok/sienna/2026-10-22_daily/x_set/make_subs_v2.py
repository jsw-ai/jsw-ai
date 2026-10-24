import json,re,hashlib,os,shutil,subprocess
D='/workspace/jsw_tiktok/sienna/2026-10-22_daily'; os.chdir(D)
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def g(p):
    t=open(p).read(); m=re.search(r"^(PASS|FAIL) \S+ (\{.*\})$",t,re.M); return m.group(1),eval(m.group(2))
APPLE='https://music.apple.com/us/album/salt-in-my-hair/6825685962'
CRED="""Higgsfield credits today (from credits.txt): Seedream stills A/B/B2/B3 30, X stills xs1-xs7 52.5, Kling k1-k5 37.5 -> 120.0 total incl. all redos (k1/k3/k4 and failed-gate stills are redos/rejects). Balance at 15:36 ET: 5738.88. xs7_b returned an nsfw flag (charge unknown)."""
PROC="""Process statement: Valentina's process (Hard Rule #1). Seedream 5.0 Pro (seedream_v5_pro, 2k) single-ref edit of an approved v4C final ("Edit this exact photo: keep everything identical..."), locked body/hair line, soft even front daylight, soft smile, unretouched-skin tail; no chained edits, no generated frames as refs. Finished with finish_v4C.py (no blur). identity_gate.py (face venv, --source seedream --body) on every still, run one at a time with >=3 GB free; stills bar 0.79 centroid. By-eye check: fuller natural bust and even golden tan confirmed against sienna_v4C_reference_sheet.jpg. Banned stills sC2_b, sA2_b, eB4_b, eB4_c not used; hero face is not b1a, gc_surf_i, bal_p or v2sA2_c."""
posts_old=[
 ('xs1_b','x_tease_champagne_cami','tease',"Champagne, a satin cami and 30,000 feet of nobody watching 🥂 link in bio"),
 ('xs4_a','x_tease_lace_canopy','tease',"Villa mornings hit different when you never planned on getting dressed 🖤 link in bio"),
 ('xs6_b','x_tease_outdoor_shower','tease',"Rinsing off the salt before round two 🌴💦 link in bio"),
 ('xs5_b','x_album_coconut',"album",f"Coconut in one hand, my album on repeat in the other 🥥 Salt In My Hair is out now on Apple Music 🌊 {APPLE}"),
 ('xs5_c','x_album_beach',"album",f"Sunset, sand and the songs I wrote about all of it ☀️ Salt In My Hair, out now on Apple Music {APPLE}"),
]
posts=[('xs5_c','x_tease_sunrise_beach','tease',"Sunrise swim, salt on my skin and nowhere to be 🌅 ")]
for n,slug,kind,cap in posts:
    src=f'x/fin/{n}_v4C.jpg'; dst=f'x_set/sienna_x_20261022_{slug}_v2.jpg'
    if not os.path.exists(dst): shutil.copy(src,dst)
    v,d=g(f'x/gate/{n}.txt'); p=os.path.join(D,dst)
    pr=open(f'x/p_{n.split("_")[0]}.txt').read().strip()
    size=subprocess.run(['identify',p],capture_output=True,text=True).stdout
    md=f"""# REVIEW SUBMISSION: {slug} (Sienna, X, 2026-10-22)

- File: `{p}`
- md5: `{md5(p)}`  size: {os.path.getsize(p)} bytes  spec: JPEG {size}
- Source still: `{D}/{src}` (raw: `{D}/x/raw/{n}.png` and `_tex.png`)
- Platform: X only ({'spicy-but-SFW teaser, no link, no nudity' if kind=='tease' else 'album post with the Apple Music link, no Spotify'}). Not for TikTok/IG/YT/FB.
- Type: still image (no transition).

## Identity gate (stills bar 0.79)
| frame | verdict | centroid | best | body |
|---|---|---|---|---|
| {n}_v4C.jpg | {v} | {d['score_centroid']} | {d['score_best']} | {'pass' if d['body_pass'] else 'fail'} (bust_w {d['body'].get('bust_w')}) |

By-eye: face matches refs, fuller bust and golden tan present, frame filled, no bars. Contact sheet: `{D}/qc/xpass.jpg`

{PROC}

Prompt used:
```
{pr}
```

## Caption (X)
{cap}

{CRED}
"""
    f=os.path.join(D,'x_set',f'REVIEW_SUBMISSION_{slug}_v2.md'); open(f,'w').write(md); print(f, md5(p))
