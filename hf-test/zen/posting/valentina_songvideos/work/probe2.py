import sys,cv2;sys.path.insert(0,'.');from fgate import score
for v in ['hraw/h_b3.png','hfin/h_b3_v4C.jpg','hraw/h_b8r.png','hfin/h_b8r_v4C.jpg']: print(v,score(cv2.imread(v)),flush=True)
