import sys,cv2
sys.path.insert(0,'../deglossed')
from pp2 import process
for n,s in [('ref_face_front','../refs/ref_face_front.jpg'),('ref_face_tq_matte','../refs/ref_face_tq_matte.jpg'),('ref_body_waistup','../refs/ref_body_waistup.jpg')]:
    img=cv2.imread(s);cv2.imwrite(n+'_loc.jpg',process(img,1.0),[cv2.IMWRITE_JPEG_QUALITY,93])
