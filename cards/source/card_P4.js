// CARD P4 — the Henrici departure of the moment chain is finite and converges; the opposite book grows with N
(function () {
  const D = DATA.P4, rows = D.rows, NT = 160, NMAX = 400;
  const Ns = Object.keys(D.ev).map(Number).sort((a, b) => a - b);
  const NofP = p => 2 + (NMAX - 2) * G3.clock(p);
  const col = (j) => rows.map(r => r[j]); const RN = col(0);
  const at = (j, n) => G3.interp(RN, col(j), n);
  const LG = re => Math.log10(Math.max(1e-4, re + 1)), X = re => (LG(re) + 2.0) * 1.0, Y = im => im * 1.5, Z = n => n / NT * 2.3 - 1.25;
  let pts, ptsGeo, layerOf = [], cur, curGeo, sheet;
  window.CARD = {
    title: 'Every moment adds weight. The departure stays finite.',
    sub: 'Truncated neutrino chain L_N = −ikM − κ(I − P₀), k = κ = 1, exact eigenvalues for each N',
    mainLabel: 'Eigenvalues of L_N, stacked by N (a tower of spectra)',
    caption: 'each layer = one truncation · the hidden modes close in on the cut like 1/N · the density pole stands still',
    setup3D(scene, camera) {
      const P = [], C = [];
      for (const n of Ns) for (const [re, im] of D.ev[n]) { P.push(X(re), Y(im), Z(n)); const c = H.inferno(0.25 + 0.75 * n / NT); C.push(c[0] / 255, c[1] / 255, c[2] / 255); layerOf.push(n); }
      const PP = []; for (const n of Ns) for (const [re, im] of D.ev[n]) if (re > -0.5) { PP.push(X(re), Y(im), Z(n)); this._pn = (this._pn || []).concat([n]); }
      this._pg = new THREE.BufferGeometry(); this._pg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(PP), 3));
      this._pp = new THREE.Points(this._pg, new THREE.PointsMaterial({ size: 0.13, map: G3.glowTex(), color: 0xffc850, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); scene.add(this._pp);
      ptsGeo = new THREE.BufferGeometry(); ptsGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(P), 3));
      ptsGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(C), 3)); ptsGeo.setAttribute('base', new THREE.BufferAttribute(new Float32Array(C), 3));
      pts = new THREE.Points(ptsGeo, new THREE.PointsMaterial({ size: 0.06, map: G3.glowTex(), vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
      scene.add(pts);
      curGeo = new THREE.BufferGeometry(); curGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(3 * 200), 3));
      cur = new THREE.Points(curGeo, new THREE.PointsMaterial({ size: 0.16, map: G3.glowTex(), color: 0xffffff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); scene.add(cur);
      // the limit: the cut Re = -kappa, |Im| <= k, drawn as a faint vertical sheet
      sheet = new THREE.Mesh(new THREE.PlaneGeometry(Y(1) - Y(-1), Z(NT) - Z(0)), new THREE.MeshBasicMaterial({ color: 0x58c8ff, transparent: true, opacity: 0.07, side: THREE.DoubleSide, depthWrite: false }));
      const fl = []; for (let lg = -4; lg <= 0; lg += 1) fl.push(new THREE.Vector3(lg + 2, Y(-1.05), Z(0)), new THREE.Vector3(lg + 2, Y(1.05), Z(0)));
      for (let im = -1; im <= 1 + 1e-9; im += 0.25) fl.push(new THREE.Vector3(-2, Y(im), Z(0)), new THREE.Vector3(2, Y(im), Z(0)));
      scene.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(fl), new THREE.LineBasicMaterial({ color: 0x2a2a2a })));
      const ax = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-2.1, Y(-1.1), Z(0)), new THREE.Vector3(-2.1, Y(-1.1), Z(NT))]);
      scene.add(new THREE.Line(ax, new THREE.LineBasicMaterial({ color: 0x555555 })));
    },
    update3D(p, scene, camera) {
      const n = NofP(p), nt = Math.min(n, NT), c = ptsGeo.attributes.color.array, b = ptsGeo.attributes.base.array;
      for (let i = 0; i < layerOf.length; i++) { const on = layerOf[i] <= nt ? 1 : 0, f = on * (layerOf[i] > nt - 6 ? 1.4 : 0.8); c[3 * i] = b[3 * i] * f; c[3 * i + 1] = b[3 * i + 1] * f; c[3 * i + 2] = b[3 * i + 2] * f; }
      ptsGeo.attributes.color.needsUpdate = true; this._pg.setDrawRange(0, this._pn.filter(v => v <= nt).length);
      const ln = Ns.reduce((a, v) => (v <= nt ? v : a), 2), ev = D.ev[ln], pa = curGeo.attributes.position.array; pa.fill(0);
      ev.forEach(([re, im], i) => { if (i < 200) pa.set([X(re), Y(im), Z(ln)], 3 * i); }); curGeo.setDrawRange(0, Math.min(200, ev.length)); curGeo.attributes.position.needsUpdate = true;
      cur.material.opacity = n <= NT + 4 ? 1 : 0.35;
      G3.orbit(camera, p, 8.4, 17, -0.9); camera.lookAt(0, 0, -0.15); this._cam = camera; this._ln = ln;
    },
    overlay(p, MX, MY, MW, MH) { const cam = this._cam;
      const [a, b] = G3.project(new THREE.Vector3(X(1 / Math.tan(1) - 1), 0, Z(NT) + 0.2), cam, MX, MY, MW, MH); H.text('density pole, Re λ = −0.358', a, b, { size: 13, color: '#ffd27a', align: 'center' }); H.text('(card P2: k/tan(k/κ) − κ)', a, b + 16, { size: 11, color: CC.mut, align: 'center' });
      const [c, d] = G3.project(new THREE.Vector3(-2.1, Y(-1.1), Z(NT) + 0.12), cam, MX, MY, MW, MH); H.text('N = 160', c, d, { size: 12, color: CC.mut, align: 'center' });
      const [e, f] = G3.project(new THREE.Vector3(-2.1, Y(-1.1), Z(0) - 0.12), cam, MX, MY, MW, MH); H.text('N = 2', e, f + 8, { size: 12, color: CC.mut, align: 'center' });
      for (const lg of [-4, -3, -2, -1, 0]) { const [g, h] = G3.project(new THREE.Vector3(lg + 2, Y(-1.15), Z(0)), cam, MX, MY, MW, MH); H.text(lg === 0 ? '1' : '10' + '⁻¹⁻²⁻³⁻⁴'.slice(0, 0) + ['', '⁻¹', '⁻²', '⁻³', '⁻⁴'][-lg], g, h + 16, { size: 11.5, color: CC.mut, align: 'center' }); }
      const [g, h] = G3.project(new THREE.Vector3(0, Y(-1.75), Z(0)), cam, MX, MY, MW, MH); H.text('distance to the cut, Re λ + κ (log)', g, h + 22, { size: 12.5, color: '#9fd8ff', align: 'center' }); },
    left(p) { const n = Math.round(NofP(p));
      return [{ label: 'moments kept', value: [`N = ${n}`], big: true }, { label: n > NT ? 'tower drawn to N = 160' : (G3.rewinding(p) ? 'rewinding the loop' : ''), value: [] },
        { label: '‖L‖²_F (grows)', value: [at(1, n).toFixed(3)] }, { label: 'Σ|λ|² (grows)', value: [at(2, n).toFixed(3)] },
        { label: 'departure dep²', value: [at(3, n).toFixed(5)], color: '#ffd27a' },
        { label: 'book E₋ (stays)', value: [at(4, n).toFixed(5) + ' = k²κ²/3'], color: '#9cff9c' },
        { label: 'book E₊ (grows)', value: [at(5, n).toFixed(2)], color: '#ff8c3c' }]; },
    scale(p, X0, Y0) { H.text('colour = N', X0, Y0, { size: 14, color: CC.mut });
      for (let i = 0; i < 300; i++) { H.ctx.fillStyle = H.rgb(H.inferno(0.25 + 0.75 * i / 300)); H.ctx.fillRect(X0 + 20, Y0 + 330 - i, 22, 1.2); }
      H.text('160', X0 + 50, Y0 + 36, { size: 12, color: CC.mut }); H.text('80', X0 + 50, Y0 + 186, { size: 12, color: CC.mut }); H.text('2', X0 + 50, Y0 + 334, { size: 12, color: CC.mut });
      H.text('white = current', X0, Y0 + 368, { size: 12, color: CC.fg }); H.text('layer', X0, Y0 + 385, { size: 12, color: CC.fg }); },
    panels: [
      { title: 'Both grow: ‖L‖² and Σ|λ|²', draw(ctx, X0, Y0, w, h, p) { const n = NofP(p);
        const F = H.frame(X0, Y0, w, h, { x0: 0, x1: NMAX, y0: 0, y1: 620, xt: [[0, '0'], [100, '100'], [200, '200'], [300, '300'], [400, '400']], yt: [[0, '0'], [200, '200'], [400, '400'], [600, '600']], xl: 'N' });
        H.curve(RN, col(1), F, { color: '#ffffff', width: 3.2 }); H.curve(RN, col(2), F, { color: '#ff6fd8', width: 1.6, dash: [6, 4] });
        H.dot(F.fx(n), F.fy(at(1, n)), { color: '#ffffff', r: 6 });
        H.text('white ‖L‖²_F · pink Σ|λ|²', F.L + 6, F.T + 12, { size: 11, color: CC.mut }); H.text('curves overlap: the gap is ~1', F.L + 6, F.T + 27, { size: 11, color: CC.mut }); } },
      { title: 'Their gap converges (Henrici)', draw(ctx, X0, Y0, w, h, p) { const n = NofP(p);
        const F = H.frame(X0, Y0, w, h, { x0: 2, x1: NMAX, y0: 0, y1: 1.4, logx: true, xt: [[2, '2'], [10, '10'], [50, '50'], [200, '200']], yt: [[0, '0'], [0.5, '0.5'], [1, '1']], xl: 'N (log)' });
        H.hline(F, at(3, 400), { color: '#ffd27a', label: 'N = 400: 1.17446' });
        H.curve(RN, col(3), F, { color: '#ffc850', width: 2.4, glow: 8 }); H.dot(F.fx(n), F.fy(at(3, n)), { color: '#ffc850' });
        H.text('dep² = ‖L‖²_F − Σ|λ|²', F.R - 4, F.B - 10, { size: 11, color: CC.mut, align: 'right' }); H.text('200 → 400: +0.08%', F.R - 4, F.B - 25, { size: 11, color: CC.mut, align: 'right' }); } },
      { title: 'Two books: one stays, one grows', draw(ctx, X0, Y0, w, h, p) { const n = NofP(p);
        const F = H.frame(X0, Y0, w, h, { x0: 2, x1: NMAX, y0: 0.1, y1: 1000, logx: true, logy: true, xt: [[2, '2'], [10, '10'], [50, '50'], [200, '200']], yt: [[0.1, '0.1'], [1, '1'], [10, '10'], [100, '100'], [1000, '10³']], xl: 'N (log)' });
        H.curve(RN, col(5), F, { color: '#ff8c3c', width: 2.4, logy: true }); H.curve(RN, col(4), F, { color: '#9cff9c', width: 2.4, logy: true });
        H.dot(F.fx(n), F.fy(at(5, n)), { color: '#ff8c3c', r: 6 }); H.dot(F.fx(n), F.fy(at(4, n)), { color: '#9cff9c', r: 6 });
        H.text('E₊ = ⅛‖L² − L*²‖² ≈ N', F.L + 6, F.T + 12, { size: 11, color: '#ff8c3c' }); H.text('E₋ = ⅛‖[L, L*]‖² = 1/3', F.R - 4, F.fy(0.333) - 10, { size: 11, color: '#9cff9c', align: 'right' }); } },
    ],
    foot: ['Henrici departure dep²(L) = ‖L‖²_F − Σ|λ|² is zero iff L is normal · E7: 1.1735 (N = 200), 1.1745 (N = 400) at k = κ = 1',
      'Two books (E4): E₋ = k²κ²/3 for every N (only the density–flux link is non-normal) · E₊ = k²Σ c_l²(D_l + D_(l+1))² grows with N',
      'Card P4 · proposed atlas card (measured) · When the Neutrinos Leave · doi:10.5281/zenodo.23858157 · atlas: B64, B201, B183/B184, B37'],
  };
})();
