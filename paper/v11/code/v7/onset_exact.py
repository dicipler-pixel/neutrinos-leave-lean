# SCRIPT: NU-V7-ONSET  exact onset kappa_c = 2k/pi of the kept-sector pole and its non-orthogonality K = 4 phi^2/sin^2(2 phi)
import numpy as np
from mpmath import mp, mpf, cot, atan, pi, sin
mp.dps = 30
def chain(N, kap, k=1.0):
    l = np.arange(N-1); c = (l+1)/np.sqrt((2*l+1)*(2*l+3))
    M = np.diag(c,1)+np.diag(c,-1)
    D = np.full(N, -kap); D[0] = 0.0
    return -1j*k*M + np.diag(D)
def least(N, kap):
    w, V = np.linalg.eig(chain(N, kap)); i = np.argmax(w.real); return w[i], V[:, i]
print('1) exact pole from I4: s = k cot(k/kappa) - kappa, kappa_c = 2k/pi =', float(2/pi))
for kap in [1.0, 2.0, 0.8]:
    phi = 1/mpf(kap); s = cot(phi) - kap
    g = atan(1/(s+kap)); print('  kappa=%.2f  s=%.12f  1-kappa*g=%.2e' % (kap, float(s), float(1-kap*g)))
print('2) chain eigenvalue vs exact pole and K vs 4phi^2/sin^2(2phi)')
for kap in [2.0, 1.0, 0.8, 0.7]:
    w, v = least(400, kap); phi = 1/kap
    Kc = (np.vdot(v, v).real)**2/abs(v @ v)**2; Ke = 4*phi**2/np.sin(2*phi)**2
    print('  kappa=%.2f  chain s=%.10f%+.1ej  exact s=%.10f  K chain=%.6f exact=%.6f' % (kap, w.real, w.imag, np.cos(phi)/np.sin(phi)-kap, Kc, Ke))
print('3) truncation onset (least-damped mode real) vs N')
def isreal(N, kap): w, _ = least(N, kap); return abs(w.imag) < 1e-9
for N in [50, 100, 200, 400, 800]:
    lo, hi = 0.55, 0.75
    for _ in range(40):
        m = 0.5*(lo+hi)
        if isreal(N, m): hi = m
        else: lo = m
    print('  N=%4d  onset kappa/k = %.5f   minus 2/pi = %+.5f' % (N, hi, hi-2/np.pi))
