# SCRIPT: NU-V6-FIGS  figures 8-10 for v6; every number is copied from the printed outputs named beside it
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = __file__.rsplit('/', 1)[0] + '/figs/'
INK, MUT, RUST, TEAL, GOLD, VIOL = '#1d1a16', '#8a8478', '#b5451b', '#0f7fa8', '#c8900a', '#5b3fa8'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'savefig.dpi': 200})

# ---- Fig 8: the door in the full collapse (A4_restart/PREREGISTERED.txt, trisection results; widths = full bracket widths)
base = 0.5107500   # f = 0 restart at eps_s = 2
pairs = {  # eps_s: (dplus, dminus, wplus, wminus)
 ('l3', 0.5): (0.5107685, 0.5107510, 1.85e-5, 8.2e-6),
 ('l3', 2.0): (0.5125833, 0.5088395, 1.85e-5, 1.65e-5),
 ('l3', 4.0): (0.5108796, 0.5106358, 1.85e-5, 1.23e-5),
 ('l4', 0.5): (0.5107685, 0.5107500, 1.85e-5, 1.85e-5),
 ('l4', 2.0): (0.5096749, 0.5117726, 8.2e-6, 1.03e-5),
 ('l4', 4.0): (0.5106759, 0.5108241, 1.85e-5, 1.85e-5),
 ('d', 2.0): (0.5134352, 0.5079300, 1.85e-5, 8.2e-6)}
dK = 1.65e-4  # drift allowance, Nmu 32 -> 48 on the (2, l3) pair
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.7))
ax = axs[0]
for key, col, mk, off, lab in [('l3', TEAL, 'o', -0.06, r'$\ell=3$'), ('l4', RUST, 's', 0.06, r'$\ell=4$'), ('d', VIOL, 'D', 0.0, 'readout-Gramian direction')]:
    xs, ys = [], []
    for (k, es), (p, m, wp, wm) in pairs.items():
        if k != key: continue
        diff = p - m; err = 0.5 * (wp + wm) + 2 * dK
        ax.errorbar(es + off, diff * 1e3, yerr=err * 1e3, fmt=mk, color=col, ms=6, capsize=3, label=lab if es == 2.0 else None)
        xs.append(es); ys.append(diff)
ax.axhline(0, color=MUT, lw=0.8); ax.axvspan(1.6, 2.4, color=GOLD, alpha=0.12)
ax.set_xticks([0.5, 2, 4]); ax.set_xticklabels(['0.5\ncoupled', '2\ndecoupling', '4\nfree streaming'])
ax.set_xlabel(r'restart surface $\epsilon_s$ where the hidden structure is planted'); ax.set_ylabel(r'$\delta_c(+f)-\delta_c(-f)$  [$10^{-3}$]')
ax.set_title('Same density, flux and stress; different hidden angular structure', fontsize=9.5); ax.legend(frameon=False, fontsize=8)
ax.text(2.45, 4.6, 'error bars: bracket + drift allowance', fontsize=7.5, color=MUT)
ax = axs[1]
labs = [r'$+p_3$', r'$-p_3$', r'$+p_4$', r'$-p_4$', '+d', '-d']
vals = [0.5125833, 0.5088395, 0.5096749, 0.5117726, 0.5134352, 0.5079300]
cols = [TEAL, TEAL, RUST, RUST, VIOL, VIOL]
ax.barh(range(6), [(v - base) * 1e3 for v in vals], color=cols, height=0.6)
ax.axvline(0, color=INK, lw=0.8); ax.set_yticks(range(6)); ax.set_yticklabels(labs); ax.invert_yaxis()
ax.set_xlabel(r'threshold shift from the unperturbed restart, $\epsilon_s=2$  [$10^{-3}$]')
ax.set_title('Odd structure raises the threshold, even lowers it', fontsize=9.5)
fig.tight_layout(); fig.savefig(D + 'fig8_door_nonlinear.png'); plt.close(fig)

# ---- Fig 9: self-scattering in McCormick's physical model (A2_selfscatter/REPORT.md, A2b_decisive/PREREGISTERED.txt)
fig, ax = plt.subplots(figsize=(9.6, 3.2))
rows = [('perfect fluid (his Table VII)', 0.49742, 0, MUT), ('with self-scattering (his run)', 0.519406, 0.000156, INK),
        ('r = 1: same isotropy history, no flux-shear split', 0.51972, 0.00009, TEAL), ('without self-scattering (his run)', 0.526391, 0.000109, INK),
        ('instantaneous free streaming (this paper)', 0.533125, 0.00012, MUT)]
for i, (l, v, e, c) in enumerate(rows):
    ax.errorbar(v, i, xerr=e, fmt='o', color=c, ms=6, capsize=3)
ax.set_yticks(range(5)); ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
ax.vlines(0.5194, 1.6, 2.4, color=GOLD, lw=2); ax.vlines(0.5204, 1.6, 2.4, color=RUST, lw=2)
ax.annotate('timing reading 0.5194', (0.5194, 2.4), (0.5056, 2.9), fontsize=7.5, color=GOLD, arrowprops=dict(arrowstyle='-', color=GOLD, lw=0.6))
ax.annotate('frozen link law 0.5204', (0.5204, 1.6), (0.5225, 1.25), fontsize=7.5, color=RUST, arrowprops=dict(arrowstyle='-', color=RUST, lw=0.6))
ax.invert_yaxis(); ax.set_xlabel(r'$\delta_c$ at $T_H=1$ MeV, McCormick multigroup model'); ax.set_xlim(0.495, 0.536)
ax.set_title('Self-scattering lowers the threshold mostly through timing; the flux-shear split carries +0.0003', fontsize=9.5)
fig.tight_layout(); fig.savefig(D + 'fig9_selfscatter.png'); plt.close(fig)

# ---- Fig 10: which hidden directions the future reads (A5_kinetic/REPORT.md)
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.5))
ax = axs[0]
ep = {'coupled\n(s=0.5)': [1.1e-7, 9e-12, 1e-15], 'decoupling\n(s=2)': [0.367, 0.148, 0.040], 'free\n(s=3)': [0.147, 0.024, 0.0016]}
for j, (k, v) in enumerate(ep.items()):
    for i, x in enumerate(v): ax.scatter([j + (i - 1) * 0.15], [x], color=[TEAL, RUST, MUT][i], s=30, zorder=3)
ax.set_yscale('log'); ax.set_xticks(range(3)); ax.set_xticklabels(list(ep)); ax.set_ylabel('readout Gramian eigenvalues')
ax.set_title(r'History $n=3,\ \epsilon_{\rm dec}=2$: top three directions' + '\n(blue odd, l=3-led; red even, l=4-led)', fontsize=9)
ax = axs[1]
pairs = ['R1', 'R2', 'R3', 'R4', 'R5\n(r=4)', 'R6\n(r=1/4)']; fw = [0.705, 0.705, 0.662, 0.411, 0.712, 0.700]; rv = [0.641, 0.598, 0.544, 0.572, 0.649, 0.633]
x = np.arange(6); ax.bar(x - 0.18, fw, 0.36, color=TEAL, label='rate falling (forward)'); ax.bar(x + 0.18, rv, 0.36, color=GOLD, label='same opacity, reversed order')
ax.set_xticks(x); ax.set_xticklabels(pairs, fontsize=8); ax.set_ylabel(r'memory form $g_2$'); ax.set_ylim(0, 0.95); ax.legend(frameon=False, fontsize=8, loc='upper left', ncol=2)
ax.set_title('Equal optical depth and equal connection energy,\ndifferent order: the memory form tells them apart', fontsize=9)
fig.tight_layout(); fig.savefig(D + 'fig10_gramian_order.png'); plt.close(fig)
print('ok')
