import pathlib
r = pathlib.Path(__file__).resolve().parent.parent
p = r / 'src/app.js'; s = p.read_text(encoding='utf-8')
a = s.index("/* ============ pack builder: the cooler ============ */"); b = s.index("/* ============ footer letters ============ */")
js = r'''/* ============ vending machine ============ */
const packEl = $('#pack'), vm = $('#vm'), led = $('#led'), shakeBtn = $('#shake'), chute = $('#chute'), flap = $('#flap');
const pack = new Play($('#world2'), $('#fx2'), { mouseEl: packEl });
const stock = [3, 3, 3, 3];
let picked = 0, floorCans = [], busy = false;
const vmwin = $('#vmwin'), vbtns = $('#vbtns');
const slotEls = [[], [], []];
for (let r = 0; r < 3; r++) {
  const row = document.createElement('div'); row.className = 'vrow';
  FL.forEach((f, i) => {
    const sl = document.createElement('div'); sl.className = 'slot';
    sl.innerHTML = `<img src="${can(i)}" alt=""><i class="coil"></i>`;
    row.appendChild(sl); slotEls[r][i] = sl;
  });
  vmwin.appendChild(row);
}
FL.forEach((f, i) => {
  const b = document.createElement('button'); b.className = 'vbtn'; b.style.setProperty('--c', f.c); b.style.setProperty('--cd', f.cd);
  b.innerHTML = `<b></b><span>${f.name.join('')}<br>${f.sub}</span>`;
  b.setAttribute('aria-label', `Get a ${f.name.join('')} ${f.sub}`);
  b.onclick = () => vend(i, b); vbtns.appendChild(b);
});
function setLed(t, blink) { led.textContent = t; led.classList.toggle('blink', !!blink); }
function chutePoint() {
  const r = chute.getBoundingClientRect(), s = packEl.getBoundingClientRect();
  return { x: r.left - s.left + r.width / 2, y: r.top - s.top + r.height * .55, w: r.width };
}
function vend(i, btn) {
  pack.start(); pack.visible = true;
  btn.classList.add('press'); setTimeout(() => btn.classList.remove('press'), 160);
  if (busy) return;
  if (stock[i] === 0) { setLed('SOLD OUT', true); setTimeout(() => updLed(), 1200); return; }
  busy = true;
  const row = stock[i] - 1; stock[i]--;
  const sl = slotEls[row][i], img = sl.querySelector('img'), coil = sl.querySelector('.coil');
  packEl.style.setProperty('--g', FL[i].c);
  setLed(`${FL[i].name.join('')}…`);
  coil.classList.remove('spin'); void coil.offsetWidth; coil.classList.add('spin');
  const fall = vmwin.getBoundingClientRect().bottom - img.getBoundingClientRect().top + 20;
  gsap.timeline({ onComplete: () => { gsap.set(img, { opacity: 0 }); dispense(i); } })
    .to(img, { scale: 1.08, y: -4, duration: .35, ease: 'power2.out' })
    .to(img, { y: fall, rotation: gsap.utils.random(-25, 25), duration: .45, ease: 'power2.in' });
  if (stock[i] === 0) btn.classList.add('out');
}
function dispense(i) {
  gsap.fromTo(vm, { y: 0 }, { y: 5, duration: .07, yoyo: true, repeat: 3, ease: 'none', clearProps: 'y' });
  gsap.fromTo(flap, { rotationX: 0 }, { rotationX: -70, duration: .18, ease: 'power2.out', yoyo: true, repeat: 1 });
  const c = chutePoint(), h = Math.min(pack.H * (PHONE() ? .17 : .22), 210), w = h * CAN_AR[i];
  const im = new Image(); im.src = can(i); im.alt = ''; im.draggable = false; im.className = 'can';
  const it = pack.add(im, w, h, c.x + (Math.random() - .5) * c.w * .4, c.y, { sx: .9, sy: .97, rot: 1.6, den: .003, rest: .32 });
  const dir = Math.random() < .5 ? -1 : 1;
  M.Body.setVelocity(it.body, { x: dir * (5 + Math.random() * 6), y: -6 - Math.random() * 3 });
  M.Body.setAngularVelocity(it.body, dir * (.15 + Math.random() * .15));
  floorCans.push(it);
  while (floorCans.length > 8) pack.remove(floorCans.shift());
  for (let k = 0; k < 3; k++) {
    const pi = new Image(); pi.src = piece(i, 1 + Math.floor(Math.random() * FL[i].pieces)); pi.alt = ''; pi.className = 'pc';
    pi.onload = () => { const s = PHONE() ? .24 : .32; const p = pack.add(pi, pi.naturalWidth * s, pi.naturalHeight * s, c.x, c.y, { sx: .78, sy: .78, ch: .4, rot: 6, den: .0008, rest: .5 }); M.Body.setVelocity(p.body, { x: (Math.random() - .5) * 18, y: -8 - Math.random() * 6 }); p.extra = true; trimPieces(); };
  }
  pack.fx.burst(c.x, c.y, 16, FL[i].c);
  picked = Math.min(4, picked + 1); busy = false; updLed();
}
function updLed() {
  if (picked >= 4) { setLed('SHAKE IT!', true); shakeBtn.disabled = false; shakeBtn.classList.add('go'); }
  else { setLed(`PICK 4 · ${picked}/4`); shakeBtn.disabled = true; shakeBtn.classList.remove('go'); }
}
function trimPieces() { const ex = pack.items.filter(i => i.extra); while (ex.length > 24) pack.remove(ex.shift()); }
shakeBtn.onclick = () => {
  gsap.timeline().to(vm, { rotation: -4, duration: .08 }).to(vm, { rotation: 4, duration: .1, repeat: 5, yoyo: true }).to(vm, { rotation: 0, duration: .6, ease: 'elastic.out(1,.3)' });
  slotEls.flat().forEach(sl => { const im = sl.querySelector('img'); gsap.fromTo(im, { rotation: 0 }, { rotation: gsap.utils.random(-14, 14), duration: .09, repeat: 7, yoyo: true, clearProps: 'rotation' }); });
  const c = chutePoint(); let n = 0;
  const iv = setInterval(() => { pack.pop(c.x + (Math.random() - .5) * pack.W * .5, pack.H, 1.5, FL[n % 4].c); if (++n > 5) clearInterval(iv); }, 130);
  setLed('RIOT!!', true); setTimeout(() => { picked = 0; updLed(); }, 2200);
};
$('#clear').onclick = () => {
  [...pack.items].forEach(it => pack.remove(it)); floorCans = []; picked = 0; stock.fill(3);
  slotEls.flat().forEach((sl, k) => { const im = sl.querySelector('img'); gsap.fromTo(im, { opacity: 0, y: -30, scale: .6 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: .8, ease: 'elastic.out(1,.5)', delay: k * .03 }); });
  vbtns.querySelectorAll('.vbtn').forEach(b => b.classList.remove('out'));
  updLed();
};
new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) pack.start(); }), { threshold: .2 }).observe(packEl);

'''
s = s[:a] + js + s[b:]
# Play: optional separate element for pointer input, and ignore clicks on buttons
s = s.replace("const mouse = M.Mouse.create(this.el);", "const mouse = M.Mouse.create(this.opts.mouseEl || this.el);")
s = s.replace("this.el.addEventListener('pointerdown', e => { const p = this.local(e); down =", "const IN = this.opts.mouseEl || this.el;\n    IN.addEventListener('pointerdown', e => { if (e.target.closest('button,a')) { down = null; return; } const p = this.local(e); down =")
s = s.replace("this.el.addEventListener('pointerup', e => {\n      if (!down) return;", "IN.addEventListener('pointerup', e => {\n      if (!down) return;")
s = s.replace("this.el.addEventListener('pointermove', e => { this.ptr", "IN.addEventListener('pointermove', e => { this.ptr")
s = s.replace("this.el.addEventListener('pointerleave', () => this.ptr = null);", "IN.addEventListener('pointerleave', () => this.ptr = null);")
s = s.replace("""    let st = null;
    this.el.addEventListener('pointerdown', e => { st =""", """    let st = null; const IN = this.opts.mouseEl || this.el;
    IN.addEventListener('pointerdown', e => { if (e.target.closest('button,a')) { st = null; return; } st =""")
s = s.replace("""    this.el.addEventListener('pointerup', e => {
      if (!st) return;""", """    IN.addEventListener('pointerup', e => {
      if (!st) return;""")
p.write_text(s, encoding='utf-8')
print('js ok', s.count('IN.addEventListener'))
