# AGENT F: McCormick's self-scattering leaves the neutrino flux undamped by nu-nu; only plasma drag kappa_e removes it.
# Does strong self-scattering SEAL the flux pocket (Zeno), so it survives longer than plasma drag alone would allow?
import numpy as np
def chain(L,k,D):
    c=np.array([(l+1)/np.sqrt((2*l+1)*(2*l+3)) for l in range(L)]); M=np.diag(c[:L-1],1)+np.diag(c[:L-1],-1); return -1j*k*M-np.diag(D),c
L,k,ke=40,1.0,0.02
for kn in [0,1,3,10,30,100]:
    D=np.r_[0,ke,[ke+kn]*(L-2)]; Lm,c=chain(L,k,D); w=np.linalg.eigvals(Lm)
    w=sorted(w,key=lambda z:-z.real)
    print(f" self-scatter kappa_n={kn:4d}: two slowest (sound pair) Re = {w[0].real:+.5f}, {w[1].real:+.5f}; next {w[2].real:+.5f}")
print("Reading: with strong self-scattering the density+flux pair (sound) decays at ~ kappa_e/2 + k²c1²/(2 kappa_n): the shear layer seals the flux.")
