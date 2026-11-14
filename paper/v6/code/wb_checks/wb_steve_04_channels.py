# SCRIPT: WB-STEVE-04-CHANNELS
# (i) Non-normality channels of a collision operator with different rates per multipole (Steve open item (c)), via the paper's
#     connection-energy identity.  (ii) Item (e): neutrinos as a self-interacting fluid that exchanges NO momentum with the plasma.
# KILL CONDITIONS (written before the run):
#  C1  For L = -i k mu - diag(kappa_l), S_2 = ||[D,K]||^2 = (1/4)||[H',H'^dag]||^2 splits over Legendre edges l<->l+1 as
#      sum_l 2 k^2 a_{l+1}^2 (kappa_l - kappa_{l+1})^2, a_l^2 = l^2/(4l^2-1).  Dies if off by > 1e-10 relative.
#      Consequence (derived): the relaxation-time model (all kappa_l equal for l>=1) puts ALL non-normality on edge 0-1; any
#      model with kappa_1 != kappa_2 puts weight on edge 1-2.
#  E1  Two perfect fluids with equal sound speed and no momentum exchange are one fluid: in pure radiation (p = e/3) the shift of
#      the first maximum must vanish as the neutrino self-interaction rate K0 = kappa/H -> infinity.  Prediction from the paper's
#      rung -1 (viscosity weight of the 1-2 edge, S_-1 = (4/15) k^2/kappa): the shift times K0 tends to a constant.
#      Dies if (a) shift does not decrease monotonically with K0, or (b) shift*K0 differs by more than 15 percent between
#      K0 = 100 and K0 = 1000.  Opposite run: the same operator with the drag rate on (flux relaxed to the plasma) instead.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
fro2 = lambda X: float(np.real(np.vdot(X, X)))
lmax = 60; a2 = lambda l: l*l/(4.0*l*l-1)
M = np.zeros((lmax+1, lmax+1))
for l in range(1, lmax+1): M[l, l-1] = M[l-1, l] = np.sqrt(a2(l))
print('=== C1 non-normality channels ===')
k = 1.3
for name, kap in [('relaxation time (all l>=1 equal) kappa_e=1', [0]+[1.0]*lmax),
                  ('nu_e: flux damped by e+- (1), stress by e+- + nu-nu (1+1.5)', [0, 1.0]+[2.5]*(lmax-1)),
                  ('nu_mu,tau: flux (1), stress (1+7)', [0, 1.0]+[8.0]*(lmax-1))]:
    D = np.diag(kap); Hp = D+1j*k*M
    S2 = fro2(D @ (k*M)-(k*M) @ D); chk = 0.25*fro2(Hp @ Hp.conj().T-Hp.conj().T @ Hp)
    edges = [2*k*k*a2(l+1)*(kap[l]-kap[l+1])**2 for l in range(0, 6)]
    tot = sum(2*k*k*a2(l+1)*(kap[l]-kap[l+1])**2 for l in range(0, lmax))
    print('%-62s S_2 = %.6f (commutator form %.6f, edge sum %.6f)' % (name, S2, chk, tot))
    assert abs(S2/chk-1) < 1e-10 and abs(S2/tot-1) < 1e-10
    print('    edge energies 0-1, 1-2, 2-3, 3-4: %s ; share on edge 1-2: %.1f %%' % (np.round(edges[:4], 4), 100*edges[1]/tot))
wt = np.array([1/3, 2/3]); e12 = np.array([2.25*(4/15), 49*(4/15)]); e01 = np.array([1/3, 1/3])
print('flavour-weighted ratio (stress edge)/(flux edge) in units of kappa_e^2 k^2 : %.2f' % (np.sum(wt*e12)/np.sum(wt*e01)))
print('E_B for the cut P0 (plasma-coupled monopole): k^2/3 ; for the cut P01 (flux kept, i.e. nu as own fluid): 4 k^2/15 ; ratio %.4f' % ((4/15)/(1/3)))
E_B01 = fro2(np.diag([1, 1]+[0]*(lmax-1)) @ (k*M) @ np.diag([0, 0]+[1]*(lmax-1)))
print('numerical E_B(P01) = %.10f ; 4k^2/15 = %.10f' % (E_B01, 4*k*k/15))

print('\n=== E1 self-interacting neutrinos with no momentum exchange, pure radiation (first-max shift of Delta) ===')
LM = 40
def run(k, Rn, K0, drag, tau0=0.02, tg=None):
    n = 4+(LM-1); LS = np.arange(3, LM+1)
    def rhs(t, y):
        dg, tg_, dn, tn = y[:4]; F = np.zeros(LM+2); F[2:LM+1] = y[4:]; F[LM+1] = (2*LM+1)/(k*t)*F[LM]-F[LM-1]
        th = (1-Rn)*tg_+Rn*tn; de = (1-Rn)*dg+Rn*dn; sg = F[2]/2; Dl = de+4*th/(k*k*t)
        phi = -1.5*Dl/(k*t)**2; psi = phi-6*Rn*sg/(k*t)**2; dphi = -psi/t+2*th/(k*k*t*t)
        K = K0/t; dy = np.empty_like(y)               # a*kappa = K0 * (a H) = K0 / tau
        Kd = K if drag else 0.0
        dy[0] = -4/3*tg_+4*dphi
        dy[1] = k*k*dg/4+k*k*psi-Kd*(Rn/(1-Rn))*(tg_-tn)
        dy[2] = -4/3*tn+4*dphi
        dy[3] = k*k*(dn/4-sg)+k*k*psi+Kd*(tg_-tn)
        dy[4] = 8/15*tn-0.6*k*F[3]-K*F[2]
        dy[5:] = k/(2*LS+1)*(LS*F[2:LM]-(LS+1)*F[4:LM+2])-K*F[3:LM+1]
        return dy
    psi0 = 2/3; d0 = -2*psi0-(2/3)*(k*tau0)**2*psi0; t0 = 0.5*k*k*tau0*psi0
    y0 = np.zeros(n); y0[:4] = [d0, t0, d0, t0]
    sol = solve_ivp(rhs, (tau0, tg[-1]), y0, method='BDF', t_eval=tg, rtol=1e-10, atol=1e-13)
    Y = sol.y; th = (1-Rn)*Y[1]+Rn*Y[3]; de = (1-Rn)*Y[0]+Rn*Y[2]
    return de+4*th/(k*k*tg)
def fmax(x, y):
    s = -y
    for i in range(1, len(s)-1):
        if s[i] > s[i-1] and s[i] >= s[i+1]:
            A, B, C = s[i-1], s[i], s[i+1]; off = 0.5*(A-C)/(A-2*B+C); return B-0.25*(A-C)*off
tg = np.linspace(0.02, 8.0, 3000); kk = 1.0
m_pf = fmax(tg, run(kk, 0.0, 0.0, False, tg=tg))
for drag, tag in [(False, 'self-interaction only (no momentum exchange with plasma)'), (True, 'drag on the plasma included (Steve relaxation model)')]:
    print(tag)
    prev = None; vals = {}
    for K0 in [3, 10, 30, 100, 300, 1000, 3000]:
        r = fmax(tg, run(kk, 0.409, K0, drag, tg=tg))/m_pf; vals[K0] = 1/r-1
        print('   K0 = %5d : first-max ratio %.5f ; implied threshold rise %.4f %% ; rise*K0 = %.3f' % (K0, r, 100*vals[K0], 100*vals[K0]*K0))
    if not drag:
        mono = all(vals[a] > vals[b] for a, b in zip([3, 10, 30, 100, 300, 1000], [10, 30, 100, 300, 1000, 3000]))
        const = abs(vals[1000]*1000/(vals[100]*100)-1)
        print('   E1 (a) monotone decrease: %s ; (b) rise*K0 changes by %.1f %% between K0=100 and 1000 -> %s' % (mono, 100*const, 'PASS' if mono and const < .15 else 'DIES'))
