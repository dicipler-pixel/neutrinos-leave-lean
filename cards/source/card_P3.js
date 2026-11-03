// CARD P3 — the door: a difference planted in moment l first reaches the stress (l = 2) at order l-2
(function () {
  const D = DATA.P3, L = 4, TMAX = 6, NL = 13;
  const tOf = p => TMAX * G3.clock(p);
  const P = (l, x) => { let a = 1, b = x; if (l === 0) return 1; for (let n = 1; n < l; n++) { const c = ((2 * n + 1) * x * b - n * a) / (n + 1); a = b; b = c; } return b; };
  const pmax = (() => { let m = 0; for (let i = 0; i <= 400; i++) m = Math.max(m, Math.abs(P(L, -1 + i / 200))); return m; })();
  const aAt = (Lh, l, t) => G3.interp(D.t, D['a' + Lh][l], t);
  let sph, sphGeo, base, discs = [], ladderGroup, rings = [];
  const SX = -1.15, LX = 1.3;
  window.CARD = {
    title: 'Hidden, then visible: the door opens at order ℓ − 2.',
    sub: 'Two histories equal in every fluid moment, different only in moment ℓ (exact free streaming)',
    mainLabel: 'The hidden difference on the sphere of directions (ℓ = 4)',
    caption: 'radius = size of the difference (it never shrinks) · colour = its phase · right: the moment ladder fills from ℓ down to the fluid',
    setup3D(scene, camera) {
      sphGeo = new THREE.SphereGeometry(1, 200, 140); base = Float32Array.from(sphGeo.attributes.position.array);
      sphGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(base.length), 3));
      const pos = sphGeo.attributes.position.array;
      for (let i = 0; i < base.length; i += 3) { const x = base[i], y = base[i + 1], z = base[i + 2], r = 0.42 + 0.62 * Math.abs(P(L, z)) / pmax; pos[i] = x * r; pos[i + 1] = y * r; pos[i + 2] = z * r; }
      sphGeo.computeVertexNormals();
      sph = new THREE.Mesh(sphGeo, new THREE.MeshPhongMaterial({ vertexColors: true, shininess: 40, specular: 0x333333 }));
      sph.position.x = SX; scene.add(sph);
      scene.add(new THREE.AmbientLight(0xffffff, 0.5)); const dl = new THREE.DirectionalLight(0xffffff, 0.85); dl.position.set(3, -4, 5); scene.add(dl);
      const ag = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(SX, 0, -1.35), new THREE.Vector3(SX, 0, 1.35)]);
      scene.add(new THREE.Line(ag, new THREE.LineBasicMaterial({ color: 0x666666 })));
      ladderGroup = new THREE.Group(); scene.add(ladderGroup);
      for (let l = 0; l < NL; l++) { const z = -1.3 + l * 0.215;
        const ring = new THREE.Mesh(new THREE.RingGeometry(0.565, 0.575, 64), new THREE.MeshBasicMaterial({ color: 0x333333, side: THREE.DoubleSide })); ring.position.set(LX, 0, z); ladderGroup.add(ring); rings.push(ring);
        const d = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.07, 64), new THREE.MeshPhongMaterial({ color: l <= 2 ? 0xffc850 : (l === L ? 0xff6fd8 : 0x58c8ff), emissive: l <= 2 ? 0x553300 : 0x0a2030 }));
        d.rotation.x = Math.PI / 2; d.position.set(LX, 0, z); ladderGroup.add(d); discs.push(d); }
      const lp = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(LX, 0, -1.35), new THREE.Vector3(LX, 0, -1.3 + 12 * 0.215 + 0.05)]);
      ladderGroup.add(new THREE.Line(lp, new THREE.LineBasicMaterial({ color: 0x555555 })));
      const fb = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.02, 0.62), new THREE.MeshBasicMaterial({ color: 0xffc850, transparent: true, opacity: 0.07, depthWrite: false })); fb.position.set(LX, 0, -1.3 + 0.215); ladderGroup.add(fb);
      camera.up.set(0, 0, 1); camera.position.set(0.05, -7.4, 1.6); camera.lookAt(0.05, 0, -0.05); this._cam = camera;
    },
    update3D(p) {
      const t = tOf(p), col = sphGeo.attributes.color.array, c = new THREE.Color();
      for (let i = 0; i < base.length; i += 3) { const z = base[i + 2], v = P(L, z), ph = -z * t + (v < 0 ? Math.PI : 0), m = Math.abs(v) / pmax;
        c.setHSL(((ph / (2 * Math.PI)) % 1 + 1) % 1, 0.85, 0.12 + 0.5 * Math.sqrt(m)); col[i] = c.r; col[i + 1] = c.g; col[i + 2] = c.b; }
      sphGeo.attributes.color.needsUpdate = true; sph.rotation.z = 2 * Math.PI * p;
      discs.forEach((d, l) => { const a = aAt(L, l, t), r = Math.max(0.004, 0.57 * Math.sqrt(a)); d.scale.set(r, 1, r); });
    },
    overlay(p, MX, MY, MW, MH) { const cam = this._cam;
      const lab = (l, s, col) => { const [x, y] = G3.project(new THREE.Vector3(LX + 0.62, 0, -1.3 + l * 0.215), cam, MX, MY, MW, MH); H.text(s, x + 6, y + 4, { size: 12.5, color: col }); };
      lab(0, 'ℓ = 0 density', '#ffd27a'); lab(1, 'ℓ = 1 flux', '#ffd27a'); lab(2, 'ℓ = 2 stress', '#ffd27a'); lab(L, `ℓ = ${L} planted`, '#ff9be6'); lab(12, 'ℓ = 12', CC.mut);
      const [x0, y0] = G3.project(new THREE.Vector3(LX, 0, -1.62), cam, MX, MY, MW, MH); H.text('moment ladder · disc area = |a_ℓ(t)|', x0, y0 + 8, { size: 13, color: '#dddddd', align: 'center' });
      const [x1, y1] = G3.project(new THREE.Vector3(SX, 0, 1.55), cam, MX, MY, MW, MH); H.text('k', x1 + 10, y1 + 10, { size: 17, bold: true, color: '#cfcfcf' });
      const [x2, y2] = G3.project(new THREE.Vector3(LX - 0.75, 0, -1.3 + 0.215), cam, MX, MY, MW, MH); H.text('fluid', x2 - 8, y2 - 4, { size: 12, color: '#ffd27a', align: 'right' }); H.text('sees', x2 - 8, y2 + 10, { size: 12, color: '#ffd27a', align: 'right' }); },
    left(p) { const t = tOf(p), a2 = aAt(L, 2, t), pr = D.coef4 * t * t;
      return [{ label: 'time', value: [`kt = ${t.toFixed(3)}`], big: true }, { label: G3.rewinding(p) ? 'rewinding the loop' : '', value: [] },
        { label: 'planted in moment', value: [`ℓ = ${L}`], color: '#ff9be6' },
        { label: 'stress |a₂(t)|', value: [a2.toExponential(3)], color: '#ffd27a' },
        { label: 'leading term (small kt)', value: ["c₂c₃ (kt)²/2!", t < 1.0 ? pr.toExponential(3) + `  (×${(a2 / pr).toFixed(4)})` : 'higher orders take over'] },
        { label: 'density |a₀(t)|', value: [aAt(L, 0, t).toExponential(3)] },
        { label: 'first return', value: ['stress: order ℓ − 2 = 2', 'density: order ℓ = 4'] }]; },
    scale(p, X, Y) { H.text('colour = phase', X, Y, { size: 14, color: CC.mut }); H.text('of the difference', X, Y + 19, { size: 14, color: CC.mut }); H.wheel(X + 70, Y + 82, 34);
      H.text('radius =', X, Y + 150, { size: 14, color: CC.mut }); H.text('|P₄(cos θ)|', X, Y + 169, { size: 14, color: CC.mut }); H.text('constant in time', X, Y + 188, { size: 13, color: CC.dim });
      H.text('gold discs:', X, Y + 236, { size: 14, color: '#ffd27a' }); H.text('what a fluid', X, Y + 255, { size: 14, color: CC.mut }); H.text('closure can see', X, Y + 274, { size: 14, color: CC.mut }); },
    panels: [
      { title: 'First return to the stress (log–log)', draw(ctx, X, Y, w, h, p) { const t = tOf(p);
        const F = H.frame(X, Y, w, h, { x0: 1e-3, x1: 2, y0: 1e-10, y1: 2, logx: true, logy: true, xt: [[1e-3, '10⁻³'], [1e-2, '10⁻²'], [1e-1, '10⁻¹'], [1, '1']], yt: [[1e-9, '10⁻⁹'], [1e-6, '10⁻⁶'], [1e-3, '10⁻³'], [1, '1']], xl: 'kt' });
        const cols = { 3: '#58c8ff', 4: '#ff6fd8', 5: '#ffc850' };
        for (const l of [3, 4, 5]) { H.curve(D.tl, D.tl.map(x => D['coef' + l] * Math.pow(x, l - 2)), F, { color: 'rgba(255,255,255,0.45)', width: 1, dash: [4, 4], logy: true });
          H.curve(D.tl, D['a2l' + l], F, { color: cols[l], width: 2.2, logy: true });
          const i = 44; H.text(`ℓ=${l}  slope ${D['slope' + l].toFixed(4)}`, F.fx(D.tl[i]) - 6, F.fy(D['a2l' + l][i]) - 10, { size: 11, color: cols[l] }); }
        if (t > 1e-3 && t < 2) H.dot(F.fx(t), F.fy(G3.interp(D.tl, D.a2l4, t)), { color: '#ff6fd8', r: 6 });
        H.text('dashed: c₂⋯c_(ℓ−1)(kt)^(ℓ−2)/(ℓ−2)!', F.R - 4, F.B - 8, { size: 10.5, color: CC.mut, align: 'right' }); } },
      { title: 'Moment ladder, ℓ = 4 planted', draw(ctx, X, Y, w, h, p) { const t = tOf(p);
        const F = H.frame(X, Y, w, h, { x0: -0.6, x1: 12.6, y0: 0, y1: 1.05, xt: [0, 2, 4, 6, 8, 10, 12].map(v => [v, String(v)]), yt: [[0, '0'], [0.5, '0.5'], [1, '1']], xl: 'moment ℓ' });
        ctx.fillStyle = 'rgba(255,200,80,0.08)'; ctx.fillRect(F.fx(-0.5), F.T, F.fx(2.5) - F.fx(-0.5), F.B - F.T); H.text('fluid', F.fx(1), F.T + 14, { size: 11, color: '#ffd27a', align: 'center' });
        for (let l = 0; l < NL; l++) { const a = aAt(L, l, t), x = F.fx(l), bw = (F.fx(1) - F.fx(0)) * 0.62;
          ctx.fillStyle = l <= 2 ? '#ffc850' : (l === L ? '#ff6fd8' : '#58c8ff'); ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = 8; ctx.fillRect(x - bw / 2, F.fy(a), bw, F.B - F.fy(a)); ctx.shadowBlur = 0; }
        H.text('total Σ|a_ℓ|² = 1 always', F.R - 4, F.T + 14, { size: 11, color: CC.mut, align: 'right' }); } },
      { title: 'Coefficient: exact vs computed', draw(ctx, X, Y, w, h, p) { ctx.fillStyle = CC.panel; ctx.fillRect(X, Y, w, h);
        const cols = { 3: '#58c8ff', 4: '#ff6fd8', 5: '#ffc850' }; let y = Y + 30;
        H.text('|a₂| ≈ c₂⋯c_(ℓ−1) (kt)^(ℓ−2) / (ℓ−2)!', X + 14, y, { size: 13, color: CC.fg }); y += 34;
        H.text('ℓ', X + 14, y, { size: 12, color: CC.mut }); H.text('order', X + 44, y, { size: 12, color: CC.mut }); H.text('coefficient', X + 110, y, { size: 12, color: CC.mut }); H.text('measured/exact', X + 222, y, { size: 12, color: CC.mut }); y += 8;
        ctx.strokeStyle = '#333'; ctx.beginPath(); ctx.moveTo(X + 10, y); ctx.lineTo(X + w - 10, y); ctx.stroke(); y += 24;
        for (const l of [3, 4, 5]) { const r = D['a2l' + l][0] / (D['coef' + l] * Math.pow(D.tl[0], l - 2));
          H.text(String(l), X + 14, y, { size: 15, bold: true, color: cols[l] }); H.text(String(l - 2), X + 54, y, { size: 15 }); H.text(D['coef' + l].toFixed(6), X + 110, y, { size: 15 }); H.text(r.toFixed(6), X + 230, y, { size: 15, color: '#9cff9c' }); y += 34; }
        y += 8; H.text('c₂ = 3/√35 · c₃ = 4/√63 · c₄ = 5/√99', X + 14, y, { size: 12, color: CC.mut }); y += 22;
        H.text('measured at kt = 10⁻³; slopes 1.0000, 2.0000, 3.0000', X + 14, y, { size: 12, color: CC.mut }); y += 22;
        H.text('density returns two orders later (order ℓ)', X + 14, y, { size: 12, color: CC.mut }); y += 22;
        H.text('Lean proof of the door theorem: not yet built', X + 14, y, { size: 12, color: '#ff9c9c' }); } },
    ],
    foot: ['δI(μ,t) = √(2ℓ+1) P_ℓ(μ) e^(−ikμt) · a_l(t) = ½∫ √(2l+1) P_l(μ) δI dμ (160-point Gauss–Legendre) · |δI| never changes, only its phase winds',
      'First return: a₂(t) = (−ikt)^(ℓ−2) c₂⋯c_(ℓ−1)/(ℓ−2)! + O(t^(ℓ−1)), c_l = (l+1)/√((2l+1)(2l+3)) · the matched pair stays matched until then',
      'Card P3 · proposed atlas card (theorem, measured) · When the Neutrinos Leave · doi:10.5281/zenodo.23858157 · collisionless, units of k'],
  };
})();
