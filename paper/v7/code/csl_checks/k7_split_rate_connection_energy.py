# SCRIPT: K7-SPLIT-RATE-NONNORMALITY
# Steve open item (c): collision terms beyond one relaxation time (momentum-transfer rate k1 for l=1, total rate k2 for l>=2).
# Paper App A.1 (connection energy = (1/8)||[L,L^dag]||_F^2) extended to L = -i k mu - D, D = diag(0,k1,k2,k2,...) in the orthonormal Legendre basis.
# Derivation (written first): [L,L^dag] = 2i[K,D]; K_{l,l+1} = k (l+1)/sqrt((2l+1)(2l+3)); ||[K,D]||^2 = 2 sum K_{l,l+1}^2 (d_{l+1}-d_l)^2, so
#   E = (1/8)*4*2*sum = sum_l K_{l,l+1}^2 (d_{l+1}-d_l)^2 = k^2 k1^2/3 + (4 k^2/15)(k2-k1)^2        (only the 0-1 and 1-2 links carry it).
# KILL: numeric Frobenius norm differs from this closed form by > 1e-10 relative for any of 200 random (k,k1,k2,Nmax).
import numpy as np
rng=np.random.default_rng(7); worst=0
for _ in range(200):
    k=rng.uniform(.2,5); k1=rng.uniform(0,5); k2=rng.uniform(0,5); N=int(rng.integers(6,30))
    K=np.zeros((N,N))
    for l in range(N-1): K[l,l+1]=K[l+1,l]=k*(l+1)/np.sqrt((2*l+1)*(2*l+3))
    d=np.array([0,k1]+[k2]*(N-2)); L=-1j*K-np.diag(d)
    C=L@L.conj().T-L.conj().T@L; E=np.linalg.norm(C)**2/8
    Ec=k*k*k1**2/3+4*k*k*(k2-k1)**2/15; worst=max(worst,abs(E-Ec)/Ec)
print('worst relative error of closed form over 200 cases: %.1e  -> KILL %s'%(worst,'FIRED' if worst>1e-10 else 'did not fire'))
for r in (1.0,0.5,2.0,1.5):
    k1=1.0;k2=r; print('k2/k1=%.1f: share of non-normality in the 0-1 (flux) link %.3f, in the 1-2 (shear) link %.3f'%(r,(1/3)/((1/3)+4*(r-1)**2/15),(4*(r-1)**2/15)/((1/3)+4*(r-1)**2/15) if r!=1 else 0))
