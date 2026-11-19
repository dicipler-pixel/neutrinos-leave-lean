# SCRIPT: WB-LIN-MODULE (solver copied verbatim from WB-STEVE-02-LINEAR)
import numpy as np
from scipy.integrate import solve_ivp
LMAX = 48
Rn_default = 0.409

def run_mode(k, tau0, tau_grid, Rn, eps_dec, lmax=LMAX, rtol=1e-9):
    """eps_dec=None: neutrinos free-stream (kappa=0) from tau0. eps_dec=inf: perfect fluid. otherwise gradual."""
    n = 4+(lmax-1); LS = np.arange(3, lmax+1)
    def Kc(t):
        if eps_dec is None: return 0.0
        return eps_dec**3/t**4
    def rhs(t, y):
        dg, tg, dn, tn = y[:4]; F = np.zeros(lmax+2); F[2:lmax+1] = y[4:]
        F[lmax+1] = (2*lmax+1)/(k*t)*F[lmax]-F[lmax-1]
        th = (1-Rn)*tg+Rn*tn; de = (1-Rn)*dg+Rn*dn; sg = F[2]/2
        Dl = de+4*th/(k*k*t)
        phi = -1.5*Dl/(k*t)**2; psi = phi-6*Rn*sg/(k*t)**2
        dphi = -psi/t+2*th/(k*k*t*t)
        K = Kc(t); dy = np.empty_like(y)
        dy[0] = -4/3*tg+4*dphi
        dy[1] = k*k*dg/4+k*k*psi-K*(Rn/(1-Rn))*(tg-tn) if Rn < 1 else 0
        dy[2] = -4/3*tn+4*dphi
        dy[3] = k*k*(dn/4-sg)+k*k*psi+K*(tg-tn)
        dy[4] = 8/15*tn-0.6*k*F[3]-K*F[2]
        dy[5:] = k/(2*LS+1)*(LS*F[2:lmax]-(LS+1)*F[4:lmax+2])-K*F[3:lmax+1]
        return dy
    psi0 = phi0 = 2/3; d0 = -2*psi0-(2/3)*(k*tau0)**2*phi0; t0 = 0.5*k*k*tau0*psi0
    y0 = np.zeros(n); y0[:4] = [d0, t0, d0, t0]
    sol = solve_ivp(rhs, (tau0, tau_grid[-1]), y0, method='BDF', t_eval=tau_grid, rtol=rtol, atol=1e-13)
    assert sol.success, sol.message
    Y = sol.y; th = (1-Rn)*Y[1]+Rn*Y[3]; de = (1-Rn)*Y[0]+Rn*Y[2]
    Delta = de+4*th/(k*k*tau_grid)
    return Delta, Y

def first_max(x, y):
    # first local maximum of -Delta (positive overdensity convention), parabolic refinement
    s = -y
    for i in range(1, len(s)-1):
        if s[i] > s[i-1] and s[i] >= s[i+1]:
            a, b, c = s[i-1], s[i], s[i+1]; den = a-2*b+c
            off = 0.5*(a-c)/den if den != 0 else 0
            return x[i]+off*(x[1]-x[0]), b-0.25*(a-c)*off
    return np.nan, np.nan

