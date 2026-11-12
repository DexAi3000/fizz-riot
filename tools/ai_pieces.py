"""Fruit pieces from a flat-lay photo with an AI mask (rembg isnet). Drops ice (unsaturated) and, with SINGLE=1, clusters."""
import sys, os, glob, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
from rembg import remove, new_session
src, out = sys.argv[1], sys.argv[2]; single = os.environ.get('SINGLE') == '1'
os.makedirs(out, exist_ok=True)
for f in glob.glob(out + '/*.webp'): os.remove(f)
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.float32)
m = np.asarray(remove(im, session=new_session('isnet-general-use'), only_mask=True)).astype(np.float32)
hard = m > 128; lab, n = nd.label(hard); objs = nd.find_objects(lab)
mx, mn = a.max(2), a.min(2); sat = (mx - mn) / (mx + 1)
areas = nd.sum(hard, lab, range(1, n + 1)); big = areas[areas > 3000]
med = np.median(big) if len(big) else 1
k = 0
for i, sl in enumerate(objs):
    ar = areas[i]
    if ar < 3000: continue
    obj = lab[sl] == i + 1
    if sat[sl][obj].mean() < .14: continue                      # ice / shadows
    h, w = obj.shape; fill = ar / (h * w); asp = max(h, w) / min(h, w)
    if single and (asp > 1.25 or fill < .68 or ar > med * 1.6): continue   # clusters, sprigs
    y0, y1, x0, x1 = max(0, sl[0].start - 4), sl[0].stop + 4, max(0, sl[1].start - 4), sl[1].stop + 4
    al = np.where(lab[y0:y1, x0:x1] == i + 1, m[y0:y1, x0:x1], 0).astype(np.uint8)
    alpha = Image.fromarray(al).filter(ImageFilter.MinFilter(3))
    crop = im.crop((x0, y0, x1, y1)); crop.putalpha(alpha); crop.thumbnail((240, 240), Image.LANCZOS)
    k += 1; crop.save(f'{out}/q{k:02d}.webp', quality=90)
print(src, k)
