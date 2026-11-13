# SCRIPT: NU-V7-FIG-ONSET  figure for the exact onset kappa_c = 2k/pi
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import importlib.util, sys, os
plt.rcParams.update({'font.size': 11, 'font.family': 'serif'})
def chain(N, kap):
    l = np.arange(N-1); c = (l+1)/np.sqrt((2*l+1)*(2*l+3))
    D = np.full(N, -kap); D[0] = 0.0
    return -1j*(np.diag(c,1)+np.diag(c,-1)) + np.diag(D)
kc = 2/np.pi
ka = np.linspace(kc+1e-4, 3.0, 600); s = 1/np.tan(1/ka) - ka
kd = np.array([0.66, 0.7, 0.8, 1.0, 1.3, 1.7, 2.2, 3.0])
sd = [max(np.linalg.eigvals(chain(400, x)), key=lambda z: z.real).real for x in kd]
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(ka, s, color='#1f4e79', lw=2, label='pole $k\\cot(k/\\kappa)-\\kappa$')
ax[0].plot(ka, -ka, '--', color='#a33', lw=1.2, label='branch-cut centre $-\\kappa$')
ax[0].plot(kd, sd, 'o', color='#e08a00', ms=6, label='400-moment chain')
ax[0].axvline(kc, color='0.4', lw=0.8, ls=':'); ax[0].text(kc+0.04, -0.95, '$2k/\\pi$', color='0.3')
ax[0].set_xlabel('$\\kappa/k$'); ax[0].set_ylabel('$s/k$'); ax[0].set_ylim(-3, 0.05); ax[0].legend(frameon=False, fontsize=9, loc='center right')
ph = np.linspace(0.01, np.pi/2-0.02, 500); K = 4*ph**2/np.sin(2*ph)**2
ax[1].semilogy(ph, K, color='#1f4e79', lw=2)
ax[1].axvline(np.pi/2, color='0.4', lw=0.8, ls=':'); ax[1].text(np.pi/2-0.3, 2e3, '$\\phi=\\pi/2$', color='0.3')
ax[1].set_xlabel('$\\phi=k/\\kappa$'); ax[1].set_ylabel('$K=4\\phi^2/\\sin^2 2\\phi$')
ax[1].text(0.05, 300, 'chain onset $\\kappa/k$:\n50: 0.665\n200: 0.645\n800: 0.639\nexact: $2/\\pi$ = 0.637', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(__file__), '../../figs/fig_v7_onset.png'), dpi=200)
