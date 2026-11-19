# SCRIPT: NU-A6-LEVEL3-RATES  the odd rate at three resolution levels, from the stored brackets, as fixed in PREREGISTERED.txt
# Reads res_L3_r125.json and res_L3_r08.json (this folder). Level 1 and 2 thresholds are those of PREREGISTERED.txt.
import json, math, itertools
DF, DI = 0.49773, 0.52832
tau = lambda d: math.log((DI - d) / (d - DF))
rate = lambda d125, d08: (tau(d125) - tau(d08)) / math.log(1.25)
L1 = dict(a=0.50984158, b=0.51169233); L2 = dict(a=0.50991687, b=0.51175643)
ra = json.load(open('res_L3_r125.json')); rb = json.load(open('res_L3_r08.json'))
la, ha, lb, hb = ra['lo'], ra['hi'], rb['lo'], rb['hi']; ma, mb = 0.5 * (la + ha), 0.5 * (lb + hb)
R1, R2, R3 = rate(L1['a'], L1['b']), rate(L2['a'], L2['b']), rate(ma, mb)
corners = [rate(x, y) for x in (la, ha) for y in (lb, hb)]
print(f'level 3 thresholds: r=1.25 {ma:.8f} +- {0.5*(ha-la):.8f} [{la:.8f}, {ha:.8f}];  r=0.8 {mb:.8f} +- {0.5*(hb-lb):.8f} [{lb:.8f}, {hb:.8f}]')
print(f'odd rate: R1 = {R1:.5f}, R2 = {R2:.5f}, R3 = {R3:.5f}, four-corner range of R3 [{min(corners):.5f}, {max(corners):.5f}]')
s12, s23 = R2 - R1, R3 - R2
print(f's12 = {s12:+.5f}, s23 = {s23:+.5f} (four-corner range {min(corners)-R2:+.5f} .. {max(corners)-R2:+.5f})')
print(f'KILL LINE (b): |R3 - R2| = {abs(s23):.5f} against |R2 - R1| = {abs(s12):.5f}: {"NOT converging" if abs(s23) > abs(s12) else "passes (the shift shrinks)"};'
      f' at the four corners |R3 - R2| <= {max(abs(c - R2) for c in corners):.5f}; sign of s23 {"same as" if s12 * s23 > 0 else "opposite to"} s12')
for name, lo2, d12, lo, hi, mid in (('r=1.25', L2['a'], L2['a'] - L1['a'], la, ha, ma), ('r=0.8', L2['b'], L2['b'] - L1['b'], lb, hb, mb)):
    f = (mid - lo2) / d12
    print(f'{name}: shift L1->L2 {d12:+.3e}, L2->L3 {mid-lo2:+.3e} (range {lo-lo2:+.3e} .. {hi-lo2:+.3e}); factor {f:.3f} (range {(lo-lo2)/d12:.3f} .. {(hi-lo2)/d12:.3f})')
    for lab, fac in (('first order in the cell size (2/3)', 2/3), ('second order in the cell size (4/9)', 4/9), ('first order in the time step (1/3)', 1/3)):
        p = lo2 + d12 * fac; print(f'    predicted by {lab}: {p:.8f}  {"inside" if lo <= p <= hi else "outside"} the bracket')
q = 1.5
if s12 / s23 > 1:
    p_obs = math.log(s12 / s23) / math.log(q); Rinf = R3 + s23 / (q ** p_obs - 1)
    print(f'RICHARDSON as fixed before the runs: p_obs = {p_obs:.2f}, R_inf = {Rinf:.5f}' + ('  -- p_obs outside [0.5, 4]: reported, marked untrustworthy' if not 0.5 <= p_obs <= 4 else ''))
    vals = []
    for c in corners:
        s = c - R2
        if s12 / s > 1: po = math.log(s12 / s) / math.log(q); vals.append(c + s / (q ** po - 1))
        else: vals.append(None)
    print('    over the four corners of the level-3 range: R_inf =', [None if v is None else round(v, 5) for v in vals], '(None: the shift does not shrink at that corner, no extrapolation)')
print(f'two-level extrapolations from L2, L3: p = 1: {R3 + s23/(q-1):.5f}; p = 2: {R3 + s23/(q*q-1):.5f}')
half = 0.5 * (max(corners) - min(corners)); fl, sp = 0.0038, 0.0036
print(f'budget at level 3: bracket half-range {half:.4f}, fluid reference {fl}, pair spread {sp}: quadrature {math.sqrt(half**2+fl**2+sp**2):.4f}, linear {half+fl+sp:.4f}')
