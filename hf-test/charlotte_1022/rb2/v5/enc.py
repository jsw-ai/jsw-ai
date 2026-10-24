import json,subprocess,sys
exec(open('v4/build4.py').read().split('for f in sys.argv')[0].replace("'-preset','slow'","'-preset','medium'"))
_run=run
def run(c):
    if c[-1].startswith('seg/') and not c[-1].endswith(('yt1v4_cat.mp4','x2v4_cat.mp4')) or 'concat' in c: print('skip',c[-1],flush=True); return
    if c[-1].startswith('seg/'): print('skip',c[-1],flush=True); return
    _run(c)
for f in sys.argv[1:]:
    cfg=json.load(open(f)); n=cfg['name']; build(cfg); print('done',cfg['out'],flush=True)
