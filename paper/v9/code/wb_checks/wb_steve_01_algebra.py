# SCRIPT: WB-STEVE-01-ALGEBRA
# Tests T0-T4 mapping "The Weight Between" v1.1 onto McCormick's free-streaming PBH preprint (algebraic part).
# KILL CONDITIONS (written before any run):
#  T0  Steve-internal consistency (so the targets are trustworthy). Table II: recompute Delta C_l,c/C_l,c from the delta_c
#      columns through Eq.(15) delta = C - 3C^2/8; dies (flag only) if any row differs from the printed value by > 0.3 pt.
#      Also recompute G = shift/shift_inst for the gradual rows (flag if any differs from the brief's G by > 0.005).
#  T1  Prop 5 / Def 4 on Steve's operator L = -i k mu - kappa (I-P), P = projector on l=0 (orthonormal Legendre basis).
#      H = k mu, E_B = ||P H (1-P)||_F^2 must equal k^2/3 = (1/2)||[H,P]||_F^2 = Var_{|0>}(H) to 1e-12 relative. Dies otherwise.
#      Connection-energy identity (scalar form, H' = -L = D + iK, D=diag(kappa_l), K = k mu):
#      (1/4)||[H',H'^dag]||^2 = ||[D,K]||^2 = S_2. Dies if off by > 1e-10 relative.
#  T2  Hidden-walk (Schur) formula of the paper: G_B(z) = [z - E - W (z-F)^{-1} W^dag]^{-1} with E=0, W the l=0->l>=1 block,
#      F the hidden block of L, must equal the closed form G(z) = g(s)/(1 - kappa g(s)), g(s)=arctan(k/s)/k, s=z+kappa,
#      to 1e-8 relative at 50 random complex z (Re s>0). Dies otherwise.
#      Two-level EP: eigenvalues of [[0,-i k/sqrt3],[-i k/sqrt3,-kappa]] coalesce at kappa = 2 k/sqrt3 = 2 sqrt(E_B). Dies otherwise.
#  T3  Ladder on Steve's single-rate model: all gaps equal kappa, so S_0^2 = S_-2 S_2 and S_-1^2 = S_-2 S_0 must be EQUALITIES
#      (1e-12). Dies otherwise.  For the energy-dependent (multigroup) rates the same inequalities must be strict.
#  T4  Which rung is the effective single rate of a spread of rates?  Pre-registered claim (to be killed if wrong): the paper's
#      ladder says the effective rate is a power mean of the group rates, M_p, p in {-2,-1,0,+1,+2}. PASS only if ONE rung p
#      reproduces BOTH of Steve's calibrated decoupling temperatures, e+- only: 1.6 MeV and with nu-nu: 0.93-1.0 MeV,
#      each within 15 percent, using only the rate numbers printed in his Appendix C. Opposite run: every other p tried.
import numpy as np
from scipy.special import erfc
from scipy.optimize import brentq
rng = np.random.default_rng(3010)
fro2 = lambda X: float(np.real(np.vdot(X, X)))

print('=== T0 Steve-internal consistency ===')
dc_f = 0.49773
rows = [('inst eps0=0.1 Rnu=.409', 0.52832, 9.6), ('dec 0.25', 0.52709, 9.2), ('dec 0.5', 0.52428, 8.3), ('dec 1', 0.51865, 6.5),
        ('dec 2', 0.51092, 4.0), ('dec 4', 0.50354, 1.8), ('dec 8', 0.49967, 0.6),
        ('Rnu=.10', 0.50547, 2.3), ('Rnu=.20', 0.51297, 4.7), ('Rnu=.30', 0.52027, 7.0), ('Rnu=.488', 0.53379, 11.5),
        ('alpha .3', 0.47747, 9.3), ('alpha .5', 0.49682, 9.4), ('alpha 2', 0.56342, 9.9), ('alpha 4', 0.59734, 10.0)]
Cl = lambda d: (4/3)*(1-np.sqrt(1-1.5*d))
fl = {'alpha .3': 0.44805, 'alpha .5': 0.46687, 'alpha 2': 0.53274, 'alpha 4': 0.56819}
for nm, dn, printed in rows:
    df = fl.get(nm, dc_f); s = 100*(Cl(dn)/Cl(df)-1)
    print('%-24s Delta C_l,c = %5.2f %%  printed %5.1f  diff %+5.2f %s' % (nm, s, printed, s-printed, 'FLAG' if abs(s-printed) > 0.3 else ''))
sh = {0.25: 5.90, 0.5: 5.33, 1: 4.20, 2: 2.65, 4: 1.17, 8: 0.39}; inst = 6.15
Gbr = {0.25: .959, .5: .867, 1: .683, 2: .431, 4: .190, 8: .063}
G = {e: (v)/inst for e, v in sh.items()}
# use the delta_c columns directly (more digits than the percent column)
dcs = {0.25: 0.52709, .5: 0.52428, 1: 0.51865, 2: 0.51092, 4: 0.50354, 8: 0.49967}
G = {e: (dcs[e]-dc_f)/(0.52832-dc_f) for e in dcs}
for e in G: print('eps_dec %5.2f  G(from delta_c) = %.3f   brief %.3f   diff %+.3f %s' % (e, G[e], Gbr[e], G[e]-Gbr[e], 'FLAG' if abs(G[e]-Gbr[e]) > .005 else ''))
Rv = np.array([.1, .2, .3, .409, .488]); dC = np.array([2.3, 4.7, 7.0, 9.6, 11.5]); dd = np.array([1.56, 3.06, 4.53, 6.15, 7.24])
print('shift/R_nu  C_l: ', np.round(dC/Rv, 2), ' spread %.1f %%' % (100*np.std(dC/Rv)/np.mean(dC/Rv)))
print('shift/R_nu  delta_c: ', np.round(dd/Rv, 2), ' spread %.1f %%' % (100*np.std(dd/Rv)/np.mean(dd/Rv)))
# Table III slopes and ratios
x = np.array([1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]); pf = np.array([.679, .497, .390, .288, .215, .151, .105]); fs = np.array([.799, .590, .470, .343, .255, .178, .123])
print('Table III ratios', np.round(fs/pf, 3), ' slopes', np.polyfit(np.log(x), np.log(pf), 1)[0].round(3), np.polyfit(np.log(x), np.log(fs), 1)[0].round(3))
# beta^1.18 rule: Gaussian C_l, erfc(C/(sqrt2 sigma))
for b in [1e-9, 1e-12, 1e-15]:
    sig = 0.662/np.sqrt(2)/brentq(lambda y: np.log(erfc(y))-np.log(b), 0.5, 10)
    bn = erfc(0.726/(np.sqrt(2)*sig)); print('beta_pf %.0e -> beta_nu/beta_pf = %.4f (Steve: 0.021/0.0052/0.0013), exponent %.3f' % (b, bn/b, np.log(bn)/np.log(b)))
print('coincidence list for the 1.19 mass ratio: (1-Rnu)^(-1/3) = %.4f ; (delta_c ratio)^3 = %.4f ; (C_l ratio)^2 = %.4f ; Table III 1.17-1.20' %
      ((1-.409)**(-1/3), (0.52832/0.49773)**3, (Cl(0.52832)/Cl(0.49773))**2))
print('Rnu-dependence of a power law (1-Rnu)^-x needed for the C_l shift: x = %.3f at .409, %.3f at .488, %.3f at .1 (not constant -> rejected)' %
      tuple(np.log(Cl(d)/Cl(dc_f))/(-np.log(1-r)) for d, r in [(0.52832, .409), (0.53379, .488), (0.50547, .1)]))

print('\n=== T1 Prop 5 / connection energy on Steve operator ===')
lmax = 80; a = lambda l: l/np.sqrt(4.0*l*l-1)
M = np.zeros((lmax+1, lmax+1))
for l in range(1, lmax+1): M[l, l-1] = M[l-1, l] = a(l)
k, kap = 1.7, 0.9
P = np.zeros_like(M); P[0, 0] = 1; I = np.eye(lmax+1)
H = k*M
EB = fro2(P @ H @ (I-P)); comm = 0.5*fro2(H @ P - P @ H); var = (H @ H)[0, 0]-(H)[0, 0]**2
print('E_B = %.15f  k^2/3 = %.15f  (1/2)||[H,P]||^2 = %.15f  Var_0(H) = %.15f' % (EB, k*k/3, comm, var))
assert abs(EB/(k*k/3)-1) < 1e-12 and abs(comm/EB-1) < 1e-12 and abs(var/EB-1) < 1e-12
Dg = np.diag([0.0]+[kap]*lmax); Hp = Dg+1j*H
lhs = 0.25*fro2(Hp @ Hp.conj().T-Hp.conj().T @ Hp); rhs = fro2(Dg @ H-H @ Dg)
print('(1/4)||[H,H^dag]||^2 = %.12f   ||[D,K]||^2 = %.12f   kappa^2 k^2 * 2/3 = %.12f' % (lhs, rhs, kap**2*k*k*2/3))
assert abs(lhs/rhs-1) < 1e-10
print('T1 PASS: sqrt(E_B)/k = %.6f = c_s = 1/sqrt3 (= <mu^2>^(1/2), the radiation sound speed)' % (np.sqrt(EB)/k))

print('\n=== T2 hidden-walk (Schur) formula vs arctan closed form ===')
lm = 600; Mb = np.zeros((lm+1, lm+1))
for l in range(1, lm+1): Mb[l, l-1] = Mb[l-1, l] = a(l)
Lm = -1j*k*Mb-kap*(np.eye(lm+1)-np.diag([1.0]+[0]*lm))
W = Lm[0:1, 1:]; F = Lm[1:, 1:]; Wd = Lm[1:, 0:1]
worst = 0
for _ in range(50):
    z = complex(rng.uniform(0.2, 2), rng.uniform(-3, 3))
    GB = 1/(z-0-(W @ np.linalg.solve(z*np.eye(lm)-F, Wd))[0, 0])      # paper formula with E=0
    s = z+kap; g = np.arctan(k/s)/k; Gc = g/(1-kap*g)
    full = np.linalg.inv(z*np.eye(lm+1)-Lm)[0, 0]
    worst = max(worst, abs(GB-Gc)/abs(Gc), abs(full-Gc)/abs(Gc))
print('worst relative difference (Schur vs closed form vs full inverse): %.2e' % worst); assert worst < 1e-8
for kp in [0.5, 2*k/np.sqrt(3)-1e-3, 2*k/np.sqrt(3), 2*k/np.sqrt(3)+1e-3, 3.0]:
    ev = np.linalg.eigvals(np.array([[0, -1j*k/np.sqrt(3)], [-1j*k/np.sqrt(3), -kp]]))
    print('  kappa = %.4f  two-level eigenvalue separation %.2e' % (kp, abs(ev[0]-ev[1])))
print('T2 PASS. EP at kappa = 2 sqrt(E_B) = %.4f' % (2*np.sqrt(EB)))

print('\n=== T3 ladder on the single-rate model ===')
Kc = k*M; gaps = np.zeros((lmax+1, lmax+1)); gaps[0, 1:] = kap; gaps[1:, 0] = kap   # only the cut edge has a gap kappa; hidden-hidden gaps are 0
def Sk(kk, gp):
    m = (np.abs(Kc) > 0) & (gp > 0); return float(np.sum(np.abs(Kc[m])**2*gp[m]**kk))
S = {kk: Sk(kk, gaps) for kk in [-2, -1, 0, 1, 2]}
print('S_k:', {kk: round(v, 6) for kk, v in S.items()})
print('equality checks: S0^2/(S-2 S2) = %.12f ; S-1^2/(S-2 S0) = %.12f' % (S[0]**2/(S[-2]*S[2]), S[-1]**2/(S[-2]*S[0])))
assert abs(S[0]**2/(S[-2]*S[2])-1) < 1e-12 and abs(S[-1]**2/(S[-2]*S[0])-1) < 1e-12
print('rung +1 for this model: S_1 = E_B*2*kappa (counting both orderings) = %.6f' % S[1])

print('\n=== T4 which rung is the effective rate? (Steve Appendix C numbers only) ===')
# Gamma = c G_F^2 T^4 E.  Calibrate with the unblocked E=T coefficients: 0.506 -> 1.9 MeV (nu_e), 0.108 -> 3.1 MeV (nu_mu,tau) : T_dec = 1.9 (0.506/C)^(1/3)
def Tdec(C): return 1.9*(0.506/C)**(1/3)
print('sanity: C=0.108 -> %.2f MeV (Steve 3.1)' % Tdec(0.108))
# energy groups: six groups x=0.4..20, edges uniform in ln x (Steve App. C), energy weight x^4/(e^x+1) dlnx, c(x) interpolated linearly in ln x between his endpoints
edges = np.linspace(np.log(0.4), np.log(20), 7); xs = np.exp(0.5*(edges[1:]+edges[:-1]))
w = xs**4/(np.exp(xs)+1)*np.diff(edges); w /= w.sum()
def cfun(x, c0, c1): return c0+(c1-c0)*np.log(x/0.5)/np.log(20/0.5)
flav = {'nu_e': dict(wt=1/3, ee=(0.34, 0.47)), 'nu_mutau': dict(wt=2/3, ee=(0.073, 0.101))}
cnn = (0.49, 0.68)
def rates(fl, withnn):
    r = xs*cfun(xs, *flav[fl]['ee']);
    if withnn: r = r+xs*cfun(xs, *cnn)       # anisotropy (l>=2) damped by e+- plus nu-nu
    return r
def pmean(r, wt, p):
    if p == 0: return np.exp(np.sum(wt*np.log(r)))
    return np.sum(wt*r**p)**(1/p)
print('group energy weights', np.round(w, 3))
print('model check: single-group at x=3.15 (e+- only) T_dec: nu_e %.2f MeV (Steve 1.3), nu_mutau %.2f MeV (Steve 2.3)' %
      (Tdec(3.15*cfun(3.15, *flav['nu_e']['ee'])), Tdec(3.15*cfun(3.15, *flav['nu_mutau']['ee']))))
res = {}
for withnn in [False, True]:
    for p in [-2, -1, 0, 1, 2]:
        # level 1: power mean over energy groups within a flavour; level 2: same-p mean over flavours (flavour weights 1/3, 2/3)
        Cf = [pmean(rates(f, withnn), w, p) for f in flav]; wf = np.array([flav[f]['wt'] for f in flav])
        Ceff = pmean(np.array(Cf), wf, p); res[(withnn, p)] = Tdec(Ceff)
for p in [-2, -1, 0, 1, 2]:
    t1, t2 = res[(False, p)], res[(True, p)]
    ok = abs(t1/1.6-1) < .15 and (0.93*0.85 <= t2 <= 1.0*1.15)
    print('rung p=%+d : T_dec(e+- only) = %.2f MeV (target 1.6)   T_dec(with nu-nu) = %.2f MeV (target 0.93-1.0)   both within 15%%: %s' % (p, t1, t2, ok))
print('ratio of masses (T^-2) e+- only -> with nu-nu, rung +1: %.2f, rung -1: %.2f (Steve: 2.5-3)' % ((res[(False, 1)]/res[(True, 1)])**2, (res[(False, -1)]/res[(True, -1)])**2))
