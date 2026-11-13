# SCRIPT: CONN-ENERGY-STEVE-02  viscous-side repair, forms fixed before the run
import numpy as np
G=np.array([5.90,5.33,4.20,2.65,1.17,0.39])/6.15
ed=np.array([.25,.5,1,2,4,8])
eps=np.linspace(1,4,3001)
forms={
 'A escape prob k/(k+kappa)':lambda kap,k: k/(k+kap),
 'B no-scatter crossing exp(-kappa/k)':lambda kap,k: np.exp(-kap/k),
 'C opposite 1-exp(-k/kappa)':lambda kap,k: 1-np.exp(-k/kap),
}
for kr in [1.0,2.0]:
  for name,f in forms.items():
    for wname,wt in [('uniform',np.ones_like(eps)),('log',1/eps)]:
      pred=np.array([np.sum(f((e/eps)**3, kr/eps)*wt)/np.sum(wt) for e in ed])
      err=np.max(np.abs(pred-G))
      print('k r_m=%.0f %-38s %-8s pred %s maxerr %.3f %s'%(kr,name,wname,np.round(pred,3),err,'PASS' if err<=0.10 else 'fail'))
print('Steve G', np.round(G,3))
