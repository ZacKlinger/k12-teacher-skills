// The Jeopardy review board fills one screen at every classroom size: no scrolling, the
// last row of tiles above the bottom edge, category names large enough for the back row,
// and a clicker's → reveals an open clue and then closes it.
//   node review_board.js <review_game_template.html or a filled copy>
const path = require('path');
const { launch, fileUrl } = require('./common');
(async () => {
  const b = await launch();
  let fail = 0;
  for (const [w, h] of [[800, 600], [1024, 768], [1280, 720], [1366, 657], [1920, 1080]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(fileUrl(process.argv[2])); await p.waitForTimeout(300);
    const r = await p.evaluate(() => {
      const tiles = [...document.querySelectorAll('.tile')], last = tiles[tiles.length - 1].getBoundingClientRect();
      return { scroll: document.documentElement.scrollHeight - innerHeight, bottom: last.bottom, cat: parseFloat(getComputedStyle(document.querySelector('.cat')).fontSize) };
    });
    await p.click('.tile'); await p.waitForTimeout(100);
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
    const revealed = await p.evaluate(() => document.getElementById('curAnswer').classList.contains('on'));
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(100);
    const closed = await p.evaluate(() => !document.getElementById('curtain').classList.contains('show'));
    const bad = [];
    if (r.scroll > 1) bad.push(`scrolls ${r.scroll}px`);
    if (r.bottom > h) bad.push('last row below the screen');
    if (r.cat < 13) bad.push(`category names ${r.cat}px`);
    if (!revealed || !closed) bad.push('→ does not reveal then close a clue');
    bad.push(...errs);
    fail += bad.length;
    console.log(`${w}x${h}: ${bad.length ? 'FAIL ' + bad.join('; ') : 'ok'} (category names ${Math.round(r.cat)}px)`);
    await p.close();
  }
  await b.close();
  process.exit(fail ? 1 : 0);
})();
