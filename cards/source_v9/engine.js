// CARD ENGINE v1 — 1080x1350 portrait card, hydrogen-card layout: title, left readouts, main WebGL view, scale at right,
// three live panels, footer. window.render(p) draws loop phase p in [0,1). Deterministic: no clocks, no randomness.
(function () {
  const W = 1080, H = 1350, MX = 190, MY = 112, MW = 700, MH = 640;
  const FONT = '"DejaVu Sans", "Helvetica Neue", Arial, sans-serif';
  const C = { bg: '#000', fg: '#f2f2f2', mut: '#a6a6a6', dim: '#6f6f6f', acc: '#ffbf4d', grid: '#262626', panel: '#0b0b0d', line: '#333' };
  window.CC = C; window.FONT = FONT;
  document.body.style.cssText = 'margin:0;background:#000;width:1080px;height:1350px;overflow:hidden;position:relative';
  const gl = document.createElement('canvas'); gl.width = MW; gl.height = MH;
  gl.style.cssText = `position:absolute;left:${MX}px;top:${MY}px;width:${MW}px;height:${MH}px`;
  const ov = document.createElement('canvas'); ov.width = W; ov.height = H; ov.style.cssText = 'position:absolute;left:0;top:0';
  document.body.append(gl, ov);
  const ctx = ov.getContext('2d');
  const renderer = new THREE.WebGLRenderer({ canvas: gl, antialias: true, preserveDrawingBuffer: true, alpha: false });
  renderer.setPixelRatio(1); renderer.setSize(MW, MH, false); renderer.setClearColor(0x000000, 1);
  const scene = new THREE.Scene(); const camera = new THREE.PerspectiveCamera(34, MW / MH, 0.05, 100);
  const card = window.CARD;

  // ---------- helpers exposed to cards
  const H_ = window.H = {};
  H_.text = (s, x, y, o = {}) => { ctx.font = `${o.bold ? 'bold ' : ''}${o.size || 15}px ${FONT}`; ctx.fillStyle = o.color || C.fg; ctx.textAlign = o.align || 'left'; ctx.textBaseline = o.base || 'alphabetic'; ctx.fillText(s, x, y); };
  H_.hsl = (phase, light = 0.55) => { const h = ((phase / (2 * Math.PI)) % 1 + 1) % 1; return `hsl(${(h * 360).toFixed(1)},95%,${(light * 100).toFixed(1)}%)`; };
  H_.inferno = (t) => { // compact inferno ramp
    const S = [[0, 0, 4], [40, 11, 84], [101, 21, 110], [159, 42, 99], [212, 72, 66], [245, 125, 21], [250, 193, 39], [252, 255, 164]];
    t = Math.max(0, Math.min(1, t)) * (S.length - 1); const i = Math.min(S.length - 2, Math.floor(t)), f = t - i;
    return S[i].map((a, j) => a + (S[i + 1][j] - a) * f); };
  H_.rgb = (a) => `rgb(${a[0] | 0},${a[1] | 0},${a[2] | 0})`;
  // a plot frame: returns mapping functions; opts {x0,x1,y0,y1,logx,logy,xt:[[v,label]],yt,xl,yl}
  H_.frame = (X, Y, w, h, o) => {
    ctx.fillStyle = C.panel; ctx.fillRect(X, Y, w, h);
    const L = X + 52, R = X + w - 12, T = Y + 30, B = Y + h - 34;
    const fx = v => { const a = o.logx ? Math.log10(v) : v, a0 = o.logx ? Math.log10(o.x0) : o.x0, a1 = o.logx ? Math.log10(o.x1) : o.x1; return L + (a - a0) / (a1 - a0) * (R - L); };
    const fy = v => { const a = o.logy ? Math.log10(v) : v, a0 = o.logy ? Math.log10(o.y0) : o.y0, a1 = o.logy ? Math.log10(o.y1) : o.y1; return B - (a - a0) / (a1 - a0) * (B - T); };
    ctx.strokeStyle = C.grid; ctx.lineWidth = 1;
    for (const [v, s] of o.yt || []) { const y = fy(v); ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(R, y); ctx.stroke(); H_.text(s, L - 6, y + 4, { size: 11, color: C.mut, align: 'right' }); }
    for (const [v, s] of o.xt || []) { const x = fx(v); ctx.beginPath(); ctx.moveTo(x, T); ctx.lineTo(x, B); ctx.stroke(); H_.text(s, x, B + 15, { size: 11, color: C.mut, align: 'center' }); }
    if (o.xl) H_.text(o.xl, (L + R) / 2, B + 29, { size: 11, color: C.mut, align: 'center' });
    if (o.yl) H_.text(o.yl, X + 8, Y + 18, { size: 12, color: C.mut });
    return { fx, fy, L, R, T, B, clip: () => { ctx.save(); ctx.beginPath(); ctx.rect(L, T - 2, R - L, B - T + 4); ctx.clip(); }, unclip: () => ctx.restore() };
  };
  H_.curve = (xs, ys, F, o = {}) => { ctx.beginPath(); let on = false;
    for (let i = 0; i < xs.length; i++) { const v = ys[i]; if (v === null || !isFinite(v) || (o.logy && v <= 0)) { on = false; continue; }
      const x = F.fx(xs[i]), y = F.fy(v); if (!on) { ctx.moveTo(x, y); on = true; } else ctx.lineTo(x, y); }
    ctx.strokeStyle = o.color || C.acc; ctx.lineWidth = o.width || 2; ctx.setLineDash(o.dash || []); if (o.glow) { ctx.shadowColor = o.color; ctx.shadowBlur = o.glow; } ctx.stroke(); ctx.setLineDash([]); ctx.shadowBlur = 0; };
  H_.hline = (F, v, o = {}) => { ctx.beginPath(); ctx.moveTo(F.L, F.fy(v)); ctx.lineTo(F.R, F.fy(v)); ctx.strokeStyle = o.color || C.mut; ctx.lineWidth = o.width || 1; ctx.setLineDash(o.dash || [5, 4]); ctx.stroke(); ctx.setLineDash([]);
    if (o.label) H_.text(o.label, o.right ? F.R - 4 : F.L + 6, F.fy(v) + (o.below ? 14 : -5), { size: 11, color: o.color || C.mut, align: o.right ? 'right' : 'left' }); };
  H_.dot = (x, y, o = {}) => { ctx.beginPath(); ctx.arc(x, y, o.r || 7, 0, 2 * Math.PI); ctx.fillStyle = o.color || C.acc; ctx.shadowColor = o.color || C.acc; ctx.shadowBlur = 14; ctx.fill(); ctx.shadowBlur = 0; };
  H_.vline = (F, x, o = {}) => { ctx.beginPath(); ctx.moveTo(x, F.T); ctx.lineTo(x, F.B); ctx.strokeStyle = o.color || '#555'; ctx.lineWidth = 1; ctx.stroke(); };
  H_.wheel = (cx, cy, r, o = {}) => { for (let a = 0; a < 360; a += 2) { ctx.beginPath(); ctx.arc(cx, cy, r, a * Math.PI / 180, (a + 2.5) * Math.PI / 180); ctx.strokeStyle = H_.hsl(-a * Math.PI / 180); ctx.lineWidth = r * 0.45; ctx.stroke(); }
    H_.text('0', cx + r + 16, cy + 4, { size: 11, color: C.mut }); H_.text('π', cx - r - 16, cy + 4, { size: 11, color: C.mut, align: 'right' }); };
  H_.ctx = ctx;
  card.setup3D && card.setup3D(scene, camera, renderer);

  window.render = function (p) {
    ctx.clearRect(0, 0, W, H);
    card.update3D && card.update3D(p, scene, camera);
    renderer.render(scene, camera);
    // header
    H_.text(card.title, W / 2, 52, { size: 33, bold: true, align: 'center' });
    H_.text(card.sub, W / 2, 84, { size: 18, color: C.mut, align: 'center' });
    H_.text(card.mainLabel, MX + MW / 2, 132, { size: 19, bold: true, align: 'center' });
    // left readouts
    let y = 190;
    for (const r of card.left(p)) {
      if (r.gap) { y += r.gap; continue; }
      H_.text(r.label, 16, y, { size: 15, color: C.mut }); y += r.big ? 30 : 22;
      for (const v of [].concat(r.value)) { H_.text(v, 16, y, { size: r.big ? 27 : 15, bold: !!r.big, color: r.big ? C.acc : (r.color || C.fg) }); y += r.big ? 24 : 20; }
      y += 16;
    }
    card.scale && card.scale(p, 900, 160);
    card.overlay && card.overlay(p, MX, MY, MW, MH);
    H_.text(card.caption, W / 2, 786, { size: 17, color: '#e8e8e8', align: 'center' });
    // panels
    const PW = 344, PY = 800, PHt = 362, gap = 12, PX0 = 10;
    card.panels.forEach((pn, i) => { const X = PX0 + i * (PW + gap); H_.text(pn.title, X + 4, PY + 18, { size: 15, bold: true }); pn.draw(ctx, X, PY + 28, PW, PHt - 28, p); });
    // footer
    let fy = 1196; card.foot.forEach((s, i) => { H_.text(s, W / 2, fy, { size: i === 0 ? 13 : 14.5, color: i === 0 ? C.mut : '#dcdcdc', align: 'center' }); fy += 21; });
    ctx.strokeStyle = '#2a2a2a'; ctx.beginPath(); ctx.moveTo(0, 1318); ctx.lineTo(W, 1318); ctx.stroke();
    H_.text('Jeromie Beasley · X @d1c1pler · YouTube @AtlasMemoriae · GitHub dicipler-pixel · atlas-memoriae.dicipler.workers.dev', W / 2, 1338, { size: 13.5, color: C.mut, align: 'center' });
    return true;
  };
  window.__ready = true;
})();
