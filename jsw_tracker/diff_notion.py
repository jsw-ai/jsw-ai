import json,datetime as dt
posts=json.load(open('out/posts.json')); rows=json.load(open('out/notion_posts_now.json'))
def norm(u): return (u or '').rstrip('/').replace('/reels/','/reel/').replace('/p/','/reel/').replace('twitter.com','x.com').lower()
byurl={norm(r['Post URL']):r for r in rows}
new,upd,fbcand=[],[],[]
for p in posts:
    r=byurl.get(norm(p['url']))
    if not r and p['platform']=='Facebook':
        # match by date + views to an existing FB row of the same model
        for q in rows:
            if q['Model']==p['model'] and 'facebook.com' in (q['Post URL'] or '') and q['posted'] and p['created'] and q['posted'][:16].replace(' ','T')==p['created'][:16]:
                r=q; fbcand.append((p['url'],q['Post URL'])); break
    if not r:
        new.append(p); continue
    ch={}
    for k,pk in (('Views','views'),('Likes','likes'),('Comments','comments'),('Shares','shares')):
        v=p[pk]
        if v is not None and v!=r[k]: ch[k]=[r[k],v]
    if ch: upd.append({'page':r['url'],'model':p['model'],'platform':p['platform'],'url':p['url'],'ch':ch})
json.dump({'new':new,'upd':upd,'fbmatch':fbcand},open('out/diff.json','w'),indent=1,ensure_ascii=False)
print('NEW',len(new))
for p in new: print(' ',p['model'],p['platform'],p['url'],p['created'],p['views'],p['likes'],(p['text'] or '')[:70])
print('UPD',len(upd))
for u in upd: print(' ',u['model'],u['platform'],u['url'][-40:],u['ch'])
print('FBMATCH',fbcand)
