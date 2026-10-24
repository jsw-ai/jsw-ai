import sys,subprocess,os
from PIL import Image, ImageDraw
out=sys.argv[1]; vids=sys.argv[2:]
H=400; rows=[]
ref=Image.open('/workspace/hf-test/keepers/charlotte_face_keeper.png').convert('RGB'); ref=ref.resize((int(ref.width*H/ref.height),H))
for v in vids:
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v]))
    ts=[0.1,d*0.2,d*0.4,d*0.6,d*0.8,d-0.1]; tiles=[ref]
    for t in ts:
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',v,'-frames:v','1','/workspace/hf-test/charlotte_1022/work/seg/q.png'])
        im=Image.open('/workspace/hf-test/charlotte_1022/work/seg/q.png').convert('RGB'); im=im.resize((int(im.width*H/im.height),H))
        ImageDraw.Draw(im).text((4,4),'%.1fs'%t,fill='yellow'); tiles.append(im)
    r=Image.new('RGB',(sum(t.width for t in tiles),H)); x=0
    for t in tiles: r.paste(t,(x,0)); x+=t.width
    ImageDraw.Draw(r).text((4,H-14),os.path.basename(v)[10:60],fill='red'); rows.append(r)
S=Image.new('RGB',(max(r.width for r in rows),H*len(rows)),'white')
for i,r in enumerate(rows): S.paste(r,(0,i*H))
S.save(out,quality=85)
