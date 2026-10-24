import sys,os; sys.path.insert(0,'work')
from lib import caption_png,run
def finish(raw,out,caps,music=None,mvol=0.14,speech=True,y=1330):
    os.makedirs('work/fin',exist_ok=True); base=os.path.basename(out)[:-4]; ins=''; fc='[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.4,noise=alls=4:allf=t[v0];'; last='v0'
    for i,(a,b,t) in enumerate(caps):
        p=f'work/fin/{base}_cap{i}.png'; caption_png(t,p,y=y,size=72); ins+=f' -loop 1 -i {p}'
        fc+=f'[{i+2}:v]format=rgba[c{i}];[{last}][c{i}]overlay=0:0:enable=\'between(t,{a},{b})\':format=auto[v{i+1}];'; last=f'v{i+1}'
    fc+=f'[{last}]format=yuv420p[vo];'
    if speech: fc+=f'[0:a]volume=1.0[sp];[1:a]volume={mvol}[mu];[sp][mu]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=7.4:d=0.6[ao]'
    else: fc+='[1:a]afade=t=in:d=0.3,afade=t=out:st=7.2:d=0.8,volume=0.9[ao]'
    run(f'ffmpeg -y -loglevel error -i {raw} -i {music}{ins} -filter_complex "{fc}" -map "[vo]" -map "[ao]" -t 8 -c:v libx264 -crf 22 -maxrate 6M -bufsize 12M -c:a aac -b:a 160k -movflags +faststart -map_metadata -1 {out}')
if __name__=='__main__':
    finish('video/raw/lip1_raw.mp4','lip1_pier_flirting_with_sunsets.mp4',[(0,2.5,"tell me i'm not the only one..."),(2.5,5.0,"flirting with sunsets"),(5.0,8,"(golden hour does this to me)")],'music/track_golden_hour_pop.wav')
    finish('video/raw/dance_raw.mp4','dance_beach_nobody_is_watching.mp4',[(0,3.5,"me when the sun hits just right"),(3.5,8,"tell me you'd dance too")],'music/track_evening_drive.wav',speech=False)
