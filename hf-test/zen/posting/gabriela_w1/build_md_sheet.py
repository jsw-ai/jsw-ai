from plan_data2 import *
from collections import Counter
import re
from PIL import Image, ImageDraw, ImageFont
ROOT='/workspace/hf-test/zen/posting/'
gate={'A':'0.846/0.828','B':'0.794/0.779','C':'0.818/0.805','D':'0.855/0.859','E':'0.795/0.782','F':'0.905/0.898','G':'0.862/0.846','H':'0.902/0.890'}
def site(p): return p[2].split(' ')[0]
cnt=Counter(site(p) for p in ALL)
lines=[]
lines.append("""# Gabriela — Week 1 Content Plan, ALL SITES (for Samuel's approval)
Updated Wed Oct 14 2026 ~11:59 PM ET (previous version: `gabriela_week1.bak_pre_allsites.md`). Window: Thu Oct 15 – Wed Oct 21 (ET). Samuel's rule applied: every JSW model on every possible site, no skipping → Instagram, TikTok, X, Reddit, **YouTube**, **Facebook**.
> **HARD RULES:** no AI mention anywhere in post content (captions, hashtags, on-screen text, Reddit titles/bodies, X posts, YouTube/Facebook text). Platform AI toggles/labels (TikTok AI-generated, IG AI info, YouTube altered/synthetic-content disclosure, Facebook/Meta AI label) stay ON as **settings only**. No Fanvue links/teasers, no NSFW or lingerie on any lane (all SFW: beachwear-classy only). No video this week except two silent slideshow Shorts rendered locally from existing stills (0 credits). **Nothing is posted until Samuel approves the exact files and captions.** `go_live` stays OFF. 0 new credits used.

Status: **PLAN + 8 finished stills. Nothing queued, nothing posted.**

## Per-site link status (Ayrshare, Gabriela)
Source: `ACCOUNT_INVENTORY_2026-09-05.md` (the only Ayrshare check on file; no newer status output exists in /workspace). I did NOT re-query Ayrshare live (would need her vault profile key; not read).
| Site | Link status for Gabriela | Plan |
|---|---|---|
| Ayrshare profile | **Profile key stored** (vault); account list/linkage not exposed | – |
| Instagram | **UNCONFIRMED** (no handle, no scheduled items, no linked-platform list) | Slots drafted; HOLD until linked |
| TikTok | **UNCONFIRMED** | Slots drafted; HOLD until linked |
| X | **UNCONFIRMED** (X consumer key stored globally; no Gabriela handle) | Slots drafted; HOLD until linked |
| Reddit | **UNCONFIRMED** (no handle; Reddit not in Ayrshare's list in the inventory) | Slots drafted; may need manual posting |
| YouTube | **No account linked** (none in inventory) | Slots drafted; HOLD. Ayrshare's YouTube posting is video-only, so image "community-style" posts would be manual; the 2 Shorts are silent slideshows made from stills |
| Facebook | **No account/Page linked yet** (none in inventory) | Slots drafted; HOLD. Needs a Facebook Page (Ayrshare posts to Pages, not profiles) |
To confirm: Samuel links her socials in the Ayrshare dashboard (profile → Social Accounts), then JSW AI re-checks `/user` for `activeSocialAccounts`.

## Rules applied
- **Max 3 posts per site per day** (actual: 1 per site per day, so at most 6 posts/day across 6 sites, spaced out). TikTok = photo-mode slideshows only. IG = feed/carousel. X = stills + text. Reddit = own-profile posts only (no subreddit posts, no AI subs). YouTube = community-style image posts + 2 silent slideshow Shorts. Facebook = Page photo posts/albums.
- Persona voice (draft, Samuel to confirm): warm, sunny, easygoing, short lowercase captions, light humour, golden-hour/beach/pool lifestyle. No location claimed until a bio is set. No store/affiliate promo. Soft CTA only. Facebook/YouTube text is slightly more conversational (questions) and not word-for-word identical to IG where avoidable.
- Hashtags: lifestyle only. Never any AI tag.

## Timing (ET)
IG/TikTok/X/Reddit as before (lunch 12–1 PM, evening 6:30–7:30 PM, one 11 AM weekend slot). **Facebook 12:00 PM daily**, **YouTube 4:00–5:00 PM daily** (after-school/work window).

## Image library (all finished v4C, gated vs Gabriela pack; Gabriela-only)
| ID | File | Source | Gate (centroid / best) |
|---|---|---|---|""")
for k,(d,f) in IMG.items():
    lines.append(f"| {k} | `/workspace/hf-test/zen/posting/{f}` (copy: `gabriela_w1/final/`) | {d} | {gate[k]} |")
lines.append("\nOnly 8 images for 38 posts, so images repeat across platforms (never the same file twice on one platform on one day; recap slideshows reuse). Recommend 4–6 more stills before week 2 (cost: credits, needs approval). P16 now uses H, so **no new image is required this week**.\n\n## 7-day calendar (ET)")
cur=None
for p in ALL:
    if p[1]!=cur:
        cur=p[1]; lines.append(f"\n### {cur}")
    cap=p[5]; tg=(' · '+p[6]) if p[6].strip() and not p[6].startswith('(') else ''
    im=p[4]
    lines.append(f"- **{p[0]} · {p[2]} — {p[3]}** · Image(s): {im} · Caption: {cap}{tg}"+(' · (text-only, no image)' if im=='-' else ''))
lines.append("\n## Counts\n| Platform | Posts |\n|---|---|")
names={'Instagram':'Instagram (1 carousel)','TikTok':'TikTok photo-mode slideshows','Reddit':'Reddit own-profile','X':'X (1 text-only)','YouTube':'YouTube (5 community-style image, 2 Shorts slideshows)','Facebook':'Facebook (2 albums)'}
for s in ['Instagram','TikTok','X','Reddit','YouTube','Facebook']:
    lines.append(f"| {names[s]} | {cnt[s]} |")
lines.append(f"| **Total** | **{len(ALL)}** |")
lines.append("""
## Changes vs previous version
- Added Facebook (7) and YouTube (7) slots, and extra TikTok (Sat) and X (Mon, Wed) so every site posts most days.
- Removed the "No YouTube" rule; Facebook/YouTube listed as unlinked.
- P16 now uses existing still H (no new image needed).
- Contact sheet regenerated with the new mapping.

## Blockers before go_live
- Samuel approves exact files + captions; then copy to `approved/gabriela/week1/`.
- Link Gabriela's accounts in Ayrshare: IG, TikTok, X, YouTube channel, Facebook Page (Reddit likely manual). Fill handles.
- Posting tool must set the AI toggles/labels ON as settings (TikTok, IG, YouTube synthetic-content disclosure, Facebook); Reddit needs title field; YouTube Shorts slideshows need a local ffmpeg render (0 credits) after approval.
- Visual check pending Samuel: sheet `review_gabriela_week1.jpg`.""")
open(ROOT+'gabriela_week1.md','w').write('\n'.join(lines)+'\n')
# contact sheet
F=lambda s,b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'%('-Bold' if b else ''),s)
W=360; cols=4; keys=list(IMG)
tw=W; 
def wrap(t,w,f):
    out=[];cur=''
    for wd in t.split():
        if f.getlength(cur+' '+wd)>w and cur: out.append(cur);cur=wd
        else: cur=(cur+' '+wd).strip()
    out.append(cur);return out
f9=F(10); 
cells=[]
for k in keys:
    im=Image.open(ROOT+IMG[k][1]).convert('RGB'); im=im.resize((W,int(im.height*W/im.width)))
    posts=[p for p in ALL if k in p[4].split(',')]
    txt=[]
    for p in posts:
        txt+=wrap(f"{p[0]} {p[1][:3]} {p[1][4:]} {p[3]} {site(p)}{' Short' if 'Short' in p[2] else ''}",W-8,f9)
    cells.append((k,im,txt))
rowh=[];rows=[cells[i:i+cols] for i in range(0,len(cells),cols)]
for r in rows: rowh.append(max(c[1].height+30+13*len(c[2]) for c in r)+10)
H=60+sum(rowh)
S=Image.new('RGB',(W*cols,H),'white'); d=ImageDraw.Draw(S)
d.text((6,6),"Gabriela week 1 — all sites (IG/TikTok/X/Reddit/YouTube/Facebook), Thu 10/15–Wed 10/21 ET. Mapping: image → post id · day · time · site",fill='black',font=F(13,True))
d.text((6,28),"Gate PASS A–H. Gabriela-only images; nothing posted, go_live OFF. 38 posts, 8 images (no new image needed).",fill=(160,0,0),font=F(11))
y=60
for r,h in zip(rows,rowh):
    for i,(k,im,txt) in enumerate(r):
        x=i*W; S.paste(im,(x,y)); yy=y+im.height+3
        d.text((x+4,yy),f"{k} · {IMG[k][0].split(",")[0]} · {gate[k]} · {sum(1 for p in ALL if k in p[4].split(','))} posts",fill='black',font=F(10,True)); yy+=16
        for t in txt: d.text((x+4,yy),t,fill=(40,40,40),font=f9); yy+=13
    y+=h
S.save(ROOT+'review_gabriela_week1.jpg',quality=88); print(S.size)
