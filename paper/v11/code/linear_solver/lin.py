# SCRIPT: LIN-FS-01  linear free-streaming + relaxation collisions, radiation era, Newtonian gauge (Ma-Bertschinger)
import numpy as np
from scipy.integrate import solve_ivp
LMAX=36
def build(k,Rnu,eps_dec,r_m=1.0):
    n=4+(LMAX-1)  # dg,tg,dn,tn,F2..FLMAX
    iF=lambda l:4+(l-2)
    def A(t):
        M=np.zeros((n,n))
        kt2=(k*t)**2
        # phi, thetaT, deltaT, sigma as linear functionals
        dT=np.zeros(n); dT[0]=1-Rnu; dT[2]=Rnu
        thT=np.zeros(n); thT[1]=1-Rnu; thT[3]=Rnu
        sig=np.zeros(n); sig[iF(2)]=0.5
        phi=-1.5/kt2*(dT+4*thT/(k*k*t))
        psi=phi-6*Rnu*sig/kt2
        phid=-psi/t+2*thT/(t*t*k*k)
        aK=0.0 if eps_dec is None else (1.0/t)*((eps_dec*r_m/t)**3)
        M[0]=4*phid; M[0,1]+=-4/3.
        M[1]=k*k*psi; M[1,0]+=k*k/4
        if Rnu>0:
            c=aK*Rnu/(1-Rnu); M[1,3]+=c; M[1,1]+=-c
        M[2]=4*phid; M[2,3]+=-4/3.
        M[3]=k*k*psi; M[3,2]+=k*k/4; M[3]-=k*k*sig; M[3,3]+=-aK; M[3,1]+=aK
        # F2
        M[iF(2),3]+=8/15.; M[iF(2),iF(3)]+=-0.6*k; M[iF(2),iF(2)]+=-aK
        for l in range(3,LMAX+1):
            r=iF(l)
            M[r,iF(l-1)]+=k*l/(2*l+1.)
            if l<LMAX: M[r,iF(l+1)]+=-k*(l+1)/(2*l+1.)
            else:
                # closure F_{L+1}=(2L+1)/(k t) F_L - F_{L-1}
                M[r,iF(l)]+=-k*(l+1)/(2*l+1.)*((2*l+1)/(k*t)); M[r,iF(l-1)]+=k*(l+1)/(2*l+1.)
            M[r,r]+=-aK
        return M,dT,thT,phi
    return n,A
def run(k,Rnu,eps_dec,t0,tmax,r_m=1.0,npts=400):
    n,A=build(k,Rnu,eps_dec,r_m)
    zeta=1.0; psi0=2/3.*zeta
    th0=0.5*k*k*t0*psi0
    d0=-2*psi0-(2/3.)*(k*t0)**2*psi0
    y0=np.zeros(n); y0[0]=d0; y0[1]=th0; y0[2]=d0; y0[3]=th0
    f=lambda t,y:A(t)[0]@y
    J=lambda t,y:A(t)[0]
    ts=np.linspace(t0,tmax,npts)
    s=solve_ivp(f,(t0,tmax),y0,method='Radau',jac=J,t_eval=ts,rtol=1e-8,atol=1e-11)
    Y=s.y; out={}
    dT=(1-Rnu)*Y[0]+Rnu*Y[2]; thT=(1-Rnu)*Y[1]+Rnu*Y[3]
    out['t']=s.t
    out['Delta']=dT+4*thT/(k*k*s.t)           # zero-momentum slices
    out['dpl']=dT+4*Y[1]/(k*k*s.t)            # plasma-orthogonal slices
    return out
def firstmax(t,y):
    i=np.where((y[1:-1]>y[:-2])&(y[1:-1]>=y[2:]))[0]
    if len(i)==0: return None
    j=i[0]+1
    # parabolic refinement
    a,b,c=y[j-1],y[j],y[j+1]
    d=0.5*(a-c)/(a-2*b+c); return t[j]+d*(t[1]-t[0]), b-0.25*(a-c)*d
if __name__=="__main__":
    # validation: single mode, nu decoupled from start (instant) vs perfect fluid
    for k in [1.0]:
        for Rnu in [0.409,0.488]:
            pf=run(k,0.0,None,0.01/k,12/k)
            fs=run(k,Rnu,None,0.01/k,12/k)
            for key in ['Delta','dpl']:
                m1=firstmax(pf['t'],pf[key]); m2=firstmax(fs['t'],fs[key])
                print(k,Rnu,key,m1,m2,'ratio',m2[1]/m1[1])
