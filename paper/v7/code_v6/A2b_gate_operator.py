# SCRIPT: A2B_GATE_OPERATOR
"""Gate for the r1 variant (nnmode = 2), single frozen group, through the compiled rhs()/state() of the copies.
Why this checks what it claims: the collision term is the only part of dI that depends on (kbe, kbn) except through the
plasma momentum kq -> ae -> lapse A and the angular term mu*ac. With a uniform, enormous plasma density (e ~ 1e60) the
pressure gradient is zero and ae = kq/(e+p) ~ 1e-60, so A = 1 exactly in double precision and mu*ac*I is ~1e-60 of the
collision term. Then dI(kbe,kbn) - dI(0,0) IS the collision term, from the compiled code itself. Columns are taken on
perturbations orthogonal to the constant (so eps and hence kap_n are unchanged), and the constant column is C(1)."""
import sys, numpy as np
which = sys.argv[1]                     # 'r1' or 'orig'
sys.path.insert(0, f'/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A2b_decisive/{which}')
import ms_mg
nn = 2 if which == 'r1' else 0
K = 32; N = 4; PI = np.pi
mue = np.linspace(-1, 1, K+1); dmu = mue[1]-mue[0]; mu = 0.5*(mue[:-1]+mue[1:])
le = np.linspace(100.0, 180.0, 50); lp = le + np.log(1/3); lg = le/4; lT = le/4 - 30.0
lchi = np.zeros(50)
R = np.linspace(1.0, 2.0, N+1); U = np.zeros(N+1); Gam = np.ones(N+1)
e = np.full(N, np.exp(140.0)); Tb = float(np.exp(140.0/4 - 30.0)); pe = 4.0
rng = np.random.default_rng(1)
def dI_of(I, kbe, kbn, enub):
    dR = np.zeros(N+1); dU = np.zeros(N+1); dG = np.zeros(N+1); de = np.zeros(N); dI = np.zeros(I.shape)
    ms_mg.rhs(0.0, R, U, Gam, e, I, mue, le, lp, lg, lT, np.array([kbe]), np.array([kbn]), Tb, enub, pe, 1, 0.1, 0.0,
              np.zeros(1), dR, dU, dG, de, dI, lchi, 0.0, nn)
    return dI
I0 = (1.0 + 0.3*rng.standard_normal((1, N, K)))
eps0 = 2*PI*I0[0].sum(axis=1)*dmu
ke, kbn = 0.7, 1.9
enub = float(eps0[1])                    # kap_n = kbn * eps/enub; cell 1 then has kap_n = kbn exactly
kn = kbn*eps0/enub
def coll(I): return dI_of(I, ke, kbn, enub) - dI_of(I, 0.0, 0.0, enub)
# discrete orthonormal Legendre basis on the bin centres, inner product sum_k f g dmu
V = np.vander(mu, K, increasing=True); Q, _ = np.linalg.qr(V*np.sqrt(dmu)); Q = Q/np.sqrt(dmu)
for j in range(K):
    if Q[:, j] @ V[:, j] < 0: Q[:, j] *= -1
i = 1
Cmat = np.zeros((K, K))
const = np.ones((1, N, K)); Cmat[:, 0] = coll(const)[0, i]
for j in range(1, K):
    Ij = I0.copy(); Ij[0, i] = I0[0, i] + 1.0*Q[:, j]
    Cmat[:, j] = coll(Ij)[0, i] - coll(I0)[0, i]
# operator in the Legendre basis: L = Q^T W C Q with W = dmu (Q orthonormal under that product)
L = (Q.T*dmu) @ Cmat
kk = ke + kn[i]
target = -kk*np.diag([0.0] + [1.0]*(K-1)) if nn == 2 else -np.diag([0.0, ke] + [ke+kn[i]]*(K-2))
print(f'{which}: nnmode {nn}, k_e = {ke}, k_n(cell) = {kn[i]:.15f}')
print('  max |L - target| =', np.abs(L - target).max(), ' (|target| ~', np.abs(target).max(), ')')
print('  diag(L)[:5] =', np.round(np.diag(L)[:5], 15))
print('  eigenvalues (sorted, first 4):', np.round(np.sort(np.linalg.eigvals(L).real)[::-1][:4], 14), '... min', np.linalg.eigvals(L).real.min())
# nonlinear check on random anisotropic I in every cell: C(I) vs closed form
C = coll(I0)[0]
if nn == 2:
    closed = -(ke + kn)[:, None]*(I0[0] - (eps0/(4*PI))[:, None])
else:
    q = 2*PI*(I0[0]*mu).sum(axis=1)*dmu; cs = q/(2*PI*(mu*mu*dmu).sum())
    closed = ke*((eps0/(4*PI))[:, None] - I0[0]) + kn[:, None]*((eps0/(4*PI))[:, None] + cs[:, None]*mu[None, :] - I0[0])
print('  C(I) vs closed form, all cells: max rel err =', np.abs(C - closed).max()/np.abs(closed).max())
# energy and momentum moments of the collision term (per cell)
dE = 2*PI*C.sum(axis=1)*dmu; dQ = 2*PI*(C*mu).sum(axis=1)*dmu
q0 = 2*PI*(I0[0]*mu).sum(axis=1)*dmu
print('  energy moment of collisions / (k eps):', np.abs(dE).max()/np.abs((ke+kn)*eps0).max())
# momentum handed to the plasma: from state(); moderate plasma density so ae = kq/(e+p) is resolved
e_mod = np.full(N, np.exp(110.0))
Tb_mod = float(np.exp(110.0/4 - 30.0))       # same local/background temperature ratio (= 1) as the collision run
args = (0.0, R, U, Gam, e_mod, I0, mue, le, lp, lg, lT, np.array([ke]), np.array([kbn]), Tb_mod, enub, pe, lchi, 0.0)
st = ms_mg.state(*args, nn) if which == 'r1' else ms_mg.state(*args)
ae = st[8]; p_mod = np.exp(np.interp(110.0, le, lp))
kq_code = ae[N]*(e_mod[-1] + p_mod)          # ae[N] = kq[N-1]/(e+p)
loss = -dQ[N-1]                              # neutrino momentum removed by collisions in the last cell
print(f'  momentum: neutrino collisional loss = {loss:.15e}, handed to plasma (code kq) = {kq_code:.15e}, '
      f'rel diff = {abs(loss-kq_code)/abs(loss):.2e}')
print(f'  (nu-e part alone k_e q = {ke*q0[N-1]:.15e})')
