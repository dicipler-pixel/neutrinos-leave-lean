# SCRIPT: WB-STEVE-02-LINEAR
# Linear (Ma-Bertschinger, Newtonian gauge, radiation era, r_m = 1, conformal time tau = epsilon) Boltzmann solver for
# plasma + relaxing neutrinos, written from Steve's App. B equations and the textbook hierarchy, then used to test candidate
# predictors of his gradual-decoupling curve G(eps_dec).  Collision term: relaxation toward isotropy in the plasma frame at
# a_kappa = eps_dec^3/eps^4 (his kappa = H (eps_dec/eps)^3 with a H = 1/tau).
# KILL CONDITIONS (written before any run):
#  V1  solver validity (if this dies nothing below is trusted):  (a) superhorizon Delta ratio (neutrinos free from the start)
#      equals (15+6R)/(15+4R) = 1.049 (R=.409) to 0.003;  (b) single-mode first-max ratio 0.911 (R=.409) and 0.897 (R=.488) to 0.01;
#      (c) Gaussian-profile centre: first max of Delta at eps = 1.7 +-0.15 with factor 0.944 +-0.01.
#  D1  linear first-max diagnostic (baseline, open item (a)): G_lin = (1/r-1)/(1/r_inst-1), r = first max with free-streaming /
#      first max perfect fluid, Gaussian centre.  Dies if max_eps |G_lin - G| >= 0.10 over the six Table II points.
#  D2  paper's memory object: monopole survival A under the time-dependent relaxing operator L(kappa(eps)), readout at the epoch
#      Steve's own numbers give (first max 1.7; apparent horizon 4.0); g = (1-A)/(1-A_inst).  No fitted parameter.
#      Dies if max error >= 0.10 at BOTH epochs.
#  D3  paper's 'crossing' object: energy that has crossed from the kept sector (l=0,1) into the hidden sector (l>=2),
#      X = sum_{l>=2}|F_l|^2/(2l+1) integrated over the perturbation, g = X/X_inst at the same two epochs.  Dies the same way.
#  H1  half-point: the decoupling time at which G = 1/2 equals the first-max epoch within 10 percent.
#  Opposite runs: (i) fitted-epoch readouts (diagnostic only, never a pass); (ii) D2/D3 with the cut moved so the kept sector is
#  l=0,1 (flux kept) instead of l=0; (iii) k r_m = 2 versus the Gaussian-profile weighted average.
import numpy as np, sys, time
from scipy.special import roots_legendre
from wb_lin import run_mode, first_max, LMAX
Rn_default = 0.409

print('=== V1a/b single mode, neutrinos free from the start (k tau0 = 1e-2, rtol 1e-11) ===')
k = 1.0; tau0 = 1e-2; tg = np.linspace(tau0, 14, 2801)
for R in [0.409, 0.488]:
    D_pf, _ = run_mode(k, tau0, tg, 0.0, None, rtol=1e-11); D_fs, _ = run_mode(k, tau0, tg, R, None, rtol=1e-11)
    xs, mpf = first_max(tg, D_pf); xf, mfs = first_max(tg, D_fs)
    i = np.searchsorted(tg, 0.05)
    print('R=%.3f: first max at k tau = %.3f (pf) %.3f (fs); ratio of maxima %.4f ; implied threshold rise %.2f %% ; superhorizon Delta ratio at k tau=.05: %.4f (formula %.4f)' %
          (R, xs, xf, mfs/mpf, 100*(mpf/mfs-1), D_fs[i]/D_pf[i], (15+6*R)/(15+4*R)))

print('\n=== V1c Gaussian-profile centre, tau0 = 0.02, free streaming from tau0 ===')
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
zeta = np.exp(-ks**2/4)
eg = np.linspace(0.02, 6.0, 1200)
def centre(Rn, eps_dec):
    acc = np.zeros_like(eg); allY = []
    for kk, w_, z_ in zip(ks, wk, zeta):
        D, Y = run_mode(kk, 0.02, eg, Rn, eps_dec); acc += w_*kk**2*z_*D; allY.append(Y)
    return acc, allY
t_=time.time(); C_pf, Y_pf = centre(0.0, None); print('perfect-fluid centre done in %.0fs' % (time.time()-t_))
C_inst, Y_inst = centre(Rn_default, None)
e1, m1 = first_max(eg, C_pf); e2, m2 = first_max(eg, C_inst)
r_inst = m2/m1
print('centre first max: perfect fluid eps=%.3f, free-streaming eps=%.3f; ratio %.4f (Steve 0.944), implied rise %.2f %% (Steve 6-7 %%)' % (e1, e2, r_inst, 100*(1/r_inst-1)))
# lmax convergence for a typical mode
Dtest, _ = run_mode(3.0, 0.02, eg, Rn_default, None, lmax=48); Dtest2, _ = run_mode(3.0, 0.02, eg, Rn_default, None, lmax=80)
print('lmax 48 vs 80 at k=3: max relative difference %.1e' % (np.max(np.abs(Dtest-Dtest2))/np.max(np.abs(Dtest))))

Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
print('\n=== D1 baseline: first maximum of the centre density contrast, gradual decoupling ===')
G1 = {}; G1k = {}
Rr = {}
for ed in Gs:
    C_g, _ = centre(Rn_default, ed); eg_, mg = first_max(eg, C_g); r = mg/m1
    G1[ed] = (1/r-1)/(1/r_inst-1); Rr[ed] = (eg_, r)
    print('eps_dec %4.2f : first max at eps %.3f  ratio %.4f  G_lin = %.3f   Steve G = %.3f   err %+.3f' % (ed, eg_, r, G1[ed], Gs[ed], G1[ed]-Gs[ed]))
print('D1 max |error| = %.3f  -> %s' % (max(abs(G1[e]-Gs[e]) for e in Gs), 'DIES (>=0.10)' if max(abs(G1[e]-Gs[e]) for e in Gs) >= .10 else 'survives'))
np.save('wb_steve_02_state.npy', dict(G1=G1, Rr=Rr, r_inst=r_inst), allow_pickle=True)
