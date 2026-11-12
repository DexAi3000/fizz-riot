"""Cut a rotating can out of a turntable clip with a FIXED cylinder-silhouette mask (a spinning can's
outline never changes). Measures body L/R/top/bottom from saturation, adds lid + bottom tapers."""
import sys, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter
src, out = sys.argv[1], sys.argv[2]; every = int(sys.argv[3]) if len(sys.argv) > 3 else 1
OW = int(os.environ.get('OW', '360')); Q = int(os.environ.get('Q', '82')); EXT = os.environ.get('EXT', 'webp')
os.makedirs(out, exist_ok=True)
raw = subprocess.run(['C:/ffmpeg/bin/ffmpeg','-v','error','-i',src,'-vf','fps=3','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1,1080,1920,3)  # sample for measuring only
acc = np.zeros((1080,1920), np.int32)
for im in fr:
    a = im.astype(np.int16); acc += ((a.max(2)-a.min(2)) > 60)
m = acc > len(fr)*0.5
cols = np.where(m.sum(0) > 300)[0]; L, R = cols.min()-2, cols.max()+2
rows = np.where(m[:, L+40:R-40].mean(1) > .5)[0]; T, B = rows.min(), rows.max()
w = R-L; cx = (L+R)/2; hw = w/2
print(src, 'L R T B', L, R, T, B)
import math
SS = 4
def P(x, y): return (x*SS, y*SS)
pts = []
prof = [(0, -.02), (.03, -.005), (.052, .005), (.07, .022), (.09, .044), (.13, .072), (.2, .088), (.3, .094), (.5, .097)]  # (inset, dy) in can widths
pts.append((cx+hw-.022*w, T-.052*w)); pts.append((cx+hw-.006*w, T+.01*w)); pts.append((cx+hw, T+.05*w))
for ins, dy in prof: pts.append((cx+hw-ins*w, B+dy*w))
for ins, dy in reversed(prof[:-1]): pts.append((cx-hw+ins*w, B+dy*w))
pts.append((cx-hw, T+.05*w)); pts.append((cx-hw+.006*w, T+.01*w)); pts.append((cx-hw+.022*w, T-.052*w))
ex2 = hw-.022*w; ty = T-.052*w; rise = .05*w
for k in range(1, 40):
    t = math.pi*k/40; pts.append((cx-ex2*math.cos(t), ty-rise*math.sin(t)))
mk = Image.new('L', (1920*SS, 1080*SS), 0); ImageDraw.Draw(mk).polygon([P(x, y) for x, y in pts], fill=255)
mk = mk.resize((1920, 1080), Image.LANCZOS)
# refine the base: inside the outline, below the band, keep pixels darker / more coloured than the backdrop
med = np.median(fr.astype(np.int16), 0)
side = np.r_[80:600, 1350:1650]; bgc = np.median(med[:, side], 1)
dark = (bgc[:, None, :] - med).mean(2); sat = med.max(2) - med.min(2)
poly = np.asarray(mk) > 127; y0 = int(B - .09*w)
keep = (dark > 9) | (sat > 28)
from scipy import ndimage as nd
reg = poly.copy(); reg[y0:] &= keep[y0:]
reg = nd.binary_opening(reg, iterations=2); reg = nd.binary_closing(reg, iterations=3)
for y in range(y0, 1080):  # solid rows, never wider than the row above
    xs = np.where(reg[y])[0]
    if len(xs) < 6: reg[y:] = False; break
    a0, a1 = xs.min(), xs.max()
    prev = np.where(reg[y-1])[0]
    if len(prev): a0, a1 = max(a0, prev.min()), min(a1, prev.max())
    reg[y] = False; reg[y, a0:a1+1] = True
mk = Image.fromarray((reg*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: 255 if v > 150 else (0 if v < 40 else int((v-40)*255/110)))
mk = mk.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.7))
lid = .11*w; bot = .1*w
box = (int(L-6), int(T-lid-6), int(R+6), int(B+bot+6))
mkc = mk.crop(box)
OH = round(OW*(box[3]-box[1])/(box[2]-box[0]))
proc = subprocess.Popen(['C:/ffmpeg/bin/ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
FS = 1080*1920*3; k = n = 0
while True:
    buf = proc.stdout.read(FS)
    if len(buf) < FS: break
    if n % every == 0:
        im = np.frombuffer(buf, np.uint8).reshape(1080,1920,3)
        rgba = Image.fromarray(im).crop(box); rgba.putalpha(mkc)
        k += 1; rgba.resize((OW, OH), Image.LANCZOS).save(f'{out}/c_{k:03d}.{EXT}', quality=Q)
    n += 1
print('done', k, OW, OH)
