"""Cut a turntable can with a fixed AI silhouette (raw/masks/can-N.png, median of rembg masks over 6 angles)."""
import sys, os, subprocess, numpy as np
from PIL import Image, ImageFilter
src, maskp, out = sys.argv[1], sys.argv[2], sys.argv[3]
OW = int(os.environ.get('OW', '400')); EXT = os.environ.get('EXT', 'png')
os.makedirs(out, exist_ok=True)
mk = Image.open(maskp).convert('L')
mk = mk.point(lambda v: 0 if v < 20 else (255 if v > 235 else v)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.6))
a = np.asarray(mk) > 128; ys, xs = np.where(a)
box = (int(xs.min() - 6), int(ys.min() - 6), int(xs.max() + 7), int(ys.max() + 7))
mkc = mk.crop(box); OH = round(OW * (box[3] - box[1]) / (box[2] - box[0]))
p = subprocess.Popen(['C:/ffmpeg/bin/ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
FS = 1080 * 1920 * 3; k = 0
while True:
    b = p.stdout.read(FS)
    if len(b) < FS: break
    im = Image.fromarray(np.frombuffer(b, np.uint8).reshape(1080, 1920, 3)).crop(box); im.putalpha(mkc)
    k += 1; im.resize((OW, OH), Image.LANCZOS).save(f'{out}/c_{k:03d}.{EXT}', quality=90)
print(src, 'done', k, OW, OH)
