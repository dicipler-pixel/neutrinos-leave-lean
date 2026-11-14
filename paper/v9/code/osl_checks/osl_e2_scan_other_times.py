# SCRIPT: OSL-STEVE-E2-SCAN-OTHER-TIMES
# Opposite / other-time run of Check E (rule: never call an eye dead from one setup). Same solver (validated in E), Gaussian centre.
# Diagnostics now read at EVERY epoch eps* in [0.3, 6] and also CUMULATIVELY (integral from tau0 to eps*), still normalised to instantaneous decoupling.
# Scanning eps* is ONE free parameter, so a pass is a fit, flagged as such. KILL (written before the run): the eye is dead only if NO eps* and no
# cumulative window gives max |G_pred - G| <= 0.10; if some eps* does, report where it sits relative to Steve's named epochs (1.7 first max, 4.0-4.5 horizon).
import numpy as np, importlib.util, sys
sp = importlib.util.spec_from_file_location('e', 'osl_e_linear_two_clock.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
taus = m.taus; ks = np.linspace(0.15, 9.0, 60); wk = ks**2 * np.exp(-ks**2 / 4) * (ks[1] - ks[0])
def gauss(mode, edec=None):
    acc = np.zeros((len(taus), 5))
    for kk, ww in zip(ks, wk): acc += ww * m.run_mode(kk, mode, edec, taus)
    return acc
G = np.array([5.90, 5.33, 4.20, 2.65, 1.17, 0.39]) / 6.15; edecs = [0.25, 0.5, 1, 2, 4, 8]
gpf = gauss('pf'); gin = gauss('inst'); gr = {e: gauss('grad', e) for e in edecs}
np.savez('osl_e2_data.npz', taus=taus, gpf=gpf, gin=gin, **{'g%g' % e: gr[e] for e in edecs})
def DS(a): return np.abs(a[:, 2] - a[:, 1])
def DSG(a): return np.abs(a[:, 3])
def SNAP(a): return 1 - a[:, 0] / gpf[:, 0]
def cum(x): return np.concatenate(([0], np.cumsum(0.5 * (x[1:] + x[:-1]) * np.diff(taus))))
for nm, f in [('DS', DS), ('DSG', DSG), ('SNAP_Delta', SNAP)]:
    for mode in ['snapshot', 'cumulative']:
        den = f(gin); den = cum(den) if mode == 'cumulative' else den
        best = (9, None)
        for j in range(30, len(taus), 3):
            if abs(den[j]) < 1e-12: continue
            pred = np.array([(cum(f(gr[e]))[j] if mode == 'cumulative' else f(gr[e])[j]) / den[j] for e in edecs]); err = abs(pred - G).max()
            if err < best[0]: best = (err, taus[j], pred)
        print('%-11s %-10s best eps* = %.2f max err %.3f %s  G_pred=%s' % (nm, mode, best[1], best[0], 'PASS(fit)' if best[0] <= 0.10 else 'FAIL', np.round(best[2], 3)))
