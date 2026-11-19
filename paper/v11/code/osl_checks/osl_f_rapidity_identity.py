# SCRIPT: OSL-STEVE-F-RAPIDITY-IDENTITY
# Structural identity only (no Steve number is claimed): for a two-stream intensity with forward weight p and backward weight 1-p the flux-to-energy ratio is
# r = q/e = 2p-1 = tanh(tau/2) with tau = log(p/(1-p)) (the paper's balance map). KILL: any |r - tanh(tau/2)| > 1e-12, or the positivity edge of the
# first-order dipole target (e + 3 q mu)/4pi >= 0 at mu=-1, i.e. r <= 1/3, failing to equal tau = ln 2.
import numpy as np
p = np.random.default_rng(1).uniform(0.01, 0.99, 100000); tau = np.log(p / (1 - p)); r = 2 * p - 1
print('max |r - tanh(tau/2)| = %.2e' % np.abs(r - np.tanh(tau / 2)).max())
print('r = 1/3 (Steve App. C positivity edge) <-> tau = %.6f = ln 2 = %.6f ; r = 0.031, 0.26, 0.8 (his quoted fluxes) <-> tau = %.3f, %.3f, %.3f' % (2 * np.arctanh(1 / 3), np.log(2), *[2 * np.arctanh(x) for x in (0.031, 0.26, 0.8)]))
