import re,sys,subprocess
jobs={l.split()[1]:l.split()[0] for l in open('man/kling_jobs.tsv')}
for f in sys.argv[1:]:
    for u in re.findall(r'https://\S+?\.mp4',open(f).read()):
        jid=re.search(r'([0-9a-f-]{36})\.mp4',u).group(1)
        if jid in jobs:
            subprocess.run(['curl','-s','-o',f'clips/{jobs[jid]}.mp4',u]); print(jobs[jid])
