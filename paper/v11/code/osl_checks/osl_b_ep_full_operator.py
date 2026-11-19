# SCRIPT: OSL-STEVE-B-EP-FULL-OPERATOR
# Question: Steve's neutrino operator L = -i k mu - kappa (I - P0) (momentum given to plasma, so l=1 is damped too).
# Paper-derived claim to test: the two-moment truncation has its exceptional point at kappa_EP = 2 sqrt(E_B) = 2k/sqrt3
# (critical damping of a pair coupled with weight E_B = k^2/3). Does that EP survive when all l are kept?
# KILL CONDITIONS (written before the run):
# KB1 (truncation control) N=2 EP must come out at 2/sqrt3 = 1.1547 (k=1) to 1e-6, else the code is wrong.
# KB2 the claim 'kappa_EP = 2 sqrt(E_B)' survives in the full operator iff the N=200 value is within 10% of 1.1547.
# KB3 (opposite / inverse reading) the statement 'above kappa_EP the neutrinos are overdamped (no oscillating mode)' survives
#     iff for N=200 every eigenvalue with Re > -kappa/2... is real for kappa > 1.5*kappa_EP; we report the least-damped eigenvalue's Im.
import numpy as np
def L(N, kap, k=1.0):
    n = np.arange(1, N); a = n / np.sqrt(4.0 * n**2 - 1.0)       # mu P_n = a_{n+1} P_{n+1} + a_n P_{n-1}, orthonormal Legendre
    J = np.diag(a, 1) + np.diag(a, -1)
    D = np.eye(N); D[0, 0] = 0.0
    return -1j * k * J - kap * D
def slowest(N, kap):
    ev = np.linalg.eigvals(L(N, kap)); i = np.argmax(ev.real); return ev[i], ev
def ep(N, lo=0.01, hi=6.0):
    # smallest kappa such that the least-damped eigenvalue is real (|Im| < 1e-9) and stays real above it
    ks = np.linspace(lo, hi, 5901); flag = np.array([abs(slowest(N, x)[0].imag) < 1e-7 for x in ks])
    # last kappa at which a non-real least-damped eigenvalue occurs
    bad = np.where(~flag)[0]
    return ks[bad.max() + 1] if len(bad) and bad.max() + 1 < len(ks) else (ks[0] if len(bad) == 0 else np.nan)
print('2/sqrt3 = %.6f' % (2 / 3**0.5))
res = {}
for N in [2, 3, 5, 10, 40, 200]:
    res[N] = ep(N); print('N = %3d : least-damped eigenvalue becomes real (and stays real) for kappa >= %.4f' % (N, res[N]))
print('KB1: |EP(N=2) - 2/sqrt3| = %.2e' % abs(res[2] - 2 / 3**0.5))
print('KB2: EP(N=200)/(2/sqrt3) = %.3f' % (res[200] / (2 / 3**0.5)))
for kap in [0.5, 1.0, 1.5, 2.0, 3.0, 6.0]:
    for N in [2, 200]:
        lam, ev = slowest(N, kap); print('kappa=%.1f N=%3d least-damped lambda = %+.4f %+.4fi ; diffusion estimate -k^2/(3 kappa) = %+.4f' % (kap, N, lam.real, lam.imag, -1 / (3 * kap)))
