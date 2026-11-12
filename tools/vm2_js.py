import pathlib
r = pathlib.Path(__file__).resolve().parent.parent
p = r / 'src/app.js'; s = p.read_text(encoding='utf-8')

# ---------------- vending machine on the photo ----------------
a = s.index("/* ============ vending machine ============ */"); b = s.index("/* ============ footer letters ============ */")
js = r'''/* ============ vending machine (photo) ============ */
// coordinates measured on assets/vm.webp (990 x 1708)
const VM = { W: 990, H: 1708, win: [89, 295, 754, 1240], shelves: [573, 870, 1165], cols: [189, 309, 424, 539, 654], led: [804, 472, 912, 548], btn: { x: 857, ys: [645, 745, 845, 945], r: 38 }, chute: [420, 1470] };
const pct = (v, t) => (v / t * 100) + '%';
const packEl = $('#pack'), vm = $('#vm'), led = $('#led'), shakeBtn = $('#shake'), vmwin = $('#vmwin'), vbtns = $('#vbtns');
Object.assign(vmwin.style, { left: pct(VM.win[0], VM.W), top: pct(VM.win[1], VM.H), width: pct(VM.win[2] - VM.win[0], VM.W), height: pct(VM.win[3] - VM.win[1], VM.H) });
Object.assign(led.style, { left: pct(VM.led[0], VM.W), top: pct(VM.led[1], VM.H), width: pct(VM.led[2] - VM.led[0], VM.W), height: pct(VM.led[3] - VM.led[1], VM.H) });
const pack = new Play($('#world2'), $('#fx2'), { mouseEl: packEl, floor: .025 });
const COLS = [0, 1, 2, 3, 0];            // 5 coils: four flavours + an assorted fifth column (decor)
const DECOR = [2, 3, 1];
const stock = [3, 3, 3, 3];
let picked = 0, floorCans = [], busy = false;
const slots = [[], [], []];           // slots[row][col] = img
const winW = VM.win[2] - VM.win[0], winH = VM.win[3] - VM.win[1];
for (let row = 0; row < 3; row++) VM.cols.forEach((cx, c) => {
  const fi = c < 4 ? c : DECOR[row];
  const h = 228, w = h * CAN_AR[fi];
  const im = new Image(); im.src = can(fi); im.alt = ''; im.className = 'vcan'; im.draggable = false;
  Object.assign(im.style, { left: pct(cx - VM.win[0] - w / 2, winW), top: pct(VM.shelves[row] - 8 - h - VM.win[1], winH), width: pct(w, winW), height: pct(h, winH) });
  vmwin.appendChild(im); slots[row][c] = im;
});
FL.forEach((f, i) => {
  const b = document.createElement('button'); b.className = 'vbtn'; b.style.setProperty('--c', f.c);
  Object.assign(b.style, { left: pct(VM.btn.x, VM.W), top: pct(VM.btn.ys[i], VM.H), width: pct(VM.btn.r * 2, VM.W), aspectRatio: '1' });
  b.innerHTML = `<span class="lbl">${f.name.join('')} ${f.sub}</span>`;
  b.setAttribute('aria-label', `Get a ${f.name.join('')} ${f.sub}`);
  b.onclick = () => vend(i, b); vbtns.appendChild(b);
});
function setLed(t, blink) { led.innerHTML = t; led.classList.toggle('blink', !!blink); }
function updLed() {
  if (picked >= 4) { setLed('SHAKE<br>IT!', true); shakeBtn.disabled = false; shakeBtn.classList.add('go'); }
  else { setLed(`PICK 4<br>${picked}/4`); shakeBtn.disabled = true; shakeBtn.classList.remove('go'); }
}
function chutePoint() {
  const r = vm.getBoundingClientRect(), s = packEl.getBoundingClientRect();
  return { x: r.left - s.left + r.width * VM.chute[0] / VM.W, y: r.top - s.top + r.height * VM.chute[1] / VM.H, w: r.width * .5 };
}
function vend(i, btn) {
  pack.start(); pack.visible = true;
  btn.classList.add('press'); setTimeout(() => btn.classList.remove('press'), 160);
  if (busy) return;
  if (stock[i] === 0) { setLed('SOLD<br>OUT', true); setTimeout(updLed, 1200); return; }
  busy = true;
  const row = stock[i] - 1; stock[i]--;           // bottom shelf first
  const im = slots[row][i];
  packEl.style.setProperty('--g', FL[i].c);
  setLed(FL[i].name.join('').slice(0, 9) + '<br>♪');
  const wr = vmwin.getBoundingClientRect(), ir = im.getBoundingClientRect();
  const fall = wr.bottom - ir.top + 10;
  gsap.timeline({ onComplete: () => { gsap.set(im, { opacity: 0 }); dispense(i); } })
    .to(im, { x: 0, rotation: -4, duration: .12, ease: 'power1.inOut', repeat: 3, yoyo: true })   // the coil turns
    .to(im, { y: -6, scale: 1.05, rotation: 0, duration: .2, ease: 'power2.out' })
    .to(im, { y: fall, rotation: gsap.utils.random(-30, 30), duration: .5, ease: 'power2.in' });
  if (stock[i] === 0) btn.classList.add('out');
}
function dispense(i) {
  vm.classList.add('opened'); setTimeout(() => vm.classList.remove('opened'), 520);
  gsap.fromTo(vm, { y: 0 }, { y: 4, duration: .06, yoyo: true, repeat: 3, ease: 'none', clearProps: 'y' });
  const c = chutePoint(), h = Math.min(pack.H * (PHONE() ? .15 : .21), 200), w = h * CAN_AR[i];
  const im = new Image(); im.src = can(i); im.alt = ''; im.draggable = false; im.className = 'can';
  const it = pack.add(im, w, h, c.x, c.y, { sx: .9, sy: .97, rot: 0, den: .003, rest: .32 });
  M.Body.setAngle(it.body, Math.PI / 2);
  const dir = Math.random() < .5 ? -1 : 1;
  M.Body.setVelocity(it.body, { x: dir * (6 + Math.random() * 6), y: -4 - Math.random() * 3 });
  M.Body.setAngularVelocity(it.body, dir * (.12 + Math.random() * .15));
  floorCans.push(it);
  while (floorCans.length > 8) pack.remove(floorCans.shift());
  for (let k = 0; k < 3; k++) {
    const pi = new Image(); pi.src = piece(i, 1 + Math.floor(Math.random() * FL[i].pieces)); pi.alt = ''; pi.className = 'pc';
    pi.onload = () => { const s = PHONE() ? .22 : .3; const p = pack.add(pi, pi.naturalWidth * s, pi.naturalHeight * s, c.x, c.y, { sx: .78, sy: .78, ch: .4, rot: 6, den: .0008, rest: .5 }); M.Body.setVelocity(p.body, { x: (Math.random() - .5) * 18, y: -8 - Math.random() * 6 }); p.extra = true; trimPieces(); };
  }
  pack.fx.burst(c.x, c.y, 16, FL[i].c);
  picked = Math.min(4, picked + 1); busy = false; updLed();
}
function trimPieces() { const ex = pack.items.filter(i => i.extra); while (ex.length > 24) pack.remove(ex.shift()); }
shakeBtn.onclick = () => {
  gsap.timeline().to(vm, { rotation: -3, duration: .08 }).to(vm, { rotation: 3, duration: .1, repeat: 5, yoyo: true }).to(vm, { rotation: 0, duration: .6, ease: 'elastic.out(1,.3)' });
  slots.flat().forEach(im => gsap.fromTo(im, { rotation: 0 }, { rotation: gsap.utils.random(-12, 12), duration: .09, repeat: 7, yoyo: true }));
  const c = chutePoint(); let n = 0;
  const iv = setInterval(() => { pack.pop(c.x + (Math.random() - .5) * pack.W * .5, pack.H, 1.5, FL[n % 4].c); if (++n > 5) clearInterval(iv); }, 130);
  setLed('RIOT!!', true); setTimeout(() => { picked = 0; updLed(); }, 2200);
};
$('#clear').onclick = () => {
  [...pack.items].forEach(it => pack.remove(it)); floorCans = []; picked = 0; stock.fill(3);
  slots.flat().forEach((im, k) => gsap.fromTo(im, { opacity: 0, y: -20, scale: .7, rotation: 0 }, { opacity: 1, y: 0, scale: 1, duration: .8, ease: 'elastic.out(1,.5)', delay: k * .025 }));
  vbtns.querySelectorAll('.vbtn').forEach(b => b.classList.remove('out'));
  updLed();
};
new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) pack.start(); }), { threshold: .2 }).observe(packEl);

'''
s = s[:a] + js + s[b:]

# ---------------- loader: the can fills up ----------------
a = s.index("/* ============ preloader ============ */"); b = s.index("/* ============ bubbles fx ============ */")
pre = r'''/* ============ preloader: the can fills up ============ */
const pre = $('#pre'), preNum = $('#preNum'), pcan = $('#pcan'), pfz = $('#pfz'), flood = $('#flood');
const PF = Math.floor(Math.random() * 4);
pcan.querySelectorAll('img').forEach(im => im.src = can(PF));
pcan.style.aspectRatio = `${CAN_AR[PF]}`;
pfz.style.setProperty('--m', `url(${can(PF)})`);
const pfull = pcan.querySelector('.full');
const pb = []; for (let k = 0; k < 16; k++) { const i = document.createElement('i'); const s = 4 + Math.random() * 9; Object.assign(i.style, { width: s + 'px', height: s + 'px', left: (14 + Math.random() * 72) + '%' }); pfz.appendChild(i); pb.push({ el: i, y: Math.random(), v: .12 + Math.random() * .25, s }); }
let preShown = 0, preTarget = 0;
function loadImg(src) { return new Promise(r => { const im = new Image(); im.decoding = 'async'; im.onload = im.onerror = () => r(im); im.src = src; }); }
const heroPieces = [];
FL.forEach((f, i) => { const n = PHONE() ? 4 : 7; for (let k = 0; k < n; k++) heroPieces.push([i, 1 + Math.floor(k * f.pieces / n)]); });
const preList = [...FL.map((f, i) => can(i)), ...heroPieces.map(([i, k]) => piece(i, k))];
let preDone = 0;
const fontsP = Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 2500))]);
const imgsP = Promise.all(preList.map(s => loadImg(s).then(im => { preDone++; preTarget = preDone / preList.length; return im; })));
let preLast = performance.now();
(function preTick(now) {
  const dt = Math.min(.05, (now - preLast) / 1000 || 0); preLast = now;
  preShown = Math.min(preTarget, preShown + Math.max(.004, (preTarget - preShown) * .08));
  preNum.textContent = Math.round(preShown * 100) + '%';
  // liquid surface: a gentle wave across the can, from the base (~4%) to just under the lid (~92%)
  const lvl = 96 - preShown * 88, t = now / 1000, pts = [];
  for (let x = 0; x <= 100; x += 5) pts.push(`${x}% ${(lvl + Math.sin(x * .12 + t * 4) * 1.1 + Math.sin(x * .05 - t * 2.6) * .7).toFixed(2)}%`);
  pfull.style.clipPath = `polygon(0% 100%, ${pts.join(',')}, 100% 100%)`;
  pb.forEach(b => { b.y -= b.v * dt; if (b.y * 100 < lvl - 96 + 100 - 100 + (100 - (100 - lvl)) - 100 + 4 || b.y < (lvl - 2) / 100) b.y = .97; b.el.style.top = (b.y * 100) + '%'; b.el.style.opacity = b.y * 100 > lvl ? .9 : 0; });
  if (!pre.classList.contains('done')) requestAnimationFrame(preTick);
})(performance.now());
Promise.race([Promise.all([fontsP, imgsP]), new Promise(r => setTimeout(r, 7000))]).then(() => {
  preTarget = 1;
  const wait = setInterval(() => {
    if (preShown < .999) return; clearInterval(wait);
    flood.style.background = FL[PF].c;
    const d = Math.hypot(innerWidth, innerHeight) / 10;
    gsap.timeline({ onComplete: () => pre.remove() })
      .to(pcan, { rotation: -6, duration: .07, repeat: 5, yoyo: true, ease: 'none' })
      .to(pcan, { rotation: 0, scale: 1.08, duration: .2, ease: 'back.out(3)' })
      .add(() => { $('#preLab').textContent = 'pssst!'; })
      .to(flood, { scale: d, duration: .75, ease: 'expo.in' }, '+=.05')
      .add(() => {
        pre.classList.add('done');
        document.body.classList.add('play'); document.body.classList.remove('anim');
        setTimeout(() => document.body.classList.remove('play'), 1400);
        hero.start();
      })
      .to(pre, { opacity: 0, duration: .55, ease: 'power2.out' });
  }, 60);
});

'''
s = s[:a] + pre + s[b:]
p.write_text(s, encoding='utf-8')
print('ok')
