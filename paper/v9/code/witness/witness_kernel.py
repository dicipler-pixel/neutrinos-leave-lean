# SCRIPT: PBH-NU-WITNESS-KERNEL  exact block elimination: hidden source S = -ik B U_Q(t,s) Dh0 drives the whole retained difference
import os; os.environ['OMP_NUM_THREADS']='1'
import numpy as np, json, scipy.sparse as sp
from scipy.integrate import solve_ivp
EPS=0.5; DELTA=0.05; LM=60; N=LM+1
M=np.zeros((N,N))
for l in range(1,N): M[l,l-1]=M[l-1,l]=l/np.sqrt(4.0*l*l-1)
MQQ=M[1:,1:]; lam,V=np.linalg.eigh(MQQ); M01=M[0,1]
Sig=lambda t,n: -EPS**n/(n*t**n)            # Sig' = sigma
def full_Da(k,n,ts,L,tg,c):
    Q=np.diag(np.r_[0.0,np.ones(LM)])
    A=lambda t: -1j*k*M-(EPS**n/t**(n+1))*Q
    y0=np.zeros(N,complex); y0[L]=2*DELTA*c
    s=solve_ivp(lambda t,y:A(t)@y,(ts,tg[-1]),y0,method='BDF',jac=lambda t,y:A(t),t_eval=tg,rtol=1e-12,atol=1e-15)
    return s.y[0]
def memory_Da(k,n,ts,L,tg,c):
    # closed-form hidden propagator, no full-system solve
    h=tg[1]-tg[0]; Nt=len(tg); Sg=Sig(tg,n)
    Dh0=np.zeros(LM,complex); Dh0[L-1]=2*DELTA*c
    coef=V.T@Dh0
    S=-1j*k*M01*np.exp(-(Sg-Sg[0]))*((V[0,:]*coef)[None,:]*np.exp(-1j*k*np.outer(tg-ts,lam))).sum(1)
    g=M01**2*((V[0,:]**2)[None,:]*np.exp(-1j*k*np.outer(np.arange(Nt)*h,lam))).sum(1)   # g(t-r)
    a=np.zeros(Nt,complex); F=np.zeros(Nt,complex); F[0]=S[0]
    for i in range(Nt-1):
        j=np.arange(i+2); Kr=np.exp(-(Sg[i+1]-Sg[j]))*g[i+1-j]
        w=np.full(i+2,h); w[0]=w[-1]=h/2
        Jknown=np.sum((w*Kr*a[j])[:-1])
        # a_{i+1} = a_i + h/2 (F_i + S_{i+1} - k^2 (Jknown + w_last K_ii a_{i+1}))
        a[i+1]=(a[i]+h/2*(F[i]+S[i+1]-k*k*Jknown))/(1+h/2*k*k*w[-1]*Kr[-1])
        F[i+1]=S[i+1]-k*k*(Jknown+w[-1]*Kr[-1]*a[i+1])
    Sint=np.concatenate([[0],np.cumsum(h/2*(S[1:]+S[:-1]))])
    return a,Sint
out=[]
b=np.array([1.0,0.2,0.1]); c=1/np.sqrt(b@b+DELTA**2)
for (n,ratio,L,k) in [(3,1,3,2.0),(3,0.5,3,1.5),(6,1,4,3.0),(6,2,3,1.0)]:
    ts=ratio*EPS; row=dict(n=n,ratio=ratio,L=L,k=k)
    for h in (4e-3,2e-3,1e-3):
        tg=ts+np.arange(int(round((4.0-ts)/h))+1)*h
        ref=full_Da(k,n,ts,L,tg,c); a,Sint=memory_Da(k,n,ts,L,tg,c)
        err=np.max(abs(a-ref))/np.max(abs(ref))
        row['h=%g'%h]=dict(rel_err=float(err),max_Da=float(np.max(abs(ref))),
            src_only_rel=float(np.max(abs(Sint-ref))/np.max(abs(ref))))
        print(n,ratio,L,k,h,'max|Da|=%.3e  memory-vs-full rel err=%.2e  (source integral alone, no kernel: %.2e)'%(np.max(abs(ref)),err,row['h=%g'%h]['src_only_rel']),flush=True)
    out.append(row)
json.dump(out,open('witness_kernel.json','w'),indent=1)
