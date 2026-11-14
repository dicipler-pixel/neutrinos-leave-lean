# SCRIPT: WEIGHT-BETWEEN-CORE-01
# Fresh re-runs of the core identities of "The Weight Between" for v1 of the one paper (not carried from earlier runs).
# Why each check proves its claim: each is the claimed equality or inequality evaluated on random instances; an
# identity that holds to rounding on random inputs and fails under a deliberate perturbation (the controls) cannot be
# a coincidence of special cases.
# KILL CONDITIONS (written before the run):
#  C1 X1 chain: (1/2)||[H,P]||^2 = ||PH(1-P)||^2 = Var_psi(H) (rank one) to 1e-10 relative, else dies.
#  C2 Theorem 7 identity ||[P,[P,F]]||^2 = 2 Tr[(C(I-C))^{-1}] with F = E W E^dag, W = -(C(I-C))^{-1}: 1e-9 relative.
#  C3 Theorem 7 bound: tau_dot^2 <= 4 g S on 500 random Hamiltonian-driven cases; any ratio > 1 + 1e-9 kills it.
#     tau_dot measured by central finite difference of the actual offset, not by the formula.
#  C4 equality: P_dot = lambda T (H = i lambda [T,P]) gives ratio 1 to 1e-6, else dies.
#  C5 scalar exact gap (12): 4gS - tau_dot^2 = 4 (Im conj(b) b_dot)^2 / (c(1-c))^2 to 1e-7 on random 2x2 paths.
#  C6 ladder: S_0^2 <= S_{-2} S_2 and S_{-1}^2 <= S_{-2} S_0 on 2000 random weighted graphs; any violation kills it.
#  C7 connection energy: (1/8)||[H,H^dag]||^2 = sum_edges ||D_i - A_ij D_j A_ij^dag||^2 for H = diag D + A,
#     A anti-Hermitian with unitary edge blocks: 1e-10 relative. Control: break unitarity of one block, must fail.
import numpy as np
from scipy.linalg import expm, logm
rng = np.random.default_rng(2610)
fro2 = lambda X: float(np.real(np.vdot(X, X)))
def herm(n): X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); return (X + X.conj().T) / 2
def rand_proj(n, k):
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))); V = Q[:, :k]; return V @ V.conj().T
def offset(C): nu = np.linalg.eigvalsh(C); return float(np.sum(np.log((1 - nu) / nu)))

# C1
w = 0.0
for _ in range(300):
    n = rng.integers(3, 8); H = herm(n); P = rand_proj(n, 1); psi = np.linalg.eigh(P)[1][:, -1]
    a = 0.5 * fro2(H @ P - P @ H); b = fro2(P @ H @ (np.eye(n) - P))
    var = np.real(np.vdot(psi, H @ H @ psi) - np.vdot(psi, H @ psi)**2)
    w = max(w, abs(a - b) / b, abs(b - var) / b)
print('C1 X1 chain, worst relative difference over 300 cases: %.1e' % w)

# C2, C3, C4
def setup(n, m, k):
    while True:
        P = rand_proj(n, k); E = np.eye(n)[:, :m]; C = E.T @ P @ E; nu = np.linalg.eigvalsh(C)
        if nu.min() > 1e-3 and nu.max() < 1 - 1e-3: return P, E, C
w2 = 0.0; worst = 0.0; eqdev = 0.0
for trial in range(500):
    # 0 < C < I needs m <= k <= n - m (otherwise C has an eigenvalue 0 or 1); the first draft drew any m, k and could
    # wait forever on an impossible cut
    n = rng.integers(4, 9); m = rng.integers(1, n // 2 + 1); k = rng.integers(m, n - m + 1)
    P, E, C = setup(n, m, k)
    W = -np.linalg.inv(C @ (np.eye(m) - C)); F = E @ W @ E.T; T = P @ (P @ F - F @ P) - (P @ F - F @ P) @ P
    S = float(np.real(np.trace(-W)))
    w2 = max(w2, abs(fro2(T) - 2 * S) / (2 * S))
    H = herm(n); h = 1e-5
    def tau_at(t):
        U = expm(-1j * H * t); Pt = U @ P @ U.conj().T; return offset(E.T @ Pt @ E)
    taud = (tau_at(h) - tau_at(-h)) / (2 * h); g = 0.5 * fro2(-1j * (H @ P - P @ H))
    worst = max(worst, taud**2 / (4 * g * S))
    if trial < 50:
        lam = 0.37; Heq = 1j * lam * (T @ P - P @ T)
        def tau_eq(t):
            U = expm(-1j * Heq * t); Pt = U @ P @ U.conj().T; return offset(E.T @ Pt @ E)
        td = (tau_eq(h) - tau_eq(-h)) / (2 * h); ge = 0.5 * fro2(-1j * (Heq @ P - P @ Heq))
        eqdev = max(eqdev, abs(td**2 / (4 * ge * S) - 1))
print('C2 ||[P,[P,F]]||^2 = 2S, worst relative error over 500 cases: %.1e' % w2)
print('C3 largest tau_dot^2/(4gS) over 500 random driven cases: %.4f' % worst)
print('C4 equality generator H = i lambda [T,P]: worst |ratio - 1| over 50 cases: %.1e' % eqdev)

# C5 scalar cut with exact gap
w5 = 0.0
for _ in range(2000):
    # a random rank-one projector path |psi(s)><psi(s)| in C^2; P = [[c, b],[conj b, 1-c]]
    th0, ph0, dth, dph = rng.uniform(0.2, 1.3), rng.uniform(0, 6.28), rng.normal(), rng.normal()
    def Pof(s):
        th, ph = th0 + dth * s, ph0 + dph * s; v = np.array([np.cos(th / 2), np.exp(1j * ph) * np.sin(th / 2)]); return np.outer(v, v.conj())
    hh = 1e-6; P0 = Pof(0); Pd = (Pof(hh) - Pof(-hh)) / (2 * hh)
    c, b = P0[0, 0].real, P0[0, 1]; cd, bd = Pd[0, 0].real, Pd[0, 1]
    g = 0.5 * fro2(Pd); S = 1 / (c * (1 - c)); taud = -cd / (c * (1 - c))
    lhs = 4 * g * S - taud**2; rhs = 4 * (np.imag(np.conj(b) * bd))**2 / (c * (1 - c))**2
    w5 = max(w5, abs(lhs - rhs) / max(1, 4 * g * S))
print('C5 scalar exact gap (12), worst error / max(1,4gS) over 2000 paths: %.1e' % w5)

# C6
viol = 0
for _ in range(2000):
    n = rng.integers(3, 8); d = rng.uniform(-3, 3, n); K = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); K = (K + K.conj().T) / 2
    msk = ~np.eye(n, dtype=bool); D = np.abs(d[:, None] - d[None, :])[msk]; k2 = np.abs(K[msk])**2
    Sk = lambda k: np.sum(k2 * D**k)
    viol += (Sk(0)**2 > Sk(-2) * Sk(2) * (1 + 1e-12)) + (Sk(-1)**2 > Sk(-2) * Sk(0) * (1 + 1e-12))
print('C6 ladder inequalities violated in %d of 4000 tests' % viol)

# C7
def unitary(r):
    Q, R = np.linalg.qr(rng.normal(size=(r, r)) + 1j * rng.normal(size=(r, r))); return Q * (np.diag(R) / abs(np.diag(R)))
nv, r = 5, 2; edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
def check(break_one):
    Ds = [herm(r) for _ in range(nv)]; U = {e: unitary(r) for e in edges}
    if break_one: U[edges[0]] = U[edges[0]] * 1.3
    Hm = np.zeros((nv * r, nv * r), complex)
    for i in range(nv): Hm[i*r:(i+1)*r, i*r:(i+1)*r] = Ds[i]
    for (i, j) in edges: Hm[i*r:(i+1)*r, j*r:(j+1)*r] = U[(i, j)]; Hm[j*r:(j+1)*r, i*r:(i+1)*r] = -U[(i, j)].conj().T
    lhs = fro2(Hm @ Hm.conj().T - Hm.conj().T @ Hm) / 8
    rhs = sum(fro2(Ds[i] - U[(i, j)] @ Ds[j] @ U[(i, j)].conj().T) for (i, j) in edges)
    return abs(lhs - rhs) / rhs
print('C7 connection energy identity: relative error %.1e; control with one non-unitary block: %.2e' % (max(check(False) for _ in range(50)), check(True)))
