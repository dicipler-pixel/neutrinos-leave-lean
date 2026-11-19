# SCRIPT: OSL-STEVE-A-BOUND-ON-STREAMING
# Question: does the paper's Theorem 1 (tau_dot^2 <= 4 g S) apply to Steve's free-streaming generator H = k*mu acting on
# the isotropic angular state, with the cut = {l=0} versus {l>=1}? What rate does it set?
# Setup (exact, no fit): angular Hilbert space L2([-1,1], dmu/2), H = k mu, psi0 = isotropic (constant), P(t)=|psi><psi|,
# accessible block = the single mode psi0, so C(t) = |<psi0|psi(t)>|^2, tau = log((1-C)/C), g = Var_psi(H), S = 1/(C(1-C)).
# KILL CONDITIONS (written before the run):
# KA1 the bound is violated: max over t of tau_dot^2/(4 g S) > 1 + 1e-9  -> Theorem 1 fails in this setting.
# KA2 no saturation: the ratio at k t = 0.01 differs from 1 by more than 1e-3 -> 'equality case' not met by free streaming at short time.
# KA3 Delta H = k/sqrt(3) fails: |sqrt(g) - k/sqrt3| > 1e-10 -> the weight between is not c_s k.
# KA4 Anandan-Aharonov corollary arccos(sqrt C) <= sqrt(g) t fails anywhere before C reaches 0.
# Then (not a kill): how close is the bound to the true depopulation time of l=0 (C=1/2)?
import numpy as np
k = 1.0
mu, w = np.polynomial.legendre.leggauss(600); w = w / 2.0
H = k * mu
g = float(np.sum(w * H**2) - np.sum(w * H)**2)
print('g = Var(H) = %.15f ; k^2/3 = %.15f ; sqrt(g) = %.12f ; k/sqrt3 = %.12f' % (g, k**2 / 3, g**0.5, k / 3**0.5))
t = np.linspace(0.005, 3.0, 6000)  # k t up to 3 (< pi: C stays > 0)
a = np.array([np.sum(w * np.exp(-1j * H * tt)) for tt in t]); ad = np.array([np.sum(w * (-1j * H) * np.exp(-1j * H * tt)) for tt in t])
C = np.abs(a)**2; Cd = 2 * np.real(np.conj(a) * ad)
print('C vs sinc^2 (kt): max err %.2e' % np.max(np.abs(C - np.sinc(t / np.pi)**2)))
S = 1 / (C * (1 - C)); taud = -Cd / (C * (1 - C)); ratio = taud**2 / (4 * g * S)
print('KA1: max tau_dot^2/(4gS) = %.12f' % ratio.max())
for x in [0.01, 0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    i = np.argmin(abs(t - x)); print('   k t = %.2f  C = %.5f  tau = %+.4f  ratio = %.6f' % (t[i], C[i], np.log((1 - C[i]) / C[i]), ratio[i]))
i = np.argmin(abs(t - 0.01)); print('KA2: ratio at kt=0.01: %.6f (|1-ratio| = %.1e)' % (ratio[i], abs(1 - ratio[i])))
ang = np.arccos(np.sqrt(np.clip(C, 0, 1))); bound = np.sqrt(g) * t
print('KA4: min over t of (sqrt(g) t - arccos sqrt C) = %.3e (must be >= 0)' % np.min(bound - ang))
th = t[np.argmin(abs(C - 0.5))]
print('time for l=0 occupation to fall to 1/2: exact k t = %.4f ; Mandelstam-Tamm minimum = arccos(1/sqrt2)/(1/sqrt3) = %.4f ; ratio exact/bound = %.4f'
      % (th, (np.pi / 4) * 3**0.5, th / ((np.pi / 4) * 3**0.5)))
print('speeds: rms speed sqrt(<mu^2>) = %.5f (= plasma c_s = 1/sqrt3 = %.5f) ; front speed max|mu| = 1' % (np.sqrt(np.sum(w * mu**2)), 3**-0.5))
