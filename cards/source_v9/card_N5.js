// SCRIPT: NU-ART-CARD-N5  the kept mode at the wall: f(mu) = 1/(s + kappa + i k mu), right and left eigenvectors, as kappa falls to 2k/pi
(function () {
  const D = window.DATA_N5, NP = D.phi.length;
  const idxOf = p => Math.min(NP - 1, Math.round(G3.clock(p) * (NP - 1)));          // kappa sweeps down to the wall, then rewinds
  const profAt = i => { let best = D.prof[0]; for (const q of D.prof) if (Math.abs(q.i - i) < Math.abs(best.i - i)) best = q; return best; };
  const fAt = (i, z) => { const a = D.a[i], d = a * a + z * z; return [a / d, -z / d]; };                 // f = 1/(a + i mu), k = 1
  let sR, sL, gR, gL, baseR;
  const XR = -1.2, XL = 1.2;
  function makeSphere(scene, x) {
    const g = new THREE.SphereGeometry(1, 220, 160); const b = Float32Array.from(g.attributes.position.array);
    g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(b.length), 3));
    const m = new THREE.Mesh(g, new THREE.MeshPhongMaterial({ vertexColors: true, shininess: 50, specular: 0x2a2a2a }));
    m.position.x = x; scene.add(m);
    const ag = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x, 0, -1.45), new THREE.Vector3(x, 0, 1.45)]);
    scene.add(new THREE.Line(ag, new THREE.LineBasicMaterial({ color: 0x666666 })));
    return [m, g, b];
  }
  function shape(g, b, i, conj) {
    const pos = g.attributes.position.array, col = g.attributes.color.array, c = new THREE.Color();
    // normalise |f| on the sphere's own sample points (the equator row is mu = 0 exactly only at the onset)
    let mx = 0; for (let j = 0; j < b.length; j += 3) { const [re, im] = fAt(i, b[j + 2]); mx = Math.max(mx, Math.hypot(re, im)); }
    for (let j = 0; j < b.length; j += 3) {
      const z = b[j + 2]; const [re, im] = fAt(i, z); const m = Math.hypot(re, im) / mx, ph = Math.atan2(conj ? -im : im, re);
      const r = 0.30 + 0.80 * m; pos[j] = b[j] * r; pos[j + 1] = b[j + 1] * r; pos[j + 2] = z * r;
      c.setHSL(((ph / (2 * Math.PI)) % 1 + 1) % 1, 0.88, 0.14 + 0.46 * Math.sqrt(m)); col[j] = c.r; col[j + 1] = c.g; col[j + 2] = c.b;
    }
    g.attributes.position.needsUpdate = true; g.attributes.color.needsUpdate = true; g.computeVertexNormals();
  }
  window.CARD = {
    title: 'At the wall, the kept mode turns sideways.',
    sub: 'The kept-sector mode of the neutrino gas, exact: f(μ) ∝ 1/(s + κ + ikμ),  s = k cot(k/κ) − κ',
    mainLabel: 'The kept mode on the sphere of directions: right and left eigenvectors',
    caption: 'radius = |f| along each direction · colour = phase · at the wall the mode pours into μ = 0, sideways to the wave',
    setup3D(scene, camera) {
      [sR, gR, baseR] = makeSphere(scene, XR); const t = makeSphere(scene, XL); sL = t[0]; gL = t[1];
      scene.add(new THREE.AmbientLight(0xffffff, 0.5)); const dl = new THREE.DirectionalLight(0xffffff, 0.85); dl.position.set(3, -4, 5); scene.add(dl);
      camera.up.set(0, 0, 1); camera.position.set(0.0, -7.6, 1.9); camera.lookAt(0, 0, -0.05); this._cam = camera;
    },
    update3D(p) { const i = idxOf(p); shape(gR, baseR, i, false); shape(gL, baseR, i, true); sR.rotation.z = 2 * Math.PI * p; sL.rotation.z = 2 * Math.PI * p; },
    overlay(p, MX, MY, MW, MH) { const cam = this._cam;
      const [x1, y1] = G3.project(new THREE.Vector3(XR, 0, 1.62), cam, MX, MY, MW, MH); H.text('k', x1 + 10, y1 + 10, { size: 17, bold: true, color: '#cfcfcf' });
      const [x2, y2] = G3.project(new THREE.Vector3(XR, 0, -1.75), cam, MX, MY, MW, MH); H.text('right eigenvector  f(μ)', x2, y2 + 10, { size: 14, color: '#dddddd', align: 'center' });
      const [x3, y3] = G3.project(new THREE.Vector3(XL, 0, -1.75), cam, MX, MY, MW, MH); H.text('left eigenvector  f̄(μ)', x3, y3 + 10, { size: 14, color: '#dddddd', align: 'center' });
},
    left(p) { const i = idxOf(p), q = profAt(i);
      return [{ label: 'collision rate', value: [`κ = ${D.kap[i].toFixed(4)} k`], big: true }, { label: G3.rewinding(p) ? 'rewinding the loop' : '', value: [] },
        { label: 'the wall', value: ['κ = 2k/π = 0.63662 k'] },
        { label: 'pole  s = k cot(k/κ) − κ', value: [`s = ${D.s[i].toFixed(5)} k`] },
        { label: 'distance to the cut', value: [`s + κ = ${D.a[i] >= 0.1 ? D.a[i].toFixed(4) : D.a[i].toExponential(3)} k`], color: '#ffd27a' },
        { label: 'non-orthogonality', value: [`K = 4φ²/sin²2φ = ${D.K[i] < 1e4 ? D.K[i].toFixed(2) : D.K[i].toExponential(3)}`] },
        { label: 'left–right overlap', value: [`1/√K = ${D.ov[i].toFixed(5)}`], color: '#9cff9c' },
        { label: 'weight within |μ| < 0.1', value: [`${(100 * q.sharecentre).toFixed(1)} %  (10 % if even)`] }]; },
    scale(p, X, Y) { H.text('colour = phase', X, Y, { size: 14, color: CC.mut }); H.text('of f(μ)', X, Y + 19, { size: 14, color: CC.mut }); H.wheel(X + 70, Y + 82, 34);
      H.text('radius = |f(μ)|', X, Y + 150, { size: 14, color: CC.mut }); H.text('scaled to its max', X, Y + 169, { size: 13, color: CC.dim });
      H.text('left = right with', X, Y + 217, { size: 14, color: CC.mut }); H.text('the phase reversed', X, Y + 236, { size: 14, color: CC.mut }); H.text('(complex symmetric)', X, Y + 255, { size: 13, color: CC.dim }); },
    panels: [
      { title: 'The pole walks to the centre of the cut', draw(ctx, X, Y, w, h, p) { const i = idxOf(p);
        const F = H.frame(X, Y, w, h, { x0: -0.15, x1: 3.2, y0: -1.25, y1: 1.25, xt: [[0, '0'], [1, '1'], [2, '2'], [3, '3']], yt: [[-1, '−k'], [0, '0'], [1, 'k']], xl: 'Re s + κ  (units of k)', yl: 'Im s' });
        ctx.strokeStyle = '#ff6fd8'; ctx.lineWidth = 5; ctx.shadowColor = '#ff6fd8'; ctx.shadowBlur = 10; ctx.beginPath(); ctx.moveTo(F.fx(0), F.fy(-1)); ctx.lineTo(F.fx(0), F.fy(1)); ctx.stroke(); ctx.shadowBlur = 0;
        H.text('branch cut', F.fx(0) + 8, F.fy(0.86), { size: 11, color: '#ff9be6' });
        H.curve(D.a.slice(0, i + 1), D.a.slice(0, i + 1).map(() => 0), F, { color: 'rgba(255,191,77,0.55)', width: 2 });
        H.dot(F.fx(Math.min(D.a[i], 3.2)), F.fy(0), { color: '#ffbf4d', r: 7 });
        H.text('pole', F.fx(Math.min(D.a[i], 3.2)), F.fy(0) - 14, { size: 11, color: '#ffd27a', align: 'center' });
        H.text('meets the cut at its centre, s = −κ', F.R - 4, F.B - 8, { size: 11, color: CC.mut, align: 'right' }); } },
      { title: 'Left–right overlap 1/√K = sin 2φ / 2φ', draw(ctx, X, Y, w, h, p) { const i = idxOf(p);
        const F = H.frame(X, Y, w, h, { x0: 0.55, x1: 3.4, y0: 0, y1: 1.05, logx: true, xt: [[0.6, '0.6'], [2 / Math.PI, ''], [1, '1'], [2, '2'], [3, '3']], yt: [[0, '0'], [0.5, '0.5'], [1, '1']], xl: 'κ / k (log)' });
        H.vline(F, F.fx(2 / Math.PI), { color: '#ff6fd8' }); H.text('2/π', F.fx(2 / Math.PI) + 4, F.T + 12, { size: 11, color: '#ff9be6' });
        for (const [n, v] of Object.entries(D.onset_chain)) { const x = F.fx(v); ctx.strokeStyle = '#58c8ff'; ctx.beginPath(); ctx.moveTo(x, F.B - 10); ctx.lineTo(x, F.B); ctx.stroke(); }
        H.text('chain onsets: 50, 200, 800 moments', F.R - 4, F.B - 14, { size: 10.5, color: '#58c8ff', align: 'right' });
        H.curve(D.kap, D.ov, F, { color: '#9cff9c', width: 2.2 });
        H.dot(F.fx(D.kap[i]), F.fy(D.ov[i]), { color: '#9cff9c', r: 6 }); } },
      { title: 'Where the mode lives: |f(μ)|²', draw(ctx, X, Y, w, h, p) { const i = idxOf(p), q = profAt(i);
        const F = H.frame(X, Y, w, h, { x0: -1, x1: 1, y0: 0, y1: 1.08, xt: [[-1, '−1'], [-0.5, '−½'], [0, '0'], [0.5, '½'], [1, '1']], yt: [[0, '0'], [0.5, '½'], [1, '1']], xl: 'μ = cos(angle to k)' });
        ctx.fillStyle = 'rgba(255,200,80,0.07)'; ctx.fillRect(F.fx(-0.1), F.T, F.fx(0.1) - F.fx(-0.1), F.B - F.T);
        const m2 = q.mag.map(v => v * v);
        H.curve(D.mu, m2, F, { color: '#ffbf4d', width: 2.2, glow: 6 });
        H.text('peak scaled to 1', F.R - 4, F.T + 14, { size: 11, color: CC.mut, align: 'right' });
        H.text('|μ| < 0.1', F.fx(0), F.B - 8, { size: 10.5, color: '#ffd27a', align: 'center' }); } },
    ],
    foot: [],
  };
  // footer lines set below so they can carry the computed checks
  const c = D.fchk, kq = D.chk;
  window.CARD.foot = [
    `checks: 400-moment chain eigenvector = closed form to ${Math.max(...c.map(x => x.max_rel_err)).toExponential(0)} (κ = 2, 1, 0.8) · K by quadrature = 4φ²/sin²2φ to ${Math.max(...kq.map(x => Math.abs(x.K_quad / x.K_closed - 1))).toExponential(0)}`,
    'pole and onset: Romatschke 2016, Eq. (37) · K, the overlap and the centre of the cut: this paper · phase set real at μ = 0',
    'Card N5 · When the Neutrinos Leave · What the Neutrino State Must Keep, v9 · units of k · nothing drawn by hand',
  ];
})();
