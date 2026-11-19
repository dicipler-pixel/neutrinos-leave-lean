# SCRIPT: K1-THEOREM2-HYPOTHESIS-AUDIT
# Claim under test (paper Thm 2, Sec.6): a positive/nonnegative linear map sends any positive start to its Perron eigenvector, rate = gap,
# settle ~ 1/gap, exact tie => start decides. Does it apply to Steve's transport operator L = -i k mu - kappa (I-P)?
# H1: in the Fourier-Legendre basis L is NOT Metzler (has negative off-diagonals) and at kappa=0 has equal-modulus eigenvalue pairs
#     (the paper's swap-matrix case: no settling). H2: in the real-space mu-bin (finite-volume upwind) basis with vacuum outflow
#     the generator IS Metzler, so exp(tL) >= 0 and Perron/Krein-Rutman applies to the neutrino-intensity sector alone.
# WHY THIS PROVES WHAT IT CLAIMS: Metzler (off-diagonal >= 0) is the exact condition for exp(tA) >= 0 for all t; Perron needs it.
# KILL: H2 is dead if the real-space generator has any negative off-diagonal, or its leading eigenvalue is not real, or its leading
#     eigenvector is not one-signed. H1 is dead if the Fourier-Legendre generator is Metzler.
# OPPOSITE: the same audit on the coupled system (plasma delta, theta + neutrino hierarchy) - does a positive leader exist there?
import numpy as np
from numpy.linalg import eig, eigvals
# ---- H1: Fourier-Legendre generator, F_l' = k/(2l+1) [l F_{l-1} - (l+1) F_{l+1}] - sigma F_l (l>=1), F_0' = -k F_1/3*... use exact form
def FL(k,sig,N=40):
    A=np.zeros((N,N))
    for l in range(N):
        if l>0: A[l,l-1]= k*l/(2*l+1)
        if l<N-1: A[l,l+1]= -k*(l+1)/(2*l+1)
        if l>=1: A[l,l]-=sig
    return A
for sig in (0.0,1.0,5.0):
    A=FL(2.0,sig); off=A-np.diag(np.diag(A)); w=eigvals(A)
    print('H1 sigma=%.1f: negative off-diagonals %d of %d nonzero; max|Re| %.3f, # eigenvalues with Re>-1e-9: %d, imag parts of those: %s' %
          (sig,(off<0).sum(),(off!=0).sum(),np.max(w.real),(w.real>-1e-9).sum(), np.round(np.sort(np.abs(w[w.real>-1e-9].imag)),3)[:6]))
# ---- H2: real-space slab, vacuum boundaries, mu-bins, upwind
def slab(sig,Nx=80,Nm=16,W=2.0):
    dx=W/Nx; mu=(np.arange(Nm)+.5)/Nm*2-1; n=Nx*Nm; A=np.zeros((n,n)); idx=lambda i,m:i*Nm+m
    for i in range(Nx):
        for m in range(Nm):
            r=idx(i,m); c=mu[m]/dx
            A[r,r]-=abs(c)
            if c>0 and i>0: A[r,idx(i-1,m)]+=c
            if c<0 and i<Nx-1: A[r,idx(i+1,m)]+=-c
            A[r,r]-=sig
            for m2 in range(Nm): A[r,idx(i,m2)]+=sig/Nm
    return A
for sig in (0.0,0.5,2.0,10.0,40.0):
    A=slab(sig); off=A-np.diag(np.diag(A)); met=(off>=-1e-14).all()
    w,V=eig(A); i0=np.argmax(w.real); v=V[:,i0].real; w0=w[i0]
    oneSigned=(v>=-1e-9*np.abs(v).max()).all() or (v<=1e-9*np.abs(v).max()).all()
    ws=np.sort(w.real)[::-1]; gap=ws[0]-ws[1]
    diff=-(np.pi/(2.0+2*0.7104/sig))**2/(3*sig) if sig>0 else np.nan
    print('H2 sigma=%5.1f: Metzler %s | lead eig %.4f%+.1e i | one-signed %s | 2nd real part %.4f (gap %.4f) | diffusion-limit estimate %.4f'%(sig,met,w0.real,w0.imag,oneSigned,ws[1],gap,diff))
# ---- OPPOSITE: coupled gravity-free system (plasma delta,theta + neutrinos), k=2, constant sigma
def coupled(k,sig,R=0.409,N=30):
    # state: dg, tg, F0..F_{N-1} ; F_l normalised so F0=delta_nu, F1=(4/3)theta_nu/k
    n=2+N; A=np.zeros((n,n)); iF=lambda l:2+l
    A[0,1]=-4/3; A[1,0]=k*k/4
    A[1,iF(1)]+=sig*R/(1-R)*(3*k/4); A[1,1]-=sig*R/(1-R)           # theta_nu = 3k F1/4
    A[iF(0),iF(1)]=-k
    for l in range(1,N):
        A[iF(l),iF(l-1)]+=k*l/(2*l+1)
        if l<N-1: A[iF(l),iF(l+1)]+=-k*(l+1)/(2*l+1)
        A[iF(l),iF(l)]-=sig
    A[iF(1),1]+=sig*4/(3*k)                                        # relax to plasma velocity
    return A
for sig in (0.0,1.0,100.0):
    w=eigvals(coupled(2.0,sig)); top=w[np.argsort(-w.real)][:4]
    print('OPP coupled sigma=%.0f: leading eigenvalues'%sig,np.round(top,3))
