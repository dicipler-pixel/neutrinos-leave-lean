# SCRIPT: OSL-STEVE-D2-ONE-PARAMETER-SCAN
# FOLLOW-UP to D (flagged: ONE free parameter eps*, so a pass here is a fit, not a prediction). Model M3: G = 1/(1+rho^q),
# rho = eps_dec^3 / (eps*^4 * 4/sqrt3), q = 1/sqrt3 or q = 5/9. Question: is the best eps* an epoch Steve's paper already names?
# KILL: if best-fit eps* is outside [1.5, 4.6] (first-max epoch 1.7 .. last apparent-horizon epoch 4.5) the model has no physical anchor.
import numpy as np
ed = np.array([0.25, 0.5, 1, 2, 4, 8.0]); G = np.array([5.90, 5.33, 4.20, 2.65, 1.17, 0.39]) / 6.15
for q, nm in [(3**-0.5, '1/sqrt3'), (5 / 9, '5/9'), (1.0, '1')]:
    best = min(((abs(1 / (1 + (ed**3 / (es**4 * 4 / 3**0.5))**q) - G).max(), es) for es in np.linspace(0.5, 6, 5501)))
    print('q = %-8s best eps* = %.3f with max err %.4f ; anchored (1.5..4.6)? %s' % (nm, best[1], best[0], 'yes' if 1.5 <= best[1] <= 4.6 else 'NO'))
