# SCRIPT: CONN-ENERGY-STEVE-04  corrected scaling k/(aH) = k r_m * eps
import numpy as np
from scipy.optimize import brentq
G=np.array([5.90,5.33,4.20,2.65,1.17,0.39])/6.15; ed=np.array([.25,.5,1,2,4,8])
print('EP crossing (k r_m=2): kappa/H=(edec/eps)^3 equals (2/sqrt3)*2*eps')
print([round(brentq(lambda e:(x/e)**3-(4/np.sqrt(3))*e,1e-3,100),3) for x in ed], ' vs 0.811*edec^0.75 =',np.round(0.811*ed**0.75,3))
forms={'wall sqrt(1-3kap^2/4k^2)':lambda kap,k:np.sqrt(np.clip(1-0.75*kap**2/k**2,0,1)),
       'A k/(k+kappa)':lambda kap,k:k/(k+kap),'B exp(-kappa/k)':lambda kap,k:np.exp(-kap/k),'C 1-exp(-k/kappa)':lambda kap,k:1-np.exp(-k/kap)}
for lo in [1.0,0.1]:
  eps=np.linspace(lo,4,6001)
  for kr in [1.0,2.0]:
    for name,f in forms.items():
      for wname,wt in [('uniform',np.ones_like(eps)),('log',1/eps)]:
        pred=np.array([np.sum(f((e/eps)**3,kr*eps)*wt)/np.sum(wt) for e in ed]); err=np.max(np.abs(pred-G))
        print('win %.1f-4 k r_m=%.0f %-26s %-8s %s maxerr %.3f %s'%(lo,kr,name,wname,np.round(pred,3),err,'PASS' if err<=0.10 else ''))
