import glob, os, subprocess, shutil, time
BLOCK = '''
    location = /org { return 301 /org/; }
    location /org/ {
        proxy_pass http://127.0.0.1:5061/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Prefix /org;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
'''
target = None
for f in glob.glob('/etc/nginx/sites-enabled/*'):
    try:
        txt = open(f).read()
    except Exception:
        continue
    if 'server_name _;' in txt and '/var/www/html' in txt:
        target = f; break
if not target:
    for f in glob.glob('/etc/nginx/sites-enabled/*'):
        if 'server_name _;' in open(f).read():
            target = f; break
print('TARGET', target)
if not target:
    raise SystemExit('no catch-all server found')
txt = open(target).read()
if 'location /org/' in txt:
    print('ALREADY_PATCHED'); raise SystemExit(0)
BAKDIR = '/opt/jsw-ai/org/nginx_backups'
os.makedirs(BAKDIR, exist_ok=True)
bak = os.path.join(BAKDIR, os.path.basename(target) + '.bak.' + str(int(time.time())))
shutil.copy(target, bak)
anchor = 'root /var/www/html;' if 'root /var/www/html;' in txt else 'server_name _;'
idx = txt.index(anchor) + len(anchor)
open(target, 'w').write(txt[:idx] + '\n' + BLOCK + txt[idx:])
r = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
print('NGINX_T', r.returncode, (r.stderr or '')[-200:])
if r.returncode == 0:
    subprocess.run(['systemctl', 'reload', 'nginx'])
    print('RELOADED')
else:
    shutil.copy(bak, target)
    print('RESTORED_ON_ERROR')
