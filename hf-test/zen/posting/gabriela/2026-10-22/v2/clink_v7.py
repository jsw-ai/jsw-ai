import sys,subprocess; sys.path.insert(0,'edit'); from mk2 import txt_png
txt_png(['São Paulo: saúde!'],'edit/clink_v7_t0.png',ty=1306)
out='collab/gabriela_collab_oktoberfest_clink_v7_silent.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-t','5.033','-i','v2/k/kv2_clink7.mp4','-loop','1','-t','5.033','-i','edit/clink_v7_t0.png','-filter_complex',
 '[0:v]fps=30,setsar=1,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
 '-map','[o]','-an','-t','5.033','-r','30','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','20','-preset','medium','-threads','2','-movflags','+faststart','-map_metadata','-1',out],check=True)
print(out)
