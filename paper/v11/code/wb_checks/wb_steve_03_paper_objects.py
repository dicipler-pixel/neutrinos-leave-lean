# SCRIPT: WB-STEVE-03-PAPER-OBJECTS
# D2 (memory survival of the kept sector under the time-dependent relaxing operator) and D3 (energy that has crossed into the
# hidden sector) as predictors of Steve's G(eps_dec).  Kill conditions are those stated in WB-STEVE-02-LINEAR (D2, D3, H1 and
# opposite runs); restated:
#  D2  g = (1-A)/(1-A_inst), A = population of the kept sector l=0 at readout epoch eps* in {1.7, 4.0} (the two epochs Steve's
#      own numbers give), no fitted parameter.  Dies if max_eps |g - G| >= 0.10 at BOTH epochs.
#  D3  g = X/X_inst, X = sum_{l>=2} |F_l|^2/(2l+1) summed over the Gaussian perturbation (weights k^2 zeta^2), same epochs, same kill.
#  Opposite runs: kept sector = l in {0,1} (flux kept), and k r_m fixed at 2 instead of the profile average.
#  Fitted-epoch scan is diagnostic only (a fitted epoch is not a pass).
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
import wb_lin
Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
wE = wk*ks**2*np.exp(-ks**2/2)          # energy weights k^2 zeta(k)^2 of the Gaussian perturbation
wE /= wE.sum()
LM = 60; a = lambda l: l/np.sqrt(4.0*l*l-1)
M = np.zeros((LM+1, LM+1))
for l in range(1, LM+1): M[l, l-1] = M[l-1, l] = a(l)
tau0 = 0.02; eg = np.linspace(tau0, 6.0, 1200)

def survival(k, ed, keep):
    """population of kept sector (keep=1: l=0; keep=2: l=0,1) vs tau, under dv/dtau = -(i k M + Kc (1-P)) v, v(tau0)=|0>."""
    n = LM+1; P = np.zeros(n); P[:keep] = 1
    def rhs(t, v):
        K = 0.0 if ed is None else ed**3/t**4
        x, y = v[:n], v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M @ y), -K*(1-P)*y-k*(M @ x)])
    v0 = np.zeros(2*n); v0[0] = 1
    sol = solve_ivp(rhs, (tau0, eg[-1]), v0, method='BDF', t_eval=eg, rtol=1e-9, atol=1e-12)
    pop = sol.y[:keep]**2+sol.y[n:n+keep]**2
    return np.sum(pop, axis=0)

def avg_surv(ed, keep, single=None):
    if single is not None: return survival(single, ed, keep)
    out = np.zeros_like(eg)
    for kk, w_ in zip(ks, wE): out += w_*survival(kk, ed, keep)
    return out

res = {}
for keep, tag in [(1, 'kept=l0'), (2, 'kept=l0,1')]:
    for single, stag in [(None, 'profile-averaged'), (2.0, 'k r_m=2')]:
        Ai = avg_surv(None, keep, single); curves = {}
        for ed in Gs:
            A = avg_surv(ed, keep, single); curves[ed] = (1-A)/(1-Ai)
        res[(tag, stag)] = curves
        for es in [1.7, 4.0]:
            i = np.searchsorted(eg, es); err = {ed: curves[ed][i]-Gs[ed] for ed in Gs}
            print('D2 %-10s %-17s eps*=%.1f : g = %s  max|err| = %.3f' % (tag, stag, es, np.round([curves[ed][i] for ed in Gs], 3), max(abs(v) for v in err.values())))
        # fitted-epoch scan (diagnostic only)
        best = min(((max(abs(curves[ed][i]-Gs[ed]) for ed in Gs), eg[i]) for i in range(40, len(eg), 5)))
        print('   fitted-epoch scan (diagnostic only): best eps* = %.2f with max|err| = %.3f' % (best[1], best[0]))
print('Steve G :', [Gs[e] for e in Gs])

# D3 from the full linear solver
def hidden_energy(ed, Rn=0.409):
    X = np.zeros_like(eg)
    for kk, w_ in zip(ks, wE):
        _, Y = wb_lin.run_mode(kk, tau0, eg, Rn, ed)
        F = Y[4:]; ls = np.arange(2, 2+F.shape[0])
        X += w_*np.sum(F**2/(2*ls[:, None]+1), axis=0)
    return X
Xi = hidden_energy(None); D3 = {}
for ed in Gs:
    D3[ed] = hidden_energy(ed)/Xi
for es in [1.7, 4.0]:
    i = np.searchsorted(eg, es); print('D3 eps*=%.1f : g = %s  max|err| = %.3f' % (es, np.round([D3[ed][i] for ed in Gs], 3), max(abs(D3[ed][i]-Gs[ed]) for ed in Gs)))
best = min(((max(abs(D3[ed][i]-Gs[ed]) for ed in Gs), eg[i]) for i in range(40, len(eg), 5)))
print('D3 fitted-epoch scan (diagnostic only): best eps* = %.2f with max|err| = %.3f' % (best[1], best[0]))
