import pathlib
r = pathlib.Path(__file__).resolve().parent.parent
p = r / 'src/shell.html'; s = p.read_text(encoding='utf-8')
a = s.index("/* ---------- pack builder: the cooler ---------- */"); b = s.index("/* ---------- footer ---------- */")
css = '''/* ---------- vending machine ---------- */
.pack{position:relative;height:100vh;height:100svh;min-height:760px;overflow:hidden;--g:#E5618A;background:var(--g);transition:background-color .7s;color:var(--ink)}
.pack .wall{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.07) 0 2px,transparent 2px 120px),radial-gradient(70% 60% at 50% 40%,rgba(255,255,255,.35),transparent 70%)}
.pack .floor{position:absolute;left:0;right:0;bottom:0;height:16%;background:linear-gradient(180deg,rgba(0,0,0,.14),rgba(0,0,0,.04) 30%,rgba(255,255,255,.08))}
.pack .head{position:absolute;z-index:6;left:clamp(16px,3vw,40px);top:clamp(84px,13vh,130px);max-width:30vw;pointer-events:none}
.pack h2{font-family:var(--disp);font-size:clamp(36px,4.6vw,80px);line-height:.92;letter-spacing:-.02em;color:var(--ink)}
.pack h2 span{display:block}.pack h2 span:last-child{color:#fff;text-shadow:0 .05em 0 rgba(26,15,46,.18)}
.pack .lead{margin-top:2.4vh;max-width:24ch;font-size:clamp(15px,1.2vw,18px);font-weight:600}
.pack .tag{position:absolute;z-index:6;right:clamp(16px,3vw,40px);top:clamp(84px,13vh,130px);text-align:right;font-size:12px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;line-height:2}
.pack .tag b{display:block;font-family:var(--disp);font-size:clamp(28px,3vw,46px);letter-spacing:0;line-height:1.1}
.vm{position:absolute;z-index:3;left:50%;bottom:9%;width:min(520px,88vw);height:min(80vh,760px);transform:translateX(-50%);display:grid;grid-template-columns:1fr 30%;grid-template-rows:auto 1fr 17%;border-radius:34px 34px 18px 18px;background:linear-gradient(100deg,#2A1B48 0%,#1A0F2E 38%,#120A22 100%);box-shadow:inset 0 2px 0 rgba(255,255,255,.18),inset 6px 0 0 rgba(255,255,255,.05),0 50px 70px -30px rgba(26,15,46,.65);padding:16px;transform-origin:50% 100%}
.vm::after{content:"";position:absolute;left:8%;right:8%;bottom:-22px;height:22px;border-radius:50%;background:radial-gradient(closest-side,rgba(26,15,46,.45),transparent);z-index:-1}
.vm-sign{grid-column:1/3;display:flex;align-items:center;justify-content:space-between;padding:6px 10px 14px;font-family:var(--disp);font-size:clamp(18px,2vw,28px);color:#fff;letter-spacing:.02em}
.vm-sign i{font-style:normal;color:var(--g);text-shadow:0 0 14px var(--g),0 0 2px #fff;transition:color .5s}
.vm-sign .neon{color:#fff;text-shadow:0 0 6px rgba(255,255,255,.9),0 0 22px var(--g),0 0 40px var(--g);animation:flick 4s steps(1) infinite}
@keyframes flick{0%,92%,94%,97%,100%{opacity:1}93%{opacity:.55}96%{opacity:.7}}
.vm-win{position:relative;border-radius:16px;overflow:hidden;background:linear-gradient(180deg,#FFF6EA,#F2DFC6);box-shadow:inset 0 0 0 3px rgba(0,0,0,.35),inset 0 10px 20px rgba(0,0,0,.18);display:grid;grid-template-rows:repeat(3,1fr);padding:10px 8px 0}
.vm-win::after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.55) 0 8%,transparent 8% 22%,rgba(255,255,255,.25) 22% 25%,transparent 25%);pointer-events:none;z-index:3}
.vrow{display:grid;grid-template-columns:repeat(4,1fr);align-items:end;border-bottom:6px solid #CDB9A0;box-shadow:0 3px 0 rgba(0,0,0,.12);position:relative}
.slot{position:relative;height:100%;display:flex;align-items:flex-end;justify-content:center}
.slot img{height:84%;width:auto;filter:drop-shadow(0 6px 6px rgba(0,0,0,.28));will-change:transform;position:relative;z-index:1}
.slot .coil{position:absolute;left:12%;right:12%;bottom:0;height:14%;border-radius:4px;background:repeating-linear-gradient(100deg,#9A9AA6 0 3px,#E4E4EC 3px 5px,transparent 5px 11px);z-index:2}
.slot .coil.spin{animation:coil .5s linear 1}
@keyframes coil{to{background-position:44px 0}}
.vm-side{grid-row:2/4;grid-column:2;display:flex;flex-direction:column;align-items:center;gap:12px;padding:6px 0 6px 14px}
.led{width:100%;border-radius:10px;background:#07140B;box-shadow:inset 0 0 0 2px #000,inset 0 0 18px rgba(80,255,140,.12);padding:12px 8px;font-family:var(--disp);font-size:clamp(11px,1.05vw,15px);color:#8CFFA9;text-shadow:0 0 8px rgba(140,255,169,.8);text-align:center;letter-spacing:.06em;min-height:52px;display:grid;place-items:center}
.led.blink{animation:blink .5s steps(1) infinite}
@keyframes blink{50%{opacity:.25}}
.vbtns{display:grid;gap:10px;width:100%}
.vbtn{display:flex;align-items:center;gap:10px;color:#fff;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;text-align:left;line-height:1.1}
.vbtn b{flex:0 0 auto;width:clamp(34px,3.4vw,46px);height:clamp(34px,3.4vw,46px);border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.75),var(--c) 45%,var(--cd) 100%);box-shadow:0 4px 0 var(--cd),0 0 0 3px rgba(255,255,255,.08);transition:transform .12s,box-shadow .12s,filter .3s}
.vbtn:hover b{filter:brightness(1.15) drop-shadow(0 0 10px var(--c))}
.vbtn:active b,.vbtn.press b{transform:translateY(4px);box-shadow:0 0 0 var(--cd),0 0 0 3px rgba(255,255,255,.08)}
.vbtn.out{opacity:.35}
.coin{width:14px;height:44px;border-radius:7px;background:#05030A;box-shadow:inset 0 0 0 2px #3A2C55;margin-top:auto}
.vshake{width:100%;padding:12px 6px;border-radius:12px;background:#3A2C55;color:#fff;font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;transition:background .3s}
.vshake[disabled]{opacity:.35;pointer-events:none}
.vshake.go{background:var(--g);color:var(--ink);animation:glowp 1s ease-in-out infinite}
@keyframes glowp{50%{box-shadow:0 0 24px var(--g)}}
.vreset{font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.55)}
.vm-chute{grid-column:1;grid-row:3;margin-top:14px;border-radius:12px;background:#07040E;box-shadow:inset 0 8px 16px rgba(0,0,0,.8),inset 0 0 0 2px #3A2C55;position:relative;overflow:hidden;perspective:500px}
.vm-chute .flap{position:absolute;inset:6px;border-radius:8px;background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.04));transform-origin:50% 0;border:1px solid rgba(255,255,255,.1)}
.vm-chute span{position:absolute;bottom:8px;left:0;right:0;text-align:center;font-size:9px;letter-spacing:.3em;color:rgba(255,255,255,.35);font-weight:600}
.world2{position:absolute;inset:0;z-index:4}
#fx2{position:absolute;inset:0;z-index:7;pointer-events:none}
.vm-side,.vm-sign{position:relative;z-index:5}
@media (max-width:900px){.pack .head{max-width:none;right:16px}.pack .tag{display:none}.vm{height:min(64vh,640px);bottom:7%}}
@media (max-width:760px){.pack{min-height:740px}.pack .head{top:76px}.pack h2{font-size:34px}.pack .lead{display:none}.vm{width:94vw;height:min(66vh,560px);padding:12px}.vm-side{padding-left:10px;gap:8px}.vbtn span{display:none}.vbtns{justify-items:center}.led{font-size:10px;min-height:44px;padding:8px 4px}}

'''
s = s[:a] + css + s[b:]
a = s.index('<section class="pack"'); b = s.index('</section>', a) + len('</section>')
html = '''<section class="pack" id="pack" aria-label="Riot vending machine">
  <div class="wall"></div><div class="floor"></div>
  <div class="head"><h2><span>Hit a button.</span><span>Get a riot.</span></h2><p class="lead">Pick any four from the machine. Grab them off the floor, throw them around, then shake the whole thing.</p></div>
  <div class="tag">Per can<b>&euro;2.50</b>4-pack &middot; &euro;9.00</div>
  <div class="vm" id="vm">
    <div class="vm-sign"><span class="neon">FIZZ RIOT</span><i>&#10022;</i></div>
    <div class="vm-win" id="vmwin"></div>
    <div class="vm-side">
      <div class="led" id="led">PICK 4 &middot; 0/4</div>
      <div class="vbtns" id="vbtns"></div>
      <button class="vshake" id="shake" disabled>Shake it</button>
      <button class="vreset" id="clear">Restock</button>
      <div class="coin" aria-hidden="true"></div>
    </div>
    <div class="vm-chute" id="chute" aria-hidden="true"><div class="flap" id="flap"></div><span>PUSH</span></div>
  </div>
  <div class="world2" id="world2" aria-hidden="true"></div>
  <canvas id="fx2" aria-hidden="true"></canvas>
</section>'''
s = s[:a] + html + s[b:]
import re
s = re.sub(r"  \.pack \.head\{flex-direction:column[^\n]*\n  \.dock[^\n]*\n", "", s)
p.write_text(s, encoding='utf-8'); print('shell ok', '.dock' in s)
