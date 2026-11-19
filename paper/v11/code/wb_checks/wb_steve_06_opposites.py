# SCRIPT: WB-STEVE-06-OPPOSITES
# (i) T3 second half: the ladder inequalities on the multigroup rate spread must be STRICT (kill: equality within 1e-9 would mean
#     the multigroup model has no rate spread).  Reports the slack.
# (ii) Opposite run for D1: instead of the first maximum, read the linear central density contrast averaged over the window
#     between Steve's two decisive epochs, [1.7, 4.0] (fixed beforehand), G_win = (<D_pf>/<D_g> - 1)/(<D_pf>/<D_inst> - 1).
#     Kill (written before running): dies if max |G_win - G| >= 0.10.
import numpy as np
from scipy.special import roots_legendre
import wb_lin
edges = np.linspace(np.log(0.4), np.log(20), 7); xs = np.exp(0.5*(edges[1:]+edges[:-1]))
w = xs**4/(np.exp(xs)+1)*np.diff(edges); w /= w.sum()
cf = lambda x, c0, c1: c0+(c1-c0)*np.log(x/0.5)/np.log(20/0.5)
print('=== ladder slack on the multigroup rates (nu_mu,tau, e+- + nu-nu on the stress edge) ===')
for lab, r in [('nu_e e+- only', xs*cf(xs, .34, .47)), ('nu_mu,tau e+- only', xs*cf(xs, .073, .101)), ('nu_mu,tau e+- + nu-nu', xs*(cf(xs, .073, .101)+cf(xs, .49, .68)))]:
    S = {k: np.sum(w*r**k) for k in (-2, -1, 0, 2)}
    print('%-24s S0^2/(S-2 S2) = %.4f ; S-1^2/(S-2 S0) = %.4f ; rate spread max/min = %.1f' % (lab, S[0]**2/(S[-2]*S[2]), S[-1]**2/(S[-2]*S[0]), r.max()/r.min()))
flav = [(1/3, xs*cf(xs, .34, .47)), (2/3, xs*cf(xs, .073, .101))]
print('flavour-mixed e+- only: rates spread across the two flavours at the mean energy: %.1f' % (flav[0][1][3]/flav[1][1][3]))
Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw; zeta = np.exp(-ks**2/4)
eg = np.linspace(0.02, 6.0, 1200)
def centre(Rn, ed):
    acc = np.zeros_like(eg)
    for kk, w_, z_ in zip(ks, wk, zeta):
        D, _ = wb_lin.run_mode(kk, 0.02, eg, Rn, ed); acc += w_*kk**2*z_*D
    return -acc
pf = centre(0.0, None); inst = centre(0.409, None)
win = (eg >= 1.7) & (eg <= 4.0)
avg = lambda c: np.mean(c[win])
print('\n=== opposite run for D1: windowed linear density contrast over [1.7, 4.0] ===')
print('window averages: perfect fluid %.4f, instantaneous free streaming %.4f; sign of central contrast over window: min pf %.3f' % (avg(pf), avg(inst), pf[win].min()))
err = []
for ed in Gs:
    g = centre(0.409, ed); Gw = (avg(pf)/avg(g)-1)/(avg(pf)/avg(inst)-1); err.append(Gw-Gs[ed])
    print('eps_dec %4.2f : G_win = %.3f   Steve %.3f   err %+.3f' % (ed, Gw, Gs[ed], Gw-Gs[ed]))
print('max |err| = %.3f -> %s' % (np.max(np.abs(err)), 'DIES' if np.max(np.abs(err)) >= .10 else 'survives'))
