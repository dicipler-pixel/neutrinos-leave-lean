// usage: node capture.js P1 [still p1,p2,...] | [video out.mp4]
const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async () => {
  const [card, mode, arg] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  pg.on('console', m => { if (m.type() === 'error') console.error('PAGE', m.text()); }); pg.on('pageerror', e => console.error('PAGEERR', e.message));
  await pg.goto('file://' + __dirname + '/card_' + card + '.html'); await pg.waitForFunction(() => window.__ready, null, { timeout: 60000 });
  if (mode === 'still') { for (const p of arg.split(',').map(Number)) { await pg.evaluate(p => window.render(p), p); await pg.screenshot({ path: `${__dirname}/still_${card}_${p}.png` }); } }
  else { const NF = 480; const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', arg], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < NF; i++) { await pg.evaluate(p => window.render(p), i / NF); const buf = await pg.screenshot({ type: 'png' }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 60 === 0) console.log(card, i, ((Date.now() - t0) / 1000).toFixed(0) + 's'); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await b.close();
})();
