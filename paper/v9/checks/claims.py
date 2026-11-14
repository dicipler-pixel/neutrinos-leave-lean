# SCRIPT: NU-V9-CLAIMS  claim harness: recompute every disputed number from archived data, then check the paper text
# Usage: python3 claims.py [paper_dir] [main_tex_name]   (defaults: ../paper, neutrinos_v9.tex; data paths from NU_GRAMIAN, NU_A6RES)
# Exit code 1 if any check fails. Each check prints WHY it decides the claim before its result.
import sys, os, re, json, math, glob
import numpy as np
from scipy.special import roots_legendre

HERE = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'paper')
MAIN = sys.argv[2] if len(sys.argv) > 2 else 'neutrinos_v9.tex'
GRAMIAN = os.environ.get('NU_GRAMIAN', os.path.join(P, 'results', 'A5_raw', 't2_gramian.json'))
A6RES = os.environ.get('NU_A6RES', os.path.join(P, 'code', 'A6', 'res_L3_r125.json'))

def tex_all():
    txt = {}
    for f in [MAIN] + sorted(os.path.basename(x) for x in glob.glob(P + '/sec_new_*.tex') + glob.glob(P + '/app_new_*.tex')):
        txt[f] = open(os.path.join(P, f)).read()
    return txt
TX = tex_all()
ALL = '\n'.join(TX.values())

results = []
def check(cid, why, ok, detail):
    results.append((cid, ok))
    print(f'[{"PASS" if ok else "FAIL"}] {cid}\n    why: {why}\n    {detail}')

def has(s): return s in ALL
def where(s): return [f for f, t in TX.items() if s in t]

# ---------- computed facts ----------
DF, DI = 0.49773, 0.52832
G = lambda d: (d - DF) / (DI - DF)
tau = lambda d: math.log((DI - d) / (d - DF))

# C1  G at r = 1/16
g16 = G(0.521485)
check('C1 G(r=1/16)', 'the abstract quotes G at r=1/16; recomputing from its threshold and the references fixes the printed digit',
      f'{g16:.3f}' == '0.777' and not has('0.776') and has('0.777'),
      f'computed {g16:.4f}; "0.776" in {where("0.776")}; "0.777" present: {has("0.777")}')

# C2  Gramian ratios from the raw outputs
gr = json.load(open(GRAMIAN))
top = lambda key, kind: gr[key][kind]['eigs'][0] if isinstance(gr[key][kind], dict) and 'eigs' in gr[key][kind] else gr[key][kind]
def topv(key, kind):
    v = gr[key][kind]
    return v['eigs'][0] if isinstance(v, dict) else v
i2 = topv('ed2_n3_s0.5', 'integral') / topv('ed2_n3_s2', 'integral')
i05 = topv('ed0.5_n3_s0.125', 'integral') / topv('ed0.5_n3_s0.5', 'integral')
t05 = topv('ed0.5_n3_s0.125', 'terminal') / topv('ed0.5_n3_s0.5', 'terminal')
surv2 = lambda ed, s, n=3: (ed / s) ** n / n * 2  # exponent of the squared survival factor
# the Gramian ratio is coupled/transition, so the relevant exponent is the difference: 128/3 - 2/3 = 42 exactly
e05 = surv2(0.5, 0.125) - surv2(0.5, 0.5); e2 = surv2(2.0, 0.5) - surv2(2.0, 2.0)
check('C2a integral Gramian ratios', 'the paper quotes 3e-7 (eps_dec=2) and 2.5e-9 (eps_dec=0.5); the raw json top eigenvalues give the ratios directly',
      round(i2, 7) > 2.95e-7 and i2 < 3.1e-7 and 2.4e-9 < i05 < 2.55e-9 and has('3\\times10^{-7}') and has('2.5\\times10^{-9}'),
      f'eps_dec=2: {i2:.3e}; eps_dec=0.5: {i05:.3e}; squared-survival exponents: eps_dec=0.5 {e05:.2f}, eps_dec=2 {e2:.2f}')
fac = t05 / math.exp(-42)
t2 = topv('ed2_n3_s0.5', 'terminal') / topv('ed2_n3_s2', 'terminal')
check('C2b snapshot Gramian', 'the snapshot (terminal) ratio is in the raw json; its factor against e^-42 is arithmetic; the text must not claim "factor of ten"',
      not has('factor of ten') and ALL.count('10^{1.1}') == ALL.count('says $10^{1.1}$ where the ratio') and abs(e05 - 42) < 1e-9 and abs(e2 - 42) < 1e-9 and round(fac, -1) == 80 and has('4.8\\times10^{-17}') and has('a factor of about $80$') and has('1.4\\times10^{-13}') and has('$2\\times10^{5}$ above the same') and f'{t2/math.exp(-42):.0e}' == '2e+05' and f'{t2:.1e}' == '1.4e-13' and abs(math.log10(i05 / math.exp(-42)) - math.log10(4e9)) < 0.1,
      f'terminal ratio eps_dec=0.5 {t05:.3e} (/e^-42 = {fac:.1f}); eps_dec=2 {t2:.2e} (/e^-42 = {t2/math.exp(-42):.2e}); integrated/e^-42 = {i05/math.exp(-42):.2e}; exponents {e05:.6f}, {e2:.6f}; "factor of ten" in {where("factor of ten")}')

# C3  K and the left/right overlap on the chain
def chain(N, kap, k=1.0):
    l = np.arange(N - 1); c = (l + 1) / np.sqrt((2 * l + 1) * (2 * l + 3))
    M = np.diag(c, 1) + np.diag(c, -1); D = np.full(N, -kap); D[0] = 0
    return -1j * k * M + np.diag(D)
rows = []
for kap in (2.0, 1.0, 0.8, 0.7):
    w, V = np.linalg.eig(chain(400, kap)); i = np.argmax(w.real); v = V[:, i]
    K = (np.vdot(v, v).real) ** 2 / abs(v @ v) ** 2
    Mc = chain(400, kap); wl, Vl = np.linalg.eig(Mc.conj().T); j = np.argmin(abs(wl - np.conj(w[i]))); l = Vl[:, j]  # left eigenvector: y^H M = lambda y^H
    ov = abs(np.vdot(l, v)) / (np.linalg.norm(l) * np.linalg.norm(v))
    rows.append((kap, K, 4 / kap**2 / np.sin(2 / kap) ** 2, ov, 1 / math.sqrt(K)))
okK = all(abs(a[1] - a[2]) / a[2] < 1e-4 and abs(a[3] - a[4]) < 1e-6 for a in rows)
check('C3 K and left/right overlap', 'K computed from the right eigenvector must equal 4phi^2/sin^2 2phi, and the true left eigenvector overlap must equal 1/sqrt(K) (so it goes to 0 as K diverges); the text must not say the mode is non-orthogonal to its left eigenvector',
      okK and not has('non-orthogonal to its own left eigenvector') and has('K^{-1/2}=\\sin2\\phi/2\\phi') and all(abs(math.sin(2/a[0])/(2/a[0]) - a[3]) < 1e-6 for a in rows),
      'kappa, K chain, K exact, |<l,r>|, 1/sqrt K: ' + '; '.join(f'{a[0]}: {a[1]:.5f} {a[2]:.5f} {a[3]:.6f} {a[4]:.6f}' for a in rows))

# C4  profile weight below the wall
kn, kw = roots_legendre(36); ks = 0.5 * 8.75 * (kn + 1) + 0.25; wk = 0.5 * 8.75 * kw
wE = wk * ks**2 * np.exp(-ks**2 / 2); wE /= wE.sum()
wall = 0.958 * math.pi / 2
nodes = wE[ks < wall].sum()
from scipy.integrate import quad
f = lambda k: k * k * math.exp(-k * k / 2)
cont = quad(f, 0.25, wall)[0] / quad(f, 0.25, 9)[0]
check('C4 profile weight below the wall', 'the 36-node sum and the continuous integral of the same weight are both computable; the text must state the figure it actually computed and not present the node sum as exact',
      abs(nodes - 0.5135) < 5e-4 and abs(cont - 0.4785) < 5e-4 and not has('51\\%') and has('$0.51$ on the $36$ nodes used here, $0.48$ by direct integration'),
      f'wall k={wall:.9f}; 36 nodes {nodes:.4f}; continuous {cont:.4f}; "51\\%" in {where("51\\%")}')

# C5  positivity windows on 32 midpoint bins, from the actual generator matrices
N = 32; mu = -1 + (np.arange(N) + 0.5) * 2 / N; w = np.full(N, 2 / N)
Bas = []; vecs = [mu**j for j in range(4)]
for v in vecs:
    u = v.copy()
    for b in Bas: u = u - (np.sum(w * u * b) / np.sum(w * b * b)) * b
    Bas.append(u)
def proj(b): return np.outer(b, w * b) / np.sum(w * b * b)
P0, P1, P2 = proj(Bas[0]), proj(Bas[1]), proj(Bas[2]); I = np.eye(N)
def gen_all(r): return r * (P0 - I) + (r - 1) * P1           # kappa1=1, kappa2=r: all l>=2 at r
def gen_shear(r): return (P0 - I) + (1 - r) * P2              # shear alone at r
def offmin(Mx): return (Mx - np.diag(np.diag(Mx))).min()
def window(gen):
    rs = np.linspace(0.3, 3.0, 270001); ok = np.array([offmin(gen(r)) >= -1e-15 for r in rs[::100]])
    # refine edges by bisection
    def edge(a, b):
        fa = offmin(gen(a)) >= -1e-15
        for _ in range(60):
            m = 0.5 * (a + b)
            if (offmin(gen(m)) >= -1e-15) == fa: a = m
            else: b = m
        return 0.5 * (a + b)
    rr = rs[::100]; idx = np.where(ok)[0]
    return edge(rr[idx[0] - 1], rr[idx[0]]), edge(rr[idx[-1]], rr[idx[-1] + 1])
wa, ws = window(gen_all), window(gen_shear)
check('C5 positivity windows', 'the Markov condition is non-negative off-diagonals of the bin generator; scanning r on the actual matrices gives the exact windows to compare with what the text calls them',
      f'{wa[0]:.3f}' == '0.725' and f'{wa[1]:.2f}' == '1.55' and f'{ws[0]:.2f}' == '0.56' and f'{ws[1]:.2f}' == '1.24' and has('$0.725\\le r\\le1.55$ and $0.56\\le r\\le1.24$'), f'all l>=2: [{wa[0]:.4f}, {wa[1]:.4f}] (continuum [0.75, 1.5]); shear alone: [{ws[0]:.4f}, {ws[1]:.4f}]')

# C6  A6 third level
res = json.load(open(A6RES))
lo, hi = res.get('lo'), res.get('hi')
L1, L2 = 0.50984158, 0.50991687  # r=1.25 thresholds at levels 1 and 2 (v6 tables)
d2 = L2 - L1; mid = 0.5 * (lo + hi)
p1s, p2s, p1t = L2 + d2 / 1.5, L2 + d2 / 1.5**2, L2 + d2 / 3
check('C6 A6 third level', 'the bracket and the three refinement predictions come from the stored result file and the level-1/2 thresholds; the text must quote them as computed',
      lo <= p2s <= hi and lo <= p1t <= hi and not (lo <= p1s <= hi) and has('0.5099481\\pm0.0000063') and has('$0.42$') and has('0.50996706') and has('0.50995033') and has('0.50994197') and has('1.094$--$1.098'),
      f'bracket [{lo:.8f}, {hi:.8f}] mid {mid:.8f}; shift ratio {(mid-L2)/d2:.3f} (range {(lo-L2)/d2:.3f}-{(hi-L2)/d2:.3f}); p1 space {p1s:.8f}, p2 space {p2s:.8f}, p1 time {p1t:.8f}')

# C7  forbidden and stale phrases (the slips found so far)
bad = ['non-orthogonal to its own left eigenvector', 'factor of ten', 'every scalar summary', 'No scalar summary',
       'is exact only for structure set', 'The dipole coefficient of the common-frame target', '0.776', '0.646', '51\\%']
found = {b: where(b) for b in bad if has(b)}
check('C7 forbidden phrases', 'each phrase is a slip found by an audit; any occurrence means a fix did not land everywhere', not found, f'found: {found}')

# C8  references consistency: shifts at r=1/4, 4 from the measured 0.425
d14, d4 = 0.516498, 0.505442
check('C8 shifts r=1/4,4', 'the shifts quoted against the measured r=1 share must follow from the table thresholds, and the text must print exactly those values',
      f'{G(d14)-0.4253:+.3f}' == '+0.188' and f'{G(d4)-0.4253:+.3f}' == '-0.173' and f'{tau(d14)-tau(0.510741):+.3f}' == '-0.763' and f'{tau(d4)-tau(0.510741):+.3f}' == '+0.786' and has('+0.188') and has('-0.173') and has('-0.763') and has('+0.786'), f'G(1/4)-0.4253={G(d14)-0.4253:+.3f}; G(4)-0.4253={G(d4)-0.4253:+.3f}; offsets {tau(d14)-tau(0.510741):+.3f}, {tau(d4)-tau(0.510741):+.3f}')

# C9  item 6: every "law" claim about the rapidity must carry "of the rulers tested" in the same sentence
sents = [x for x in re.split(r'(?<=[.;])\s+', ALL) if re.search(r"law (?:lives|is a law) in the|is a law in the operator", x)]
unq = [x[:120] for x in sents if 'rulers tested' not in x]
check('C9 rapidity claims qualified', 'audit item 6: any sentence placing the law in the link rapidity without the scope of the comparison is an overclaim',
      not unq and len(sents) >= 3, f'{len(sents)} law sentences; unqualified: {unq}')

# C10 printed listings: scan every file pulled in by \lstinputlisting for known slips, which must carry a note in the appendix
lst = re.findall(r'\\lstinputlisting(?:\[[^\]]*\])?\{([^}]+)\}', ALL)
hits = {}
for f in lst:
    fp = os.path.join(P, f)
    if os.path.exists(fp):
        t = open(fp, errors='replace').read()
        for b_ in ['10^1.1', '/tmp/claude-0']:
            if b_ in t: hits.setdefault(b_, []).append(f)
noted = has('says $10^{1.1}$ where the ratio')
ok10 = set(hits.get('10^1.1', [])) <= {'code_v6/A5_PREREGISTERED.txt'} and (not hits.get('10^1.1') or noted) and not hits.get('/tmp/claude-0')
check('C10 printed listings', 'listings are printed into the PDF and HTML, so a slip inside a listed file is a slip in the paper unless the appendix notes it',
      ok10 and len(lst) > 50, f'{len(lst)} listings; hits {hits}; note present {noted}')

# C11 extrapolation 1.094-1.098 recomputed from the third-level factor applied to r=0.8
L1_08, L2_08 = 0.51169233, 0.51175643
d08 = L2_08 - L1_08
def odd(d125, d08): return (tau(d125) - tau(d08)) / math.log(1.25)
R3 = odd(mid, L2_08 + d08 * (mid - L2) / d2)
q = (mid - L2) / d2
Rinf = [odd(L2 + d2 * x / (1 - x), L2_08 + d08 * x / (1 - x)) for x in ((lo - L2) / d2, q, (hi - L2) / d2)]
check('C11 extrapolation', 'the third-level and extrapolated rates follow from the measured shrink factor applied to both thresholds; the text must print the rounded values',
      f'{R3:.3f}' == '1.099' and 1.093 < min(Rinf) and max(Rinf) < 1.0985 and has('1.094$--$1.098') and has('$1.099$'),
      f'R3 {R3:.4f}; Rinf over factor range {[round(x,4) for x in Rinf]}')

nf = sum(1 for _, ok in results if not ok)
print(f'\n{len(results)} checks, {nf} failed')
sys.exit(1 if nf else 0)
