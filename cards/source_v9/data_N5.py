# SCRIPT: NU-ART-N5-DATA  the kept-sector mode of the neutrino gas, exact, as the collision rate falls to the wall 2k/pi
# Writes data_N5.js for card_N5.js. Units of k (k = 1). Every number on the card comes from here.
#
# The kept-sector eigenfunction of  s f + i k mu f + kappa (f - P f) = 0  is  f(mu) = 1/(s + kappa + i k mu)  (up to a constant),
# with s = k cot(k/kappa) - kappa (Romatschke 2016, Eq. 37), existing for kappa > 2k/pi. Write a = s + kappa = k cot(phi), phi = k/kappa.
# Closed forms used below, each checked numerically here:
#   Hermitian norm   N_H = int |f|^2 dmu = (2/(a k)) arctan(k/a) = 2 phi / (k^2 cot phi)
#   bilinear norm    N_B = int f^2 dmu   = 2/(a^2 + k^2)        = 2 sin^2(phi) / k^2
#   K = N_H^2/|N_B|^2 = 4 phi^2 / sin^2(2 phi);  normalised left-right overlap = 1/sqrt(K) = sin(2 phi)/(2 phi)
import json, numpy as np
from scipy.integrate import quad

k = 1.0
phis = np.concatenate([np.linspace(0.30, 1.45, 240), np.linspace(1.45, 1.5583, 120)[1:]])   # kappa/k from 3.33 down to 0.6418 (2/pi = 0.6366)
kap = k / phis
a = k / np.tan(phis)
s = a - kap
K = 4 * phis**2 / np.sin(2 * phis)**2
ov = np.sin(2 * phis) / (2 * phis)

# check the closed forms by direct quadrature at a few points
chk = []
for ph in (0.5, 1.0, 1.3, 1.5):
    aa = k / np.tan(ph)
    NH = quad(lambda m: 1 / (aa**2 + k**2 * m**2), -1, 1, limit=400)[0]
    NBr = quad(lambda m: ((aa**2 - k**2 * m**2) / (aa**2 + k**2 * m**2)**2), -1, 1, limit=400)[0]
    NBi = quad(lambda m: (-2 * aa * k * m / (aa**2 + k**2 * m**2)**2), -1, 1, limit=400)[0]
    Kq = NH**2 / (NBr**2 + NBi**2)
    chk.append(dict(phi=ph, K_quad=Kq, K_closed=4 * ph**2 / np.sin(2 * ph)**2))

# check the eigenfunction against the truncated moment chain (400 moments): rebuild f(mu) from the chain eigenvector
def chain(N, kp):
    l = np.arange(N - 1); c = (l + 1) / np.sqrt((2 * l + 1) * (2 * l + 3))
    M = np.diag(c, 1) + np.diag(c, -1); D = np.full(N, -kp); D[0] = 0.0
    return -1j * k * M + np.diag(D)
from numpy.polynomial import legendre as Lg
mus = np.linspace(-0.995, 0.995, 399)
fchk = []
for kp in (2.0, 1.0, 0.8):
    w, V = np.linalg.eig(chain(400, kp)); i = np.argmax(w.real); v = V[:, i]
    coef = np.array([v[l] * np.sqrt(2 * l + 1) for l in range(400)])      # orthonormal moments -> Legendre series
    fc = Lg.legval(mus, coef)
    ph = k / kp; aa = k / np.tan(ph); fe = 1 / (aa + 1j * k * mus)
    lam = (fc @ fe.conj()) / (fe @ fe.conj()); err = np.max(np.abs(fc - lam * fe)) / np.max(np.abs(lam * fe))
    fchk.append(dict(kappa=kp, s_chain=float(w[i].real), s_exact=float(aa - kp), max_rel_err=float(err)))

# profiles |f(mu)|^2 normalised to the Hermitian norm, and phase, on a mu grid, for the card's sphere and panel
mg = np.linspace(-1, 1, 401)
sel = np.unique(np.round(np.linspace(0, len(phis) - 1, 90)).astype(int))
prof = []
for j in sel:
    aa = a[j]; f = 1 / (aa + 1j * k * mg)
    prof.append(dict(i=int(j), mag=(np.abs(f) / np.abs(f).max()).round(6).tolist(), ph=np.angle(f).round(6).tolist(),
                     sharecentre=float(quad(lambda m: 1 / (aa**2 + k**2 * m**2), -0.1, 0.1)[0] / quad(lambda m: 1 / (aa**2 + k**2 * m**2), -1, 1)[0])))
out = dict(phi=phis.round(8).tolist(), kap=kap.round(8).tolist(), s=s.round(8).tolist(), a=a.round(8).tolist(), K=K.round(6).tolist(),
           ov=ov.round(8).tolist(), mu=mg.round(5).tolist(), prof=prof, chk=chk, fchk=fchk, wall=2 / np.pi,
           onset_chain={'50': 0.665, '200': 0.645, '800': 0.639})
open('data_N5.js', 'w').write('window.DATA_N5 = ' + json.dumps(out) + ';\n')
for c in chk: print('K quad vs closed', c)
for c in fchk: print('chain vs exact', c)
print('points', len(phis), 'kappa range', kap[0], kap[-1], 'K max', K[-1], 'overlap min', ov[-1], 'profiles', len(prof))
