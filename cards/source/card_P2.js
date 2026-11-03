// CARD P2 — the density pole exists exactly when kappa > Z_b^free(0) = 2k/pi; the pole is born out of the cut
(function () {
  const D = DATA.P2, ON = 2 / Math.PI;
  const kapOf = p => 0.74 - 0.30 * Math.cos(2 * Math.PI * p);
  // complex arithmetic on [re, im]
  const add = (a, b) => [a[0] + b[0], a[1] + b[1]], mul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
  const div = (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; };
  const log = a => [Math.log(Math.hypot(a[0], a[1])), Math.atan2(a[1], a[0])];
  const atan = z => { const iz = [-z[1], z[0]]; const L = add(log([1 - iz[0], -iz[1]]), mul([-1, 0], log([1 + iz[0], iz[1]]))); return [-L[1] / 2, L[0] / 2]; }; // (i/2)(log(1-iz)-log(1+iz))
  const Gs = (x, y, kap) => { const g = atan(div([1, 0], [x + kap, y])); return div(g, [1 - kap * g[0], -kap * g[1]]); };
  const pole = kap => kap > ON ? 1 / Math.tan(1 / kap) - kap : null;
  const X0 = -1.6, X1 = 0.45, Y0 = -1.45, Y1 = 1.45, NX = 190, NY = 230, HS = 0.42, HMIN = -1.0, HMAX = 1.3;
  const px = x => (x - (X0 + X1) / 2) * 1.55, py = y => y * 1.25, pz = h => (h - HMIN) * HS - 0.55;
  let geo, mesh, cut, beam, beamGlow, floorGrid;
  const domain = document.createElement('canvas'); domain.width = 150; domain.height = 150;
  window.CARD = {
    title: 'When collisions win, the density gets a pole.',
    sub: 'Kept propagator G = g/(1 − κg), g = arctan(k/(s+κ))/k, exact (all moments kept)',
    mainLabel: 'Landscape of |G(s)| over the complex rate s',
    caption: 'height = log₁₀|G| · colour = phase of G · the slit is the cut Re s = −κ · the spike is the density pole',
    setup3D(scene, camera) {
      geo = new THREE.PlaneGeometry(1, 1, NX, NY); geo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(geo.attributes.position.count * 3), 3));
      mesh = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide })); scene.add(mesh);
      scene.add(new THREE.AmbientLight(0xffffff, 0.55)); const dl = new THREE.DirectionalLight(0xffffff, 0.9); dl.position.set(-2, -3, 5); scene.add(dl);
      const lg = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
      cut = new THREE.Line(lg, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.95 })); scene.add(cut);
      beam = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1, 12), new THREE.MeshBasicMaterial({ color: 0xfff2c0 })); beam.rotation.x = Math.PI / 2; scene.add(beam);
      beamGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: G3.glowTex(), color: 0xffd27a, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false })); scene.add(beamGlow);
      const fp = []; for (let i = -6; i <= 6; i++) { fp.push(new THREE.Vector3(px(X0), py(i * 0.25), pz(HMIN)), new THREE.Vector3(px(X1), py(i * 0.25), pz(HMIN))); }
      for (let x = -1.5; x <= 0.45; x += 0.25) fp.push(new THREE.Vector3(px(x), py(Y0), pz(HMIN)), new THREE.Vector3(px(x), py(Y1), pz(HMIN)));
      floorGrid = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(fp), new THREE.LineBasicMaterial({ color: 0x2a2a2a })); scene.add(floorGrid);
    },
    update3D(p, scene, camera) {
      const kap = kapOf(p), pos = geo.attributes.position.array, col = geo.attributes.color.array, c = new THREE.Color();
      for (let j = 0; j <= NY; j++) for (let i = 0; i <= NX; i++) {
        const k = j * (NX + 1) + i, x = X0 + (X1 - X0) * i / NX, y = Y1 - (Y1 - Y0) * j / NY, G = Gs(x, y, kap);
        const h = Math.max(HMIN, Math.min(HMAX, Math.log10(Math.hypot(G[0], G[1]) + 1e-12)));
        pos[3 * k] = px(x); pos[3 * k + 1] = py(y); pos[3 * k + 2] = pz(h);
        const ph = Math.atan2(G[1], G[0]); c.setHSL(((ph / (2 * Math.PI)) % 1 + 1) % 1, 0.78, 0.18 + 0.42 * (h - HMIN) / (HMAX - HMIN));
        col[3 * k] = c.r; col[3 * k + 1] = c.g; col[3 * k + 2] = c.b; }
      geo.attributes.position.needsUpdate = true; geo.attributes.color.needsUpdate = true; geo.computeVertexNormals();
      const cp = []; for (let i = 0; i <= 80; i++) { const y = -1 + 2 * i / 80, G = Gs(-kap + 1e-4, y, kap), h = Math.max(HMIN, Math.min(HMAX, Math.log10(Math.hypot(G[0], G[1]) + 1e-12))); cp.push(new THREE.Vector3(px(-kap), py(y), pz(h) + 0.03)); } cut.geometry.dispose(); cut.geometry = new THREE.BufferGeometry().setFromPoints(cp);
      const sp = pole(kap); beam.visible = beamGlow.visible = sp !== null;
      if (sp !== null) { const z0 = pz(HMIN), z1 = pz(HMAX) + 0.35; beam.position.set(px(sp), 0, (z0 + z1) / 2); beam.scale.set(1, z1 - z0, 1); beamGlow.position.set(px(sp), 0, z1); beamGlow.scale.setScalar(0.45); }
      const a = -2.35 + 0.55 * Math.sin(2 * Math.PI * p), e = 38 * Math.PI / 180, d = 6.4;
      camera.up.set(0, 0, 1); camera.position.set(d * Math.cos(e) * Math.cos(a), d * Math.cos(e) * Math.sin(a), d * Math.sin(e) + 0.2); camera.lookAt(0, 0, 0.1);
      this._cam = camera;
    },
    overlay(p, MX, MY, MW, MH) { const kap = kapOf(p), sp = pole(kap), cam = this._cam;
      const [cx, cy] = G3.project(new THREE.Vector3(px(-kap), py(1.12), pz(0.3)), cam, MX, MY, MW, MH); H.text('cut, Re s = −κ', cx, cy - 8, { size: 13, color: '#e8e8e8', align: 'center' });
      if (sp !== null) { const [bx, by] = G3.project(new THREE.Vector3(px(sp), 0, pz(HMAX) + 0.45), cam, MX, MY, MW, MH); H.text('density pole', bx, by - 14, { size: 14, bold: true, color: '#ffd27a', align: 'center' }); }
      for (const [x, s] of [[0, 'Re s = 0'], [-1, '−k']]) { const [ax, ay] = G3.project(new THREE.Vector3(px(x), py(Y0) - 0.08, pz(HMIN)), cam, MX, MY, MW, MH); H.text(s, ax, ay + 12, { size: 12, color: CC.mut, align: 'center' }); } },
    left(p) { const kap = kapOf(p), sp = pole(kap);
      return [{ label: 'collision rate', value: [`κ = ${kap.toFixed(3)} k`], big: true }, { gap: 18 },
        { label: 'exact onset', value: ['κ* = 2k/π', '= 0.63662 k'], color: '#ffd27a' },
        { label: 'state', value: sp === null ? ['no pole:', 'density only leaks', 'through the cut'] : ['pole present'], color: sp === null ? '#9fd8ff' : '#ffd27a' },
        { label: 'pole position', value: sp === null ? ['—'] : [`s* = ${sp.toFixed(4)} k`] },
        { label: 'pole above the cut', value: sp === null ? ['—'] : [`s* + κ = ${(sp + kap).toFixed(4)} k`] },
        { label: 'onset reads', value: ['κ > Z_b,free(0) = 2k/π', '(card P1)'] }]; },
    scale(p, X, Y) { H.text('colour = arg G', X, Y, { size: 14, color: CC.mut }); H.wheel(X + 70, Y + 62, 34);
      H.text('height and', X, Y + 135, { size: 14, color: CC.mut }); H.text('brightness =', X, Y + 154, { size: 14, color: CC.mut }); H.text('log₁₀|G|', X, Y + 173, { size: 14, color: CC.mut });
      for (let i = 0; i < 120; i++) { const c = new THREE.Color().setHSL(0.08, 0.78, 0.18 + 0.42 * i / 120); H.ctx.fillStyle = c.getStyle(); H.ctx.fillRect(X + 20, Y + 330 - i, 22, 1.2); }
      H.text(HMAX.toFixed(1), X + 50, Y + 215, { size: 12, color: CC.mut }); H.text(HMIN.toFixed(1), X + 50, Y + 333, { size: 12, color: CC.mut });
      H.text('clipped above', X, Y + 355, { size: 12, color: CC.dim }); },
    panels: [
      { title: 'How far the pole sits above the cut', draw(ctx, X, Y, w, h, p) { const kap = kapOf(p);
        const F = H.frame(X, Y, w, h, { x0: 0.4, x1: 1.6, y0: 0, y1: 1.3, xt: [[0.5, '0.5'], [ON, '2/π'], [1, '1'], [1.5, '1.5']], yt: [[0, '0'], [0.5, '0.5'], [1, '1']], xl: 'κ / k', yl: '' });
        ctx.fillStyle = 'rgba(80,160,255,0.08)'; ctx.fillRect(F.fx(0.4), F.T, F.fx(ON) - F.fx(0.4), F.B - F.T);
        H.text('no pole', F.fx(0.52), F.T + 16, { size: 11, color: '#9fd8ff', align: 'center' });
        H.curve(D.kap, D.kap.map((k, i) => D.spole[i] + k), F, { color: '#ffc850', width: 2.4, glow: 8 }); H.vline(F, F.fx(ON), { color: '#ffd27a' });
        const sp = pole(kap); H.dot(F.fx(kap), F.fy(sp === null ? 0 : sp + kap), { color: sp === null ? '#9fd8ff' : '#ffc850' });
        H.text('s* + κ = k / tan(k/κ)', F.R - 4, F.T + 12, { size: 11, color: CC.mut, align: 'right' }); } },
      { title: 'Truncated chains miss it, then converge', draw(ctx, X, Y, w, h, p) {
        const F = H.frame(X, Y, w, h, { x0: 1.6, x1: 1200, y0: 0.6, y1: 1.2, logx: true, xt: [[2, '2'], [10, '10'], [100, '100'], [1000, '1000']], yt: [[0.7, '0.7'], [0.9, '0.9'], [1.1, '1.1']], xl: 'moments kept, N' });
        H.hline(F, ON, { color: '#ffd27a', label: 'exact 2/π = 0.6366' });
        H.curve(D.N, D.kstar, F, { color: '#ff8c3c', width: 1.6 });
        const hi = Math.floor(p * D.N.length * 2) % D.N.length;
        D.N.forEach((n, i) => H.dot(F.fx(n), F.fy(D.kstar[i]), { r: i === hi ? 6.5 : 3.5, color: i === hi ? '#ffffff' : '#ff8c3c' }));
        const n = D.N[hi]; H.text(`N = ${n}: κ* = ${D.kstar[hi].toFixed(4)} k`, F.R - 4, F.T + 12, { size: 12, color: CC.fg, align: 'right' });
        H.text('N = 2 is 2/√3, the two-moment merger', F.R - 4, F.T + 28, { size: 10.5, color: CC.mut, align: 'right' }); } },
      { title: 'Seen from above (phase colouring)', draw(ctx, X, Y, w, h, p) { const kap = kapOf(p);
        ctx.fillStyle = CC.panel; ctx.fillRect(X, Y, w, h); const g = domain.getContext('2d'), im = g.createImageData(150, 150);
        const x0 = -1.6, x1 = 0.45, y0 = -1.45, y1 = 1.45;
        for (let j = 0; j < 150; j++) for (let i = 0; i < 150; i++) { const x = x0 + (x1 - x0) * (i + 0.5) / 150, y = y1 - (y1 - y0) * (j + 0.5) / 150, G = Gs(x, y, kap);
          const m = Math.log10(Math.hypot(G[0], G[1]) + 1e-12), c = new THREE.Color().setHSL(((Math.atan2(G[1], G[0]) / (2 * Math.PI)) % 1 + 1) % 1, 0.85, Math.max(0.06, Math.min(0.62, 0.32 + 0.16 * m)));
          const q = 4 * (j * 150 + i); im.data[q] = c.r * 255; im.data[q + 1] = c.g * 255; im.data[q + 2] = c.b * 255; im.data[q + 3] = 255; }
        g.putImageData(im, 0, 0); const S = Math.min(w - 20, h - 40), ox = X + (w - S) / 2, oy = Y + 22;
        ctx.imageSmoothingEnabled = true; ctx.drawImage(domain, ox, oy, S, S);
        const sx = x => ox + (x - x0) / (x1 - x0) * S, sy = y => oy + (y1 - y) / (y1 - y0) * S;
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(sx(-kap), sy(-1)); ctx.lineTo(sx(-kap), sy(1)); ctx.stroke();
        ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(sx(0), oy); ctx.lineTo(sx(0), oy + S); ctx.moveTo(ox, sy(0)); ctx.lineTo(ox + S, sy(0)); ctx.stroke();
        const sp = pole(kap); if (sp !== null) { ctx.strokeStyle = '#ffd27a'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(sx(sp), sy(0), 7, 0, 2 * Math.PI); ctx.stroke(); }
        H.text('Re s →', ox + S - 4, oy + S + 14, { size: 11, color: CC.mut, align: 'right' }); H.text('Im s ↑', ox + 4, oy - 6, { size: 11, color: CC.mut });
        H.text('white: cut · gold ring: pole', ox + S / 2, Y + h - 4, { size: 11, color: CC.mut, align: 'center' }); } },
    ],
    foot: ['Pole: κ·arctan(k/(s+κ)) = k has a real root s* > −κ iff k/κ < π/2 · s* = k/tan(k/κ) − κ · at κ → 2k/π⁺ it sinks into the cut',
      'Exact onset κ* = 2k/π (kτ = π/2; Romatschke, EPJC 76 (2016) Eq. 37) · truncation values: 200 moments 0.645k, 800 moments 0.639k',
      'Card P2 · proposed atlas card · corrects "0.646k" in When the Neutrinos Leave v3.1 §2 · doi:10.5281/zenodo.23858157 · κ sweeps 0.44k ↔ 1.04k'],
  };
})();
