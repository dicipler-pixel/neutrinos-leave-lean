# SCRIPT: PBH-NU-MEMORY-CURVE  kept-sector survival (memory form) curves for the figures; same object as WB-STEVE-07
import numpy as np, json
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
kn,kw=roots_legendre(36); kmin,kmax=0.25,9.0; ks=0.5*(kmax-kmin)*(kn+1)+kmin; wk=0.5*(kmax-kmin)*kw
wE=wk*ks**2*np.exp(-ks**2/2); wE/=wE.sum()
LM=60; M=np.zeros((LM+1,LM+1))
for l in range(1,LM+1): M[l,l-1]=M[l-1,l]=l/np.sqrt(4.0*l*l-1)
tau0=0.02; eg=np.linspace(tau0,6.0,1200); n=LM+1; P=np.zeros(n); P[0]=1
def surv(k,ed,p):
    def rhs(t,v):
        K=0.0 if ed is None else ed**p/t**(p+1)
        x,y=v[:n],v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M@y),-K*(1-P)*y-k*(M@x)])
    v0=np.zeros(2*n); v0[0]=1
    s=solve_ivp(rhs,(tau0,eg[-1]),v0,method='BDF',t_eval=eg,rtol=1e-9,atol=1e-12)
    return s.y[0]**2+s.y[n]**2
f=lambda ed,p: sum(w_*surv(kk,ed,p) for kk,w_ in zip(ks,wE))
i17,i40=np.searchsorted(eg,1.7),np.searchsorted(eg,4.0); w=0.890; Ai=f(None,3)
out={}
for p,eds in [(3,[0.25,0.5,0.75,1,1.5,2,3,4,6,8]),(6,[0.5,1,1.5,2,3,4])]:
    for ed in eds:
        g=(1-f(ed,p))/(1-Ai); out['%d_%g'%(p,ed)]=dict(first_max=float(g[i17]),two_epoch=float(w*g[i17]+(1-w)*g[i40]))
        print(p,ed,round(g[i17],3),round(w*g[i17]+(1-w)*g[i40],3),flush=True)
json.dump(out,open('memory_curve.json','w'))
