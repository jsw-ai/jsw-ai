import sys; sys.path.insert(0,'work')
from lib import *
def finish(src,out,caps,music=None,mvol=0.2,music_ss=0,work='work/fin'):
    os.makedirs(work,exist_ok=True)
    ins=f'-i {src}'; fc='[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.4:5:5:0.0,noise=alls=5:allf=t[v0];'
    last='v0'; n=1
    for i,(txt,s,e,y) in enumerate(caps):
        p=f'{work}/c_{os.path.basename(out)}_{i}.png'; caption_png(txt,p,y=y,size=70); ins+=f' -i {p}'
        fc+=f"[{last}][{n}:v]overlay=0:0:enable='between(t,{s},{e})'[v{n}];"; last=f'v{n}'; n+=1
    dur=float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {src}',shell=True))
    if music:
        ins+=f' -ss {music_ss} -i {music}'
        hasa=subprocess.check_output(f'ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 {src}',shell=True).strip()
        if hasa:
            fc+=f'[{n}:a]volume={mvol},afade=t=in:d=0.3,afade=t=out:st={dur-0.7}:d=0.7[m];[0:a]volume=1.0[s];[s][m]amix=inputs=2:duration=first:normalize=0[a]'
        else:
            fc+=f'[{n}:a]volume={mvol},afade=t=in:d=0.3,afade=t=out:st={dur-0.7}:d=0.7[a]'
    amap='-map "[a]" -c:a aac -b:a 160k' if music else '-an'
    run(f'ffmpeg -y -loglevel error {ins} -filter_complex "{fc}" -map "[{last}]" {amap} -t {dur} -c:v libx264 -crf 24 -preset medium -pix_fmt yuv420p -movflags +faststart -map_metadata -1 {out}')
R='raw/'
finish(R+'lipsync1_raw.mp4','lipsync1_new_york_growing_on_me.mp4',[("new in town, being honest",0,2.2,330),("new york's growing on me. so are you.",2.3,7.2,1500),("your move",7.2,8.1,1500)],'music/track_brunch_pop.wav',0.16)
finish(R+'lipsync2b_raw.mp4','lipsync2_reformer_one_me_zero.mp4',[("me vs the reformer, round 47",0,2.2,330),("reformer, one. me, zero. still cute though.",2.3,5.2,1500),("rematch tomorrow, 7am",5.3,8.1,1500)],'music/track_late_night_house.wav',0.16)
finish(R+'dance_raw.mp4','dance_living_room_nobody_watching.mp4',[("me when the reformer cancels",0,3,330),("living room, 4pm, nobody's watching",3,6.8,1500),("(you're watching)",6.8,10.1,1500)],'music/track_late_night_house.wav',0.9,music_ss=2)
