// Drive every interactive format with real pointer and key events, the way a teacher at
// the board or a presentation clicker would, and assert what the room would see.
//   node interactions.js <deck built from fixtures/interactive_formats.slides.html> [WxH]
const path = require('path');
const { launch } = require('./common');
const deck = path.resolve(process.argv[2]);
const [W, H] = (process.argv[3] || '1366x657').split('x').map(Number);
let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log('  ok   ' + msg); } else { fail++; console.log('  FAIL ' + msg); } }

(async () => {
  const b = await launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + deck); await p.waitForTimeout(400);
  const go = async title => { await p.evaluate(t => { const i = [...document.querySelectorAll('.slide')].findIndex(s => s.dataset.title === t); document.querySelectorAll('#jumpList li')[i].click(); }, title); await p.waitForTimeout(350); };
  const box = async sel => p.locator('.slide.on ' + sel).first().boundingBox();
  const drag = async (from, to, steps = 12) => { await p.mouse.move(from.x, from.y); await p.mouse.down(); await p.mouse.move(from.x + 8, from.y + 4, { steps: 2 }); await p.mouse.move(to.x, to.y, { steps }); await p.mouse.up(); await p.waitForTimeout(150); };
  const mid = r => ({ x: r.x + r.width / 2, y: r.y + r.height / 2 });
  const txt = async sel => p.locator('.slide.on ' + sel).first().innerText();
  const title = async () => p.evaluate(() => document.querySelector('.slide.on').dataset.title);

  console.log('hinge');
  await go('Hinge question');
  const opts = p.locator('.slide.on .hinge .opt');
  for (let i = 0; i < 5; i++) await opts.nth(0).click();
  for (let i = 0; i < 3; i++) await opts.nth(1).click();
  await opts.nth(1).click({ modifiers: ['Shift'] });
  ok((await txt('.hinge .opt >> nth=1')).includes('×2'), 'hand counts show on the card, shift-click takes one away');
  await p.keyboard.press('v'); await p.waitForTimeout(200);
  ok((await txt('.hinge .tally')).includes('5 of 7 chose A · move on') === false && (await txt('.hinge .tally')).includes('5 of 7 chose A'), 'tally reports the share that chose the answer: ' + await txt('.hinge .tally'));
  ok(await p.locator('.slide.on .hinge').evaluate(e => e.classList.contains('revealed')), 'V reveals');
  ok(await p.locator('.slide.on .hinge .opt >> nth=1 >> .trap').evaluate(e => getComputedStyle(e).visibility === 'visible'), 'each wrong option shows its trap');
  await p.keyboard.press('v');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  ok(await title() === 'Hinge question' && await p.locator('.slide.on .hinge').evaluate(e => e.classList.contains('revealed')), '→ reveals the hinge before moving on (clicker)');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  ok(await title() === 'Order it', 'a second → moves on');

  console.log('order');
  const cards = p.locator('.slide.on .ocard');
  const firstText = (await cards.nth(0).locator('.otx').innerText()).trim();
  await drag(mid(await cards.nth(0).boundingBox()), (b5 => ({ x: b5.x + 40, y: b5.y + b5.height - 4 }))(await cards.nth(4).boundingBox()));
  const otx = async i => (await cards.nth(i).locator('.otx').innerText()).trim();
  ok(await otx(4) === firstText, 'dragging the first card to the bottom moves it there');
  ok((await cards.nth(0).locator('.opos').innerText()) === '1', 'positions renumber');
  const t1 = await cards.nth(0).innerText(), t2 = await cards.nth(1).innerText();
  await cards.nth(0).click(); await cards.nth(1).click();
  ok((await cards.nth(0).innerText()).split('\n').pop() === t2.split('\n').pop() && (await cards.nth(1).innerText()).split('\n').pop() === t1.split('\n').pop(), 'tap one, tap another: they swap');
  await p.keyboard.press('c'); await p.waitForTimeout(150);
  ok(/of 5 in the right place/.test(await txt('.order .tally')), 'C checks: ' + await txt('.order .tally'));
  await p.locator('.slide.on .order button', { hasText: 'Show the order' }).click();
  ok((await txt('.order .tally')) === '5 of 5 in the right place', 'show the order solves it');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(200);
  ok(await title() === 'Number line', 'after a button click, → still turns the slide (focus handed back)');

  console.log('number line');
  const zone = await box('.lzone');
  const half = p.locator('.slide.on .ltray .lcard', { hasText: '½' });
  await drag(mid(await half.boundingBox()), { x: zone.x + zone.width * 0.5, y: zone.y + zone.height * 0.4 });
  ok(await p.locator('.slide.on .lzone .lcard', { hasText: '½' }).count() === 1, 'a card dragged onto the line lands on it');
  const tenth = p.locator('.slide.on .ltray .lcard', { hasText: '1/10' });
  await tenth.click(); await p.mouse.click(zone.x + zone.width * 0.6, zone.y + zone.height * 0.5);
  ok(await p.locator('.slide.on .lzone .lcard', { hasText: '1/10' }).count() === 1, 'tap a card, tap the line: it lands where tapped');
  await p.keyboard.press('c'); await p.waitForTimeout(200);
  ok((await txt('.line .tally')) === '1 of 5 in the right place', 'C checks within tolerance: ' + await txt('.line .tally'));
  ok(await p.locator('.slide.on .lcard.ghost').count() === 4, 'a dashed ghost shows where each wrong or missing card lives');
  const overlap = await p.evaluate(() => { const r = [...document.querySelectorAll('.slide.on .lzone .lcard')].map(c => c.getBoundingClientRect());
    for (let i = 0; i < r.length; i++) for (let j = i + 1; j < r.length; j++) { const a = r[i], b = r[j]; if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) return true; } return false; });
  ok(!overlap, 'no two cards on the line overlap (lanes)');
  await p.locator('.slide.on .line button', { hasText: 'Show where' }).click(); await p.waitForTimeout(200);
  ok((await txt('.line .tally')) === '5 of 5 in the right place', 'show where they go solves it');

  console.log('estimate');
  await go('Estimate');
  const midFlag = await box('.eflag.mid'), ez = await box('.ezone');
  await drag(mid(midFlag), { x: ez.x + ez.width * 0.56, y: midFlag.y + midFlag.height / 2 });
  const mv = await txt('.eflag.mid span');
  ok(/^2[6-9]\d seeds|^30\d seeds/.test(mv), 'dragging just right moves its value: ' + mv);
  await p.mouse.click(ez.x + ez.width * 0.02, ez.y + ez.height * 0.5);
  ok(/^1\d seeds|^\d seeds/.test(await txt('.eflag.low span')), 'a tap on the line moves the nearest marker: ' + await txt('.eflag.low span'));
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(1400);
  ok(await title() === 'Estimate' && (await txt('.eanslab')) === 'Actual: 263 seeds', '→ reveals the real number, counted up: ' + await txt('.eanslab'));
  ok(/Inside our range/.test(await txt('.eresult')), 'verdict: ' + await txt('.eresult'));

  console.log('wodb');
  await go("Which one doesn't belong");
  await p.locator('.slide.on .wodb .odd').nth(3).click(); await p.waitForTimeout(100);
  ok(await p.locator('.slide.on .wodb .odd >> nth=3 >> .owhy').evaluate(e => getComputedStyle(e).visibility === 'visible'), 'clicking a tile shows one reason it could be the odd one');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  ok(await p.locator('.slide.on .wodb').evaluate(e => e.classList.contains('revealed')), '→ reveals every reason');

  console.log('mistake');
  await go('Find the mistake');
  await p.locator('.slide.on .ms').nth(2).click();
  ok((await txt('.ms >> nth=2 >> .mtag')).toLowerCase() === 'we think', 'clicking a step marks the class pick');
  await p.keyboard.press('v'); await p.waitForTimeout(150);
  ok((await txt('.ms >> nth=1 >> .mtag')).toLowerCase() === 'went wrong here' && (await txt('.ms >> nth=2 >> .mtag')).toLowerCase() === 'not this one', 'V shows the wrong step and answers the pick');
  ok((await txt('.mfix')).includes('3x = 15'), 'the fix appears: ' + (await txt('.mfix')).replace(/\n/g, ' '));

  console.log('true or false');
  await go('True or false');
  const claim = async () => p.evaluate(() => { const c = document.querySelector('.slide.on .claim.on').cloneNode(true); c.querySelectorAll('.es, .tfprint').forEach(x => x.remove()); return c.textContent.replace(/\s+/g, ' ').trim(); });
  ok(await claim() === 'Plants need soil to grow.', 'starts on the first claim');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  ok(await p.locator('.slide.on .tf').evaluate(e => e.classList.contains('revealed')) && (await txt('.tfo.right')) === 'False', '→ reveals the answer');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  ok(await claim() === 'A pump can run without water around it.', '→ again moves to the next claim, unrevealed');
  for (let i = 0; i < 3; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(80); }
  ok(await claim() === 'A grow light can stand in for the sun.' && await p.locator('.slide.on .tf').evaluate(e => e.classList.contains('revealed')), 'runs through every claim with → alone');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  ok(await title() === 'Match', 'after the last claim, → moves on');
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(150);
  ok(await claim() === 'A grow light can stand in for the sun.', '← back shows the run finished');
  const said = await p.evaluate(() => { const out = []; const real = window.speechSynthesis; window.speechSynthesis.speak = u => out.push(u.text); window.speechSynthesis.getVoices = () => []; document.dispatchEvent(new KeyboardEvent('keydown', { key: 'a' })); return out; }).catch(() => []);
  ok(said.includes('A grow light can stand in for the sun.') && !said.includes('Plants need soil to grow.'), 'A reads the claim on screen, not the hidden ones: ' + JSON.stringify(said));

  console.log('match');
  await go('Match');
  const L = p.locator('.slide.on .mcol.left .mcard'), R = p.locator('.slide.on .mcol.right .mcard');
  const rTexts = await R.allInnerTexts();
  const pumpJob = rTexts.findIndex(t => t.includes('Pushes the water up'));
  await drag(mid(await L.nth(1).boundingBox()), mid(await R.nth(pumpJob).boundingBox()));
  ok(await p.locator('.slide.on .mlines line').count() === 1, 'dragging from a word to a job draws a line');
  const resJob = rTexts.findIndex(t => t.includes('Holds the water'));
  await L.nth(0).click(); await R.nth(resJob).click();
  ok(await p.locator('.slide.on .mlines line').count() === 2, 'tap a word, tap a job: a second line');
  const wrongJob = rTexts.findIndex(t => t.includes('Turns the pump'));
  await L.nth(2).click(); await R.nth(wrongJob).click();
  await p.keyboard.press('c'); await p.waitForTimeout(150);
  ok((await txt('.match .tally')) === '2 of 5 matched', 'C checks the lines: ' + await txt('.match .tally'));
  ok(await p.locator('.slide.on .mlines line[stroke-dasharray]').count() === 1, 'a wrong line turns dashed');
  const lineFits = await p.evaluate(() => { const s = document.querySelector('.slide.on'); const g = s.querySelector('.mgrid').getBoundingClientRect();
    return [...s.querySelectorAll('.mlines line')].every(l => +l.getAttribute('x1') >= 0 && +l.getAttribute('x2') <= g.width + 1); });
  ok(lineFits, 'lines run between the two columns');

  console.log('what if');
  await go('What if');
  ok((await txt('.wival')) === '?', 'starts under cover: predict first');
  await p.keyboard.press('v'); await p.waitForTimeout(900);
  ok((await txt('.wival')) === '21 L', 'V reveals 12 plants × 0.25 L × 7 = 21 L: ' + await txt('.wival'));
  ok((await txt('.wistat')) === 'inside the band', 'status in words, not colour alone');
  const slider = p.locator('.slide.on .wirow input').first(); const sb = await slider.boundingBox();
  await p.mouse.click(sb.x + sb.width * 0.99, sb.y + sb.height / 2); await p.waitForTimeout(150);
  ok((await txt('.wival')) === '?', 'moving a slider puts the answer back under cover');
  ok(await p.evaluate(() => !document.activeElement || document.activeElement.tagName !== 'INPUT'), 'the slider hands the keyboard back after a change');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(900);
  ok(await title() === 'What if' && (await txt('.wival')) === '42 L' && (await txt('.wistat')) === 'above the band', '→ reveals the new value: ' + await txt('.wival') + ', ' + await txt('.wistat'));

  console.log('zoom-in');
  await go('Zoom in');
  const z = async () => p.evaluate(() => getComputedStyle(document.querySelector('.slide.on .zframe img')).getPropertyValue('--z').trim());
  ok(await z() === '6', 'starts zoomed in at the focus');
  ok(await p.locator('.slide.on .zoomin .cap').evaluate(e => getComputedStyle(e).visibility === 'hidden'), 'caption waits until the whole photo is up');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
  ok(await z() === '3', '→ steps back once');
  await p.locator('.slide.on .zframe').click(); await p.waitForTimeout(100);
  ok(await z() === '1' && await p.locator('.slide.on .zoomin').evaluate(e => e.classList.contains('done')), 'a click steps back too, to the whole photo');
  ok(!(await p.evaluate(() => document.querySelector('.zoom').classList.contains('on'))), 'clicking while zooming does not open the enlarged view');
  const zf = await p.evaluate(() => { const f = document.querySelector('.slide.on .zframe').getBoundingClientRect(); const s = document.querySelector('.slide.on').getBoundingClientRect(); return f.height > 150 && f.bottom < s.bottom && f.width <= s.width; });
  ok(zf, 'the zoom frame fills its band and stays inside the slide');

  console.log('label the photo');
  await go('Name the parts');
  const shown = async () => p.evaluate(() => [...document.querySelectorAll('.slide.on .pin')].filter(x => getComputedStyle(x.querySelector('.lab')).visibility === 'visible').length);
  ok(await shown() === 0, 'names start hidden, numbers showing');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(80);
  ok(await shown() === 1, '→ brings back one name');
  await p.keyboard.press('v'); await p.waitForTimeout(80);
  ok(await shown() === 3, 'V shows them all');

  console.log('dark slide');
  await go('Dark slide');
  const bg = await p.evaluate(() => getComputedStyle(document.querySelector('.slide.on .claim')).backgroundColor);
  ok(bg === 'rgb(59, 53, 46)', 'components on a dark slide use the caviar surface: ' + bg);

  console.log(errs.length ? 'JS errors: ' + errs.join(' | ') : 'no JS errors');
  console.log(`\n${pass} passed, ${fail} failed`);
  await b.close();
  process.exit(fail || errs.length ? 1 : 0);
})();
