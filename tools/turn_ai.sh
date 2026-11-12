#!/bin/bash
set -e
cd "$(dirname "$0")/.."; FF=/c/ffmpeg/bin/ffmpeg; T=C:/Users/PCMOD/AppData/Local/Temp/claude/0f02a2e5dba35198/8da862dc-b9dc-425a-8deb-bd0c7ab53786/scratchpad/hq
one() { i=$1
  rm -rf $T/png-$i; python tools/can_turn_ai.py $T/A60-$i.mp4 raw/masks/can-$i.png $T/png-$i
  $FF -v error -y -framerate 60 -i $T/png-$i/c_%03d.png -c:v libvpx-vp9 -pix_fmt yuva420p -crf 20 -b:v 0 -deadline good -cpu-used 1 -row-mt 1 -auto-alt-ref 0 -an assets/turn-$i.webm
  $FF -v error -y -framerate 60 -i $T/png-$i/c_%03d.png -vf scale=320:-2 -c:v libvpx-vp9 -pix_fmt yuva420p -crf 30 -b:v 0 -deadline good -cpu-used 2 -row-mt 1 -auto-alt-ref 0 -an assets/turn-m-$i.webm
  python -c "
from PIL import Image; import glob
fs=sorted(glob.glob('$T/png-$i/*.png'))[::4]
for k,f in enumerate(fs): Image.open(f).save('assets/turn-$i/c_%03d.webp'%(k+1), quality=88)
print('turn $i frames', len(fs), Image.open(fs[0]).size)"
}
for i in 1 2 3 4; do one $i & done; wait; echo ALLDONE
