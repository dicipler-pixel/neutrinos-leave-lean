// SCRIPT: NU-V9-RENDER  render the HTML paper with MathJax 3.2.2 served locally; count maths elements and errors
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const fs = require('fs'); const base = (process.env.NU_MATHJAX || './node_modules/mathjax/es5') + '/';  // local MathJax 3.2.2 (npm install mathjax@3.2.2)
  await p.route(/cdnjs\.cloudflare\.com\/ajax\/libs\/mathjax\/3\.2\.2\/es5\/(.*)/, async (route) => {
    const m = route.request().url().match(/es5\/(.*)$/); const f = base + m[1];
    if (fs.existsSync(f)) await route.fulfill({ body: fs.readFileSync(f), contentType: f.endsWith('.js') ? 'application/javascript' : 'application/octet-stream' });
    else await route.fulfill({ status: 404, body: '' });
  });
  await p.goto('file://' + process.argv[2], { waitUntil: 'load' });
  await p.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, { timeout: 60000 });
  await p.evaluate(() => MathJax.startup.promise);
  const r = await p.evaluate(() => ({ math: document.querySelectorAll('mjx-container').length, err: document.querySelectorAll('mjx-merror, [data-mjx-error]').length, raw: (document.body.innerText.match(/\\\(|\\\[/g) || []).length }));
  console.log(JSON.stringify(r)); await b.close();
})();
