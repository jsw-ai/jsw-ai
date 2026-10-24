import json,subprocess,sys
sys.argv=['x','v4/cfg_yt1.json']
src=open('v4/build4.py').read()
# reuse build but skip segment re-encode: monkeypatch run for seg steps
import builtins
exec(src.split('for f in sys.argv')[0])
cfg=json.load(open('v4/cfg_yt1.json'))
_run=run
def run(c):
    if c[-1].startswith('seg/'): print('skip',c[-1]); return
    _run(c)
build(cfg)
