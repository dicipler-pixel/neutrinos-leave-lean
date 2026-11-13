// SCRIPT: NU-ART-CARD-B1  the twin collapse: two GR runs identical in every fluid and metric array and in l = 0, 1, 2, 4,
// opposite only in hidden l = 3 structure planted at decoupling; one forms a black hole, the other disperses
(function () {
  const D = window.DATA_B1, R = D.r, NR = R.length, E0 = 2.0, E1 = Math.max(D.plus.eps_end, D.minus.eps_end);
  const epsOf = p => E0 + (E1 - E0) * G3.clock(p);
  const XS = 2.1 / 2.6, YS = 2.6 / (E1 - E0), ZS = 1.15, XL = -1.25, XRt = 1.25;
  const GOLD = new THREE.Color(0xffc850), BLUE = new THREE.Color(0x58c8ff);
  const allSh = [].concat(...D.minus.share, ...D.plus.share); const shMin = Math.floor(Math.min(...allSh) * 100) / 100, shMax = Math.ceil(Math.max(...allSh) * 100) / 100;
  let surf = {}, hole, rim, horizonShown = false;
  function build(scene, run, x0) {
    const NE = run.eps.length, g = new THREE.BufferGeometry();
    const pos = new Float32Array(NR * NE * 3), col = new Float32Array(NR * NE * 3), idx = [];
    for (let j = 0; j < NE - 1; j++) for (let i = 0; i < NR - 1; i++) { const a = j * NR + i, b = a + 1, c = a + NR, d = c + 1; idx.push(a, b, c, b, d, c); }
    g.setIndex(idx); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const m = new THREE.Mesh(g, new THREE.MeshPhongMaterial({ vertexColors: true, side: THREE.DoubleSide, shininess: 30, specular: 0x222222 }));
    scene.add(m);
    const wire = new THREE.LineSegments(new THREE.WireframeGeometry(g), new THREE.LineBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.18 }));
    return { run, g, NE, x0, m };
  }
  function fill(s, ec) {
    const pos = s.g.attributes.position.array, col = s.g.attributes.color.array, c = new THREE.Color(), run = s.run;
    let jl = 0; while (jl + 1 < s.NE && run.eps[jl + 1] <= ec) jl++;           // last row reached
    for (let j = 0; j < s.NE; j++) { const jj = Math.min(j, jl);
      for (let i = 0; i < NR; i++) { const k = (j * NR + i) * 3, C = run.C[jj][i], sh = run.share[jj][i];
        pos[k] = s.x0 - 1.05 + R[i] * XS; pos[k + 1] = -1.3 + (run.eps[jj] - E0) * YS; pos[k + 2] = C * ZS;
        const t = Math.max(0, Math.min(1, (sh - shMin) / (shMax - shMin))); c.copy(GOLD).lerp(BLUE, t);
        const L = 0.30 + 0.85 * Math.min(1, Math.max(0, C) / 0.6); col[k] = c.r * L; col[k + 1] = c.g * L; col[k + 2] = c.b * L; } }
    s.g.attributes.position.needsUpdate = true; s.g.attributes.color.needsUpdate = true; s.g.computeVertexNormals();
    return jl;
  }
  window.CARD = {
    title: 'Same density. Same flux. Same stress. Different future.',
    sub: "McCormick's general-relativistic collapse, restarted at decoupling (ε = 2) with hidden ℓ = 3 structure of opposite sign",
    mainLabel: 'Compaction C(r, ε) of the twin runs, δ = 0.5107',
    caption: 'height = compaction · colour = share of the energy in neutrinos (gold radiation → blue neutrinos) · time runs into the page',
    setup3D(scene, camera) {
      surf.minus = build(scene, D.minus, XL); surf.plus = build(scene, D.plus, XRt);
      scene.add(new THREE.AmbientLight(0xffffff, 0.55)); const dl = new THREE.DirectionalLight(0xffffff, 0.8); dl.position.set(-2, -5, 6); scene.add(dl);
      const lg = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, -1.4, 0), new THREE.Vector3(0, 1.45, 0)]);
      scene.add(new THREE.Line(lg, new THREE.LineBasicMaterial({ color: 0xffc850, transparent: true, opacity: 0.6 })));
      for (const x0 of [XL, XRt]) { const bg = new THREE.Mesh(new THREE.PlaneGeometry(2.25, 2.75), new THREE.MeshBasicMaterial({ color: 0x0b0b0d, side: THREE.DoubleSide }));
        bg.position.set(x0, 0.0, -0.002); scene.add(bg); }
      hole = new THREE.Mesh(new THREE.SphereGeometry(0.12, 48, 32), new THREE.MeshBasicMaterial({ color: 0x000000 }));
      rim = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.010, 16, 96), new THREE.MeshBasicMaterial({ color: 0xffc850 }));
      hole.visible = rim.visible = false; scene.add(hole, rim);
      camera.up.set(0, 0, 1); camera.position.set(0.0, -4.9, 4.4); camera.lookAt(0, 0.35, 0.1); this._cam = camera;
    },
    update3D(p) { const ec = epsOf(p);
      const jm = fill(surf.minus, ec); fill(surf.plus, ec);
      horizonShown = ec >= D.minus.eps_end - 1e-9;
      const last = D.minus.C[jm], ip = last.indexOf(Math.max(...last));
      const hx = XL - 1.05 + R[ip] * XS, hy = -1.3 + (D.minus.eps[jm] - E0) * YS, hz = last[ip] * ZS + 0.05;
      hole.position.set(hx, hy, hz); rim.position.set(hx, hy, hz); rim.lookAt(this._cam.position); hole.visible = rim.visible = horizonShown; },
    overlay(p, MX, MY, MW, MH) { const cam = this._cam, ec = epsOf(p);
      const lab = (v, s, o) => { const [x, y] = G3.project(v, cam, MX, MY, MW, MH); H.text(s, x, y, o); };
      lab(new THREE.Vector3(XL, -1.55, 0), 'hidden ℓ = 3 negative', { size: 14, color: '#dddddd', align: 'center' });
      lab(new THREE.Vector3(XRt, -1.55, 0), 'hidden ℓ = 3 positive', { size: 14, color: '#dddddd', align: 'center' });
      lab(new THREE.Vector3(XL + 1.1, -1.42, 0), 'r', { size: 13, color: CC.mut });
      lab(new THREE.Vector3(XRt + 1.18, 1.3, 0), 'ε', { size: 15, bold: true, color: CC.mut });
      if (horizonShown) lab(hole.position.clone().add(new THREE.Vector3(0.0, 0, 0.22)), `apparent horizon, ε = ${D.minus.eps_end.toFixed(3)}`, { size: 14, bold: true, color: '#ffd27a', align: 'left' });
      if (ec >= D.plus.eps_end - 1e-9) lab(new THREE.Vector3(XRt, 1.3, 0.75), `disperses, ε = ${D.plus.eps_end.toFixed(3)}`, { size: 14, bold: true, color: '#9cc9ff', align: 'center' }); },
    left(p) { const ec = epsOf(p), at = (run) => { let j = 0; while (j + 1 < run.eps.length && run.eps[j + 1] <= ec) j++; return run.Cmax[j]; };
      const cm = at(D.minus), cp = at(D.plus), M = D.mom;
      return [{ label: 'time', value: [`ε = ${ec.toFixed(3)}`], big: true }, { label: G3.rewinding(p) ? 'rewinding the loop' : '', value: [] },
        { label: 'peak compaction', value: [`ℓ₃ −: ${cm.toFixed(4)}`, `ℓ₃ +: ${cp.toFixed(4)}`] },
        { label: 'restart, ℓ = 0, 1, 2, 4', value: [`equal to ${Math.max(M.maxdiff_rel[0], M.maxdiff_rel[1], M.maxdiff_rel[2], M.maxdiff_rel[4]).toExponential(0)}`, 'fluid, metric:', 'bit-identical'], color: '#9cff9c' },
        { label: 'restart, ℓ = 3', value: [`${M.minus[3].toFixed(4)}`, `+${M.plus[3].toFixed(4)}`, 'of the density'], color: '#9cc9ff' },
        { label: 'thresholds', value: [`ℓ₃ − ${D.thresholds.minus}`, `ℓ₃ + ${D.thresholds.plus}`, `apart ${(D.thresholds.plus - D.thresholds.minus).toExponential(2)}`] }]; },
    scale(p, X, Y) { H.text('neutrino share', X, Y, { size: 14, color: CC.mut }); H.text('of the energy', X, Y + 19, { size: 14, color: CC.mut });
      const ctx = H.ctx; for (let i = 0; i <= 120; i++) { const t = i / 120, c = GOLD.clone().lerp(BLUE, t); ctx.fillStyle = '#' + c.getHexString(); ctx.fillRect(X + 4, Y + 160 - i, 26, 1.5); }
      H.text(shMax.toFixed(2), X + 38, Y + 46, { size: 12, color: CC.mut }); H.text(shMin.toFixed(2), X + 38, Y + 164, { size: 12, color: CC.mut });
      H.text('height =', X, Y + 205, { size: 14, color: CC.mut }); H.text('compaction C', X, Y + 224, { size: 14, color: CC.mut });
      H.text('brighter = higher', X, Y + 243, { size: 13, color: CC.dim }); },
    panels: [
      { title: 'Peak compaction, the twins', draw(ctx, X, Y, w, h, p) { const ec = epsOf(p);
        const F = H.frame(X, Y, w, h, { x0: 2, x1: 5.7, y0: 0.2, y1: 1.0, xt: [[2, '2'], [3, '3'], [4, '4'], [5, '5']], yt: [[0.25, '0.25'], [0.5, '0.5'], [0.75, '0.75'], [1, '1']], xl: 'ε' });
        const cut = (run) => { const xs = [], ys = []; for (let j = 0; j < run.eps.length && run.eps[j] <= ec + 1e-9; j++) { xs.push(run.eps[j]); ys.push(run.Cmax[j]); } return [xs, ys]; };
        const [xm, ym] = cut(D.minus), [xp, yp] = cut(D.plus);
        H.curve(xp, yp, F, { color: '#58c8ff', width: 2.4, glow: 6 }); H.curve(xm, ym, F, { color: '#ffbf4d', width: 2.4, glow: 6 });
        if (xm.length) H.dot(F.fx(xm[xm.length - 1]), F.fy(ym[ym.length - 1]), { color: '#ffbf4d', r: 5 });
        if (xp.length) H.dot(F.fx(xp[xp.length - 1]), F.fy(yp[yp.length - 1]), { color: '#58c8ff', r: 5 });
        H.text('ℓ₃ negative → black hole', F.L + 6, F.T + 14, { size: 11, color: '#ffd27a' }); H.text('ℓ₃ positive → disperses', F.L + 6, F.T + 30, { size: 11, color: '#9cc9ff' }); } },
      { title: 'The two restart states, ℓ = 1…4', draw(ctx, X, Y, w, h, p) { const M = D.mom;
        const F = H.frame(X, Y, w, h, { x0: 0.4, x1: 4.6, y0: -0.05, y1: 0.05, xt: [[1, '1 flux'], [2, '2 stress'], [3, '3 hidden'], [4, '4']], yt: [[-0.04, '−0.04'], [0, '0'], [0.04, '0.04']], xl: 'moment ℓ (relative to ℓ = 0, equal at 1)' });
        for (let l = 1; l <= 4; l++) { const bw = (F.fx(1) - F.fx(0.4)) * 0.28;
          for (const [v, dx, c] of [[M.minus[l], -bw * 0.55, '#ffbf4d'], [M.plus[l], bw * 0.55, '#58c8ff']]) {
            const x = F.fx(l) + dx, y0 = F.fy(0), y1 = F.fy(v); ctx.fillStyle = c; ctx.shadowColor = c; ctx.shadowBlur = 8; ctx.fillRect(x - bw / 2, Math.min(y0, y1), bw, Math.abs(y1 - y0)); ctx.shadowBlur = 0; } }
        H.text(`cell r = ${M.r.toFixed(2)}, where ℓ = 3 differs most`, F.R - 4, F.B - 8, { size: 10.5, color: CC.mut, align: 'right' }); } },
      { title: 'Where each twin collapses', draw(ctx, X, Y, w, h, p) { const T = D.thresholds;
        const F = H.frame(X, Y, w, h, { x0: 0.5080, x1: 0.5134, y0: 0, y1: 1, xt: [[0.509, '0.509'], [0.511, '0.511'], [0.513, '0.513']], yt: [], xl: 'initial amplitude δ' });
        const band = (a, b, c) => { ctx.fillStyle = c; ctx.fillRect(F.fx(a), F.T, F.fx(b) - F.fx(a), F.B - F.T); };
        band(T.minus, 0.5134, 'rgba(255,191,77,0.10)'); band(T.plus, 0.5134, 'rgba(88,200,255,0.10)');
        for (const [v, s, c, yy] of [[T.minus, 'ℓ₃ negative', '#ffbf4d', 0.82], [T.none, 'no hidden ℓ₃', '#a6a6a6', 0.62], [T.plus, 'ℓ₃ positive', '#58c8ff', 0.82]]) {
          H.vline(F, F.fx(v), { color: c }); H.text(s, F.fx(v) + (v === T.plus ? -4 : 4), F.fy(yy), { size: 11, color: c, align: v === T.plus ? 'right' : 'left' }); H.text(v.toFixed(5), F.fx(v) + (v === T.plus ? -4 : 4), F.fy(yy) + 14, { size: 10.5, color: c, align: v === T.plus ? 'right' : 'left' }); }
        H.dot(F.fx(D.delta), F.fy(0.3), { color: '#ffffff', r: 6 }); H.text('this pair, δ = 0.5107', F.fx(D.delta), F.fy(0.3) + 22, { size: 11, color: '#ffffff', align: 'center' });
        H.text('black hole to the right of each line', F.R - 4, F.B - 8, { size: 10.5, color: CC.mut, align: 'right' }); } },
    ],
    foot: ['McCormick PBH_neutrino_simulation (eb7c4de) · N = 400, 32 bins, R_ν = 0.409, ε_dec = 2, n = 3 · restart dI = ±f·b(r)·m·(ε/4π)·p₃(μ), f = 0.5',
      'each run ends at an apparent horizon (2M/R ≥ 1, infalling) or McCormick\'s dispersal rule · threshold brackets under 2e-5 wide',
      'Card B1 · When the Neutrinos Leave · What the Neutrino State Must Keep, v9 · nothing drawn by hand'],
  };
})();
