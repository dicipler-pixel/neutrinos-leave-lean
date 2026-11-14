# SCRIPT: WB-STEVE-05-MIXTURE
# Exploratory (NOT a pass criterion): two-epoch readout of the memory-survival object D2.  Kill conditions written before the run:
#  M1  g_w(eps_dec) = w g(1.7) + (1-w) g(4.0) with ONE fitted weight w; any fitted quantity is graded [fit], never [derived].
#      It is only worth reporting if the one-parameter fit has max error < 0.05 on the six Table II points; it dies otherwise.
#  M2  If it survives, it must also predict out-of-sample: its curve must be monotone decreasing in eps_dec, and predict the
#      Table II values at the OTHER profile weighting (k r_m = 2) within 0.10 using the same w (cross-weighting test).
#  H1  half-point: eps_dec at which G=1/2 (log-odds interpolation of Table II) equals the first-max epoch of the centre
#      density (1.714 from WB-STEVE-02) within 10 percent.
#  H2  exceptional-point criterion: if the 'decision epoch' were the crossing of the two-moment exceptional point,
#      eps_EP = (eps_dec^3/(k r_m 2/sqrt3))^(1/4) (k r_m = 2) would equal the first-max epoch at the half point.  Dies if the
#      implied half-point differs from the measured one by more than 25 percent.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
from scipy.optimize import minimize_scalar
Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
wE = wk*ks**2*np.exp(-ks**2/2); wE /= wE.sum()
LM = 60; M = np.zeros((LM+1, LM+1))
for l in range(1, LM+1): M[l, l-1] = M[l-1, l] = l/np.sqrt(4.0*l*l-1)
tau0 = 0.02; eg = np.linspace(tau0, 6.0, 1200); n = LM+1; P = np.zeros(n); P[0] = 1
def surv(k, ed):
    def rhs(t, v):
        K = 0.0 if ed is None else ed**3/t**4
        x, y = v[:n], v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M @ y), -K*(1-P)*y-k*(M @ x)])
    v0 = np.zeros(2*n); v0[0] = 1
    sol = solve_ivp(rhs, (tau0, eg[-1]), v0, method='BDF', t_eval=eg, rtol=1e-9, atol=1e-12)
    return sol.y[0]**2+sol.y[n]**2
def curves(single):
    f = (lambda ed: surv(single, ed)) if single else (lambda ed: sum(w_*surv(kk, ed) for kk, w_ in zip(ks, wE)))
    Ai = f(None); eds = list(Gs)+[0.75, 1.5, 3.0, 6.0, 12.0]
    return {ed: (1-f(ed))/(1-Ai) for ed in eds}
i17, i40 = np.searchsorted(eg, 1.7), np.searchsorted(eg, 4.0)
out = {}
for single, tag in [(None, 'profile-averaged'), (2.0, 'k r_m=2')]:
    out[tag] = curves(single)
def mix(c, w, ed): return w*c[ed][i17]+(1-w)*c[ed][i40]
cp = out['profile-averaged']
fit = minimize_scalar(lambda w: max(abs(mix(cp, w, ed)-Gs[ed]) for ed in Gs), bounds=(0, 1), method='bounded')
w = fit.x
print('M1 fitted weight on the first-max epoch: w = %.3f ; max error on the six Table II points = %.3f' % (w, fit.fun))
print('   eps_dec  Steve G   mixture   error')
for ed in Gs: print('   %5.2f    %.3f     %.3f    %+.3f' % (ed, Gs[ed], mix(cp, w, ed), mix(cp, w, ed)-Gs[ed]))
ck = out['k r_m=2']
print('M2 cross-weighting (k r_m = 2, same w): max error %.3f' % max(abs(mix(ck, w, ed)-Gs[ed]) for ed in Gs))
print('   out-of-sample predictions (profile-averaged, same w) for Steve to test:')
for ed in [0.75, 1.5, 3.0, 6.0, 12.0]: print('   eps_dec = %5.2f : G_pred = %.3f  (shift of delta_c would be %.2f %%, of C_l %.2f %% for Rnu=.409 Gaussian)' %
                                          (ed, mix(cp, w, ed), 6.15*mix(cp, w, ed), 9.64*mix(cp, w, ed)))
print('   same w, k r_m=2 weighting (band): ' + ', '.join('%.2f->%.3f' % (ed, mix(ck, w, ed)) for ed in [0.75, 1.5, 3.0, 6.0, 12.0]))
mono = all(mix(cp, w, a) > mix(cp, w, b) for a, b in zip([0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8], [0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12]))
print('   monotone decreasing: %s' % mono)
# H1 / H2
eds = np.array(list(Gs)); G = np.array([Gs[e] for e in eds]); lo = np.log(G/(1-G))
x = np.interp(0.0, -lo, np.log(eds)); print('\nH1 half-point eps_dec(G=1/2) = %.3f ; first-max epoch 1.714 ; relative difference %.1f %%' % (np.exp(x), 100*(np.exp(x)/1.714-1)))
kr = 2.0; epEP = lambda ed: (ed**3/(kr*2/np.sqrt(3)))**0.25
ed_half_implied = (1.714**4*kr*2/np.sqrt(3))**(1/3)
print('H2 EP-crossing epoch at the measured half-point: %.3f (first max 1.714). Decoupling time that would put the EP crossing at the first max: %.3f vs measured %.3f -> %.0f %% off' %
      (epEP(np.exp(x)), ed_half_implied, np.exp(x), 100*(ed_half_implied/np.exp(x)-1)))
print('(the earlier note eps_EP = 0.658 eps_dec^1.5 is not reproduced: kappa/k = eps_dec^3/(k r_m eps^4) gives exponent 0.75: eps_EP = %.3f eps_dec^0.75)' % ((1/(kr*2/np.sqrt(3)))**0.25))
