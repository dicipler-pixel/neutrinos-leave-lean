# SCRIPT: A2_STEP2_SELFSCATTER_ALGEBRA
"""Exact algebra of McCormick's multigroup collision term (App. C, Eq. C3; ms_mg.py, nnmode=0) for one frozen group.

Checks, on his own 32-bin angle grid (mue = linspace(-1,1,33), midpoints, weight dmu):
 1. the collision operator C[I] = k_e (eps/4pi - I) + k_n (eps/4pi + c mu - I), with c = q/(2pi sum mu^2 dmu),
    built line-for-line from ms_mg.py, equals -diag(0, k_e, k_e+k_n, ..., k_e+k_n) in the discrete orthonormal
    Legendre basis (Gram-Schmidt of 1, mu, mu^2, ... under <f,g> = sum f g dmu);
 2. the k_n part of that operator, taken from McCormick's compiled rhs() itself (two calls differing only in kbn,
    with kbe = 0, so nothing else in the right-hand side moves), equals the formula of 1;
 3. (1/8)||[L,L*]||_F^2 = k^2 (c0^2 k_e^2 + c1^2 k_n^2) exactly for L = -i k M - D, M the discrete mu operator,
    with c0^2, c1^2 the discrete Jacobi weights, and these tend to 1/3 and 4/15 as N_mu grows.
"""
import sys, os
import numpy as np
SIM = '/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/steve/src/simulation'

K = 32
mue = np.linspace(-1, 1, K+1); dmu = mue[1]-mue[0]; mu = 0.5*(mue[:-1]+mue[1:])
sum_mu2 = np.sum(mu*mu*dmu)

def coll(I, ke, kn):
    """ms_mg.py collision lines (nnmode = 0), lapse A = 1."""
    eps = 2*np.pi*np.sum(I)*dmu; q = 2*np.pi*np.sum(I*mu)*dmu
    cs = q/(2*np.pi*sum_mu2)
    tgt = eps/(4*np.pi) + cs*mu
    return ke*(eps/(4*np.pi) - I) + kn*(tgt - I)

def legendre_basis(K, mu, dmu):
    """Discrete orthonormal polynomials on the bins: columns of Q, <Q_l, Q_m> = delta (weight dmu)."""
    V = np.vander(mu, K, increasing=True)
    W = np.sqrt(dmu)
    Q, Rr = np.linalg.qr(W*V)          # orthonormal in the plain dot product of sqrt(dmu)*f
    sgn = np.sign(np.diag(Rr)); Q = Q*sgn
    return Q                            # columns are sqrt(dmu) * P_l(mu_k)

Q = legendre_basis(K, mu, dmu)
ke, kn = 0.7, 3.1
Cmat = np.column_stack([coll(np.eye(K)[:, j], ke, kn) for j in range(K)])      # acts on I (bin values)
# in the orthonormal basis: f = Q^T sqrt(dmu) I  ->  C_hat = Q^T diag(sqrt dmu) C diag(1/sqrt dmu) Q
Wh = np.sqrt(dmu)
Chat = Q.T @ (Wh*Cmat/Wh) @ Q
target = -np.diag(np.r_[0.0, ke, np.full(K-2, ke+kn)])
err1 = np.max(np.abs(Chat - target))
print(f'1. max |C_hat - (-diag(0,k_e,k_e+k_n,...))| on 32 bins = {err1:.2e}  (orthonormality error {np.max(np.abs(Q.T@Q-np.eye(K))):.1e})')
# Note: high-degree monomials make QR ill-conditioned; the claim needs only span{1}, span{1,mu} to be exact.
# Basis-free check: C = -k_e (1 - P0) - k_n (1 - P01) with P0, P01 the bin-orthogonal projectors.
one = np.ones(K)
P0 = np.outer(one, one*dmu)/np.sum(one*one*dmu)
P1 = np.outer(mu, mu*dmu)/np.sum(mu*mu*dmu)
Cproj = -ke*(np.eye(K)-P0) - kn*(np.eye(K)-P0-P1)
print(f'   basis-free: max |C - [-k_e(1-P0) - k_n(1-P0-P1)]| = {np.max(np.abs(Cmat-Cproj)):.2e};'
      f' <1,mu> = {np.sum(mu*dmu):.1e}')
ev = np.sort(np.linalg.eigvals(Cmat).real)
print(f'   eigenvalues: one at {ev[-1]:.3e}, one at {ev[-2]:.15f} (-k_e = {-ke}), {np.sum(np.abs(ev[:-2]+ke+kn) < 1e-12)} at -(k_e+k_n)')

# 2. the k_n part from McCormick's compiled rhs()
sys.path.insert(0, SIM)
try:
    from ms_mg import rhs
    N = 4; G = 1
    R = np.linspace(1.0, 2.0, N+1); U = np.full(N+1, 0.3); Gam = np.ones(N+1); e = np.full(N, 1.0)
    rng = np.random.default_rng(1)
    I = 1.0 + 0.3*rng.standard_normal((1, N, K))
    le = np.log(np.array([1e-3, 1e3])); lp = le - np.log(3.0); lg = np.zeros(2); lT = 0.25*le
    lchi = np.zeros(2)
    out = []
    for kbn in (0.0, 1.0):
        dR = np.zeros(N+1); dU = np.zeros(N+1); dG = np.zeros(N+1); de = np.zeros(N); dI = np.zeros(I.shape)
        res = rhs(0.0, R, U, Gam, e, I, mue, le, lp, lg, lT, np.zeros(1), np.full(1, kbn), 1.0, 0.0, 4.0, G, 1.0, 0.0,
                  np.zeros(1), dR, dU, dG, de, dI, lchi, 0.0, 0)
        out.append((dI.copy(), res[1].copy(), res[6].copy()))
    # enub = 0 makes fn = 0 in state(); use enub > 0 instead so kap_n = kbn * eps/enub
    out = []
    for kbn in (0.0, 1.0):
        dR = np.zeros(N+1); dU = np.zeros(N+1); dG = np.zeros(N+1); de = np.zeros(N); dI = np.zeros(I.shape)
        res = rhs(0.0, R, U, Gam, e, I, mue, le, lp, lg, lT, np.zeros(1), np.full(1, kbn), 1.0, 1.0, 4.0, G, 1.0, 0.0,
                  np.zeros(1), dR, dU, dG, de, dI, lchi, 0.0, 0)
        out.append((dI.copy(), res[1].copy(), res[6].copy()))
    diff = out[1][0] - out[0][0]
    Ac = out[1][1]; kapn = out[1][2]
    err2 = 0.0
    for i in range(N):
        pred = Ac[i]*coll(I[0, i], 0.0, kapn[0, i])
        err2 = max(err2, np.max(np.abs(diff[0, i] - pred)))
    print(f'2. McCormick rhs(): k_n part minus formula, max abs = {err2:.2e} (scale of I ~ 1; kap_n = {kapn[0]})')
except Exception as ex:
    print('2. could not call ms_mg.rhs:', repr(ex))

# 3. connection energy on the discrete chain
def energy(K, ke, kn, k=1.3):
    mue = np.linspace(-1, 1, K+1); dmu = mue[1]-mue[0]; mu = 0.5*(mue[:-1]+mue[1:])
    # discrete Jacobi (Lanczos) on weights dmu: stable orthonormal basis
    w = np.full(K, dmu)
    q_prev = np.zeros(K); q = np.ones(K)/np.sqrt(np.sum(w)); a = []; b = []
    Qs = [q]
    for l in range(K-1):
        v = mu*q; al = np.sum(w*q*v); v = v - al*q - (b[-1] if b else 0.0)*q_prev
        for qq in Qs: v -= np.sum(w*qq*v)*qq          # full reorthogonalisation
        be = np.sqrt(np.sum(w*v*v)); a.append(al); b.append(be)
        q_prev, q = q, v/be; Qs.append(q)
    M = np.diag(b, 1) + np.diag(b, -1)                  # alpha = 0 by symmetry
    Dd = np.diag(np.r_[0.0, ke, np.full(K-2, ke+kn)])
    L = -1j*k*M - Dd
    Cm = L@L.conj().T - L.conj().T@L
    lhs = 0.125*np.sum(np.abs(Cm)**2)
    rhs_ = k*k*(b[0]**2*ke**2 + b[1]**2*kn**2)
    return lhs, rhs_, b[0]**2, b[1]**2, k*k*(ke**2/3 + 4*kn**2/15)
for KK in (32, 64, 128, 1024):
    lhs, r_, c0, c1, cont = energy(KK, ke, kn)
    print(f'3. N_mu={KK:5d}: (1/8)||[L,L*]||^2 = {lhs:.15f}, k^2(c0^2 ke^2 + c1^2 kn^2) = {r_:.15f}, rel diff {abs(lhs-r_)/r_:.1e};'
          f' c0^2 = {c0:.10f} (1/3 - dmu^2/12 = {1/3-(2/KK)**2/12:.10f}), c1^2 = {c1:.10f} (4/15 = {4/15:.10f});'
          f' continuum form k^2(ke^2/3+4kn^2/15) = {cont:.10f}, rel {abs(lhs-cont)/cont:.1e}')
