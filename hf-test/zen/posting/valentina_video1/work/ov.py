import subprocess,textwrap
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
caps=["pretty sure I know what you're about to say","market run, I laughed for like five minutes","wait wait let me finish the story","you can't tell me this was the last copy","caught myself smiling at a text","the sun was SO bright but worth it","quiet minute before the last set, now watch it again"]
st="borderw=4:bordercolor=black@0.8:fontcolor=white"
vf=[f"drawtext=fontfile={F}:textfile=hook.txt:fontsize=54:{st}:line_spacing=12:x=(w-text_w)/2:y=150:enable='lt(t,2.5)'"]
for i,c in enumerate(caps):
    open(f"c{i}.txt","w").write(textwrap.fill(c,26))
    s=2.5 if i==0 else i*2+0.15; e=i*2+1.95
    sz=46
    vf.append(f"drawtext=fontfile={F}:textfile=c{i}.txt:fontsize={sz}:{st}:x=(w-text_w)/2:y=1500:enable='between(t,{s},{e})'")
vf.append("noise=alls=6:allf=t,unsharp=3:3:0.4")
subprocess.check_call(["ffmpeg","-y","-v","error","-i","cat.mp4","-i","beat.wav","-vf",",".join(vf),"-map","0:v","-map","1:a","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-map_metadata","-1","-movflags","+faststart","../valentina_montage_9x16.mp4"])
ts=[0.5,1.5,3,5,7,9,11,13,13.9]
from PIL import Image
im=Image.new('RGB',(270*9,480))
for i,t in enumerate(ts):
    subprocess.check_call(["ffmpeg","-y","-v","error","-ss",str(t),"-i","../valentina_montage_9x16.mp4","-frames:v","1","-vf","scale=270:480","m.png"])
    im.paste(Image.open("m.png"),(270*i,0))
im.save("msheet.png")
