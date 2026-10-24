import json
from ayr import *
dels=[('madison','PNpSJgN8AJDO6aStO7oU'),('madison','ZwD2mBGxVxSvWWGF4a1H'),('valentina','veWypF8lyJBGqUPIrXKk'),
('madison','qE7YCHAfOdo0z3weck67'),('madison','2lkDztcV03L72zhiaAiH'),('madison','P3gOHMKirNgEtyOQW0aG'),
('valentina','tUArYEXP2wNauiKwb3WJ'),('valentina','Uosb7SNdDM00htasG3dt'),('valentina','JVlyiBLQ2pZPuYQ9CwPc'),
('sienna','YzV1ZAQEiPjsoeBplCmV'),('sienna','SmPbLEiJZQDstmZkXIJn'),('sienna','YlhXgi23x51lCzAZnQPq'),('sienna','pomBuuwPJVvXz7zuFBLl'),
('sienna','FCoB08pJcFYZfJtUml5O'),('sienna','z2ogC6KlUBZK4roTasYa'),('sienna','LyO82pUsqC61NEhmrx5N'),
('charlotte','BXjybRhw21LHFW9tM6yK'),('charlotte','2tofbOD0MUV7YNTBZz7B')]
log={}
for m,i in dels:
    r=delete(m,'/post',{'id':i}); log[i]=(r.status_code,r.text[:200]); print(m,i,r.status_code,r.text[:150])
r=requests.patch(A+'/post',headers=H('charlotte'),json={'id':'dDc7WBVCTffdBEK7rc8p','scheduleDate':'2026-10-23T19:00:00Z'},timeout=60)
log['dDc7_patch']=(r.status_code,r.text[:300]); print('patch dDc7',r.status_code,r.text[:200])
# Valentina snNY -> IG only
r=delete('valentina','/post',{'id':'snNYfbYKoPtXI5pWySna'}); print('del snNY',r.status_code,r.text[:150]); log['snNY_del']=(r.status_code,r.text[:200])
body={'post':"mami said home by 11. she didn't say WHICH 11 💃🔥\n\nMusic: Kevin MacLeod",'platforms':['instagram'],
 'mediaUrls':['https://media.ayrshare.com/a7c6402e66f7d9078c664d96c2fa224e9fc05ccd/rpiILXFhptlLhcDfKYymU.mp4'],
 'isVideo':True,'scheduleDate':'2026-10-23T01:00:00Z','instagramOptions':{'isAIGenerated':True,'shareReelsFeed':True}}
r=post('valentina','/post',body); print('create snNY IG',r.status_code,r.text[:400]); log['snNY_new']=(r.status_code,r.text[:500])
json.dump(log,open('act_1822_log.json','w'),indent=1)
