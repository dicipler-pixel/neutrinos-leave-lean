# SCRIPT: PBH-NU-IDENTITIES  checks of every derived identity used in the paper
# Kill conditions (written first): each identity must hold to 1e-10 relative, else the statement is withdrawn.
import numpy as np
from scipy.integrate import quad
LM=80
c=lambda l:(l+1)/np.sqrt((2*l+1)*(2*l+3))          # <l+1|mu|l> in the normalised Legendre basis
Mu=np.zeros((LM+1,LM+1))
for l in range(LM): Mu[l,l+1]=Mu[l+1,l]=c(l)
def L_op(k,k1,k2):
    D=np.diag([0.0,-k1]+[-k2]*(LM-1)); A=-1j*k*Mu; return A,D,A+D
fro2=lambda X:np.sum(np.abs(X)**2)
print('I1  single rate: (1/8)|[L,L*]|^2 = kappa^2 k^2/3')
for k,kap in [(1.0,0.3),(2.0,1.5),(0.7,4.0)]:
    A,D,L=L_op(k,kap,kap); lhs=fro2(L@L.conj().T-L.conj().T@L)/8
    print('    k=%.1f kappa=%.1f  lhs=%.12f  rhs=%.12f'%(k,kap,lhs,kap**2*k**2/3))
print('I2  split rates: (1/8)|[L,L*]|^2 = k^2 k1^2/3 + (4k^2/15)(k2-k1)^2')
for k,k1,k2 in [(1.0,0.3,2.0),(2.0,1.5,0.4),(0.7,4.0,9.0)]:
    A,D,L=L_op(k,k1,k2); lhs=fro2(L@L.conj().T-L.conj().T@L)/8
    print('    k=%.1f k1=%.1f k2=%.1f lhs=%.12f rhs=%.12f'%(k,k1,k2,lhs,k**2*k1**2/3+4*k**2/15*(k2-k1)**2))
print('I3  weight across the cut: |P (k mu) (1-P)|^2 = k^2/3, so sqrt(E_B) = k/sqrt3 = c_s k')
P=np.zeros((LM+1,LM+1)); P[0,0]=1; Q=np.eye(LM+1)-P
for k in [1.0,2.5]: print('    k=%.1f  E_B=%.12f  k^2/3=%.12f'%(k,fro2(P@(k*Mu)@Q),k**2/3))
print('I4  monopole propagator <0|(s+i k mu+kappa(1-P))^-1|0> = g/(1-kappa g), g=arctan(k/(s+kappa))/k')
for k,kap,s in [(1.0,0.5,0.3),(3.0,2.0,0.1),(0.5,0.2,1.0)]:
    Lfull=s*np.eye(LM+1)+1j*k*Mu+kap*Q; num=np.linalg.solve(Lfull,np.eye(LM+1)[:,0])[0]
    g=np.arctan(k/(s+kap))/k; print('    k=%.1f kappa=%.1f s=%.1f  matrix=%.12f  closed=%.12f'%(k,kap,s,num.real,(g/(1-kap*g))))
print('I5  two-moment truncation: eigenvalues of [[0,-ik/sqrt3],[-ik/sqrt3,-kappa]] merge at kappa=2k/sqrt3')
k=1.0; kap=2*k/np.sqrt(3); ev=np.linalg.eigvals(np.array([[0,-1j*k/np.sqrt(3)],[-1j*k/np.sqrt(3),-kap]])); print('    eigenvalues',np.round(ev,10))
