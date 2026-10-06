// Shared by the browser checks: find Playwright and Chromium wherever this machine keeps
// them, and open a built deck.
const path = require('path');

function playwright() {
  const tries = ['playwright', 'playwright-core'];
  try { tries.push(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright')); } catch (e) {}
  for (const m of tries) { try { return require(m); } catch (e) {} }
  console.error('Playwright is not installed. Install it with: npm i -g playwright && npx playwright install chromium');
  process.exit(2);
}

async function launch() {
  const { chromium } = playwright();
  const exe = process.env.CHROMIUM_PATH;
  return chromium.launch(exe ? { executablePath: exe } : {});
}

async function open(browser, deck, width, height) {
  const page = await browser.newPage({ viewport: { width, height } });
  page.errors = [];
  page.on('pageerror', e => page.errors.push(e.message));
  await page.goto('file://' + path.resolve(deck));
  await page.waitForTimeout(400);
  return page;
}

// open slide i (0-based) through the jump menu, exactly as a teacher's G would
async function slide(page, i) {
  await page.evaluate(n => document.querySelectorAll('#jumpList li')[n].click(), i);
  await page.waitForTimeout(300);
}

module.exports = { launch, open, slide };
