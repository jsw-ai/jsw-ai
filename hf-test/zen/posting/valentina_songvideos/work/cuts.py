import sys;sys.path.insert(0,'.');from build import *;from win import best,C,P
VS={k:P+v for k,v in dict(B3a='valentina_oct22/fin/B3a_v4C.jpg',H1='valentina_oct22/fin/H1_v4C.jpg',F1='valentina_oct22/fin/F1_v4C.jpg',s6_a='valentina_test2/fin/s6_a_v4C.jpg',s7_a='valentina_test2/fin/s7_a_v4C.jpg',s2_b='valentina_test2/fin/s2_b_v4C.jpg',s5_a='valentina_test2/fin/s5_a_v4C.jpg',b3='valentina_batch1/fin/b3_v4C.jpg',b6='valentina_batch1/fin/b6_v4C.jpg',b7='valentina_batch1/fin/b7_v4C.jpg',b8r='valentina_batch1/fin/b8r_v4C.jpg',b2='valentina_batch1/fin/b2_v4C.jpg').items()}
def mk(names,dur):
    n=len(names);fr=[round(dur*30*(i+1)/n)-round(dur*30*i/n) for i in range(n)];sh=[]
    for i,(k,f) in enumerate(zip(names,fr)):
        d=f/30; mo='in' if i%2==0 else 'out'; px=[0.5,0.3,0.7][i%3]
        if k in C:
            mn,md,ss=best(k,d+0.05); sh.append(dict(k='clip',scene=k,src=P+C[k],d=d,ss=ss,note=f'window gate min {mn:.3f} med {md:.3f}'))
        elif k in VS: sh.append(dict(k='still',scene=k,src=VS[k],d=d,mo=mo,px=px,py=0.25,zr=0.09))
        else: sh.append(dict(k='still',scene=k,src='hfin/'+k+('.jpg' if k.startswith('sc_') else '_v4C.jpg'),d=d,mo=mo,px=px,py=0.3,zr=0.07))
    return sh
w=sys.argv[1]
if w=='hook': render('valentina_fuego_lento_hook_21s_9x16_v3',mk(['b3','kB1','kA2','kS2pool','kB2','b2','rk3','b6','tt3','s5_a','rk2','b8r','b7'],21.0),1080,1920,45.0,21.0,[],2.6,17.0,'4500k','6M')
if w=='x': render('valentina_fuego_lento_X_24s_9x16_v3',mk(['rk2','kS2pool','kA2','kB1','b6','kB2','b3','tt3','b8r','s5_a','s2_b','b7','b2'],24.0),1080,1920,50.28,24.0,[],3.0,20.0,'4000k','6M')
if w=='yt': render('valentina_fuego_lento_youtube_21s_16x9_v2',mk(['h_s6_a','sc_street','h_b3','h_s5_a','sc_rooftop','h_b8r','sc_dress','sc_wall'],21.0),1920,1080,45.0,21.0,[],2.6,17.0,'5000k','6M')
