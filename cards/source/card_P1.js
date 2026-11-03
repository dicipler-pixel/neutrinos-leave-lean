// CARD P1 — free streaming gives the density a boundary impedance Z_b(0) = 2k/pi exactly
(function () {
  const D = DATA.P1, TMAX = 40, Z0 = 1 / Math.sqrt(3), ZB = 2 / Math.PI;
  const tOf = p => TMAX * G3.clock(p);
  let sph, sphBack, core, rays, raysGeo, rayDir = [], rayOff = [], axis;
  const NR = 2600;
  window.CARD = {
    title: 'One density. Every direction. One exact impedance.',
    sub: 'Free-streaming neutrinos, calculated from the exact moment chain (no truncation in the limit)',
    mainLabel: 'The sphere of directions (k points up)',
    caption: 'colour = phase each direction has picked up · centre glow = the density · nothing is lost, it walks out of view',
    setup3D(scene, camera) {
      const vs = `varying vec3 vP; varying vec3 vN; varying vec3 vW; void main(){ vP = position; vN = normalize(normalMatrix*normal); vec4 w = modelViewMatrix*vec4(position,1.0); vW = -w.xyz; gl_Position = projectionMatrix*w; }`;
      const fs = (back) => `uniform float t; varying vec3 vP; varying vec3 vN; varying vec3 vW; ${G3.HSV}
        void main(){ float mu = normalize(vP).z; float ph = -mu*t; float h = fract(ph/6.2831853);
          float rim = pow(1.0 - abs(dot(normalize(vN), normalize(vW))), 1.6);
          float band = 0.80 + 0.20*cos(ph);
          vec3 c = hsv(h, 0.80, 1.0)*band*band;
          gl_FragColor = vec4(c*(${back ? '0.06 + 0.16*rim' : '0.10 + 0.62*rim'}), 1.0); }`;
      const geo = new THREE.SphereGeometry(1, 180, 120);
      sphBack = new THREE.Mesh(geo, new THREE.ShaderMaterial({ uniforms: { t: { value: 0 } }, vertexShader: vs, fragmentShader: fs(true), side: THREE.BackSide, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
      sph = new THREE.Mesh(geo, new THREE.ShaderMaterial({ uniforms: { t: { value: 0 } }, vertexShader: vs, fragmentShader: fs(false), side: THREE.FrontSide, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
      scene.add(sphBack, sph);
      // streaming rays: deterministic directions, points flying from the centre to the shell
      const r = G3.rng(20261103); raysGeo = new THREE.BufferGeometry(); const pos = new Float32Array(NR * 3), col = new Float32Array(NR * 3);
      for (let i = 0; i < NR; i++) { const u = 2 * r() - 1, ph = 2 * Math.PI * r(), s = Math.sqrt(1 - u * u); rayDir.push([s * Math.cos(ph), s * Math.sin(ph), u]); rayOff.push(r()); }
      raysGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); raysGeo.setAttribute('color', new THREE.BufferAttribute(col, 3));
      rays = new THREE.Points(raysGeo, new THREE.PointsMaterial({ size: 0.045, map: G3.glowTex(), vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
      scene.add(rays);
      core = new THREE.Sprite(new THREE.SpriteMaterial({ map: G3.glowTex(), blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
      scene.add(core);
      const ag = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, -1.45), new THREE.Vector3(0, 0, 1.45)]);
      axis = new THREE.Line(ag, new THREE.LineBasicMaterial({ color: 0x777777, transparent: true, opacity: 0.6 })); scene.add(axis);
      const cone = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.14, 24), new THREE.MeshBasicMaterial({ color: 0xbbbbbb })); cone.rotation.x = Math.PI / 2; cone.position.z = 1.5; scene.add(cone);
    },
    update3D(p, scene, camera) {
      const t = tOf(p); sph.material.uniforms.t.value = t; sphBack.material.uniforms.t.value = t;
      G3.orbit(camera, p, 4.3, 22);
      const rho = Math.abs(t) < 1e-9 ? 1 : Math.sin(t) / t;
      core.scale.setScalar(0.25 + 1.25 * Math.abs(rho)); core.material.color.setRGB(...(rho >= 0 ? [1, 0.78, 0.35] : [0.35, 0.85, 1]).map(c => c * (0.15 + 0.85 * Math.abs(rho))));
      const pos = raysGeo.attributes.position.array, col = raysGeo.attributes.color.array, c = new THREE.Color();
      for (let i = 0; i < NR; i++) { const d = rayDir[i], f = (rayOff[i] + 3 * p) % 1, rr = 0.08 + 0.9 * f;
        pos.set([d[0] * rr, d[1] * rr, d[2] * rr], 3 * i);
        const ph = -d[2] * t; c.setHSL((((ph / (2 * Math.PI)) % 1) + 1) % 1, 0.95, 0.6); const a = 0.25 + 0.5 * Math.sin(Math.PI * f);
        col.set([c.r * a, c.g * a, c.b * a], 3 * i); }
      raysGeo.attributes.position.needsUpdate = true; raysGeo.attributes.color.needsUpdate = true;
    },
    left(p) { const t = tOf(p), rho = t < 1e-9 ? 1 : Math.sin(t) / t, R = G3.interp(D.t, D.R, t);
      return [{ label: 'time', value: [`kt = ${t.toFixed(2)}`], big: true }, { label: G3.rewinding(p) ? 'rewinding the loop' : '', value: [] },
        { label: 'density  sin kt / kt', value: [rho.toFixed(4)] },
        { label: 'kernel area so far', value: [`∫₀ᵗ K = ${R.toFixed(4)} k`] }, { gap: 6 },
        { label: 'boundary impedance', value: ['Z_b(0) = 2k/π', '= 0.63662 k'], color: '#ffd27a' },
        { label: 'sound impedance', value: ['Z₀ = k/√3', '= 0.57735 k'], color: '#7fdcff' },
        { label: 'ratio', value: ['2√3/π = 1.10266'] },
        { label: 'reflection at ω = 0', value: ['|S| = 0.0488'] }]; },
    scale(p, X, Y) { H.text('colour = phase', X, Y, { size: 14, color: CC.mut }); H.text('of e^(−ikμt)', X, Y + 19, { size: 14, color: CC.mut });
      H.wheel(X + 70, Y + 80, 34);
      H.text('μ = cos θ', X, Y + 150, { size: 14, color: CC.mut }); H.text('θ from k', X, Y + 169, { size: 14, color: CC.mut });
      H.text('centre glow', X, Y + 220, { size: 14, color: CC.mut }); H.text('= |density|', X, Y + 239, { size: 14, color: CC.mut });
      H.text('warm: +  cool: −', X, Y + 258, { size: 13, color: CC.dim }); },
    overlay(p, MX, MY, MW, MH) { H.text('k', MX + MW / 2 + 12, MY + 92, { size: 18, bold: true, color: '#cfcfcf' }); },
    panels: [
      { title: 'Memory kernel and its running area', draw(ctx, X, Y, w, h, p) { const t = tOf(p);
        const F = H.frame(X, Y, w, h, { x0: 0, x1: TMAX, y0: -0.2, y1: 0.78, xt: [[0, '0'], [10, '10'], [20, '20'], [30, '30'], [40, '40']], yt: [[0, '0'], [0.3, '0.3'], [0.6, '0.6']], xl: 'kt' });
        F.clip(); H.curve(D.t, D.K, F, { color: 'rgba(255,140,60,0.35)', width: 1.2 }); H.curve(D.t, D.R, F, { color: 'rgba(255,200,80,0.3)', width: 1.5 });
        const n = D.t.findIndex(v => v > t); const m = n < 0 ? D.t.length : n;
        H.curve(D.t.slice(0, m), D.K.slice(0, m), F, { color: '#ff8c3c', width: 1.6 }); H.curve(D.t.slice(0, m), D.R.slice(0, m), F, { color: '#ffc850', width: 2.4, glow: 8 });
        H.hline(F, ZB, { color: '#ffd27a', label: '2k/π', right: true }); H.hline(F, Z0, { color: '#7fdcff', label: 'k/√3', right: true, below: true }); F.unclip();
        H.dot(F.fx(t), F.fy(G3.interp(D.t, D.R, t)), { color: '#ffc850' });
        H.text('K(t) orange · ∫K gold', F.L + 6, F.T + 12, { size: 11, color: CC.mut }); } },
      { title: 'Z_b(s) along real s', draw(ctx, X, Y, w, h, p) {
        const F = H.frame(X, Y, w, h, { x0: 0, x1: 3, y0: 0, y1: 0.8, xt: [[0, '0'], [1, 'k'], [2, '2k'], [3, '3k']], yt: [[0, '0'], [0.2, '0.2'], [0.4, '0.4'], [0.6, '0.6']], xl: 's (Laplace rate)' });
        H.hline(F, Z0, { color: '#7fdcff', label: 'Z₀ = k/√3', right: true, below: true }); H.curve(D.s, D.Zb, F, { color: '#ffc850', width: 2.4, glow: 8 });
        const s = 1.5 - 1.5 * Math.cos(2 * Math.PI * p), z = G3.interp(D.s, D.Zb, s); H.dot(F.fx(s), F.fy(z), { color: '#ffc850', r: 6 });
        H.dot(F.fx(0), F.fy(ZB), { color: '#fff1c4', r: 5 }); H.text('2k/π at s = 0', F.fx(0) + 10, F.fy(ZB) - 8, { size: 12, color: '#ffd27a' });
        H.text('Z_b = k/arctan(k/s) − s', F.R - 4, F.T + 12, { size: 11, color: CC.mut, align: 'right' }); } },
      { title: 'Reflection S = (Z_b − Z₀)/(Z_b + Z₀)', draw(ctx, X, Y, w, h, p) {
        ctx.fillStyle = CC.panel; ctx.fillRect(X, Y, w, h); const cx = X + w / 2, cy = Y + h / 2 + 4, R = Math.min(w, h) / 2 - 26;
        ctx.strokeStyle = '#3a3a3a'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 2 * Math.PI); ctx.stroke();
        for (const g of [0.25, 0.5, 0.75]) { ctx.strokeStyle = '#1f1f1f'; ctx.beginPath(); ctx.arc(cx, cy, R * g, 0, 2 * Math.PI); ctx.stroke(); }
        ctx.beginPath(); ctx.moveTo(cx - R, cy); ctx.lineTo(cx + R, cy); ctx.moveTo(cx, cy - R); ctx.lineTo(cx, cy + R); ctx.stroke();
        for (let i = 1; i < D.w.length; i++) { const a = Math.abs(D.w[i]) / 4; ctx.strokeStyle = H.rgb(H.inferno(0.95 - 0.7 * a)); ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(cx + R * D.Sre[i - 1], cy - R * D.Sim[i - 1]); ctx.lineTo(cx + R * D.Sre[i], cy - R * D.Sim[i]); ctx.stroke(); }
        const w0 = 4 * Math.sin(2 * Math.PI * p), sr = G3.interp(D.w, D.Sre, w0), si = G3.interp(D.w, D.Sim, w0);
        H.dot(cx + R * sr, cy - R * si, { r: 6, color: '#ffffff' });
        H.text(`ω = ${w0.toFixed(2)} k`, X + 8, Y + 16, { size: 12, color: CC.mut }); H.text(`|S| = ${Math.hypot(sr, si).toFixed(3)}`, X + 8, Y + 32, { size: 12, color: CC.fg });
         H.text('centre = matched', cx, Y + h - 6, { size: 11, color: CC.mut, align: 'center' });
        H.text('|ω| < k: leaks', X + w - 8, Y + 16, { size: 11, color: CC.mut, align: 'right' }); H.text('|ω| > k: |S| = 1, total', X + w - 8, Y + 31, { size: 11, color: CC.mut, align: 'right' }); } },
    ],
    foot: ['Inset maths: I(μ,t) = e^(−ikμt) per direction · density ρ = ½∫ I dμ = sin(kt)/kt · S traced over s = iω + 0',
      'Exact: ρ̂(s) = arctan(k/s)/k = 1/(s + Z_b(s)) ⇒ Z_b(s) = k/arctan(k/s) − s ⇒ Z_b(0) = 2k/π · kernel K(t) from the hidden chain ℓ ≥ 1 (1200 moments)',
      'Card P1 · proposed atlas card · When the Neutrinos Leave · doi:10.5281/zenodo.23858157 · collisionless, one wavenumber k, units of k'],
  };
})();
