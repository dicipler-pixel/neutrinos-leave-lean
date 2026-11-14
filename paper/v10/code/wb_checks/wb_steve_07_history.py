# SCRIPT: WB-STEVE-07-HISTORY
# Discriminating prediction for the next step.  Table II interpolation cannot predict a DIFFERENT collision history, the
# two-epoch memory-survival form can.  kappa = H (eps_dec/eps)^n  with n = 2 and 6 (Steve used n = 3), eps_dec = 1 and 2.
# KILL CONDITION (before the run): the test is only worth asking Steve for if the predicted G for n = 2 or n = 6 differs from the
# n = 3 value by at least 0.10 at some eps_dec; otherwise the memory form is insensitive to history and the step is dropped.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
wE = wk*ks**2*np.exp(-ks**2/2); wE /= wE.sum()
LM = 60; M = np.zeros((LM+1, LM+1))
for l in range(1, LM+1): M[l, l-1] = M[l-1, l] = l/np.sqrt(4.0*l*l-1)
tau0 = 0.02; eg = np.linspace(tau0, 6.0, 1200); n = LM+1; P = np.zeros(n); P[0] = 1
def surv(k, ed, p):
    def rhs(t, v):
        K = 0.0 if ed is None else ed**p/t**(p+1)       # a*kappa = (1/tau)(eps_dec/tau)^p
        x, y = v[:n], v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M @ y), -K*(1-P)*y-k*(M @ x)])
    v0 = np.zeros(2*n); v0[0] = 1
    sol = solve_ivp(rhs, (tau0, eg[-1]), v0, method='BDF', t_eval=eg, rtol=1e-9, atol=1e-12)
    return sol.y[0]**2+sol.y[n]**2
f = lambda ed, p: sum(w_*surv(kk, ed, p) for kk, w_ in zip(ks, wE))
i17, i40 = np.searchsorted(eg, 1.7), np.searchsorted(eg, 4.0); w = 0.890
Ai = f(None, 3)
res = {}
for p in [2, 3, 6]:
    for ed in [1.0, 2.0]:
        g = (1-f(ed, p))/(1-Ai); res[(p, ed)] = w*g[i17]+(1-w)*g[i40]
        print('n = %d, eps_dec = %.0f : G_pred(two-epoch, w = 0.89) = %.3f  (n=3 Table II value %.3f)' % (p, ed, res[(p, ed)], {1.0: 0.684, 2.0: 0.431}[ed]))
dmax = max(abs(res[(p, ed)]-res[(3, ed)]) for p in [2, 6] for ed in [1.0, 2.0])
print('largest change from n=3: %.3f -> %s' % (dmax, 'discriminating' if dmax >= 0.10 else 'DROPPED (insensitive)'))
