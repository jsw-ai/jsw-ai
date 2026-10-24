import os, glob, re
base = '/opt/jsw-ai'
print('CONTENT_DIRS:')
for d in sorted(glob.glob(base + '/content/*')):
    if os.path.isdir(d):
        imgs = glob.glob(d + '/**/*.jpg', recursive=True) + glob.glob(d + '/**/*.png', recursive=True)
        print('  ', os.path.basename(d), len(imgs))
print('PERSONA_FILES:', [os.path.basename(f) for f in glob.glob(base + '/agents/*_persona.py')])
try:
    t = open(base + '/agents/sienna_persona.py').read()
    keys = sorted(set(re.findall(r'["\']([a-z_]{3,20})["\']\s*:', t)))
    print('SIENNA_KEYS:', keys[:40])
    print('SIENNA_LEN:', len(t))
except Exception as e:
    print('perr', e)
print('DASH_DATA:', [os.path.basename(f) for f in glob.glob(base + '/dashboard/*.json') + glob.glob(base + '/dashboard/*.db')])
for slug in ['sienna', 'charlotte', 'madison', 'camille', 'gabriela', 'valentina']:
    m = glob.glob(base + '/content/**/*' + slug + '*', recursive=True)
    print('PHOTOS_MATCH', slug, len(m), (os.path.dirname(m[0]) if m else ''))
