import cv2,sys,numpy as np
sys.path.insert(0,'.')
import pp2
for n in (4,2,7,6):
    im=cv2.imread(f'raw/g{n}.png');o=pp2.process(im,0.8);cv2.imwrite(f'raw/gentle_g{n}.png',o)
    b=pp2.facebox(im);x0,y0,x1,y1=[int(v) for v in b];w=x1-x0
    c=lambda i:cv2.resize(i[max(0,y0-int(w*.3)):y1+int(w*.2),max(0,x0-int(w*.3)):x1+int(w*.3)],(450,520))
    cv2.imwrite(f'raw/gc{n}.jpg',np.hstack([c(cv2.imread(f'../stills/camille_s{n}.jpg')),c(im),c(o)]))
