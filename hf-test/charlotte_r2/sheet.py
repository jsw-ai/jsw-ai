import sys
from PIL import Image,ImageDraw
def sheet(items,out,cols=4,w=420):
    ims=[]
    for lab,p in items:
        im=Image.open(p).convert('RGB');h=round(im.height*w/im.width);im=im.resize((w,h));d=ImageDraw.Draw(im);d.rectangle([0,0,150,22],fill=(0,0,0));d.text((4,4),lab,fill=(255,255,255));ims.append(im)
    H=max(i.height for i in ims);rows=(len(ims)+cols-1)//cols
    S=Image.new('RGB',(cols*w,rows*H),(255,255,255))
    for k,i in enumerate(ims):S.paste(i,((k%cols)*w,(k//cols)*H))
    S.save(out,quality=88)
if __name__=='__main__':
    a=sys.argv[1:];sheet([(x.split('/')[-1][:-4],x) for x in a[1:]],a[0])
