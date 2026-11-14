# SCRIPT: A4-SCREEN  D4: fixed-amplitude paired runs (+f, -f, 0) at delta 0.5100 and 0.5115, per (eps_s, l); selection rule applied
import sys, os, json, time, numpy as np
from scipy.interpolate import CubicSpline
import restart
from restart import run_member, initial, evolve
from cpuwait import wait
F = 0.5; DELTAS = (0.5100, 0.5115)
PAIRS = [(2.0, 3), (0.5, 3), (4.0, 3), (2.0, 4), (0.5, 4), (4.0, 4), (2.0, -1)]
if len(sys.argv) > 1: PAIRS = [PAIRS[int(i)] for i in sys.argv[1].split(',')]
os.makedirs('screen', exist_ok=True)
def P(*a): print(*a, flush=True)
def get(tag, fn):
    p = f'screen/{tag}.npz'
    if os.path.exists(p):
        z = np.load(p, allow_pickle=True); return dict(status=str(z['status']), eps=float(z['eps']), rec=z['rec'], Imin=float(z['Imin']), max2MR=float(z['max2MR']))
    w = wait(P); t1 = time.time()
    o = fn()
    np.savez(p, status=o['status'], eps=o['eps'], rec=o['rec'], Imin=o['Imin'], max2MR=o['max2MR'])
    P(f'  run {tag}: {o["status"]} at eps={o["eps"]:.3f}  Imin={o["Imin"]:.3e}  ({time.time()-t1:.0f}s, waited {w:.0f}s)')
    return dict(status=o['status'], eps=o['eps'], rec=o['rec'], Imin=o['Imin'], max2MR=o['max2MR'])
def spl(rec, col):
    e = rec[:, 0]; m = np.concatenate([[True], np.diff(e) > 0]); return CubicSpline(e[m], rec[m, col])
summary = json.load(open('screen_res.json')) if os.path.exists('screen_res.json') else {}
for eps_s, l in PAIRS:
    key = f'es{eps_s:g}_l{l}'; res = {}
    P(f'== pair eps_s={eps_s} l={l}  (f = +/-{F}, bump support 0.3-2 r_m)')
    for d in DELTAS:
        cont = get(f'cont_d{d}', lambda: evolve(initial(d)))
        z = get(f'zero_d{d}_es{eps_s:g}', lambda: run_member(d, eps_s, l, 0.0, 'cache'))
        p = get(f'plus_d{d}_es{eps_s:g}_l{l}', lambda: run_member(d, eps_s, l, +F, 'cache', mode='bump'))
        m = get(f'minus_d{d}_es{eps_s:g}_l{l}', lambda: run_member(d, eps_s, l, -F, 'cache', mode='bump'))
        hi = min(6.0, cont['eps'], z['eps'], p['eps'], m['eps']) - 0.02
        g = np.linspace(eps_s + 0.02, hi, 400)
        noise = max(float(np.max(np.abs(spl(z['rec'], 1)(g) - spl(cont['rec'], 1)(g)))), 1e-12)
        dC = spl(p['rec'], 1)(g) - spl(m['rec'], 1)(g)
        dPc = spl(p['rec'], 4)(g) - spl(m['rec'], 4)(g)
        dPk = spl(p['rec'], 5)(g) - spl(m['rec'], 5)(g)
        sep = float(np.max(np.abs(dC)))
        rows = [(float(E), float(spl(p['rec'], 1)(E) - spl(m['rec'], 1)(E)), float(spl(p['rec'], 4)(E) - spl(m['rec'], 4)(E)))
                for E in (2.5, 3.0, 4.0, 5.0, 5.5, 6.0) if eps_s + 0.02 <= E <= hi + 1e-9]
        res[str(d)] = dict(cont=(cont['status'], cont['eps']), zero=(z['status'], z['eps']), plus=(p['status'], p['eps']), minus=(m['status'], m['eps']),
                           Imin=(p['Imin'], m['Imin']), noise=noise, sep=sep, sepPc=float(np.max(np.abs(dPc))), sepPk=float(np.max(np.abs(dPk))),
                           rows=rows, eps_hi=float(hi), C5=(float(spl(p['rec'], 1)(min(5.0, hi))), float(spl(m['rec'], 1)(min(5.0, hi))), float(spl(z['rec'], 1)(min(5.0, hi)))))
        P(f'  delta={d}: outcomes cont {cont["status"]}@{cont["eps"]:.2f}, zero {z["status"]}@{z["eps"]:.2f}, +f {p["status"]}@{p["eps"]:.2f}, -f {m["status"]}@{m["eps"]:.2f}')
        P(f'     record eps {eps_s+0.02:.2f}-{hi:.2f}: max|dCmax(+ - -)| = {sep:.3e}; noise floor {noise:.3e}; ratio {sep/noise:.1f};'
          f' max|d(P_r/e_nu) centre| = {res[str(d)]["sepPc"]:.3e}, at C-peak cell = {res[str(d)]["sepPk"]:.3e}')
        for E, a, b in rows: P(f'       eps={E}: dCmax={a:+.3e}  d(P_r/e_nu)_centre={b:+.3e}')
    flip = any(res[str(d)]['plus'][0] != res[str(d)]['minus'][0] for d in DELTAS)
    above = any(res[str(d)]['sep'] > 10*res[str(d)]['noise'] for d in DELTAS)
    sel = flip or above
    # linearised estimate: dCmax at common eps (<=5) over dCmax/d delta from the zero runs at the two deltas
    E = min(res[str(d)]['eps_hi'] for d in DELTAS); E = min(E, 5.0)
    def at(tag): return float(spl(np.load(f'screen/{tag}.npz')['rec'], 1)(E))
    slope = (at(f'zero_d{DELTAS[1]}_es{eps_s:g}') - at(f'zero_d{DELTAS[0]}_es{eps_s:g}'))/(DELTAS[1]-DELTAS[0])
    dCE = np.mean([at(f'plus_d{d}_es{eps_s:g}_l{l}') - at(f'minus_d{d}_es{eps_s:g}_l{l}') for d in DELTAS])
    est = -dCE/slope
    P(f'  SELECTION: outcome flip={flip}, separation>10x noise={above} -> {"TRISECT" if sel else "NOT SELECTED (null)"};'
      f' linearised estimate delta_c(+)-delta_c(-) ~ {est:+.2e} (dCmax at eps={E:.2f} = {dCE:+.3e}, dCmax/d delta = {slope:.3f})')
    summary[key] = dict(res=res, selected=sel, flip=flip, above=above, est=est, slope=slope, dCE=dCE, E=E)
    json.dump(summary, open('screen_res.json', 'w'), indent=1)
