# AGENT E (odd): an undamped 'pocket' moment l* inside a heavily damped layer. Does a hotter layer protect it better? (Zeno)
import numpy as np
from scipy.linalg import expm
def chain(L,k,D):
    c=np.array([(l+1)/np.sqrt((2*l+1)*(2*l+3)) for l in range(L)]); M=np.diag(c[:L-1],1)+np.diag(c[:L-1],-1); return -1j*k*M-np.diag(D),c
L,k,ls=30,1.0,5
print("pocket at l*=5, every other l>=1 damped at sigma (the 'normal layer'), density l=0 conserved")
for s in [1,3,10,30,100,300]:
    D=np.r_[0,[s]*(L-1)]; D[ls]=0; Lm,c=chain(L,k,D)
    w=np.linalg.eigvals(Lm); slow=sorted(w,key=lambda z:-z.real)
    v=np.zeros(L,complex); v[ls]=1; P=np.abs(expm(Lm*10.0)@v)[ls]**2
    pred=k*k*(c[ls-1]**2+c[ls]**2)/s
    print(f" sigma={s:5d}: pocket survival after t=10: {P:.4f}; slowest nonzero decay {-sorted([z.real for z in w])[-2]:.5f}; Zeno estimate k²(c²+c²)/σ = {pred:.5f}")
print("Reading: leak rate falls like 1/sigma - the hotter the surrounding layer, the better the pocket is sealed.")
