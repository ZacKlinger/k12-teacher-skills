// Layout audit. Opens a built deck at the screens it meets in a classroom (an old 800x600
// projector, a 4:3 projector, 16:9 projectors, a laptop presenting in a browser window)
// and visits every slide twice: as it opens, and played (charts revealed, games answered,
// cards placed). It fails on anything that runs under the footer, spills off the side or
// overflows its body, and on a slide that fell back to scrolling at 1024x768 or larger
// (rubric row O-D8). Scrolling at 800x600, and type under 15px, are warnings.
//   node layout_audit.js deck.html [--only 1366x657,1024x768] [--shots dir]
const path = require('path');
const fs = require('fs');
const { launch, open, slide } = require('./common');

const deck = process.argv[2];
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const VIEWPORTS = (arg('--only') || '800x600,1024x768,1280x720,1280x800,1366x657,1920x1080')
  .split(',').map(s => s.split('x').map(Number));
const SHOTS = arg('--shots');

async function play(page) {
  await page.evaluate(async () => {
    const s = document.querySelector('.slide.on');
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    s.querySelectorAll('[data-step]').forEach(e => e.classList.add('shown'));
    for (const el of s.querySelectorAll('.dv-bars')) { const n = el.querySelectorAll('.row').length; for (let i = 0; i < n; i++) el.click(); }
    for (const el of s.querySelectorAll('.dv-icons, .dv-gauge')) el.click();
    for (const el of s.querySelectorAll('.dv-percent')) { el.click(); el.click(); }
    for (const el of s.querySelectorAll('.dv-guess .dv-btn')) el.click();
    for (const col of s.querySelectorAll('.dv-dots .col')) for (let i = 0; i < 6; i++) col.click();
    for (const g of s.querySelectorAll('.game, .hinge, .estimate, .wodb, .mistake, .tf, .whatif, .pinned[data-quiz]')) if (g.reveal && !g.classList.contains('revealed')) g.reveal();
    for (const z of s.querySelectorAll('.zoomin')) if (z.deckReset) z.deckReset(true);
    for (const srt of s.querySelectorAll('.sort')) {
      const bins = srt.querySelectorAll('.bin'); let k = 0;
      srt.querySelectorAll('.tray .card').forEach(c => { bins[k++ % bins.length].appendChild(c); });
      if (srt.check) srt.check();
    }
    for (const g of s.querySelectorAll('.order, .line, .match')) if (g.solve) g.solve();
    for (const t of s.querySelectorAll('.heard textarea')) t.value = 'Pair 3: the pump runs dry\nPair 5: the timer is wrong\nPair 1: the cord gets wet\nPair 7: algae clogs the intake';
    await sleep(1600);
  });
}

async function measure(page) {
  return page.evaluate(() => {
    const s = document.querySelector('.slide.on');
    const foot = document.querySelector('.footer').getBoundingClientRect();
    const W = window.innerWidth, out = [], warn = [];
    const name = el => (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : el.tagName.toLowerCase());
    // Scrolling is the deck's last resort, fair on an 800x600 projector; from 1024x768 up
    // it means the slide carries too much, and the rubric's O-D8 fails it.
    if (s.classList.contains('tall')) (window.innerWidth < 1024 ? warn : out).push('scrolls: the type reached its floor (too much on one slide for this screen)');
    let bottom = 0, bottomEl = null, right = 0, rightEl = null;
    s.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return;
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
      let r = el.getBoundingClientRect();
      // what an overflow:hidden ancestor clips (a zoomed photo inside its frame) is not on screen
      for (let a = el.parentElement; a && a !== s; a = a.parentElement) {
        const ov = getComputedStyle(a).overflow;
        if (ov.includes('hidden') || ov.includes('clip')) {
          const c = a.getBoundingClientRect();
          r = { left: Math.max(r.left, c.left), right: Math.min(r.right, c.right), top: Math.max(r.top, c.top), bottom: Math.min(r.bottom, c.bottom) };
        }
      }
      if (!(r.right - r.left > 0) || !(r.bottom - r.top > 0)) return;
      if (r.bottom > bottom) { bottom = r.bottom; bottomEl = el; }
      if (r.right > right) { right = r.right; rightEl = el; }
    });
    if (!s.classList.contains('tall')) {
      if (bottom > foot.top - 2) out.push(`runs under the footer by ${Math.round(bottom - foot.top)}px (${name(bottomEl)})`);
      // the body's content may run into its own bottom margin; what fails is running into
      // the line beneath it, or past the slide's box (the footer check above covers that)
      const body = s.querySelector('.body');
      if (body) {
        const end = body.getBoundingClientRect().top + body.scrollHeight;
        let nx = body.nextElementSibling; while (nx && !nx.getClientRects().length) nx = nx.nextElementSibling;
        const lim = nx ? nx.getBoundingClientRect().top : s.getBoundingClientRect().bottom - parseFloat(getComputedStyle(s).paddingBottom);
        if (end > lim + 2) out.push(`body runs ${Math.round(end - lim)}px into ${nx ? 'the line beneath it' : 'the slide edge'}`);
      }
    }
    if (right > W + 1) out.push(`spills off the right by ${Math.round(right - W)}px (${name(rightEl)})`);
    if (s.scrollWidth > s.clientWidth + 2) out.push(`slide scrolls sideways by ${s.scrollWidth - s.clientWidth}px`);
    const chrome = '.eyebrow,.head-right,.cred,.vhint,.vlink,.dv-hint,.timer-ctl,.say,.k,.n,.where,.frames-label,.plabel,.hlabel,.pick-label,.bn,.binlab,.rlab,.ends,.gridline,.chip,.key,.lt,.called,.tally,.rounds,.vctl,.ixlab,.msn,.mtag,.zhint,.tfdots,.wiends,.ixctl';
    let small = 99, smallEl = '';
    s.querySelectorAll('h1,h2,h3,p,li,.t,.claim,.frame,.d,.ex,.lab,.cap,.why,.ixwhy,.opt,.card,.ocard,.mcard,.odd,.mst,.tfo,.lcard,.wilab,.es').forEach(el => {
      if (el.closest(chrome)) return;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || !el.textContent.trim()) return;
      const f = parseFloat(cs.fontSize);
      if (f < small) { small = f; smallEl = name(el); }
    });
    if (small < 15) warn.push(`smallest reading type ${Math.round(small * 10) / 10}px (${smallEl})`);
    return { out, warn, title: s.getAttribute('data-title') };
  });
}

(async () => {
  const browser = await launch();
  let failures = 0;
  for (const [w, h] of VIEWPORTS) {
    const page = await open(browser, deck, w, h);
    const n = await page.evaluate(() => document.querySelectorAll('.slide').length);
    const lines = [];
    if (SHOTS) fs.mkdirSync(path.join(SHOTS, `${w}x${h}`), { recursive: true });
    for (let i = 0; i < n; i++) {
      await slide(page, i);
      const a = await measure(page);
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${w}x${h}`, `${String(i + 1).padStart(2, '0')}-open.png`) });
      await play(page);
      const b = await measure(page);
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${w}x${h}`, `${String(i + 1).padStart(2, '0')}-played.png`) });
      const errs = [...a.out.map(x => 'open: ' + x), ...b.out.filter(x => !a.out.includes(x)).map(x => 'played: ' + x)];
      const warns = [...new Set([...a.warn, ...b.warn])];
      failures += errs.length;
      if (errs.length || warns.length) lines.push(`  ${String(i + 1).padStart(2)} ${a.title}: ` + [...errs.map(e => 'FAIL ' + e), ...warns.map(e => 'warn ' + e)].join('; '));
    }
    console.log(`${w}x${h}: ${lines.length ? lines.length + ' slide(s) flagged' : 'clean'}` + (page.errors.length ? ' · JS errors: ' + page.errors.join(' | ') : ''));
    failures += page.errors.length;
    lines.forEach(l => console.log(l));
    await page.close();
  }
  await browser.close();
  console.log(failures ? `\n${failures} layout failure(s)` : '\nlayout clean');
  process.exit(failures ? 1 : 0);
})();
