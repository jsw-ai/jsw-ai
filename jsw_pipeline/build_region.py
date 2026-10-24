import re
L=open('/workspace/page_now.md').read().split('\n')
def idx(h):
    return next(i for i,l in enumerate(L) if l.strip()==h)
i_ms=idx('## Model settings'); i_ch=idx('### Charlotte'); i_md=idx('### Madison'); i_ex=idx('## Exceptions')
i_ch2=next(i for i in range(i_ex,len(L)) if L[i].strip()=='### Charlotte')
i_md2=next(i for i in range(i_ex,len(L)) if L[i].strip()=='### Madison')
i_cam=idx('## Camille settings'); i_gab=idx('## Gabriela'); i_gabs=idx('### Gabriela settings'); i_gabx=idx('### Gabriela exceptions')
i_sie=idx('## Sienna: settings and exceptions (JSW Sienna)'); i_end=idx('## Stats pull (JSW Content Tracker)')
assert i_ms<i_ch<i_md<i_ex<i_ch2<i_md2<i_cam<i_gab<i_gabs<i_gabx<i_sie<i_end
old='\n'.join(L[i_ms:i_end]).rstrip('\n')
def blk(a,b): return '\n'.join(L[a:b]).strip('\n')
charlotte_set=blk(i_ch,i_md); madison_set=blk(i_md,i_ex)
charlotte_ex=blk(i_ch2,i_md2); madison_ex=blk(i_md2,i_cam)
cam=L[i_cam+1:i_gab]
cam_rows=[l for l in cam if l.startswith('| Exceptions |')]; assert len(cam_rows)==1
cam_exc=cam_rows[0][len('| Exceptions | '):].rstrip(' |')
cam_body='\n'.join(l for l in cam if not l.startswith('| Exceptions |')).strip('\n')
gab_intro=blk(i_gab+1,i_gabs); gab_set=blk(i_gabs+1,i_gabx); gab_exc=blk(i_gabx+1,i_sie)
sie=L[i_sie+1:i_end]
def sub(name):
    a=next(i for i,l in enumerate(sie) if l.strip()=='### '+name)
    b=next((i for i in range(a+1,len(sie)) if sie[i].startswith('### ')),len(sie))
    return '\n'.join(sie[a+1:b]).strip('\n')
sie_src=next(l for l in sie if l.startswith('Source:'))
acc=sub('Accounts').split('\n')
acc_set=[x for x in acc if 'AdsPower' in x]; acc_ex=[x for x in acc if x.startswith('- ') and 'AdsPower' not in x]
def row(cells): return '| '+' | '.join(c.replace('\n','<br />') for c in cells)+' |'
# pull verbatim values for summary table
def val(block,field):
    for l in block.split('\n'):
        if l.startswith('| '+field+' |'): return l.split(' | ',2)[1] if block is not None else ''
    return None
def v3(block,field):
    for l in block.split('\n'):
        if l.startswith('| '+field+' |'):
            parts=l.strip().strip('|').split(' | ')
            return parts[1].strip()
    return 'TBD'
C=charlotte_set; M=madison_set; G=gab_set; K=cam_body
hdr=['Model','Approved ref photo paths','identity_pack key','Kling element ID','Album and Apple link','Platforms and handles','SFW or spicy','Posting time zone','Gate bars (still / Kling start / video)','AdsPower profile']
rows=[]
rows.append(['<b>Valentina</b>',
 '<code>/workspace/hf-test/zen/posting/valentina_test2/fin/{s1_a,s2_b,s4_a,s5_a,s6_a,s7_a,s8_a}_v4C.jpg</code> (approved test2 look, Samuel 2026-10-14); sheet <code>valentina_test2_contact_sheet.jpg</code>',
 '<code>valentina</code> (gate refs <code>valentina_refs/</code>; pack status DRAFTED_UNAPPROVED, approved look = test2)',
 '<code>0950a489-6b07-4db6-b0a9-95e83e4be628</code> ("Valentina-matte-test", from s1_a, s2_b, s4_a)',
 'Corazón de Cartagena · [Apple Music](https://music.apple.com/us/album/coraz%C3%B3n-de-cartagena/6825712737)',
 'TikTok @valentinareyes33240 · IG @valentina_reyes_wc26 (renamed 10/22) · X @v_reyes_wc2026 · Reddit u/valentina_reyes_mia · YouTube @valentinareyes-wc2026 · FB Page profile.php?id=61595133343203 (Ayrshare id 1413498831838808)',
 '<b>Spicy on X only</b> (sensitive-marked teases); SFW on TikTok, IG, YouTube, FB, Reddit. No Fanvue link anywhere',
 'America/New_York (Miami); this week in Colombia (COT, UTC-5)',
 '≥ 0.78 / ≥ 0.85 / median ≥ 0.78, no frame < 0.70',
 '<code>k1cwwlxv</code> (MacBook-Pro-6)'])
rows.append(['<b>Sienna</b>',
 '<code>/workspace/hf-test/zen/posting/sienna_refs/</code>: <code>story1_a_v4C.jpg</code>, <code>story2_a_v4C.jpg</code>, <code>story3_b_v4C.jpg</code>, <code>reddit_x1_b_v4C.jpg</code>',
 '<code>sienna</code>',
 '<code>2603afeb-5f21-4acc-a3de-8904d5a32cb9</code> (Sienna-v2-1020)',
 'Album name TBD (Apple URL slug "salt-in-my-hair") · [https://music.apple.com/us/album/salt-in-my-hair/6825685962](https://music.apple.com/us/album/salt-in-my-hair/6825685962)',
 'TBD in her row file. SHARED_LEARNINGS 10/17 (Ayrshare Default profile): IG siennablake0320, TikTok thesienna_blake, X BlakeSienn39605, Reddit TheSiennaBlake',
 'TBD (CONTENT_RECIPE §6: Fanvue funnel only from X bio/pinned post and Reddit profile)',
 'TBD',
 '≥ 0.79 / TBD / ≥ 0.78 on 16 frames vs story1_a_v4C',
 '<code>k1cwvh25</code>'])
def chplat(B,fields):
    return ' · '.join(f+' '+v3(B,f) for f in fields)
rows.append(['<b>Charlotte</b>',
 'Generation refs, in order: '+v3(C,'Generation refs, in order')+'; Reused approved v4C starts: '+v3(C,'Reused approved v4C starts'),
 v3(C,'identity\\_pack key'), v3(C,'Kling'),
 v3(C,'Album')+' · '+v3(C,'Apple Music'),
 chplat(C,['X','TikTok','Instagram','YouTube','Facebook','Reddit']),
 'see Platforms and handles', v3(C,'Posting time zone'),'see Exceptions ### Charlotte (3)', v3(C,'AdsPower')])
rows.append(['<b>Madison</b>',
 v3(M,'Approved ref photos (single-ref edit bases)'), v3(M,'identity\\_pack key'), v3(M,'Kling'),
 v3(M,'Album')+' · '+v3(M,'Apple Music'),
 chplat(M,['TikTok','Instagram','YouTube','Facebook','Reddit','X']),
 v3(M,'Content'), v3(M,'Posting time zone'),
 'Still: '+v3(M,'Still gate')+' · Video: '+v3(M,'Video gate'), v3(M,'AdsPower')])
rows.append(['<b>Camille</b>',
 v3(K,'Approved ref photos'), v3(K,'identity\\_pack key'), v3(K,'Kling element ID'), v3(K,'Album'),
 v3(K,'Platforms / handles'), v3(K,'Content'), v3(K,'Posting time zone'),'TBD','TBD'])
rows.append(['<b>Gabriela</b>',
 'Approved face refs (gate refs): '+v3(G,'Approved face refs (gate refs)')+'; Gate-passed v4C finals, 10/22 (Reviewer verdict pending): '+v3(G,'Gate-passed v4C finals, 10/22 (Reviewer verdict pending)'),
 v3(G,'identity\\_pack key'), v3(G,'Kling Element ID'), v3(G,'Album'),
 v3(G,'Platforms and handles (her own Ayrshare profile)'), v3(G,'SFW or spicy'), v3(G,'Posting time zone'),'TBD', v3(G,'Engagement')])
for r in rows:
    for c in r: assert 'TBD'!=c or True
table='\n'.join([row(hdr),row(['---']*len(hdr))]+[row(r) for r in rows])
val_tbl='''| Field | Value | Source |
| --- | --- | --- |
| identity\\_pack key | <code>valentina</code>; gate refs <code>valentina_refs/valentina_{bikini1,bikini2,cover,talking1_frame,lingerie_v2_1,lingerie_v2_4}.jpg</code>; status DRAFTED\\_UNAPPROVED, approved\\_look = test2 | identity\\_packs.json |
| Approved ref photos (single-ref edit bases, Kling starts) | <code>valentina_test2/fin/{s1_a,s2_b,s4_a,s5_a,s6_a,s7_a,s8_a}_v4C.jpg</code> (1080x1443) | VALENTINA\\_PIPELINE.md §2b |
| Body line | <code>/workspace/hf-test/zen/posting/valentina_exciting_oct20/LOCKED_BODY_LINE.txt</code> (word for word) | Valentina SOP §1 |
| Stills | <code>seedream_v5_pro</code>, 9:16 (video starts) or 3:4, 2k, one image\\_reference | valentina\\_oct22/work/batch1a.json |
| finish\\_v4C | <code>valentina_oct22/work/finish_v4C.py</code> (texture 0.5); <code>finish_v4Clite.py</code> (0.15) | valentina\\_oct22/work/ |
| Still gate | <code>identity_gate.py img --model valentina --source seedream --body</code>, ≥ 0.78 | Valentina SOP §6 |
| Video gate | <code>valentina_oct22/work/vgate.py &lt;clip&gt; 1</code>: median ≥ 0.78, min ≥ 0.70; Kling start ≥ 0.85 | vgate.py; SHARED\\_LEARNINGS 10/21-22 |
| Kling | Element <code>0950a489-6b07-4db6-b0a9-95e83e4be628</code>; <code>kling3_0</code>, 5 s, 9:16, pro (8.75 cr) or std (7.5 cr), sound off | batch\\_k67.json, credits.log |
| Build | <code>valentina_oct22/work/build.py &lt;spec.json&gt;</code> | build.py |
| Voice ref | <code>voicerefs-from-sam/valentina.mp3</code> | identity\\_packs.json |
| Album | Corazón de Cartagena. Album tracks used 10/22: <code>/workspace/music/mp3/valentina/valentina_music_20261021_{miami_noche,corazon_de_cartagena,salsa_class}_v1.mp3</code>. Master WAV + lyrics folder: TBD | dance\\_tt.json, snap\\_v4.json, duet.json |
| Apple Music | [https://music.apple.com/us/album/coraz%C3%B3n-de-cartagena/6825712737](https://music.apple.com/us/album/coraz%C3%B3n-de-cartagena/6825712737) | JSW AI (10/22) |
| TikTok | @valentinareyes33240: SFW, max 1 a day | Valentina SOP §3 |
| Instagram | @valentina\\_reyes\\_wc26: SFW | SHARED\\_LEARNINGS 10/22 |
| X | @v\\_reyes\\_wc2026: <b>SPICY</b>, sensitive-marked teases. Not linked in Ayrshare on 10/21; current status TBD | Valentina SOP §3, §8 |
| Reddit | u/valentina\\_reyes\\_mia: SFW, own profile, posts only | Valentina SOP §3 |
| YouTube | @valentinareyes-wc2026 (channel UCGdVqvJKNOpisLt4gQNjOyg): SFW | Valentina SOP §3; SHARED\\_LEARNINGS 10/22 |
| Facebook | Page profile.php?id=61595133343203 (Ayrshare id 1413498831838808): SFW | SHARED\\_LEARNINGS 10/22 |
| Fanvue | none: no link anywhere | Valentina SOP §3 |
| AdsPower | <code>k1cwwlxv</code>, headless only, MacBook-Pro-6; never touch proxies. Scripts <code>~/adsbot/valentina/</code> | lib.py |
| Profile key file | <code>/home/box/agent-data/secrets/JSW-valentina-ayrshare-profile-key.txt</code> (path only) | Valentina SOP §3 |
| Logins | 1Password vault "Shared with Grok Bot", items "JSW - Valentina - &lt;Platform&gt;" (e.g. "JSW - Valentina - Gmail", "JSW - Valentina Reddit (Google sign-in)") | Valentina SOP §3 |
| Posting time zone | America/New\\_York (Miami). This week she is in Colombia (COT, UTC-5) | Valentina SOP header |
| Posted log | <code>/workspace/hf-test/zen/posting/valentina_posted_log.json</code> | Valentina SOP §2 |'''
val_ex='''1. <b>She is the canonical process:</b> no exceptions to steps 1-8. Stills are single-ref edits of the test2 finals only; v4C only, never v5.
2. <b>Smile wording:</b> stills use "same natural warm smile as in the photo" (a "soft closed-mouth smirk" narrowed her face, .69-.78); Kling prompts ask for a soft closed-mouth smile that stays the same.
3. <b>TikTok:</b> max 1 a day; no dating or red-flag hashtags.
4. <b>X and Reddit:</b> not linked in Ayrshare on 10/21, so the 10/21 posts went out through AdsPower browser scripts (<code>~/adsbot/valentina/post1021/</code>) from Reviewer-PASS files. Current Ayrshare link status: TBD.
5. <b>Machine:</b> her AdsPower profile and scripts are on MacBook-Pro-6, not on <code>Mac.hsd1.mi.comcast.net</code> (her SOP §4 step 1 names the wrong machine).
6. <b>YouTube Studio:</b> blocked by a "Verify it's you" password challenge; reply to comments from the watch page instead.
7. <b>Time zone:</b> America/New\\_York, but this week's story has her in Colombia (COT).'''
ex_intro='Each model lists only the steps where she truly differs from steps 1-8 above. Everything else follows the shared steps and her row in Model settings.'
ms_intro='One row per model. Scripts read these values; nothing model-specific is hard-coded in the steps. Values in the Charlotte, Madison, Camille and Gabriela rows are copied word for word from their blocks below. <b>TBD/TODO</b> = not in any file. Paths only, no secrets.'
new=f'''## Model settings

{ms_intro}

{table}

### Valentina

Added 10/22 by Valentina's bot from VALENTINA\\_PIPELINE.md, identity\\_packs.json, valentina\\_oct22/work/, her SOP and SHARED\\_LEARNINGS.md. Paths are relative to <code>/workspace/hf-test/zen/posting/</code> unless absolute.

{val_tbl}

### Sienna

{sie_src}

#### Kling

{sub('Kling')}

#### Reference stills

{sub('Reference stills')}

#### Gates

{sub('Gates')}

#### Music

{sub('Music')}

#### Accounts

{chr(10).join(acc_set)}

{charlotte_set}

{madison_set}

### Camille

{cam_body}

### Gabriela

{gab_intro}

{gab_set}

## Exceptions

{ex_intro}

### Valentina

{val_ex}

### Sienna

- Stills bar is 0.79, not the gate's default 0.78 (see Model settings → Sienna → Gates).

#### Banned stills

{sub('Banned stills')}

#### Body check

{sub('Body check')}

#### Known face issue

{sub('Known face issue')}

#### Accounts

{chr(10).join(acc_ex)}

{charlotte_ex}

{madison_ex}

### Camille

- {cam_exc}

### Gabriela

{gab_exc}'''
open('/workspace/jsw_pipeline/old_region.md','w').write(old)
open('/workspace/jsw_pipeline/new_region.md','w').write(new)
print(len(old),len(new))
