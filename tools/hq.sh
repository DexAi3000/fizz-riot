#!/bin/bash
# 60 fps max-quality rebuild: turntables (alpha webm + safari frames) and splash frame sets (desktop + phone)
set -e
cd "$(dirname "$0")/.."; FF=/c/ffmpeg/bin/ffmpeg; T=/c/Users/PCMOD/AppData/Local/Temp/claude/0f02a2e5dba35198/8da862dc-b9dc-425a-8deb-bd0c7ab53786/scratchpad/hq; mkdir -p $T
MI="minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
turn() { i=$1
  $FF -v error -y -i raw/A-$i.mp4 -vf "delogo=x=1692:y=852:w=100:h=96,$MI" -c:v libx264 -crf 8 -preset fast -pix_fmt yuv444p $T/A60-$i.mp4
  rm -rf $T/png-$i; OW=400 EXT=png python tools/can_turn.py $T/A60-$i.mp4 $T/png-$i 1 > /dev/null
  $FF -v error -y -framerate 60 -i $T/png-$i/c_%03d.png -c:v libvpx-vp9 -pix_fmt yuva420p -crf 20 -b:v 0 -deadline good -cpu-used 1 -row-mt 1 -auto-alt-ref 0 -an assets/turn-$i.webm
  $FF -v error -y -framerate 60 -i $T/png-$i/c_%03d.png -vf scale=320:-2 -c:v libvpx-vp9 -pix_fmt yuva420p -crf 30 -b:v 0 -deadline good -cpu-used 2 -row-mt 1 -auto-alt-ref 0 -an assets/turn-m-$i.webm
  rm -rf assets/turn-$i; mkdir -p assets/turn-$i
  python -c "
from PIL import Image; import glob
fs=sorted(glob.glob('$T/png-$i/*.png'))[::4]
for k,f in enumerate(fs): Image.open(f).save('assets/turn-$i/c_%03d.webp'%(k+1), quality=88)
print('turn $i', len(fs))"
}
splash() { i=$1
  rm -rf assets/splash-$i assets/splash-m-$i; mkdir -p assets/splash-$i assets/splash-m-$i
  $FF -v error -y -i raw/B-$i.mp4 -vf "delogo=x=1692:y=852:w=100:h=96,$MI,scale=1600:-2:flags=lanczos" -c:v libwebp -quality 78 assets/splash-$i/f_%03d.webp
  $FF -v error -y -i raw/B-$i.mp4 -vf "delogo=x=1692:y=852:w=100:h=96,crop=640:1080:640:0,minterpolate=fps=48:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=540:912:flags=lanczos" -c:v libwebp -quality 66 assets/splash-m-$i/f_%03d.webp
  echo "splash $i $(ls assets/splash-$i | wc -l) $(ls assets/splash-m-$i | wc -l) $(du -sh assets/splash-$i | cut -f1) $(du -sh assets/splash-m-$i | cut -f1)"
}
for i in 1 2 3 4; do turn $i & done; wait
for i in 1 2; do splash $i & done; wait
for i in 3 4; do splash $i & done; wait
ls -la assets/*.webm; echo ALLDONE
