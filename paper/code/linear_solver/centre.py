# SCRIPT: LIN-FS-02  central density first-maximum factor for the Gaussian profile, vs decoupling time
import numpy as np, sys, time
from lin import run, firstmax
xk,wk=np.polynomial.legendre.leggauss(36)
kmax=9.0
ks=0.5*kmax*(xk+1); ws=0.5*kmax*wk
T=np.linspace(0.1,4.0,781)
def centre(Rnu,eps_dec,key):
    tot=np.zeros_like(T); 
    for k,w in zip(ks,ws):
        r=run(k,Rnu,eps_dec,0.1,4.0,npts=len(T))
        tot+=w*k*k*np.exp(-k*k/4.)*(-r[key])/(2*np.pi**2)
    return tot
if __name__=="__main__":
    t0=time.time()
    res={}
    for key in ['Delta','dpl']:
        pf=centre(0.0,None,key); fs=centre(0.409,None,key)
        mp=firstmax(T,pf); mf=firstmax(T,fs)
        print(key,'pf',mp,'fs',mf,'factor',mf[1]/mp[1],'implied shift %',100*(mp[1]/mf[1]-1),time.time()-t0,flush=True)
