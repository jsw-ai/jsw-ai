import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
from PIL import Image,ImageDraw
def crop(p,S=420):
    im=cv2.imread(p); f,(W,H)=g.faces(im)
    sc=1.0
    if max(im.shape[:2])>1280: sc=1280/max(im.shape[:2])
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    x0,y0,x1,y1=[v/sc for v in x.bbox]; cx,cy=(x0+x1)/2,(y0+y1)/2; s=(x1-x0)*1.9
    a=int(max(cx-s/2,0));b=int(max(cy-s/2,0));c=int(min(cx+s/2,im.shape[1]));d=int(min(cy+s/2,im.shape[0]))
    return Image.fromarray(cv2.cvtColor(cv2.resize(im[b:d,a:c],(S,S)),cv2.COLOR_BGR2RGB))
def sheet(items,out,cols=5):
    S=420;rows=(len(items)+cols-1)//cols
    c=Image.new('RGB',(S*cols,(S+24)*rows),'white');d=ImageDraw.Draw(c)
    for i,(lab,p) in enumerate(items):
        x=(i%cols)*S;y=(i//cols)*(S+24)
        c.paste(crop(p,S),(x,y+24));d.text((x+4,y+6),lab,fill='black')
    c.save(out,quality=90)
if __name__=='__main__':
    P='/workspace/hf-test/zen/posting/'
    items=[('NEW a','a.png'),('NEW b','b.png'),('test2 balcony',P+'valentina_test2/fin/s2_b_v4C.jpg'),('test2 cafe',P+'valentina_test2/fin/s1_a_v4C.jpg'),('test2 kitchen',P+'valentina_test2/fin/s8_a_v4C.jpg'),
    ('cafe vid f2.5',P+'valentina_video3/work/f2.5.png'),('cafe vid f4',P+'valentina_video3/work/f4.png'),('cafe vid f7.8',P+'valentina_video3/work/f7.8.png'),('REJECTED v4',P+'valentina_video4_x/work/f3.png'),('cover',P+'valentina_refs/valentina_cover.jpg')]
    sheet(items,'faces1.jpg')
