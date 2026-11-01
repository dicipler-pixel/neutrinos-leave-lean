# SCRIPT: OSL-STEVE-D-G-CURVE-TESTS
# Target: Steve's Table II gradual-decoupling curve G(eps_dec) = shift/shift_inst. Data: delta_c shifts 5.90,5.33,4.20,2.65,1.17,0.39 %
# over 6.15 % at eps_dec = 0.25,0.5,1,2,4,8 ; (Cl,c shifts 9.2,8.3,6.5,4.0,1.8,0.6 over 9.6).
# Paper link: the balance map (m-p)/(m+p) = tanh(log(m/p)/2): an occupation nu <-> log-odds tau = log((1-nu)/nu). Is G a log-odds-linear
# function of ln(eps_dec)? (observation on Steve's table; the paper never claims it).
# Parameter-free candidates built from the paper's rate scale 2*sqrt(E_B) = 2 k /sqrt3 (Check A, B) and Steve's own epochs:
#   M1: G = 1/(1+rho), rho = kappa(eps*)/(2 sqrt(E_B)) with k = 2/r_m, eps* in {1.7 (first max), 4.0, 4.25, 4.5 (apparent horizons)}
#   M2: G = exp(-N), N = number of momentum exchanges after eps*: (2/3)(eps_dec/eps*)^3   (generic optical-depth null model, not from the paper)
#   M3: G = 1/(1+rho^q) with q = 1/sqrt3.
# KILL CONDITIONS (written before the run): a candidate PASSES only if max |G_model - G_Steve| <= 0.10 with no fitted parameter.
# Logit-linearity is tested by the 2-parameter fit's max error (<= 0.03 = 'adequate'), reported as an OBSERVATION, not a prediction;
# the slope is tested against sqrt3 and 3/2 by refitting only the intercept (1-parameter, flagged as such).
import numpy as np
ed = np.array([0.25, 0.5, 1, 2, 4, 8.0])
sh = np.array([5.90, 5.33, 4.20, 2.65, 1.17, 0.39]) / 6.15; shC = np.array([9.2, 8.3, 6.5, 4.0, 1.8, 0.6]) / 9.6
print('G (delta_c) =', np.round(sh, 3), ' G (Cl,c) =', np.round(shC, 3))
lg = np.log((1 - sh) / sh); x = np.log(ed)
A = np.vstack([x, np.ones_like(x)]).T; (s, a), *_ = np.linalg.lstsq(A, lg, rcond=None)
Gfit = 1 / (1 + np.exp(s * x + a)); print('log-odds tau_G = %.3f ln(eps_dec) %+.3f ; eps_half = exp(-a/s) = %.3f ; max |G_fit-G| = %.4f' % (s, a, np.exp(-a / s), abs(Gfit - sh).max()))
print('   residuals of tau_G:', np.round(lg - (s * x + a), 3), '  slope per e-fold of kappa (kappa ~ eps_dec^3): %.3f' % (s / 3))
for sv, nm in [(3**0.5, 'sqrt3'), (1.5, '3/2'), (5 / 3, '5/3'), (2.0, '2')]:
    ai = np.mean(lg - sv * x); Gm = 1 / (1 + np.exp(sv * x + ai)); print('   slope fixed to %-5s (%.3f): intercept refit %.3f, max err %.4f' % (nm, sv, ai, abs(Gm - sh).max()))
print('\nparameter-free candidates (k = 2/r_m, eps = tau_conformal/r_m, so kappa_conf/(2 sqrt E_B) = eps_dec^3 / (eps^4 * 2*2/sqrt3)):')
def rho(edv, es): return edv**3 / (es**4 * 2 * 2 / 3**0.5)
res = []
for es in [1.7, 4.0, 4.25, 4.5]:
    r = rho(ed, es)
    m1 = 1 / (1 + r); m2 = np.exp(-(2 / 3) * (ed / es)**3); m3 = 1 / (1 + r**(3**-0.5))
    for nm, m in [('M1 1/(1+rho)', m1), ('M2 exp(-N)', m2), ('M3 rho^(1/sqrt3)', m3)]:
        e = abs(m - sh).max(); res.append((e, nm, es)); print('  eps*=%.2f %-18s G = %s  max err %.3f  %s' % (es, nm, np.round(m, 3), e, 'PASS' if e <= 0.10 else 'FAIL'))
print('best parameter-free candidate: max err %.3f (%s, eps*=%.2f)' % min(res))
# opposite: invert the key -- use 2 sqrt(E_B)/kappa as 'free fraction' would be increasing in eps_dec (wrong sign by construction); instead test the
# complementary reading 1-G against rho (coupled fraction = 1/(1+1/rho)): identical to M1 by symmetry of the logistic -> reported, no new content.
print('\nEP crossing epoch re-derived: kappa_conf = (1/(eps r_m)) (eps_dec/eps)^3 = 2k/sqrt3, k=2/r_m  ->  eps_EP = (eps_dec^3 / (4/sqrt3 * 1)... ) check:')
for e_ in [0.25, 1, 2, 4, 8]:
    epep = (e_**3 / (4 / 3**0.5))**0.25; print('   eps_dec = %-4g eps_EP = %.3f' % (e_, epep))
