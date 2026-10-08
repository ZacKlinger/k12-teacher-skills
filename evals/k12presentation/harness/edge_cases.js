// The edge cases a review found, each pinned so it can't quietly come back.
//   node edge_cases.js <deck built from fixtures/edge_cases.slides.html> [WxH]
const path = require('path');
const { launch, fileUrl } = require('./common');
const deck = path.resolve(process.argv[2]);
const [W, H] = (process.argv[3] || '1366x657').split('x').map(Number);
let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log('  ok   ' + msg); } else { fail++; console.log('  FAIL ' + msg); } }

(async () => {
  const b = await launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(fileUrl(deck)); await p.waitForTimeout(500);
  const go = async t => { await p.evaluate(t => { const i = [...document.querySelectorAll('.slide')].findIndex(s => s.dataset.title === t); document.querySelectorAll('#jumpList li')[i].click(); }, t); await p.waitForTimeout(350); };
  const title = async () => p.evaluate(() => document.querySelector('.slide.on').dataset.title);
  const on = sel => p.locator('.slide.on ' + sel).first();

  console.log('first slide written as class="slide on"');
  const chrome = await p.evaluate(() => ({ counter: document.getElementById('counter').textContent, timer: !document.getElementById('timer').hidden }));
  ok(/^1 \/ \d+$/.test(chrome.counter) && chrome.counter !== '1 / 1' && chrome.timer, 'the opening slide still gets its counter and timer: ' + chrome.counter);

  console.log('first and last slide');
  const tfState = async () => p.evaluate(() => { const t = document.querySelector('.slide.on .tf'); return { claim: [...t.querySelectorAll('.claim')].findIndex(c => c.classList.contains('on')), open: t.classList.contains('revealed') }; });
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(150);
  let st = await tfState();
  ok(st.claim === 0 && !st.open, '← on the first slide does not finish its game (a class="big tf" is found and built)');
  await go('Last claims');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  await p.keyboard.press('s'); await p.waitForTimeout(1200);
  await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  st = await tfState();
  const before = await p.evaluate(() => document.getElementById('timerTime').textContent);
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  const st2 = await tfState(), after = await p.evaluate(() => document.getElementById('timerTime').textContent);
  ok(st.claim === 1 && st.open && st2.claim === 1 && st2.open && after !== '1:00', `→ past the last slide keeps its game finished and its timer running (${before} → ${after})`);

  console.log('a game held back by a build step');
  await go('Held back');
  const held = async () => p.evaluate(() => { const s = document.querySelector('.slide.on'); return { steps: [...s.querySelectorAll('[data-step]')].map(x => x.classList.contains('shown')), open: s.querySelector('.estimate').classList.contains('revealed') }; });
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  let h = await held();
  ok(h.steps[0] && !h.steps[1] && !h.open, '→ shows the first build step, the hidden game stays unanswered');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  h = await held();
  ok(h.steps[1] && !h.open, '→ again brings the game in, still unanswered');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(1300);
  h = await held();
  ok(h.open && await title() === 'Held back', 'only then does → reveal the answer');

  console.log('focus');
  await go('Held back');
  await on('.estimate button').click(); await p.waitForTimeout(100);
  ok(await p.evaluate(() => document.activeElement === document.body || !document.activeElement || document.activeElement.tagName !== 'BUTTON'), 'a clicked game button gives the keyboard back, so Space or Enter cannot press it again');

  console.log('fraction ticks');
  await go('Fraction ticks');
  const ticks = await p.evaluate(() => [...document.querySelectorAll('.slide.on .ltick')].map(t => t.style.left + ':' + t.textContent));
  ok(JSON.stringify(ticks) === JSON.stringify(['0%:0', '25%:1/4', '50%:1/2', '75%:3/4', '100%:1']), 'ticks written as fractions land at their value: ' + ticks.join(' '));
  await on('.line button').click(); await p.waitForTimeout(100);
  await p.evaluate(() => document.querySelector('.slide.on .line').solve()); await p.waitForTimeout(200);
  ok((await on('.line .tally').innerText()) === '3 of 3 in the right place', 'card values written as fractions are placed and checked at their value');

  console.log('what if that peaks in the middle');
  await go('Peak');
  const peak = await p.evaluate(() => ({ ends: [...document.querySelectorAll('.slide.on .wiends span')].map(x => x.textContent), fill: document.querySelector('.slide.on .wifill').style.width, val: document.querySelector('.slide.on .wival').textContent }));
  ok(peak.ends[1] !== '1 m²' && parseFloat(peak.fill) < 100, `the bar's scale comes from the whole range, not the ends: ${peak.val} on 0 to ${peak.ends[1]}, fill ${peak.fill}`);
  const slider = on('.wirow input'); const sb = await slider.boundingBox();
  const thumb = await p.evaluate(() => { const r = document.querySelector('.slide.on .wirow input'); const b = r.getBoundingClientRect(); return b.left + b.width * (r.value - r.min) / (r.max - r.min); });
  await p.mouse.click(thumb, sb.y + sb.height / 2); await p.waitForTimeout(150);
  ok(await p.evaluate(() => document.activeElement.tagName !== 'INPUT'), 'clicking a slider without moving it still gives the keyboard back');

  console.log('photo tiles and photo cards');
  await go('Bare tiles');
  const tiles = await p.evaluate(() => [...document.querySelectorAll('.slide.on .wodb > .odd')].map(t => t.tagName + (t.querySelector('.oL') ? ':letter' : '')));
  ok(tiles.length === 4 && tiles.every(t => t === 'FIGURE:letter'), 'bare <img> tiles are wrapped so they carry their letter and reason: ' + tiles.join(' '));
  const fits = await p.evaluate(() => { const s = document.querySelector('.slide.on'), g = s.querySelector('.wodb').getBoundingClientRect(); return g.bottom < document.querySelector('.footer').getBoundingClientRect().top; });
  ok(fits, 'bare photo tiles stay inside the slide');
  await go('Photo match');
  const L = p.locator('.slide.on .mcol.left .mcard'), R = p.locator('.slide.on .mcol.right .mcard');
  const rb = await R.nth(0).boundingBox(), lb = await L.nth(0).boundingBox();
  await p.mouse.move(rb.x + rb.width / 2, rb.y + rb.height / 2); await p.mouse.down();
  await p.mouse.move(rb.x + rb.width / 2 - 10, rb.y + rb.height / 2, { steps: 3 });
  await p.mouse.move(lb.x + lb.width / 2, lb.y + lb.height / 2, { steps: 10 }); await p.mouse.up(); await p.waitForTimeout(150);
  ok(await p.locator('.slide.on .mlines line').count() === 1, 'dragging from a photo card with the mouse draws a line (no browser image drag)');

  console.log('fractions read as fractions everywhere');
  await go('Fraction estimate');
  await p.keyboard.press('v'); await p.waitForTimeout(1400);
  const est = await p.evaluate(() => ({ lab: document.querySelector('.slide.on .eanslab').textContent, left: document.querySelector('.slide.on .eans').style.left }));
  ok(est.left === '75%' && est.lab === 'Actual: 0.75 of the tank', 'an estimate answered 3/4 lands at three quarters: ' + est.lab + ' at ' + est.left);
  await go('Fraction slider');
  const sl = await p.evaluate(() => { const r = document.querySelector('.slide.on .wirow input'); return { step: r.step, value: r.value, val: document.querySelector('.slide.on .wival').textContent, band: document.querySelector('.slide.on .wiband').style.left }; });
  ok(sl.step === '0.25' && sl.value === '0.5' && sl.val === '0.5' && sl.band === '25%', `a slider stepping by 1/4 from 1/2, band 1/4 to 3/4: step ${sl.step}, start ${sl.value}, value ${sl.val}, band at ${sl.band}`);

  console.log('build steps around games');
  await go('Prompt first');
  const pf = async () => p.evaluate(() => { const s = document.querySelector('.slide.on'); return { s1: s.querySelectorAll('[data-step]')[0].classList.contains('shown'), game: s.querySelector('.game').classList.contains('revealed'), hinge: s.querySelector('.hinge').classList.contains('revealed') }; });
  await p.keyboard.press('v'); await p.waitForTimeout(100);
  let st3 = await pf();
  ok(st3.game && !st3.hinge, 'V reveals the visible game, never the one still hidden in a build step');
  await p.keyboard.press('v'); await p.waitForTimeout(100);
  await p.evaluate(() => { const g = document.querySelector('.slide.on .game'); if (g.classList.contains('revealed')) g.reveal(); });
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  st3 = await pf();
  ok(st3.s1 && !st3.game, 'a prompt step above the game appears before → reveals the game');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  const s2 = await p.evaluate(() => document.querySelectorAll('.slide.on [data-step]')[1].classList.contains('shown'));
  st3 = await pf();
  ok(s2 && !st3.game, 'every build step on the slide comes in before any answer, even one below the game');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  st3 = await pf();
  ok(st3.game && !st3.hinge, 'then → reveals the games one at a time');

  console.log('print');
  await p.emulateMedia({ media: 'print' });
  const pf2 = await p.evaluate(() => [...document.querySelectorAll('.slide')].map(s => getComputedStyle(s).getPropertyValue('--fit').trim()).filter(f => f && f !== '1'));
  ok(pf2.length === 0, 'printing sets every slide back to full size, whatever the screen shrank');
  await p.emulateMedia({ media: 'screen' });

  console.log('photos in order cards');
  await go('Order photos');
  const oh = await p.evaluate(() => [...document.querySelectorAll('.slide.on .ocard')].map(c => Math.round(c.getBoundingClientRect().height)));
  ok(oh.every(h => h < 160) && !(await p.evaluate(() => document.querySelector('.slide.on').classList.contains('tall'))), 'photos in order cards are thumbnails and the slide fits: ' + oh.join(', ') + 'px');

  console.log('slides that scroll, and windows that change');
  await p.setViewportSize({ width: 800, height: 600 }); await p.waitForTimeout(300);
  await go('Too much'); await p.waitForTimeout(400);
  const tm = await p.evaluate(() => { const s = document.querySelector('.slide.on'); return { tall: s.classList.contains('tall'), top: s.scrollTop }; });
  ok(tm.tall && tm.top === 0, `a slide that has to scroll opens at its top, with the question showing (tall ${tm.tall}, scrollTop ${tm.top})`);
  await p.evaluate(() => document.querySelector('.slide.on .order').solve()); await p.waitForTimeout(700);
  const tm2 = await p.evaluate(() => { const s = document.querySelector('.slide.on'); return s.scrollTop > 0; });
  ok(tm2, 'when its answer is checked, it scrolls to show the reason');
  await p.setViewportSize({ width: 1920, height: 1080 }); await p.waitForTimeout(300);
  await go('Zoom resize'); await p.waitForTimeout(400);
  const big = await p.evaluate(() => document.querySelector('.slide.on .zframe').getBoundingClientRect().height);
  await p.setViewportSize({ width: 1366, height: 657 }); await p.waitForTimeout(700);
  const z = await p.evaluate(() => { const s = document.querySelector('.slide.on'), f = s.querySelector('.zframe').getBoundingClientRect(); return { h: f.height, top: f.top, tall: s.classList.contains('tall'), foot: document.querySelector('.footer').getBoundingClientRect().top, bottom: f.bottom }; });
  ok(z.h < big && !z.tall && z.top > 0 && z.bottom < z.foot, `the zoom frame shrinks with the window (${Math.round(big)}px to ${Math.round(z.h)}px) and the slide still fits`);
  await p.setViewportSize({ width: W, height: H });

  console.log('charts by clicker');
  await go('Guess chart');
  const barH = () => p.evaluate(() => document.querySelector('.slide.on .dv-guess .actual').getBoundingClientRect().height);
  ok(await barH() === 0, 'a guess chart arrives with its bar hidden');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(1100);
  ok(await title() === 'Guess chart' && await barH() > 0, '→ shows the real number before moving on');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(200);
  ok(await title() === 'Bars chart', 'a second → moves on');
  const rowsOn = () => p.evaluate(() => document.querySelectorAll('.slide.on .dv-bars .row.on').length);
  const seen = [];
  for (let k = 0; k < 3; k++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150); seen.push(await rowsOn()); }
  ok(seen.join(',') === '1,2,3' && await title() === 'Bars chart', '→ brings in one bar per press: ' + seen.join(','));
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(200);
  ok(await title() === 'Key word options', 'after the last bar, → moves on');

  console.log('key words never single out an option');
  const kw = await p.evaluate(() => [...document.querySelectorAll('.slide.on mark.kw')].map(m => m.closest('.opts') ? 'option' : 'other'));
  ok(!kw.includes('option'), 'no option in a game is marked as a key word: ' + JSON.stringify(kw));

  console.log('a slide that scrolls keeps its clock');
  await go('Too much'); await p.waitForTimeout(400);
  const clock = await p.evaluate(() => { const s = document.querySelector('.slide.on'); s.scrollTop = s.scrollHeight;
    const r = document.querySelector('.slide.on .head-right').getBoundingClientRect(); return { tall: s.classList.contains('tall'), top: r.top, bottom: r.bottom }; });
  await p.waitForTimeout(100);
  ok(!clock.tall || (clock.top >= 0 && clock.bottom <= H), 'scrolled to its end, the timer is still on screen' + (clock.tall ? ` (top ${Math.round(clock.top)})` : ' (the slide fits; nothing to scroll)'));

  console.log(errs.length ? 'JS errors: ' + errs.join(' | ') : 'no JS errors');
  console.log(`\n${pass} passed, ${fail} failed`);
  await b.close();
  process.exit(fail || errs.length ? 1 : 0);
})();
