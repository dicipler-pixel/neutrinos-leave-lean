# SCRIPT: WEIGHT-BETWEEN-FIGURES-01
# Builds every figure of "The Weight Between" (v1 of the one paper) from computed data. Each figure carries an argument;
# none is a text box. Output: PNG at 300 dpi in ../figs (raster, so the PDF carries no figure fonts).
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Wedge
from scipy.signal import hilbert
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figs')
INK, INK2, MUTED, GRID = '#0b0b0b', '#52514e', '#8a8984', '#e4e3df'
BLUE, ORANGE, AQUA, VIOLET = '#2a78d6', '#eb6834', '#1baf7a', '#6250d6'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'lines.linewidth': 2,
                     'savefig.dpi': 300, 'savefig.bbox': 'tight', 'mathtext.fontset': 'dejavuserif'})
def save(fig, name): fig.savefig(os.path.join(OUT, name)); plt.close(fig); print('wrote', name)

# ---------------- Figure 1: the one split (hero) ----------------
fig, ax = plt.subplots(figsize=(7.6, 3.8)); ax.set_axis_off(); ax.set_xlim(-0.2, 10.4); ax.set_ylim(-0.7, 5); ax.set_aspect('equal')
# left: a reading as rate x direction
ax.add_patch(Circle((2.2, 2.5), 1.6, fill=False, ec=MUTED, lw=1.2, ls=(0, (3, 3))))
th = np.radians(38)
ax.add_patch(FancyArrowPatch((2.2, 2.5), (2.2 + 1.6 * np.cos(th), 2.5 + 1.6 * np.sin(th)), arrowstyle='-|>', mutation_scale=16, color=BLUE, lw=2.2))
off = 0.22 * np.array([-np.sin(th), np.cos(th)])
ax.add_patch(FancyArrowPatch((2.2 + off[0], 2.5 + off[1]), (2.2 + 2.4 * np.cos(th) + off[0], 2.5 + 2.4 * np.sin(th) + off[1]), arrowstyle='-|>', mutation_scale=16, color=ORANGE, lw=1.6))
ax.text(2.2, -0.45, 'every reading = rate × direction', ha='center', color=INK, fontsize=10.5)
ax.text(0.15, 4.95, 'rate (how much, how fast): the length.\nBrightness, loudness, energy,\na clock\'s ticking', color=ORANGE, fontsize=8.4, va='top')
ax.text(2.2, 0.72, 'direction (which way): the point on the sphere.\nColour, timbre, the kept sector', color=BLUE, fontsize=8.4, va='top', ha='center')
# right: kept sector and the weight between

ax.add_patch(Circle((7.25, 2.5), 0.85, fc='#dbe8f8', ec=BLUE, lw=1.6)); ax.text(7.25, 2.5, 'kept\n$P$', ha='center', va='center', color=INK, fontsize=10)
ax.add_patch(Circle((8.85, 2.5), 0.62, fc='#fbe2d8', ec=ORANGE, lw=1.6)); ax.text(8.85, 2.5, 'hidden\n$1-P$', ha='center', va='center', color=INK, fontsize=8.6)
ax.add_patch(FancyArrowPatch((8.08, 2.78), (8.25, 2.78), arrowstyle='<|-|>', mutation_scale=10, color=INK, lw=1.4))
ax.text(8.0, 4.55, r'the weight between:  $E_B=\Vert PH(1-P)\Vert_F^2$', ha='center', color=INK, fontsize=10)
ax.text(7.9, -0.3, 'every motion of what is kept\nis a crossing, and is priced by $E_B$', ha='center', color=INK2, fontsize=8.8)
save(fig, 'fig1_split.png')

# ---------------- Figure 2: the gap-power ladder, computed ----------------
rng = np.random.default_rng(6)
n = 7; d = np.sort(rng.uniform(0, 6, n)); K = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); K = (K + K.conj().T) / 2
np.fill_diagonal(K, 0); Dg = d[:, None] - d[None, :]; mask = ~np.eye(n, dtype=bool)
S = lambda k: float(np.sum(np.abs(K[mask])**2 * np.abs(Dg[mask])**k))
ks = np.linspace(-2.5, 2.5, 201); logS = [np.log(S(k)) for k in ks]
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(ks, logS, color=BLUE)
for k, lab in [(-2, 'memory geometry\n(projector metric)'), (-1, 'light\n(static response)'), (0, 'time\n(energy variance)'), (2, 'connection\n(non-normality)')]:
    ax.plot([k], [np.log(S(k))], 'o', ms=8, color=ORANGE, mec='white', mew=1.5, zorder=3)
    ax.annotate(lab, (k, np.log(S(k))), xytext=(0, 14) if k != 0 else (0, 16), textcoords='offset points', ha='center', fontsize=8.3, color=INK)
ax.plot([1], [np.log(S(1))], 'o', ms=8, mfc='white', mec=MUTED, mew=1.5, zorder=3)
ax.annotate('rung +1\nopen', (1, np.log(S(1))), xytext=(0, 14), textcoords='offset points', ha='center', fontsize=8.3, color=MUTED)
ax.set_xlabel('gap power $k$'); ax.set_ylabel(r'$\log S_k,\ \ S_k=\sum |K_{ij}|^2|\Delta_{ij}|^k$')
ax.set_title('One weight, read at different powers of the gap (log-convex: $S_0^2\\leq S_{-2}S_2$)', fontsize=9.5, color=INK)
save(fig, 'fig2_ladder.png')

# ---------------- Figure 3: colour picks its leader; the tie ----------------
a = np.array([43.33, 32.76, 1.0])
def chroma(x): p = a * x; return p / p.sum()
def dist(x, y): return 4 * np.arcsin(np.linalg.norm(np.sqrt(chroma(x)) - np.sqrt(chroma(y))) / 2)
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.1))
for gap, col in [(0.5, BLUE), (0.1, ORANGE), (0.01, AQUA)]:
    M = np.diag([0.9, 0.9 * (1 - gap), 0.5]); x = np.array([0.3, 1.0, 1.0]); ds = []
    for nn in range(400): x = M @ x; x /= x.sum(); ds.append(dist(x, np.array([1.0, 1e-300, 1e-300])))
    axs[0].semilogy(np.arange(1, 401), ds, color=col, label='gap %.2f' % gap)
axs[0].set_xlabel('passes (bounces, layers)'); axs[0].set_ylabel('distance to the leader colour'); axs[0].legend(frameon=False, fontsize=8)
axs[0].set_title('Colour settles on the leader at the gap', fontsize=9.5, color=INK)
M = np.diag([0.9, 0.9, 0.5])
for start, col in [((1, 0.2, 1.0), BLUE), ((0.2, 1, 1.0), ORANGE), ((1, 1, 1.0), AQUA)]:
    x = np.array(start, float); P = []
    for nn in range(60): x = M @ x; x /= x.sum(); P.append(chroma(x))
    P = np.array(P); axs[1].plot(np.arange(1, 61), P[:, 0], color=col)
axs[1].set_ylim(0, 1); axs[1].set_xlabel('passes'); axs[1].set_ylabel('share of channel 1')
axs[1].set_title('At a tie the start decides', fontsize=9.5, color=INK)
fig.tight_layout(); save(fig, 'fig3_leader.png')

# ---------------- Figure 4: the sound that survives ----------------
A = np.array([1.0, 0.6, 0.35, 0.2]); g = np.array([3.0, 1.2, 0.8, 0.5]); t = np.linspace(0, 8, 400)
X = (A**2)[None, :] * np.exp(-2 * np.outer(t, g)); P = X / X.sum(1, keepdims=True)
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.1))
cols = [VIOLET, ORANGE, AQUA, BLUE]
axs[0].stackplot(t, P.T, colors=cols, edgecolor='white', linewidth=0.6)
for k, (yy, lab) in enumerate([(0.08, 'partial 1'), (0.3, 'partial 2'), (0.52, 'partial 3'), (0.86, 'partial 4 (slowest)')]):
    axs[0].text(7.9 if k == 3 else [0.25, 0.9, 1.9][k], yy if k == 3 else [0.25, 0.55, 0.78][k], lab, fontsize=7.8, color='white', ha='right' if k == 3 else 'left')
axs[0].set_xlim(0, 8); axs[0].set_ylim(0, 1); axs[0].set_xlabel('time (s)'); axs[0].set_ylabel('share of the sound (timbre)'); axs[0].grid(False)
axs[0].set_title('Timbre is direction: it settles on the slowest partial', fontsize=9, color=INK)
axs[1].semilogy(t, X.sum(1) / X.sum(1)[0], color=ORANGE, label='loudness (rate)')
axs[1].semilogy(t, np.exp(-2 * g.min() * t), color=MUTED, lw=1.2, ls='--', label='slowest partial alone')
axs[1].set_xlabel('time (s)'); axs[1].set_ylabel('loudness (relative)'); axs[1].legend(frameon=False, fontsize=8)
axs[1].set_title('Loudness is rate: it keeps falling', fontsize=9, color=INK)
fig.tight_layout(); save(fig, 'fig4_sound.png')

# ---------------- Figure 5: two tones are two clocks ----------------
fs = 8000; tt = np.arange(0, 2.0, 1 / fs)
fig, axs = plt.subplots(2, 1, figsize=(7.2, 3.6), sharex=True)
for ax, c, lab in [(axs[0], 0.0, '220 Hz + 221.5 Hz'), (axs[1], 60.0, 'both raised by 60 Hz: 280 Hz + 281.5 Hz')]:
    s = np.cos(2 * np.pi * (220 + c) * tt) + np.cos(2 * np.pi * (221.5 + c) * tt + 0.7)
    ax.plot(tt, s, color='#b9c9e3', lw=0.4); ax.plot(tt, np.abs(hilbert(s)), color=BLUE, lw=1.8)
    ax.set_ylabel('signal'); ax.text(0.01, 1.02, lab, transform=ax.transAxes, fontsize=8.6, color=INK, va='bottom')
axs[1].set_xlabel('time (s)')
fig.suptitle('The beat reads only the difference of rates: 1.5 beats per second in both', fontsize=9.5, color=INK, y=1.02)
fig.tight_layout(); save(fig, 'fig5_beats.png')

# ---------------- Figure 6: the comma is a holonomy ----------------
pure = 1200 * np.log2(1.5)
fig = plt.figure(figsize=(7.2, 3.4)); ax = fig.add_subplot(1, 2, 1, projection='polar'); ax2 = fig.add_subplot(1, 2, 2)
cents = np.cumsum([0] + [pure] * 12); ang = 2 * np.pi * (cents % 1200) / 1200; rad = 1 + cents / 8400 * 0.9
ax.plot(ang, rad, color=BLUE, lw=1.4, marker='o', ms=4)
names = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'E#', "B#"]
for k in [0, 12]: ax.annotate(names[k], (ang[k], rad[k]), xytext=(6, 4), textcoords='offset points', fontsize=8.5, color=INK)
ax.set_yticklabels([]); ax.set_xticklabels([]); ax.grid(color=GRID)
ax.set_title('Twelve pure fifths go round the circle\nand miss the start by 23.46 cents', fontsize=9, color=INK)
temps = {'equal': [700.0] * 12, 'Pythagorean': [pure] * 11 + [7 * 1200 - 11 * pure],
         'meantone': [1200 * np.log2(5 ** 0.25)] * 11 + [7 * 1200 - 11 * 1200 * np.log2(5 ** 0.25)]}
for i, (nm, f) in enumerate(temps.items()):
    dev = np.array(f) - pure; ax2.bar(np.arange(12) + (i - 1) * 0.27, dev, width=0.25, color=[BLUE, ORANGE, AQUA][i], label='%s (sum %.2f)' % (nm, dev.sum()))
ax2.axhline(0, color=MUTED, lw=0.8); ax2.set_xlabel('fifth around the circle'); ax2.set_ylabel('deviation from pure (cents)')
ax2.legend(frameon=False, fontsize=7.6, loc='lower left'); ax2.set_title('Moved, never removed: every sum is -23.46', fontsize=9, color=INK)
fig.tight_layout(); save(fig, 'fig6_comma.png')

# ---------------- Figure 7: the offset speed limit on its saturating trajectory ----------------
def traj(m, sigma, Om, tgrid):
    I = np.eye(m); Z = np.zeros((m, m))
    P0 = 0.5 * np.block([[I, sigma * 1j * I], [-sigma * 1j * I, I]]); H = Om * np.block([[Z, I], [I, Z]])
    w, V = np.linalg.eigh(H); out = []
    for t in tgrid:
        U = V @ np.diag(np.exp(-1j * w * t)) @ V.conj().T; P = U @ P0 @ U.conj().T; C = P[:m, :m]
        nu = np.linalg.eigvalsh(C); out.append(np.sum(np.log((1 - nu) / nu)))
    return np.array(out)
Om = 1.0; tg = np.linspace(0.02, 0.70, 2000)
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
for m, col in [(1, BLUE), (2, ORANGE), (3, AQUA)]:
    tau = traj(m, 1, Om, tg); axs[0].plot(tg, tau, color=col, label='m = %d' % m)
    dt = tg[1] - tg[0]; taud = np.gradient(tau, dt); gS = 4 * (m * Om**2) * (4 * m / np.cos(2 * Om * tg)**2)
    axs[1].plot(tg[2:-2], (taud**2 / gS)[2:-2], color=col, label='m = %d' % m, lw=[3.4, 2.2, 1.0][m - 1])
    print('fig7 m=%d: max |ratio - 1| = %.1e' % (m, np.abs((taud**2 / gS)[2:-2] - 1).max()))
axs[0].set_xlabel(r'$\Omega t$'); axs[0].set_ylabel(r'offset $\tau(t)$'); axs[0].legend(frameon=False, fontsize=8)
axs[0].set_title(r'$\tau=2m\,\mathrm{artanh}(\sin 2\Omega t)$', fontsize=9.5, color=INK)
axs[1].set_ylim(0.98, 1.02); axs[1].set_xlabel(r'$\Omega t$'); axs[1].set_ylabel(r'$\dot\tau^2/(4gS)$')
axs[1].set_title('The speed limit is met (all three lie on 1)', fontsize=9.5, color=INK); axs[1].legend(frameon=False, fontsize=8)
fig.tight_layout(); save(fig, 'fig7_offset.png')

# ---------------- Figure 8: the fall leaf, a colour clock ----------------
eps = np.array([[0.9, 0.15, 1.0], [0.0, 0.45, 3.2], [0.1, 1.8, 0.6], [0.5, 0.8, 1.2]]); Aabs = 2.5
def leaf(days, k1=0.108, k2=0.0063, red=False, s3=0.04, death=30.0, br=0.04, dt=0.01):
    c = np.array([1.0, 0.15, 0.0, 0.0]); out = []; tt_ = 0.0
    while tt_ <= days + 1e-9:
        out.append((tt_, c.copy())); light = 1.0 if (tt_ % 1.0) < 0.5 else 0.0
        m3 = s3 * light if (red and c[0] < 20 / 29 and tt_ < death) else 0.0; m4 = br if tt_ >= death else 0.0
        dc = np.array([-k1 * c[0], -k2 * c[1], m3 - 0.03 * c[2], m4])
        if tt_ >= death: dc[:3] -= 0.08 * c[:3]
        c = c + dt * dc; tt_ += dt
    return out
def rgb(c):
    x = np.exp(-Aabs * c @ eps); return np.clip(x, 0, 1)   # transmitted light per channel, darkening kept
fig, axs = plt.subplots(2, 1, figsize=(7.2, 3.3), gridspec_kw={'height_ratios': [1, 2]})
days_show = [0, 7, 14, 21, 28, 35, 45, 60, 80, 120]
for j, red in enumerate([False, True]):
    run = leaf(120, red=red); lookup = {round(r[0], 2): r[1] for r in run}
    for i, d_ in enumerate(days_show):
        axs[0].add_patch(plt.Rectangle((i, 1 - j), 0.92, 0.85, color=rgb(lookup[round(d_, 2)])))
axs[0].set_xlim(0, 10); axs[0].set_ylim(0, 2); axs[0].set_axis_off()
for i, d_ in enumerate(days_show): axs[0].text(i + 0.46, -0.25, 'day %d' % d_, ha='center', fontsize=7, color=INK2)
axs[0].text(-0.1, 1.42, 'yellow', ha='right', fontsize=7.5, color=INK2); axs[0].text(-0.1, 0.42, 'red', ha='right', fontsize=7.5, color=INK2)
run = leaf(120); T_ = np.array([r[0] for r in run]); C_ = np.array([r[1] for r in run])
for k, (lab, col) in enumerate([('chlorophyll', AQUA), ('carotenoid', ORANGE), ('brown', INK2)]):
    idx = [0, 1, 3][k]; axs[1].semilogy(T_, np.maximum(C_[:, idx], 1e-4), color=col, label=lab)
axs[1].set_ylim(1e-3, 3); axs[1].set_xlabel('days from onset'); axs[1].set_ylabel('pigment (relative)')
axs[1].legend(frameon=False, fontsize=7.8, ncol=3, loc='lower right')
axs[1].text(2, 1.4e-3, r'colour clock rate $=k_1-k_2$ (the gap)', fontsize=8, color=INK)
fig.tight_layout(); save(fig, 'fig8_leaf.png')
