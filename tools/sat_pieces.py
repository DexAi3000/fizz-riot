import sys, os, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
for f in os.listdir(out): os.remove(os.path.join(out, f))
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
mx, mn = im.max(2), im.min(2); sat = (mx - mn) / (mx + 1)
m = (sat > float(os.environ.get("ST",".16"))) | (mn < 120)          # coloured or dark (seeds, ginger skin)
m = nd.binary_opening(m, iterations=1); m = nd.binary_closing(m, iterations=3); m = nd.binary_fill_holes(m)
lab, n = nd.label(m); objs = nd.find_objects(lab)
areas = nd.sum(m, lab, range(1, n+1))
med = np.median(areas[areas > 4000]) if (areas > 4000).any() else 1
k = 0
for i, sl in enumerate(objs):
    a = areas[i]
    if a < 4000 or a > med * 7: continue
    y0, y1, x0, x1 = sl[0].start-4, sl[0].stop+4, sl[1].start-4, sl[1].stop+4
    crop = Image.fromarray(im[y0:y1, x0:x1].astype(np.uint8))
    obj = lab[y0:y1, x0:x1] == i+1
    ss = sat[y0:y1, x0:x1]; v = mx[y0:y1, x0:x1]
    core = obj & ((ss > np.median(ss[obj]) * float(os.environ.get('KS', '.55'))) | (v < 150))
    core = nd.binary_opening(core, iterations=2); lb, nn = nd.label(core)
    if nn: core = lb == (np.argmax(nd.sum(core, lb, range(1, nn+1))) + 1)
    core = nd.binary_fill_holes(core)
    al = Image.fromarray((core * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.1))
    crop.putalpha(al); crop.thumbnail((220, 220), Image.LANCZOS)
    k += 1; crop.save(f'{out}/p{k}.webp', quality=86)
print(src, k)
