// SCRIPT: NU-V9-ART-SHOTS  render the art edition with MathJax served locally; count maths and errors; take screenshots
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const file = process.argv[2], out = process.argv[3], base = process.env.NU_MATHJAX + '/';
  const b = await chromium.launch();
  for (const [name, w, h] of [['desk', 1680, 1000], ['laptop', 1280, 800], ['phone', 390, 800]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.route(/cdnjs\.cloudflare\.com\/ajax\/libs\/mathjax\/3\.2\.2\/es5\/(.*)/, async (route) => {
      const f = base + route.request().url().match(/es5\/(.*)$/)[1];
      if (fs.existsSync(f)) await route.fulfill({ body: fs.readFileSync(f), contentType: 'application/javascript' }); else await route.fulfill({ status: 404, body: '' });
    });
    await p.goto('file://' + file, { waitUntil: 'load' });
    await p.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, { timeout: 90000 });
    await p.evaluate(() => MathJax.startup.promise); await p.waitForTimeout(1500);
    const r = await p.evaluate(() => ({ math: document.querySelectorAll('mjx-container').length, err: document.querySelectorAll('mjx-merror,[data-mjx-error]').length,
      hscroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      wide: [...document.querySelectorAll('section.level1 mjx-container')].filter(c => { const s = c.closest('section').getBoundingClientRect(), q = c.getBoundingClientRect(); return q.right > s.right + 2; }).length,
      fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style) }));
    console.log(name, JSON.stringify(r));
    await p.screenshot({ path: `${out}/${name}_top.png` });
    for (const [tag, sel] of [['cut', '[id="sec:cut"]'], ['fig', 'figure'], ['table', 'table'], ['code', 'pre'], ['link', '[id="sec:link"]'], ['proofs', '#proofs']]) {
      const ok = await p.evaluate(s => { const e = document.querySelector(s); if (!e) return false; document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - 20); return true; }, sel);
      if (ok) { await p.waitForTimeout(250); await p.screenshot({ path: `${out}/${name}_${tag}.png` }); }
    }
    await p.close();
  }
  await b.close();
})();
