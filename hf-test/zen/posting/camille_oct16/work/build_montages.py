import sys,os; sys.path.insert(0,'work')
from lib import *
R='raw/'; FB='../camille_fullbody/raw/'
A=[(R+'s2.png',"tell me i'm not the only one...",0.5),
 (R+'s1.png',"who gets ready like it's a date",0.5),
 (R+'s3.png',"...with the sunset",0.5),
 (R+'s6.png',"and checks the sky every 5 minutes",0.5),
 (R+'s5.png',"just to catch the golden hour",0.5),
 (R+'s4.png',"(you're looking. i noticed.)",0.5)]
B=[(R+'s7.png',"tell me you've never done this",0.5),
 (R+'s9.png',"\"5 minutes\" (it's been 40)",0.5),
 (FB+'fb2.png',"still deciding on the jeans",0.5),
 (R+'s10.png',"running to catch the last light",0.5),
 (FB+'fb3.png',"turns around like...",0.5),
 (R+'s8.png',"ok yes, i'm dancing. don't tell anyone",0.5)]
def mont(items,bpm,music,out,work,beats_per=4):
    os.makedirs(work,exist_ok=True); dur=60/bpm*beats_per; segs=[]
    for i,(src,cap,cx) in enumerate(items):
        img=f'{work}/p{i}.jpg'; crop916(src,img,cx)
        sg=f'{work}/seg{i}.mp4'; segment(img,cap,dur,i,sg,work,'in' if i%2==0 else 'out'); segs.append(sg)
    lst=f'{work}/list.txt'; open(lst,'w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    body=f'{work}/body.mp4'; run(f'ffmpeg -y -loglevel error -f concat -safe 0 -i {lst} -c copy {body}')
    T=dur*len(segs)
    run(f'ffmpeg -y -loglevel error -i {body} -i {music} -filter_complex "[1:a]atrim=0:{T},afade=t=in:d=0.3,afade=t=out:st={T-1.0}:d=1.0,volume=0.9[a]" -map 0:v -map "[a]" -t {T} -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -map_metadata -1 {out}')
    return T
print(mont(A,100,'music/track_golden_hour_pop.wav','montage1_tell_me_im_not_the_only_one.mp4','montage_work/m1'))
print(mont(B,112,'music/track_evening_drive.wav','montage2_getting_ready_last_light.mp4','montage_work/m2'))
