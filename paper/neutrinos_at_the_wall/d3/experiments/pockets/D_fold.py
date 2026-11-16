# AGENT D (odd): run the moment chain straight THROUGH the fold eta=0 with a collision rate even in eta, sigma=s0*eta^2 + floor,
# and plant a pocket; compare what returns on the mirror side for even vs odd angular structure (parity under mu -> -mu)
import numpy as np
from scipy.integrate import solve_ivp
L,k=30,1.5
c=np.array([(l+1)/np.sqrt((2*l+1)*(2*l+3)) for l in range(L)]); M=np.diag(c[:L-1],1)+np.diag(c[:L-1],-1)
for name,sig in [("hot at the fold (sigma = 50/(eta²+0.05))",lambda e:50/(e*e+0.05)),("cold at the fold (sigma = 0.5 e²)",lambda e:0.5*e*e)]:
    for l0 in [3,4]:
        def f(e,v): D=np.r_[0,[sig(e)]*(L-1)]; return (-1j*k*M-np.diag(D))@v
        v0=np.zeros(L,complex); v0[l0]=1
        s=solve_ivp(f,(-2,2),v0,method='BDF',rtol=1e-8,atol=1e-11); v=s.y[:,-1]
        print(f" {name}, planted l={l0}: |kept l=0| {abs(v[0]):.2e}, |l={l0}| {abs(v[l0]):.2e}, total norm {np.linalg.norm(v):.2e}")
