// shared 3D bits: glow sprite texture, hsv in GLSL, seeded random, loop time with rewind
window.G3 = {
  glowTex() { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.25, 'rgba(255,255,255,0.55)'); r.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); },
  HSV: `vec3 hsv(float h, float s, float v){ vec3 k = vec3(1.0, 2.0/3.0, 1.0/3.0); vec3 p = abs(fract(vec3(h) + k) * 6.0 - 3.0); return v * mix(vec3(1.0), clamp(p - 1.0, 0.0, 1.0), s); }`,
  rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; },
  // loop clock: run 0 -> 1 over [0, run], smooth rewind over [run, 1)
  clock(p, run = 0.88) { if (p < run) return p / run; const q = (p - run) / (1 - run); return 0.5 + 0.5 * Math.cos(Math.PI * q); },
  rewinding(p, run = 0.88) { return p >= run; },
  orbit(camera, p, dist, elev, az0 = 0.6) { const a = az0 + 2 * Math.PI * p, e = elev * Math.PI / 180;
    camera.up.set(0, 0, 1); camera.position.set(dist * Math.cos(e) * Math.cos(a), dist * Math.cos(e) * Math.sin(a), dist * Math.sin(e)); camera.lookAt(0, 0, 0); },
  interp(xs, ys, x) { if (x <= xs[0]) return ys[0]; const n = xs.length; if (x >= xs[n - 1]) return ys[n - 1];
    let lo = 0, hi = n - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (xs[m] <= x) lo = m; else hi = m; }
    const f = (x - xs[lo]) / (xs[hi] - xs[lo]); return ys[lo] + f * (ys[hi] - ys[lo]); },
  project(v, camera, MX, MY, MW, MH) { const q = v.clone().project(camera); return [MX + (q.x + 1) / 2 * MW, MY + (1 - q.y) / 2 * MH]; },
};
