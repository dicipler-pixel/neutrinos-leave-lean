# SCRIPT: NU-V4-MEMORY-SPLIT  frozen memory form (w = 0.890, unchanged) with flux rate kappa1 and shear+ rate kappa2 = r kappa1
# Same object as PBH-NU-MEMORY-CURVE; the only change is the collision diagonal (0, 1, r, r, ...) in place of (0, 1, 1, 1, ...).
import numpy as np, json, sys
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
kn,kw=roots_legendre(36); kmin,kmax=0.25,9.0; ks=0.5*(kmax-kmin)*(kn+1)+kmin; wk=0.5*(kmax-kmin)*kw
wE=wk*ks**2*np.exp(-ks**2/2); wE/=wE.sum()
LM=60; M=np.zeros((LM+1,LM+1))
for l in range(1,LM+1): M[l,l-1]=M[l-1,l]=l/np.sqrt(4.0*l*l-1)
tau0=0.02; eg=np.linspace(tau0,6.0,1200); n=LM+1
def surv(k,ed,p,r):
    d=np.full(n,r); d[0]=0.0; d[1]=1.0
    def rhs(t,v):
        K=0.0 if ed is None else ed**p/t**(p+1)
        x,y=v[:n],v[n:]
        return np.concatenate([-K*d*x+k*(M@y),-K*d*y-k*(M@x)])
    v0=np.zeros(2*n); v0[0]=1
    s=solve_ivp(rhs,(tau0,eg[-1]),v0,method='BDF',t_eval=eg,rtol=1e-9,atol=1e-12)
    return s.y[0]**2+s.y[n]**2
f=lambda ed,p,r: sum(w_*surv(kk,ed,p,r) for kk,w_ in zip(ks,wE))
i17,i40=np.searchsorted(eg,1.7),np.searchsorted(eg,4.0); w=0.890; Ai=f(None,3,1.0)
out={}
for r in [0.25,4.0]:
    g=(1-f(2.0,3,r))/(1-Ai); G=float(w*g[i17]+(1-w)*g[i40]); out[str(r)]=G
    print(f'n=3 eps_dec=2 r=kappa2/kappa1={r}: Gamma12={(r-1)/(r+1):+.4f}  memory-form G={G:.4f}',flush=True)
json.dump(out,open('memory_split_b.json','w'))
