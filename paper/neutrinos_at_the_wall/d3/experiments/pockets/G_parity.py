# AGENT G (odd, follow-up of D): even vs odd hidden structure through a cold fold, many planted moments and k values
import numpy as np
from scipy.integrate import solve_ivp
L=36
c=np.array([(l+1)/np.sqrt((2*l+1)*(2*l+3)) for l in range(L)]); M=np.diag(c[:L-1],1)+np.diag(c[:L-1],-1)
sig=lambda e:0.5*e*e
for k in [0.8,1.5,2.5]:
    row=[]
    for l0 in [2,3,4,5,6,7]:
        f=lambda e,v:(-1j*k*M-np.diag(np.r_[0,[sig(e)]*(L-1)]))@v
        v0=np.zeros(L,complex); v0[l0]=1; v=solve_ivp(f,(-2,2),v0,method='BDF',rtol=1e-8,atol=1e-11).y[:,-1]
        row.append(f"l{l0}:{abs(v[l0]):.1e}")
    print(f" k={k}: planted moment returned to itself on the mirror side -> "+"  ".join(row))
