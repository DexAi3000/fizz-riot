import pathlib, re
r = pathlib.Path(__file__).resolve().parent.parent
p = r / 'src/shell.html'; s = p.read_text(encoding='utf-8')

# ---------- CSS: photo machine ----------
a = s.index(".vm{position:absolute;"); b = s.index(".world2{position:absolute;")
css = '''.vm{position:absolute;z-index:3;left:56%;bottom:2.5%;height:min(88vh,860px);aspect-ratio:990/1708;transform:translateX(-50%);transform-origin:50% 100%}
.vm>img{position:absolute;inset:0;width:100%;height:100%;filter:drop-shadow(0 40px 40px rgba(26,15,46,.35));pointer-events:none;user-select:none}
.vm .open{opacity:0}
.vm.opened .open{opacity:1}.vm.opened .closed{opacity:0}
.vwin{position:absolute;overflow:hidden;border-radius:1.4% / .8%}
.vwin::after{content:"";position:absolute;inset:0;background:linear-gradient(112deg,rgba(255,255,255,.22) 0 9%,transparent 9% 21%,rgba(255,255,255,.12) 21% 24%,transparent 24%);pointer-events:none;z-index:5}
.vcan{position:absolute;transform-origin:50% 100%;filter:drop-shadow(0 6px 6px rgba(0,0,0,.25));will-change:transform}
.vled{position:absolute;display:grid;place-items:center;text-align:center;font-family:var(--disp);font-size:clamp(7px,.78vw,12px);line-height:1.25;color:#173B12;text-shadow:0 0 6px rgba(120,255,140,.55);letter-spacing:.04em;padding:2px}
.vled.blink{animation:blink .5s steps(1) infinite}
@keyframes blink{50%{opacity:.25}}
.vbtn{position:absolute;border-radius:50%;transform:translate(-50%,-50%);transition:box-shadow .3s,background .12s}
.vbtn::after{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.0),rgba(255,255,255,0));transition:background .1s}
.vbtn:hover{box-shadow:0 0 0 4px rgba(255,255,255,.25),0 0 26px var(--c)}
.vbtn.press::after,.vbtn:active::after{background:radial-gradient(circle,rgba(0,0,0,.28),rgba(0,0,0,.05))}
.vbtn.out{box-shadow:inset 0 0 0 100px rgba(26,15,46,.45)}
.vbtn .lbl{position:absolute;left:calc(100% + 14px);top:50%;transform:translateY(-50%);white-space:nowrap;font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);background:#fff;padding:6px 10px;border-radius:99px;opacity:0;transition:opacity .25s;pointer-events:none}
.vbtn:hover .lbl{opacity:1}
.vctl{display:flex;gap:10px;margin-top:3vh;pointer-events:auto;flex-wrap:wrap}
.vshake{padding:14px 22px;border-radius:99px;background:var(--ink);color:#fff;font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;transition:opacity .3s,transform .3s var(--expo)}
.vshake[disabled]{opacity:.3;pointer-events:none}
.vshake.go{animation:glowp 1s ease-in-out infinite}
@keyframes glowp{50%{box-shadow:0 0 0 8px rgba(255,255,255,.45)}}
.vreset{padding:14px 18px;border-radius:99px;border:1.5px solid var(--ink);font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase}
'''
s = s[:a] + css + s[b:]
s = re.sub(r"\.vm::after\{[^\n]*\n", "", s)
# drop leftovers of the CSS-drawn machine
for sel in ['.vm-sign', '.vm-sign i', '.vm-sign .neon', '.vm-win', '.vm-win::after', '.vrow', '.slot', '.slot img', '.slot .coil', '.slot .coil.spin', '.vm-side', '.led', '.led.blink', '.vbtns', '.vbtn b', '.vbtn:hover b', '.vbtn:active b,.vbtn.press b', '.coin', '.vm-chute', '.vm-chute .flap', '.vm-chute span', '.vm-side,.vm-sign']:
    s = re.sub(r"(?m)^" + re.escape(sel) + r"\{[^\n]*\n", "", s)
s = re.sub(r"(?m)^@keyframes (flick|coil)\{[^\n]*\n", "", s)
s = s.replace("@media (max-width:1180px) and (min-width:761px){.pack .lead{display:none}.pack .head{max-width:26vw}.pack h2{font-size:3.6vw}.vm{left:60%;width:min(460px,52vw)}}",
              "@media (max-width:1180px) and (min-width:761px){.pack .lead{display:none}.pack .head{max-width:30vw}.pack h2{font-size:3.6vw}.vm{left:62%;height:min(84vh,760px)}}")
s = re.sub(r"\.vm\{width:94vw;height:min\(64vh,540px\);bottom:6%;padding:12px\}\.vm-side\{[^}]*\}\.vbtn span\{display:none\}\.vbtns\{justify-items:center\}\.led\{[^}]*\}",
           ".vm{height:auto;width:min(86vw,380px);bottom:2%}.vctl{position:fixed;display:none}.pack .vctl{position:absolute;display:flex;left:16px;right:16px;top:118px;margin:0}.vshake,.vreset{padding:10px 14px;font-size:10px}.vbtn .lbl{display:none}", s)

# ---------- markup ----------
a = s.index('<div class="vm" id="vm">'); b = s.index('<div class="world2"')
html = '''<div class="vm" id="vm">
    <img class="closed" src="assets/vm.webp?v=3" alt="FIZZ RIOT vending machine">
    <img class="open" src="assets/vm-open.webp?v=3" alt="" aria-hidden="true">
    <div class="vwin" id="vmwin"></div>
    <div class="vled" id="led">PICK 4<br>0/4</div>
    <div id="vbtns"></div>
  </div>
  '''
s = s[:a] + html + s[b:]
s = s.replace('<p class="lead">Pick any four from the machine. Grab them off the floor, throw them around, then shake the whole thing.</p></div>',
              '<p class="lead">Press a coloured button on the machine. Grab the cans off the floor, throw them around, then shake the whole thing.</p><div class="vctl"><button class="vshake" id="shake" disabled>Shake it</button><button class="vreset" id="clear">Restock</button></div></div>')

# ---------- loader: can fills up ----------
a = s.index("/* ---------- preloader ---------- */"); b = s.index("/* ---------- nav ---------- */")
pre_css = '''/* ---------- preloader: the can fills up ---------- */
.pre{position:fixed;inset:0;z-index:100;background:var(--cream);overflow:hidden;display:grid;place-items:center}
.pcan{position:relative;height:min(52vh,460px);aspect-ratio:400/893}
.pcan img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}
.pcan .empty{filter:grayscale(1) brightness(1.18) contrast(.85);opacity:.55}
.pcan .full{clip-path:inset(100% 0 0 0)}
.pcan .fz{position:absolute;inset:0;pointer-events:none;-webkit-mask:var(--m) center/contain no-repeat;mask:var(--m) center/contain no-repeat}
.pcan .fz i{position:absolute;border-radius:50%;border:1.5px solid rgba(255,255,255,.85);background:radial-gradient(circle at 30% 30%,#fff,rgba(255,255,255,.1) 45%,transparent 60%)}
.pre .num{position:absolute;left:0;right:0;bottom:9vh;text-align:center;font-family:var(--disp);font-size:clamp(34px,5vw,64px);color:var(--ink);letter-spacing:-.02em}
.pre .lab{position:absolute;left:0;right:0;bottom:5.5vh;text-align:center;font-weight:600;letter-spacing:.24em;font-size:11px;text-transform:uppercase;opacity:.6}
.pre .flood{position:absolute;left:50%;top:50%;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;transform:scale(0)}
.pre.done{pointer-events:none}
'''
s = s[:a] + pre_css + s[b:]
a = s.index('<div class="pre" id="pre"'); b = s.index('</div>', s.index('class="lab"', a)) + len('</div>')
s = s[:a] + '<div class="pre" id="pre" aria-hidden="true"><div class="pcan" id="pcan"><img class="empty" alt=""><img class="full" alt=""><div class="fz" id="pfz"></div></div><div class="num" id="preNum">0%</div><div class="lab" id="preLab">filling the can…</div><div class="flood" id="flood"></div></div>' + s[b:]
p.write_text(s, encoding='utf-8')
print('shell', '.vm-side' in s, 'pcan' in s, '<div class="liq"' in s)
