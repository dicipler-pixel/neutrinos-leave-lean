# SCRIPT: OSL-STEVE-C-SPEED-CONTEST-EOS
# Mapping under test (from the paper + Check A): the neutrino rms streaming speed is sqrt(E_B)/k = sqrt(<mu^2>) = 1/sqrt3 (exact) and the
# plasma sound speed is c_s = sqrt(dp/de). In pure radiation they coincide; during e+- annihilation c_s falls below 1/sqrt3, so a
# 'speed contest' reading predicts the free-streaming advantage GROWS there. Pre-registered quantitative form (no fit):
#   shift_pred(T_H) = 0.15 * R_nu(T_H) * G(eps_dec = T_H/T_dec) * f,  f = (1 - c_s(T_H)) / (1 - 1/sqrt3)   (front speed 1 against sound)
#   baseline        = 0.15 * R_nu(T_H) * G(...)                                                             (no contrast factor)
# Steve's published envelope: relative shift of delta_c is 5.3% to 6.2% at ALL sample masses 3e5 .. 7e7 Msun (Sec. IV D).
# VALIDATION (must pass first): my plasma p/e minimum must be 0.274 +- 0.003 near T = 0.16 MeV; R_nu = 0.488 (T>>m_e) and 0.405 (T<<m_e).
# KILL CONDITIONS (written before the run):
# KC0 validation fails -> stop, code not trusted.
# KC1 'contrast enhancement' mapping dies if shift_pred (with f) exceeds 6.5% at any sample mass between 3e6 and 7e7 Msun (G ~ 1 there).
# KC2 opposite reading (the contrast SHRINKS the effect: f' = 1/f) dies if shift_pred(f') is below 5.3% at any sample mass 3e5..7e7.
import numpy as np
from scipy.integrate import quad
me = 0.511
def fd(T, n):  # fermi-dirac integrals for g=4 (e+-), zero chem. potential
    pass
def eP(T):
    f = lambda p, w: p**2 * w(p) / (np.exp(np.sqrt(p**2 + me**2) / T) + 1)
    e = quad(lambda p: p**2 * np.sqrt(p**2 + me**2) / (np.exp(np.sqrt(p**2 + me**2) / T) + 1), 0, 60 * T + 10)[0] * 4 / (2 * np.pi**2)
    P = quad(lambda p: p**4 / np.sqrt(p**2 + me**2) / (np.exp(np.sqrt(p**2 + me**2) / T) + 1), 0, 60 * T + 10)[0] * 4 / (6 * np.pi**2)
    return e + np.pi**2 / 15 * T**4, P + np.pi**2 / 45 * T**4
def sdens(T): e, P = eP(T); return (e + P) / T
s_hi_coef = 2 * np.pi**2 / 45 * 5.5
def Tnu(T): return (sdens(T) / s_hi_coef)**(1 / 3)
def Rnu(T): enu = 6 * 7 / 8 * np.pi**2 / 30 * Tnu(T)**4; e, P = eP(T); return enu / (enu + e)
def cs2(T): h = 1e-4 * T; (e1, P1), (e2, P2) = eP(T - h), eP(T + h); return (P2 - P1) / (e2 - e1)
Ts = np.geomspace(0.03, 20, 160); pe = np.array([eP(T)[1] / eP(T)[0] for T in Ts]); i = np.argmin(pe)
print('KC0 validation: min p/e = %.4f at T = %.3f MeV (Steve: 0.274 at ~0.16)' % (pe[i], Ts[i]))
print('   R_nu(T=20) = %.4f (Steve 0.488) ; R_nu(T=0.03) = %.4f (Steve 0.405 for Neff=3)' % (Rnu(20.0), Rnu(0.03)))
c2 = np.array([cs2(T) for T in Ts]); j = np.argmin(c2); print('   min c_s^2 = dp/de = %.4f (c_s = %.4f) at T = %.3f MeV ; 1/3 = 0.3333' % (c2[j], c2[j]**0.5, Ts[j]))
ok0 = abs(pe[i] - 0.274) < 0.003 and abs(Rnu(20.0) - 0.488) < 0.002 and abs(Rnu(0.03) - 0.405) < 0.002
print('KC0 PASS' if ok0 else 'KC0 FAIL')
# horizon temperature from mass: M_H = 1.5e5 (T/MeV)^-2 (g*/10.75)^-1/2 ; g* defined by rho = (pi^2/30) g* T^4 (plasma + nu)
def gstar(T):
    e, P = eP(T); enu = 6 * 7 / 8 * np.pi**2 / 30 * Tnu(T)**4; return (e + enu) / (np.pi**2 / 30 * T**4)
def TH_of(M):
    from scipy.optimize import brentq
    return brentq(lambda T: 1.5e5 * T**-2 * (gstar(T) / 10.75)**-0.5 - M, 0.02, 30)
Gtab = {0.25: 0.959, 0.5: 0.867, 1: 0.683, 2: 0.431, 4: 0.190, 8: 0.063}
def G(ed):
    x = np.log(list(Gtab.keys())); y = list(Gtab.values()); return float(np.interp(np.log(ed), x, y, left=1.0, right=0.063 * (8 / ed)**2))
print('\n  M_H[Msun]   T_H[MeV]  R_nu    c_s     f      0.15 R G   with f     with 1/f')
rows = []
for M in [3e5, 1e6, 3e6, 7e6, 1.6e7, 3e7, 7e7]:
    T = TH_of(M); R = Rnu(T); c = cs2(T)**0.5; f = (1 - c) / (1 - 3**-0.5); g_ = G(T / 1.0)
    base = 0.15 * R * g_ * 100; rows.append((M, T, base, base * f, base / f))
    print('  %8.1e  %8.3f  %.3f  %.4f  %.3f  %6.2f%%   %6.2f%%   %6.2f%%' % (M, T, R, c, f, base, base * f, base / f))
heavy = [r for r in rows if r[0] >= 3e6]
print('KC1: max shift_pred(with f) for M >= 3e6 = %.2f%% (kill if > 6.5%%) -> %s' % (max(r[3] for r in heavy), 'FAIL' if max(r[3] for r in heavy) > 6.5 else 'PASS'))
print('KC2: min shift_pred(with 1/f) over all = %.2f%% (kill if < 5.3%%) -> %s' % (min(r[4] for r in rows), 'FAIL' if min(r[4] for r in rows) < 5.3 else 'PASS'))
print('baseline (no f): range %.2f%% - %.2f%% ; envelope 5.3 - 6.2' % (min(r[2] for r in rows), max(r[2] for r in rows)))
