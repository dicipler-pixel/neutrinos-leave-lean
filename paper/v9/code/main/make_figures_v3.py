# SCRIPT: PBH-NU-FIGURES-V3
# Figures 4, 5, 6 for the PBH-NU paper. Uses only the numbers and data files listed below.
# Writes fig4_tests.png, fig5_killlines.png, fig6_door.png into figs/. Never touches fig1-fig3.
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import os
BASE = os.environ.get('NU_WORK', '.')  # working directory of the runs (set NU_WORK)
PAPER = BASE + '/paper'
MEM = PAPER + '/code/main/memory_curve.json'
WIT = BASE + '/next/witness/witness_prod.json'
OUT = PAPER + '/figs/'
PROTECTED = {'fig1_G.png', 'fig2_chain.png', 'fig3_clock.png'}

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 9.5,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Okabe-Ito based colour-blind-safe palette
BLUE = '#0072B2'
ORANGE = '#E69F00'
BLACK = '#000000'
GREY = '#7a7a7a'
BAND = '#d6e6f3'


def save(fig, name, **kw):
    assert name not in PROTECTED, 'refusing to touch an existing figure'
    path = OUT + name
    fig.savefig(path, dpi=300, facecolor='white', **kw)
    plt.close(fig)
    print('wrote', path)


# ---------- data ----------
mc = json.load(open(MEM))


def memory_curve(n):
    pts = []
    for key, val in mc.items():
        nn, ee = key.split('_')
        if int(nn) == n:
            pts.append((float(ee), val['two_epoch']))
    return sorted(pts)


c3 = memory_curve(3)
c6 = memory_curve(6)

# McCormick measured n=3 (history-blind rule)
mc_e = [0.25, 0.5, 1, 2, 4, 8]
mc_G = [0.959, 0.867, 0.683, 0.431, 0.190, 0.063]

# New measured n=6 runs (C, B, D)
new6_e = [1, 2, 3]
new6_G = [0.648, 0.317, 0.154]
new6_err = [0.006, 0.004, 0.006]
new6_lab = ['C', 'B', 'D']

# Broad profile alpha=0.3, n=3
broad_e = [4, 8]
broad_G = [0.181, 0.045]

# ---------- FIG 4 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.6))

ax.plot(mc_e, mc_G, linestyle='--', color=GREY, lw=0.9, zorder=1,
        label='history-blind rule (uses the n=3 curve for any history)')
ax.plot(mc_e, mc_G, 'o', color=BLACK, ms=5.5, zorder=3,
        label='McCormick, n=3 (measured)')

ax.plot([p[0] for p in c3], [p[1] for p in c3], '-', color=BLUE, lw=1.8, zorder=2,
        label='memory model, n=3 (fitted, one weight)')
ax.plot([p[0] for p in c6], [p[1] for p in c6], '-', color=ORANGE, lw=1.8, zorder=2,
        label='memory model, n=6 (frozen, predicted before the runs)')

ax.errorbar(new6_e, new6_G, yerr=new6_err, fmt='D', color=ORANGE, mec=ORANGE,
            ms=6, capsize=3, elinewidth=1.0, zorder=4,
            label="McCormick's code, n=6 (new runs)")
for x, y, lab in zip(new6_e, new6_G, new6_lab):
    ax.annotate(lab, (x, y), xytext=(7, -9), textcoords='offset points',
                fontsize=9, fontweight='bold', color=BLACK)

ax.plot(broad_e, broad_G, 's', mfc='none', mec=BLACK, mew=1.2, ms=6.5, zorder=4,
        label='broad profile, n=3 (new runs)')

ax.set_xscale('log')
ax.set_xlim(0.2, 10)
ax.set_ylim(0, 1)
ticks = [0.2, 0.5, 1, 2, 5, 10]
ax.set_xticks(ticks)
ax.set_xticklabels(['0.2', '0.5', '1', '2', '5', '10'])
ax.minorticks_off()
ax.set_xlabel(r'decoupling time  $\varepsilon_{\mathrm{dec}}$')
ax.set_ylabel(r'share of the neutrino effect kept, $G$')
ax.legend(loc='upper right', frameon=False, handlelength=2.4)
fig.tight_layout()
save(fig, 'fig4_tests.png')

# ---------- FIG 5 ----------
rows = [
    # label, measured, meas_err, memory, history_blind, annotation
    ('Test B  (n=6, $\\varepsilon_{\\mathrm{dec}}$=2)', 0.317, 0.004, 0.246, 0.431,
     'memory off 0.071 · history-blind off 0.114'),
    ('Test C  (n=6, $\\varepsilon_{\\mathrm{dec}}$=1)', 0.648, 0.006, 0.6625, 0.683,
     'memory off 0.014 · history-blind off 0.035'),
    ('Test D  (n=6, $\\varepsilon_{\\mathrm{dec}}$=3)', 0.154, 0.006, 0.1176, 0.30,
     'memory off 0.037 · history-blind off 0.146 (dies)'),
]
KILL = 0.08

fig, ax = plt.subplots(figsize=(10.5, 3.8))
fig.subplots_adjust(left=0.24, right=0.6, bottom=0.3, top=0.95)
half_h = 0.26
for k, (lab, meas, merr, mem, hb, note) in enumerate(rows):
    y = 2 - k
    ax.fill_betweenx([y - half_h, y + half_h], meas - KILL, meas + KILL,
                     color=BAND, lw=0, zorder=1)
    ax.errorbar([meas], [y], xerr=[merr], fmt='D', color=BLACK, ms=6.5,
                capsize=3, elinewidth=1.0, zorder=5)
    ax.plot([mem], [y], marker='|', color=ORANGE, ms=17, mew=3, ls='none', zorder=4)
    ax.plot([hb], [y], 'o', mfc='none', mec=GREY, mew=1.8, ms=9, ls='none', zorder=4)
    ax.text(1.03, y, note, transform=ax.get_yaxis_transform(),
            va='center', ha='left', fontsize=9, color=BLACK)

ax.set_xlim(0, 0.8)
ax.set_ylim(-0.6, 2.6)
ax.set_yticks([2, 1, 0])
ax.set_yticklabels([r[0] for r in rows], fontsize=9)
ax.set_xlabel('G')
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)

handles = [
    Patch(facecolor=BAND, edgecolor='none', label='kill band: ±0.08 around the measurement'),
    Line2D([], [], marker='D', color=BLACK, ls='none', ms=6, label='measured (bar = stated uncertainty)'),
    Line2D([], [], marker='|', color=ORANGE, ls='none', ms=12, mew=3, label='memory-model prediction'),
    Line2D([], [], marker='o', mfc='none', mec=GREY, mew=1.8, ls='none', ms=8,
           label='history-blind prediction'),
]
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.4, -0.2), ncol=2,
          frameon=False)
save(fig, 'fig5_killlines.png')

# ---------- FIG 6 ----------
wit = json.load(open(WIT))
RATIOS = [0.1, 0.25, 0.5, 1, 2]
LS = [1, 2, 3, 4]
FLOOR = -32.0


def height_grid(n):
    H = np.zeros((len(LS), len(RATIOS)))
    for rec in wit:
        if rec['n'] != n:
            continue
        i = int(np.argmin([abs(rec['ratio'] - r) for r in RATIOS]))
        j = LS.index(rec['L'])
        R = rec['res']['4.0']['R_ret']
        H[j, i] = max(np.log10(max(R, 1e-40)) - FLOOR, 0.0)
    return H


H = {3: height_grid(3), 6: height_grid(6)}
hmax = max(H[3].max(), H[6].max())
ZTOP = max(34.0, np.ceil(hmax) + 2)
norm = Normalize(vmin=0, vmax=ZTOP)
cmap = plt.cm.viridis
WALL_LOG = -3.0
WALL_H = WALL_LOG - FLOOR

fig = plt.figure(figsize=(11.5, 5.4))
axes = []
for k, n in enumerate([3, 6]):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d')
    axes.append(ax)
    Hn = H[n]
    xs, ys, zs, dxs, dys, dzs, cols = [], [], [], [], [], [], []
    for j, L in enumerate(LS):
        for i in range(len(RATIOS)):
            h = Hn[j, i]
            xs.append(i - 0.3)
            ys.append(L - 0.3)
            zs.append(0.0)
            dxs.append(0.6)
            dys.append(0.6)
            dzs.append(h)
            cols.append(cmap(norm(h)))
    ax.bar3d(xs, ys, zs, dxs, dys, dzs, color=cols, shade=True, alpha=1.0,
             edgecolor='none')

    # translucent "witness on" plane at log10 R = -3
    gx, gy = np.meshgrid([-0.6, len(RATIOS) - 0.4], [0.5, 4.5])
    gz = np.full_like(gx, WALL_H, dtype=float)
    ax.plot_surface(gx, gy, gz, color='#555555', alpha=0.22, shade=False,
                    linewidth=0, zorder=0)

    ax.set_xticks(range(len(RATIOS)))
    ax.set_xticklabels(['0.1', '0.25', '0.5', '1', '2'], fontsize=8)
    ax.set_yticks(LS)
    ax.set_yticklabels([str(L) for L in LS], fontsize=8)
    ax.set_zlim(0, ZTOP)
    ax.set_zticks([2, 12, 22, 32])
    ax.set_zticklabels(['−30', '−20', '−10', '0'], fontsize=8)
    ax.set_xlabel('plant time / decoupling time', fontsize=9, labelpad=6)
    ax.set_ylabel('moment that holds the difference, $l$', fontsize=9, labelpad=6)
    ax.set_zlabel(r'$\log_{10} R_{\mathrm{ret}}$', fontsize=9, labelpad=4)
    ax.view_init(elev=28, azim=-32)
    ax.text2D(0.04, 0.9, 'n = %d' % n, transform=ax.transAxes, fontsize=10,
              fontweight='bold', color=BLACK)
    ax.set_box_aspect((1.3, 1.0, 0.95))

fig.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.97, wspace=0.28)
save(fig, 'fig6_door.png', bbox_inches='tight', pad_inches=0.15)
