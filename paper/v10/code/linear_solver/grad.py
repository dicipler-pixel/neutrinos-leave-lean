# SCRIPT: LIN-FS-03  central first-max factor vs gradual decoupling kappa=H(eps_dec/eps)^3 (linear theory, Gaussian profile)
import numpy as np, time, sys
from multiprocessing import Pool
from lin import run, firstmax
xk,wk=np.polynomial.legendre.leggauss(28)
kmax=8.0
ks=0.5*kmax*(xk+1); ws=0.5*kmax*wk
T=np.linspace(0.1,4.0,586)
def job(a):
    Rnu,ed,k=a
    r=run(k,Rnu,ed,0.1,4.0,npts=len(T))
    return (-r['Delta'],-r['dpl'])
def centre(Rnu,ed,pool):
    out=pool.map(job,[(Rnu,ed,k) for k in ks])
    D=sum(w*k*k*np.exp(-k*k/4.)*o[0] for o,k,w in zip(out,ks,ws))/(2*np.pi**2)
    P=sum(w*k*k*np.exp(-k*k/4.)*o[1] for o,k,w in zip(out,ks,ws))/(2*np.pi**2)
    return D,P
if __name__=="__main__":
    t0=time.time()
    with Pool(4) as pool:
        pf=centre(0.0,None,pool); mp=[firstmax(T,x)[1] for x in pf]
        res=[]
        for ed in [None,0.25,0.5,1,2,4,8]:
            fs=centre(0.409,ed,pool)
            mf=[firstmax(T,x) for x in fs]
            sh=[100*(mp[i]/mf[i][1]-1) for i in range(2)]
            print("edec",ed,"Delta shift %.3f  dpl shift %.3f  tmax %.3f %.3f  t=%.0f"%(sh[0],sh[1],mf[0][0],mf[1][0],time.time()-t0),flush=True)
