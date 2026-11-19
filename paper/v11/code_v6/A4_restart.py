# SCRIPT: A4-RESTART  McCormick run_nuc.py loop (r=1 single-rate collision model, unchanged physics) split at a restart surface eps_s
"""
Driver for the matched-pair restart test.
Same loop as McCormick's run_nuc.py (ms_nuc.py rhs/state/timestep imported unchanged), with:
  (1) kappa(t) = (1/2t)(eps_dec/eps)^n re-evaluated at EACH SSPRK3 stage time (audit item 1), kapcap 5e5 (inactive here);
  (2) the step that would cross t_s is shortened to land exactly on t_s = eps_s^2/(4 t0);
  (3) at t_s the state (t, R, U, Gam, e, I, peakC) is saved; the continuation starts from a saved state, with an
      optional perturbation dI_ik = a * (eps_i/4pi) * p_l(mu_k) that changes only the discrete l component.
Status 'BH' only from a detected apparent horizon (2M/R >= 1 with U < 0); 'dispersed' from McCormick's rule
(eps > 3 and max C < peakC/2); a solver breakdown is 'BH_breakdown' or 'crash' and never moves a bracket.
"""
import numpy as np, os, time
from ms_nuc import rhs, state, timestep, rho_b
from ms_fluid import initial_data, make_grid

FNU = 0.409; N = 400; K = 32; EPS_DEC = 2.0; NEXP = 3; KAPCAP = 5.0e5
RMAX = 9.0; BETA = 3.0; EPS0 = 0.1; CFL_R = 0.4; CFL_MU = 0.4; CH = 0.005

def kap_of(t, t0):
    return (1/(2*t))*min((EPS_DEC/(2*np.sqrt(t*t0)))**NEXP, KAPCAP)

def discrete_legendre(mue, lmax=4):
    """Discrete orthogonal polynomials on the bin midpoints, weight dmu, leading coefficient of continuous P_l."""
    mu = 0.5*(mue[1:]+mue[:-1]); dmu = mue[1]-mue[0]
    lead = {0: 1.0, 1: 1.0, 2: 1.5, 3: 2.5, 4: 35/8}
    P = []
    for l in range(lmax+1):
        v = mu**l
        for p in P:
            v = v - (np.sum(v*p)*dmu/(np.sum(p*p)*dmu))*p
        P.append(v*lead[l])    # mu^l minus lower part has leading coeff 1; scale to P_l's leading coefficient
    return mu, np.array(P)

def initial(delta):
    r = make_grid(N, RMAX, BETA)
    t0, R, U, rho = initial_data(r, delta, EPS0, 0.0, 1.0)
    e = (1-FNU)*rho
    mue = np.linspace(-1, 1, K+1)
    I = np.repeat((FNU*rho/(4*np.pi))[:, None], K, axis=1)
    Mi = np.concatenate([[0.0], np.cumsum((4*np.pi/3)*np.diff(R**3)*rho)])
    Gam = np.ones(N+1); Gam[1:] = np.sqrt(1.0 + U[1:]**2 - 2*Mi[1:]/R[1:])
    return dict(t=t0, t0=t0, r=r, mue=mue, R=R, U=U, Gam=Gam, e=e, I=I, peakC=-1.0, step=0, Imin=float(I.min()))

def evolve(st, t_stop=None, eps_max=15.0, snap_eps=(), stop_rule=True):
    """Advance state dict st. If t_stop given, stop exactly at t_stop (no stop rules applied before it)."""
    t, t0 = st['t'], st['t0']; r, mue = st['r'], st['mue']
    R, U, Gam, e, I = st['R'].copy(), st['U'].copy(), st['Gam'].copy(), st['e'].copy(), st['I'].copy()
    peakC = st['peakC']; step = st['step']; Imin = st['Imin']
    dR = np.zeros(N+1); dU = np.zeros(N+1); dG = np.zeros(N+1); de = np.zeros(N); dI = np.zeros((N, K))
    snaps = {}; snap_eps = list(snap_eps); status = 'undecided'; mtwo = 0.0
    dmu_ = mue[1]-mue[0]; w2 = (mue[1:]**3-mue[:-1]**3)/(3*dmu_); rec = []
    while True:
        kap = kap_of(t, t0)
        Ib = FNU/(1-FNU)*e[-1]/(4*np.pi)
        try:
            M, Ac, ac, S, V = rhs(t, R, U, Gam, e, I, mue, FNU, Ib, kap, dR, dU, dG, de, dI)
        except (ZeroDivisionError, FloatingPointError):
            status = 'crash'; break
        epsn = 2*np.sqrt(t*t0)
        twoMR = 2*M[1:]/R[1:]
        C = 2*(M[1:] - (4*np.pi/3)*rho_b(t)*R[1:]**3)/R[1:]
        iC = np.argmax(C); peakC = max(peakC, C[iC])
        e0n = I[0].sum(); ePk = I[iC].sum()
        rec.append((epsn, C[iC], e[0]/rho_b(t), 2*np.pi*e0n*dmu_/rho_b(t), (I[0] @ w2)/e0n, (I[iC] @ w2)/ePk, r[1+iC]))
        while snap_eps and epsn >= snap_eps[0] - 1e-12:
            eps_c, q_c, Pr_c = state(t, R, U, Gam, e, I, mue, FNU, kap)[:3]
            snaps[snap_eps.pop(0)] = dict(eps=epsn, Cmax=float(C[iC]), rC=float(r[1+iC]), ec=float(e[0]/rho_b(t)),
                                          nuc=float(eps_c[0]/rho_b(t)), Prc=float(Pr_c[0]/rho_b(t)), q=q_c.copy(), Pr=Pr_c.copy(),
                                          C=C.copy(), e=e.copy(), nu=eps_c.copy())
        if t_stop is not None and t >= t_stop*(1-1e-15):
            status = 'surface'; break
        if stop_rule and t_stop is None:
            if np.any((twoMR >= 1.0) & (U[1:] < 0)):
                status = 'BH'; break
            if epsn > 3.0 and C[iC] < 0.5*peakC:
                status = 'dispersed'; break
        if epsn > eps_max: break
        try:
            dt = min(timestep(R, U, e, I, mue, Gam, Ac, ac, S, CFL_R, CFL_MU), CH*2*t, (0.5/(kap*np.max(Ac)) if kap > 0 else 1e30))
            if t_stop is not None and t + dt > t_stop:
                dt = t_stop - t
            R1 = R + dt*dR; U1 = U + dt*dU; G1 = Gam + dt*dG; e1 = e + dt*de; I1 = I + dt*dI
            rhs(t+dt, R1, U1, G1, e1, I1, mue, FNU, FNU/(1-FNU)*e1[-1]/(4*np.pi), kap_of(t+dt, t0), dR, dU, dG, de, dI)
            R2 = 0.75*R + 0.25*(R1+dt*dR); U2 = 0.75*U + 0.25*(U1+dt*dU); G2 = 0.75*Gam + 0.25*(G1+dt*dG)
            e2 = 0.75*e + 0.25*(e1+dt*de); I2 = 0.75*I + 0.25*(I1+dt*dI)
            rhs(t+0.5*dt, R2, U2, G2, e2, I2, mue, FNU, FNU/(1-FNU)*e2[-1]/(4*np.pi), kap_of(t+0.5*dt, t0), dR, dU, dG, de, dI)
            R = R/3 + 2/3*(R2+dt*dR); U = U/3 + 2/3*(U2+dt*dU); Gam = Gam/3 + 2/3*(G2+dt*dG)
            e = e/3 + 2/3*(e2+dt*de); I = I/3 + 2/3*(I2+dt*dI)
        except (ZeroDivisionError, FloatingPointError):
            coll = U[1:] < 0
            status = 'BH_breakdown' if (coll.any() and np.max(twoMR[coll]) > 0.95) else 'crash'
            break
        t += dt; step += 1
        if t_stop is not None and abs(t - t_stop) < 1e-14*t_stop:
            t = t_stop
        Imin = min(Imin, float(I.min())); mtwo = max(mtwo, float(np.max(twoMR)))
        if np.any(e <= 0) or not np.all(np.isfinite(U)) or not np.all(np.isfinite(I)):
            status = 'crash'; break
    return dict(t=t, t0=t0, r=r, mue=mue, R=R, U=U, Gam=Gam, e=e, I=I, peakC=peakC, step=step, Imin=Imin,
                status=status, eps=2*np.sqrt(t*t0), snaps=snaps, max2MR=mtwo, rec=np.array(rec))

KEYS = ('t', 't0', 'r', 'mue', 'R', 'U', 'Gam', 'e', 'I', 'peakC', 'step', 'Imin')

def surface_state(delta, eps_s, cache_dir):
    global K
    """Run from eps0 to the restart surface eps_s (cached on disk)."""
    os.makedirs(cache_dir, exist_ok=True)
    fn = os.path.join(cache_dir, f'surf_d{delta:.10f}_es{eps_s:g}_K{K}.npz')
    if os.path.exists(fn):
        z = np.load(fn); return {k: (z[k] if z[k].ndim else z[k].item()) for k in KEYS}
    st = initial(delta)
    t_s = eps_s**2/(4*st['t0'])
    out = evolve(st, t_stop=t_s)
    assert out['status'] == 'surface', out['status']
    np.savez(fn, **{k: out[k] for k in KEYS})
    return {k: out[k] for k in KEYS}

def perturb(st, l, a):
    """dI_ik = a * (eps_i/4pi) * p_l(mu_k): changes only the discrete l component of every cell."""
    mu, P = discrete_legendre(st['mue'])
    dmu = st['mue'][1]-st['mue'][0]
    s = dict(st); I = st['I']
    Ibar = I.sum(axis=1)*dmu/2.0          # = eps/(4 pi) with eps = 2 pi sum I dmu
    s['I'] = I + a*Ibar[:, None]*P[l][None, :]
    return s

def positivity_bound(st, l):
    mu, P = discrete_legendre(st['mue']); p = P[l]
    dmu = st['mue'][1]-st['mue'][0]; I = st['I']; Ibar = I.sum(axis=1)*dmu/2.0
    ratio = I/Ibar[:, None]
    amax_plus = np.min(ratio[:, p < 0]/(-p[p < 0])[None, :])
    amax_minus = np.min(ratio[:, p > 0]/(p[p > 0])[None, :])
    return float(amax_plus), float(amax_minus), float(1/np.max(-p)), float(1/np.max(p))

def moments(st):
    """Discrete l=0..4 Legendre components per cell, plus McCormick's e, q, P_r."""
    mu, P = discrete_legendre(st['mue']); dmu = st['mue'][1]-st['mue'][0]
    comp = np.array([st['I'] @ (P[l]*dmu) for l in range(5)])
    t = st['t']; kap = kap_of(t, st['t0'])
    eps, q, Pr = state(t, st['R'], st['U'], st['Gam'], st['e'], st['I'], st['mue'], FNU, kap)[:3]
    return comp, eps, q, Pr

def bump(rc, r1=0.3, r2=2.0):
    """C-infinity bump, 1 at the middle of [r1, r2], identically 0 outside (regular at r=0, away from the outer edge)."""
    x = (rc - 0.5*(r1+r2))/(0.5*(r2-r1))
    b = np.zeros_like(rc); m = np.abs(x) < 1
    b[m] = np.exp(1.0 - 1.0/(1.0 - x[m]**2))
    return b

def angvec(mue, l):
    """Angular direction on the bins: l >= 0 -> discrete p_l; l == -1 -> A5 L-infinity-optimal hidden direction (eps_s=2, T=4)."""
    if l >= 0:
        return discrete_legendre(mue)[1][l]
    import json
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'restart_direction_A5.json')))
    v = np.array(d['directions']['ed2_n3_s2_T4']['candidates']['Linf_optimal']['d_on_32_bins'], float)
    assert len(v) == len(mue)-1
    return v

def cell_margin(st, l):
    """Per-cell positivity margin for +/- the l perturbation on the discrete bins: largest |a_i| keeping every bin >= 0 for both signs."""
    p = angvec(st['mue'], l)
    dmu = st['mue'][1]-st['mue'][0]; I = st['I']; Ibar = I.sum(axis=1)*dmu/2.0
    ratio = I/Ibar[:, None]
    mp = np.min(ratio[:, p < 0]/(-p[p < 0])[None, :], axis=1)
    mm = np.min(ratio[:, p > 0]/(p[p > 0])[None, :], axis=1)
    return np.minimum(mp, mm)

def perturb_bump(st, l, f):
    """dI_ik = f * b(r_i) * m_i * (eps_i/4pi) * p_l(mu_k); m_i the cell's positivity margin, b the compact bump in r.
    |f| < 1 keeps every bin positive; +f and -f are exact mirrors."""
    p = angvec(st['mue'], l)
    dmu = st['mue'][1]-st['mue'][0]; I = st['I']
    Ibar = I.sum(axis=1)*dmu/2.0
    rc = 0.5*(st['r'][1:]+st['r'][:-1])
    amp = f*bump(rc)*cell_margin(st, l)
    s = dict(st); s['I'] = I + (amp*Ibar)[:, None]*p[None, :]
    return s

def run_member(delta, eps_s, l, a, cache_dir, eps_max=15.0, snap_eps=(), mode='uniform'):
    st = surface_state(delta, eps_s, cache_dir)
    if a == 0:
        s2 = st
    elif mode == 'bump':
        s2 = perturb_bump(st, l, a)
    else:
        s2 = perturb(st, l, a)
    s2 = dict(s2); s2['Imin'] = min(s2['Imin'], float(s2['I'].min()))
    return evolve(s2, eps_max=eps_max, snap_eps=snap_eps)
