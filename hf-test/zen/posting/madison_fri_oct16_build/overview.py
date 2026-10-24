import os,subprocess
from PIL import Image,ImageDraw,ImageFont
O='/workspace/hf-test/zen/posting/madison_fri_oct16/';T='tmp/'
F=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf',26)
def vf(p,t,n):
    q=f'{T}ov_{n}.jpg';subprocess.check_call(['ffmpeg','-y','-loglevel','error','-ss',str(t),'-i',p,'-frames:v','1',q]);return q
rows=[('INSTAGRAM  (Reel 11:48a | Carousel 7:44p | Stories 9:14a, 2:52p, 8:47p)',[vf(O+'instagram/ig_reel_pilates_1148am.mp4',1,'r1'),vf(O+'instagram/ig_reel_pilates_1148am.mp4',4,'r2'),vf(O+'instagram/ig_reel_pilates_1148am.mp4',6,'r3'),vf(O+'instagram/ig_reel_pilates_1148am.mp4',8,'r4'),vf(O+'instagram/ig_reel_pilates_1148am.mp4',10.5,'r5')]+[O+'instagram/'+f for f in sorted(os.listdir(O+'instagram')) if 'carousel' in f]),
('INSTAGRAM STORIES (9:14a poll | 2:52p question | 8:47p poll)',[O+'instagram/'+f for f in sorted(os.listdir(O+'instagram')) if 'story' in f]),
('TIKTOK  (photo-mode 3:37p; slides 1-7)',[O+'tiktok/'+f for f in sorted(os.listdir(O+'tiktok')) if f.endswith('.jpg')]),
('X  (8:53a text-only | 1:08p w12 | 5:11p w1)',[O+'x/'+f for f in sorted(os.listdir(O+'x'))]),
('YOUTUBE SHORT 2:24p - HELD  |  FACEBOOK Reel 10:05a + post 6:25p - HELD',[vf(O+'youtube_HELD/yt_short_224pm.mp4',1,'y1'),vf(O+'youtube_HELD/yt_short_224pm.mp4',5,'y2'),vf(O+'youtube_HELD/yt_short_224pm.mp4',10,'y3'),vf(O+'facebook_HELD/fb_reel_1005am.mp4',1,'f1'),vf(O+'facebook_HELD/fb_reel_1005am.mp4',4,'f2'),O+'facebook_HELD/fb_post_w5_625pm.jpg'])]
w,h=200,356;W=2150
sheet=Image.new('RGB',(W,40+len(rows)*(h+50)),(25,25,28));d=ImageDraw.Draw(sheet)
for r,(t,fs) in enumerate(rows):
    y=10+r*(h+50);d.text((8,y),t,font=F,fill='white')
    x=8
    for f in fs:
        im=Image.open(f).convert('RGB');s=min(w/im.width,h/im.height);im=im.resize((int(im.width*s),int(im.height*s)))
        sheet.paste(im,(x,y+38));x+=im.width+8
sheet.save(O+'overview.jpg',quality=88);print(sheet.size)
