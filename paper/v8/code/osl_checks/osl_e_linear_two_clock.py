# SCRIPT: OSL-STEVE-E-LINEAR-TWO-CLOCK
# (v2: first_max takes the maximum of -delta; v1 returned NaN for want of this sign flip and was discarded before any diagnostic was read)
# Mapping under test (paper Q3 / 'two clocks'): a diagnostic that reads the DIFFERENCE between the two fluids cancels the universal
# (slicing/gravity) part, while a diagnostic that reads the SUM (total density) does not. Steve's linear ambiguity (5% superhorizon vs 9% post-entry)
# lives in the sum. Candidate predictors of the G curve (all from linear Boltzmann theory, Steve's App. B equations, Gaussian profile centre r=0,
# plasma-orthogonal slices):
#   DS  : relative-density difference |delta_nu^pl - delta_gamma^pl| at epoch eps*  (the two-clock difference; zero for the perfect fluid)
#   DSG : neutrino shear sigma_nu at eps*  (the l=2 content; drives phi - psi)
#   D1  : suppression of the total density first maximum (the 'single-clock' sum reading; Steve found it fails)
# G_pred(eps_dec) = D(eps_dec)/D(instantaneous at eps0=0.1), for D1 using the fractional suppression 1 - X/X_pf.
# VALIDATION FIRST (kill the code, not the idea): instantaneous decoupling, R_nu=0.409: single mode, first max of Delta (zero-momentum slice)
#   must be 0.911 x perfect fluid (Steve App. B, to +-0.003); Gaussian centre: 0.944 (Delta) and 0.938 (delta^pl) (+-0.006).
# KILL CONDITIONS for the mapping (written before the run): a diagnostic PASSES iff max_eps_dec |G_pred - G_Steve| <= 0.10 at EVERY eps* in {4.0, 4.25, 4.5}
# (his apparent-horizon epochs, not fitted); it is reported separately at eps*=1.7. Opposite check: D1 (the sum reading) must be run and reported too.
import numpy as np, sys
from scipy.integrate import solve_ivp
Rn = 0.409; L = 60; TAU0 = 0.1
def make_rhs(k, R, kapf):
    def rhs(tau, y):
        dg, tg, dn, tn = y[0], y[1], y[2], y[3]; F = y[4:]; Hc = 1.0 / tau
        dt_ = (1 - R) * dg + R * dn; tt_ = (1 - R) * tg + R * tn
        phi = (-1.5 * Hc**2 * dt_ - 6 * Hc**3 * tt_ / k**2) / k**2
        sig = 0.5 * F[0]; psi = phi - 6 * R * sig * Hc**2 / k**2
        phid = 2 * Hc**2 * tt_ / k**2 - Hc * psi; kap = kapf(tau)
        out = np.empty_like(y)
        out[0] = -4 / 3 * tg + 4 * phid
        out[1] = k**2 * dg / 4 + k**2 * psi + (kap * R / (1 - R) * (tn - tg) if R > 0 else 0.0)
        out[2] = -4 / 3 * tn + 4 * phid
        out[3] = k**2 * (dn / 4 - sig) + k**2 * psi - kap * (tn - tg)
        Fm = np.concatenate(([0.0], F))  # index shift: Fm[l-1] = F_l for l>=2, Fm[0] placeholder for l=1 (unused)
        for i in range(len(F)):
            l = i + 2
            Fl1 = F[i + 1] if i + 1 < len(F) else (2 * l + 1) / (k * tau) * F[i] - (F[i - 1] if i > 0 else 0.0)
            if l == 2: out[4 + i] = 8 / 15 * tn - 3 / 5 * k * Fl1 - kap * F[i]
            else: out[4 + i] = k / (2 * l + 1) * (l * F[i - 1] - (l + 1) * Fl1) - kap * F[i]
        return out
    return rhs
def run_mode(k, mode, edec, taus):
    """mode: 'pf' perfect fluid, 'inst' instantaneous decoupling at tau0, 'grad' gradual with eps_dec. returns arrays on taus"""
    psi = 2 / 3; d0 = -2 * psi - 2 / 3 * (k * TAU0)**2 * psi; t0 = 0.5 * k**2 * TAU0 * psi
    y0 = np.zeros(4 + L); y0[:4] = [d0, t0, d0, t0]
    out = np.zeros((len(taus), 4 + L)); Hc = lambda t: 1 / t
    if mode == 'pf': segs = [(TAU0, taus[-1], 0.0, lambda t: 0.0, y0)]
    elif mode == 'inst': segs = [(TAU0, taus[-1], Rn, lambda t: 0.0, y0)]
    else:
        kf = lambda t: (1 / t) * (edec / t)**3; ts = edec / 100**(1 / 3)
        if ts <= TAU0: segs = [(TAU0, taus[-1], Rn, kf, y0)]
        else: segs = [(TAU0, ts, 0.0, lambda t: 0.0, y0), (ts, taus[-1], Rn, kf, None)]
    cur = None; res = []
    for (a, b, R, kf, y) in segs:
        if y is None: y = cur.copy(); y[2], y[3] = y[0], y[1]; y[4:] = 0.0
        grid = taus[(taus >= a) & (taus <= b)]
        sol = solve_ivp(make_rhs(k, R, kf), (a, b), y, method='LSODA', t_eval=np.unique(np.concatenate(([a], grid, [b]))), rtol=1e-8, atol=1e-11)
        for tt, yy in zip(sol.t, sol.y.T): res.append((tt, R, yy))
        cur = sol.y[:, -1].copy()
    # assemble observables on taus
    obs = np.zeros((len(taus), 5)); ti = {round(r[0], 9): r for r in res}
    for j, tau in enumerate(taus):
        r = ti[round(tau, 9)] if round(tau, 9) in ti else min(res, key=lambda q: abs(q[0] - tau))
        R, y = r[1], r[2]; Hc = 1 / tau
        # after the switch R=Rn; before it fluid: delta_nu = delta_gamma so all combos coincide
        Reff = Rn if (mode != 'pf') else 0.0
        dg, tg, dn, tn = y[:4]; dtot = (1 - Reff) * dg + Reff * dn; ttot = (1 - Reff) * tg + Reff * tn
        obs[j] = [dtot + 4 * Hc * ttot / k**2, dg + 4 * Hc * tg / k**2, dn + 4 * Hc * tg / k**2, 0.5 * y[4], dtot]
    return obs  # columns: Delta, dpl_gamma, dpl_nu, sigma, delta_tot
taus = np.round(np.linspace(0.1, 6.0, 591), 9)
def first_max(tau, x):
    x = -np.asarray(x)  # zeta>0 gives delta<0 (underdensity sign); Steve's overdensity is the negative of this, so the 'first maximum' is of -delta
    for i in range(1, len(x) - 1):
        if tau[i] > 0.5 and x[i] > x[i - 1] and x[i] >= x[i + 1]: return tau[i], x[i]
    return np.nan, np.nan
if __name__ == '__main__':
    # --- validation, single mode (k r_m = 2 isn't special; use a mode with kappa small start: k*tau0 = 0.1 -> k = 1)
    k = 1.0; pf = run_mode(k, 'pf', None, taus); ins = run_mode(k, 'inst', None, taus)
    # single-mode horizon-entry maximum of Delta: first max after kTau ~ 1
    tpf, mpf = first_max(taus, pf[:, 0]); tin, min_ = first_max(taus, ins[:, 0])
    print('VALIDATION single mode (k=1): first max Delta: pf %.4f at tau=%.2f ; inst %.4f at tau=%.2f ; ratio %.4f (Steve 0.911 +-0.003 / 0.907 for delta^pl)' % (mpf, tpf, min_, tin, min_ / mpf))
    tpf2, mpf2 = first_max(taus, pf[:, 1]); tin2, min2 = first_max(taus, ins[:, 1] * (1 - Rn) + ins[:, 2] * Rn)
    # --- Gaussian centre: integrate over k with weight k^2 exp(-k^2/4)
    ks = np.linspace(0.15, 9.0, 60); wk = ks**2 * np.exp(-ks**2 / 4) * (ks[1] - ks[0])
    def gauss(mode, edec=None):
        acc = np.zeros((len(taus), 5))
        for kk, ww in zip(ks, wk): acc += ww * run_mode(kk, mode, edec, taus)
        return acc
    import time; t0 = time.time(); gpf = gauss('pf'); gin = gauss('inst'); print('(gaussian pf+inst took %.0fs)' % (time.time() - t0)); sys.stdout.flush()
    tp, mp = first_max(taus, gpf[:, 0]); ti_, mi = first_max(taus, gin[:, 0]); tp2, mp2 = first_max(taus, gpf[:, 1]); ti2, mi2 = first_max(taus, gin[:, 1])
    print('VALIDATION Gaussian centre: first max Delta pf %.4g at eps=%.2f, inst %.4g at eps=%.2f -> ratio %.4f (Steve 0.944, eps~1.7)' % (mp, tp, mi, ti_, mi / mp))
    print('                            first max delta^pl_gamma: ratio %.4f (Steve 0.938)' % (mi2 / mp2))
    ok = abs(min_ / mpf - 0.911) < 0.004 and abs(mi / mp - 0.944) < 0.007
    print('VALIDATION', 'PASS' if ok else 'FAIL'); sys.stdout.flush()
    if not ok: sys.exit(1)
    G = np.array([5.90, 5.33, 4.20, 2.65, 1.17, 0.39]) / 6.15; edecs = [0.25, 0.5, 1, 2, 4, 8]
    gr = {e: gauss('grad', e) for e in edecs}
    def at(arr, col, es): j = np.argmin(abs(taus - es)); return arr[j, col]
    print('\nG_pred at Gaussian centre vs Steve G =', np.round(G, 3))
    results = {}
    for es in [1.7, 4.0, 4.25, 4.5]:
        # DS: |dpl_nu - dpl_gamma| ; DSG: |sigma| ; D2: suppression of delta^pl_gamma snapshot ; D3: suppression of Delta snapshot
        def D(arr, kind):
            if kind == 'DS': return abs(at(arr, 2, es) - at(arr, 1, es))
            if kind == 'DSG': return abs(at(arr, 3, es))
            if kind == 'SNAP_Delta': return 1 - at(arr, 0, es) / at(gpf, 0, es)
            if kind == 'SNAP_dpl': return 1 - at(arr, 1, es) / at(gpf, 1, es)
        for kind in ['DS', 'DSG', 'SNAP_Delta', 'SNAP_dpl']:
            den = D(gin, kind); pred = np.array([D(gr[e], kind) / den for e in edecs]); err = abs(pred - G).max(); results[(es, kind)] = err
            print('  eps*=%.2f %-11s G_pred=%s max err %.3f %s' % (es, kind, np.round(pred, 3), err, 'PASS' if err <= 0.10 else 'FAIL'))
    # D1: first-max suppression, sum reading (Steve: fails); shift_pred = pf_max/max - 1 normalised
    s_in = mp / mi - 1; p1 = []
    for e in edecs:
        tm, mm = first_max(taus, gr[e][:, 0]); p1.append((mp / mm - 1) / s_in if mm == mm else np.nan)
    print('  D1 first-max Delta (sum reading): G_pred=%s max err %.3f' % (np.round(p1, 3), np.nanmax(abs(np.array(p1) - G))))
    print('  (first-max epochs: ' + ', '.join('%g:%.2f' % (e, first_max(taus, gr[e][:, 0])[0]) for e in edecs) + ')')
