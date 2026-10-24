import json,glob,os,shutil,subprocess,hashlib
R='/workspace/hf-test/charlotte_1022'; B=R+'/rb2'; F=B+'/final'; REF='/workspace/hf-test/charlotte_ref/ref_sheet.jpg'
G={}
for f in sorted(glob.glob(B+'/qc/stills_gate*.json')):
    for k,v in json.load(open(f)).items(): G[os.path.basename(k).replace('_v4C.jpg','')]=dict(centroid=v.get('score_centroid'),best_ref=v.get('score_best'),pass_=not v.get('reasons'),reasons=v.get('reasons'),gate_file=f)
J={l.split()[0]:l.split()[1] for l in open(B+'/man/still_jobs.tsv') if l.strip()}
K={l.split()[0]:l.split()[1:] for l in open(B+'/man/kling_jobs.tsv') if l.strip()}
md5=lambda p:hashlib.md5(open(p,'rb').read()).hexdigest()
def sbs(img,out):
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',img,'-i',REF,'-filter_complex','[0]scale=-2:1200[a];[1]scale=-2:1200[b];[a][b]hstack=inputs=2','-q:v','3',out],check=True); return out
def frame(v,t,out,scale=None):
    c=['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',v,'-frames:v','1','-q:v','2']+(['-vf',scale] if scale else [])+[out]; subprocess.run(c,check=True); return out
def still(item,key,name,src=None):
    dst=f'{F}/{name}'; shutil.copy(src or f'{B}/fin/{key}_v4C.jpg',dst)
    return dict(file=dst,md5=md5(dst),key=key,job_id=J.get(key,'see rb manifest'),model='seedream_v5_pro, 3:4, 2k, single image_reference',finish_v4C='applied (rb2/finish_v4C.py)',gate=G.get(key),prompt_file=f'rb2/p/{key}.txt',sbs=sbs(dst,f'{F}/{item}_{key}_sbs.jpg'))
M={}
old=json.load(open(R+'/rb/man/Reddit2_away_kit_check.json'))
M['X3_sauna_tease']=dict(platform='X',sensitive=True,caption='warming back up after the plunge 🔥',assets=[still('X3','x3c2','X3_sauna_tease_x3c2.jpg'),still('X3','x3b2','X3_sauna_tease_x3b2.jpg')],pose_note='x3c2 standing in sauna doorway hand on frame; x3b2 ladle over-shoulder look. Neither hands-on-hips nor seated.')
M['X5_recovered_mostly_tease']=dict(platform='X',sensitive=True,caption='recovered. mostly. darling 😇',assets=[still('X5','x5h3','X5_recovered_mostly_tease_x5h3.jpg')],pose_note='sauna doorway, hand raised on door frame, open white robe over covering black lace bralette+briefs, no nudity. Not bed, not hands on hips. Expression is still a smile (closed-lip smirk attempts x5g/x5i drifted to .69-.74 and failed).')
r1=still('Reddit1','r1d','Reddit1_recovery_day_r1d.jpg')
M['Reddit1_recovery_day']=dict(platform='Reddit',sensitive=False,caption='Recovery day in Munich after a 2-2 away day',target_sub='r/Munich',assets=[r1],rules_screenshot=B+'/shots/munich_rules.png',rules_screenshot_full=B+'/shots/munich_home.png',outfit_note='white tee under cardigan (SFW)',RULE_CONFLICT='r/Munich rule 9 bans AI-generated images (removal + possible ban); rule 5 bans self-promotion. Do NOT post to r/Munich; use u/CharHayesWC26 profile or an AI-permitting sub.')
src2=R+'/rb/final/Reddit2_away_kit_check_r2b.jpg'; a2=still('Reddit2','r2b','Reddit2_away_kit_check_r2b.jpg',src2)
a2.update(job_id=old['assets'][0].get('job_id'),gate=old['assets'][0].get('gate'),prompt_file=old['assets'][0].get('prompt_file'),finish_v4C=old['assets'][0].get('finish_v4C'),note='same file as rb (unchanged, per reviewer)')
M['Reddit2_away_kit_check']=dict(platform='Reddit',sensitive=False,caption='Away day kit check from Munich',target_sub='r/selfie',assets=[a2],rules_screenshot=B+'/shots/selfie_rules.png',rules_screenshot_full=B+'/shots/selfie_home.png',RULE_CONFLICT='r/selfie rule 2 "No AI ... No AI photos"; rule 5 no self promotion. Do NOT post to r/selfie; use profile or AI-permitting sub.')
def vid(item,name,cap,txt,clips,fg,extra={}):
    v=f'{F}/{name}'; d=dict(platform=extra.pop('platform'),file=v,md5=md5(v),caption=cap,on_screen_text=txt,text_bottom_y_max=930,resolution='1080x1920 full frame (cover, no blurred bands)',ai_mention=False,clips=clips,final_gate=fg)
    d['sbs']=sbs(frame(v,1.0,f'{B}/qc/{item}_f1.jpg'),f'{F}/{item}_sbs.jpg'); d.update(extra); return d
dur=lambda p:float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
kl='kling3_0, 5s, 9:16, std, sound off, Element 8f87f513-c3f6-41cc-95ac-c201e98d0d9c, low motion'
x2=f'{F}/charlotte_x_20261022_pilates-vs-icebath_v3.mp4'
M['X2_pilates_vs_icebath']=vid('X2','charlotte_x_20261022_pilates-vs-icebath_v3.mp4','pilates girls vs the ice bath. the ice bath won. freezing','pilates girls / vs the ice bath',
 [dict(half='pilates 0-2.2s',src='pC2 still (tree pose, palms together, gate %s) slow push-in'%G['pC2']['centroid'],job_id=J.get('pC2')),
  dict(half='ice 2.2-5.1s',clip='vI',kling_job=K['vI'][0],start_still='c_I4 approved v4C',motion='steps into ice tub',kling=kl,raw_gate='median .832 min .780 (5fps)')],
 dict(median=.823,min=.775,below70=0,frames=51,file='rb2/qc/x_final.json'),dict(platform='X',duration=round(dur(x2),3),music='08_sunday_roast_hangover @158.241',stance_note='tree pose vs stepping into the tub'))
yt=f'{F}/charlotte_yt_20261022_matchday-vs-recovery_v3.mp4'
th=f'{F}/YT1_thumb.jpg'; frame(yt,0.8,th,'scale=1080:1920')
M['YT1_matchday_vs_recovery']=vid('YT1','charlotte_yt_20261022_matchday-vs-recovery_v3.mp4','matchday me vs recovery me 🧖\u200d♀️ #shorts #arsenal #gunners','matchday me / recovery me',
 [dict(half='matchday 0-2.6s',clip='rb o4',kling_job='70eeb8b3-bd5e-4afb-84f0-53b32381dcef',crop='717x1276 cover'),
  dict(half='recovery 2.6-5.3s',clip='vI 2.2-4.9s (ice tub)',kling_job=K['vI'][0],start_still='c_I4 approved v4C',note='cafe clip o5 dropped (background person); park vR/pool vR2 retries failed gate (median .705/.728)')],
 dict(median=.800,min=.738,below70=0,frames=53,file='rb2/qc/yt_final.json'),dict(platform='YouTube Shorts',duration=round(dur(yt),3),thumbnail=th,music='02_proper_gorgeous @151.164',note='recovery half reuses the same ice-bath Kling clip as X2 (different time range); cross-platform reuse'))
co=f'{F}/charlotte_collab_20261022_oktoberfest-stein-clink_v3.mp4'
M['Collab_oktoberfest_charlotte_half']=vid('Collab','charlotte_collab_20261022_oktoberfest-stein-clink_v3.mp4',{'TikTok':'Oktoberfest finished weeks ago. nobody told us 🍻 @gabriela_santos343 #oktoberfest #munich #bestie','YouTube':'Oktoberfest finished weeks ago. nobody told us 🍻 #shorts #oktoberfest','X':'Oktoberfest finished weeks ago. nobody told us. prost 🍻'},'Oktoberfest finished / weeks ago. (0-2.6s, y 760-913) then nobody told us (2.6s-end, y 800-883)',
 [dict(clip='vK',kling_job=K['vK'][0],start_still='kC3 Seedream single-ref from c_c4 (gate %s, below .83 start rule)'%G['kC3']['centroid'],start_media='f10a6e31-2260-45f1-9953-1513765921c8',kling=kl,edit='0-2.4s slowed 1.75x + 2.4-3.2s real time; raw tail 3.3-5s dropped (stein covers face, .43-.66)')],
 dict(median=.793,min=.743,below70=0,frames=50,file='rb2/qc/collab_final.json'),dict(platform='TikTok + YouTube Shorts + X',duration=round(dur(co),3),audio='silent (anullsrc track)',ending='Charlotte raises the stein in HER RIGHT HAND, starting frame-left, toward the lens (to frame centre) for the clink; hard cut on last frame',background='empty beer garden, daylight, no people',FLAG='text sits above y=930 per instruction, which is upper/middle of frame, not the lower third (lower third starts ~y1280)'))
for k,v in M.items():
    v['item']=k; json.dump(v,open(f'{R}/rb/man/{k}.json','w'),indent=1,ensure_ascii=False); json.dump(v,open(f'{B}/man/{k}.json','w'),indent=1,ensure_ascii=False)
print(json.dumps({k:[a.get('gate') for a in v.get('assets',[])] or v['final_gate'] for k,v in M.items()},default=str))
