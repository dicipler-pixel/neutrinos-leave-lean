# SCRIPT: A5-CHAIN-LIB  linear angular chain (v5.1 memory_curve / witness object) in the real basis w_l = i^l v_l
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, scipy.sparse as sp
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre

kn, kw = roots_legendre(36); KMIN, KMAX = 0.25, 9.0
KS = 0.5*(KMAX-KMIN)*(kn+1)+KMIN; WK = 0.5*(KMAX-KMIN)*kw
WE = WK*KS**2*np.exp(-KS**2/2); WE /= WE.sum()
TAU0 = 0.02

def cl(l):
    return (l+1)/np.sqrt((2*l+1)*(2*l+3))

def Kreal(LM):
    """real generator of streaming in w basis: dw/dt = k K w;  K[l,l-1]=c_{l-1}, K[l-1,l]=-c_{l-1}"""
    N = LM+1; K = np.zeros((N, N))
    for l in range(1, N):
        K[l, l-1] = cl(l-1); K[l-1, l] = -cl(l-1)
    return K

def sigma_powerlaw(ed, n):
    return lambda t: ed**n/t**(n+1)

def Sigma_powerlaw(ed, n):   # antiderivative, Sigma' = sigma
    return lambda t: -ed**n/(n*t**n)

def reversed_in_window(sig, ta, tb):
    def s(t):
        return sig(ta+tb-t) if ta <= t <= tb else sig(t)
    return s

def damp_vec(LM, r=1.0, shear_only=False):
    d = np.ones(LM+1); d[0] = 0.0
    if shear_only:
        d[2] = r
    else:
        d[2:] = r
    return d

def evolve(k, sig, LM, tgrid, w0=None, breaks=(), dvec=None, rtol=1e-9, atol=1e-12, t0=TAU0):
    """exact (truncated at LM) chain; returns w[l, t] on tgrid (real basis). sig(t) scalar rate; dvec diag pattern."""
    N = LM+1; K = sp.csr_matrix(Kreal(LM)*k)
    d = np.r_[0.0, np.ones(LM)] if dvec is None else dvec
    Dm = sp.diags(d, format='csr')
    if w0 is None:
        w0 = np.zeros(N); w0[0] = 1.0
    jac = lambda t, y: (K - sig(t)*Dm)
    rhs = lambda t, y: K@y - sig(t)*(d*y)
    edges = [t0]+[b for b in breaks if t0 < b < tgrid[-1]]+[tgrid[-1]]
    out = np.zeros((N, len(tgrid))); y = np.array(w0, float)
    for a, b in zip(edges[:-1], edges[1:]):
        m = (tgrid >= a) & (tgrid <= b) if b == edges[-1] else (tgrid >= a) & (tgrid < b)
        te = np.unique(np.r_[tgrid[m], b])
        s = solve_ivp(rhs, (a, b), y, method='BDF', jac=jac, t_eval=te, rtol=rtol, atol=atol)
        assert s.success, s.message
        out[:, m] = s.y[:, np.searchsorted(te, tgrid[m])]
        y = s.y[:, -1]
    return out

def to_complex(w):
    """v_l = (-i)^l w_l"""
    l = np.arange(w.shape[0])
    return ((-1j)**l)[:, None]*w if w.ndim == 2 else ((-1j)**l)*w
