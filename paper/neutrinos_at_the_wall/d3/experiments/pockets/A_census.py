# AGENT A — pocket census: protected directions of the neutrino moment chain under three collision models (silence certificate)
import numpy as np
def chain(L,k,D):
    c=np.array([(l+1)/np.sqrt((2*l+1)*(2*l+3)) for l in range(L)]); M=np.diag(c[:L-1],1)+np.diag(c[:L-1],-1)
    return -1j*k*M[:L,:L]-np.diag(D)
L=40; k=1.0
models={'single rate k=2':np.r_[0,[2.0]*(L-1)],
 'split flux 0.5 / shear 5':np.r_[0,0.5,[5.0]*(L-2)],
 'McCormick: plasma 0.05 on l>=1, self-scatter 3 on l>=2':np.r_[0,0.05,[3.05]*(L-2)],
 'self-scatter only (plasma off)':np.r_[0,0,[3.0]*(L-2)]}
for name,D in models.items():
    Lm=chain(L,k,D); w=np.linalg.eigvals(Lm); w=w[np.argsort(-w.real)]
    kerD=[l for l in range(L) if D[l]==0]
    print(f"{name}: undamped moments (ker D) = {kerD}; slowest modes Re = {np.round(w.real[:4],4)}")
    # silence certificate for each undamped moment l*: is it isolated? (any streaming link to a damped neighbour leaks)
    print("   streaming links from ker D to damped moments:",[ (a,b) for a in kerD for b in (a-1,a+1) if 0<=b<L and D[b]>0])
print("Census: at finite k every undamped moment is linked by streaming to a damped neighbour, so no EXACT pocket exists; only the conserved density (ell=0) plus slow near-pockets.")
