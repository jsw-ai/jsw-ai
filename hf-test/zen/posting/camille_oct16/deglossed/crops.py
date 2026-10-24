import cv2,numpy as np,sys
sys.path.insert(0,'.')
from pp import facebox
from PIL import Image
for n in (4,2,7,6):
    fs=[f'../stills/camille_s{n}.jpg',f'raw/pp_orig{n}.png',f'raw/g{n}.png',f'raw/pp_g{n}.png']
    row=[]
    for f in fs:
        im=cv2.imread(f)
        if f==fs[0]: b=facebox(im); 
        x0,y0,x1,y1=[int(v) for v in b];w=x1-x0;c=im[max(0,y0-int(w*.3)):y1+int(w*.2),max(0,x0-int(w*.3)):x1+int(w*.3)]
        row.append(cv2.resize(c,(450,520)))
    cv2.imwrite(f'raw/crop{n}.jpg',np.hstack(row))
