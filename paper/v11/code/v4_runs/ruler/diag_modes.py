# SCRIPT: NU-V4-RULER-DIAG  per-k diagnostics: least-damped pair, real-part gap (correct sign), Petermann size, principal angle at r = 1.2 and 1/1.2
import numpy as np, math
from scipy.special import roots_legendre
n=61; M=np.zeros((n,n))
for l in range(1,n): M[l,l-1]=M[l-1,l]=l/np.sqrt(4.0*l*l-1)
kn,kw=roots_legendre(36); ks=0.5*(9.0-0.25)*(kn+1)+0.25; wk=0.5*(9.0-0.25)*kw; wE=wk*ks**2*np.exp(-ks**2/2); wE/=wE.sum()
KAP=0.958
def modes(k,r):
    d=np.full(n,r); d[0]=0; d[1]=1
    L=-1j*k*M-KAP*np.diag(d); ev,R=np.linalg.eig(L); Lf=np.linalg.inv(R); o=np.argsort(-ev.real); ev,R,Lf=ev[o],R[:,o],Lf[o,:]
    pair=[0,1] if abs(ev[0].imag)>1e-9 and abs(ev[0].real-ev[1].real)<1e-7 else [0]
    m=len(pair); P=sum(np.outer(R[:,i],Lf[i,:]) for i in pair)
    gap=ev[0].real-ev[m].real; pet=np.linalg.norm(P)**2/m
    U=np.linalg.svd(P)[0][:,:m]
    return ev[:3],gap,pet,U,abs(R[0,0])**2/np.sum(abs(R[:,0])**2)
print(' k     w      ev0 (r=1)              gap    Petermann  w0(l=0)  angle(1.2) angle(1/1.2)')
for k,w in zip(ks,wE):
    e1,g1,p1,U1,w0=modes(k,1.0); e2,g2,p2,U2,_=modes(k,1.2); e3,g3,p3,U3,_=modes(k,1/1.2)
    ang=lambda A,B: math.sqrt(np.sum(np.arccos(np.clip(np.linalg.svd(A.conj().T@B,compute_uv=False),0,1))**2))
    print(f'{k:5.2f} {w:.4f}  {e1[0]:+.4f}  {g1:7.4f} {p1:9.2f} {w0:7.3f}  {ang(U1,U2):8.4f} {ang(U1,U3):8.4f}')
