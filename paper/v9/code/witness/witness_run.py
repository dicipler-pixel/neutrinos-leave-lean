# SCRIPT: PBH-NU-WITNESS-RUN  matched retained-state witness in the kept-sector model (same object as memory_curve.py)
import os, sys, json, time
os.environ['OMP_NUM_THREADS']='1'
import numpy as np, scipy.sparse as sp
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre, eval_legendre
kn,kw=roots_legendre(36); kmin,kmax=0.25,9.0; ks=0.5*(kmax-kmin)*(kn+1)+kmin; wk=0.5*(kmax-kmin)*kw
wE=wk*ks**2*np.exp(-ks**2/2); wE/=wE.sum()
EPS=0.5; DELTA=0.05; TEP=[1.7,4.0,6.0]
def Mmat(LM):
    d=np.array([l/np.sqrt(4.0*l*l-1) for l in range(1,LM+1)])
    return sp.diags([d,d],[-1,1],format='csr')
def evolve(k,n,ts,LM,rtol,atol,cols):
    N=LM+1; M=Mmat(LM); Q=sp.diags(np.r_[0.0,np.ones(LM)],format='csr'); I=sp.identity(len(cols),format='csr')
    def A(t): return (-1j*k*M - (EPS**n/t**(n+1))*Q)
    def rhs(t,y): return (A(t)@y.reshape(len(cols),N).T).T.ravel()
    def jac(t,y): return sp.kron(I,A(t),format='csc')
    Y0=np.zeros((len(cols),N),complex)
    for j,c in enumerate(cols): Y0[j,:len(c)]=c
    tg=np.unique(np.r_[np.geomspace(ts,6.0,500),TEP])
    s=solve_ivp(rhs,(ts,6.0),Y0.ravel(),method='BDF',t_eval=tg,jac=jac,rtol=rtol,atol=atol)
    assert s.success, s.message
    return s.t, s.y.reshape(len(cols),N,-1)   # [col, l, t]
def positivity(v):
    mu=np.linspace(-1,1,2001)
    return float(min(sum(v[l]*np.sqrt((2*l+1)/2)*eval_legendre(l,mu) for l in range(len(v)))))
def run(n,ratio,L,LM=60,rtol=1e-9,atol=1e-12):
    ts=ratio*EPS; b=np.array([1.0,0.2,0.1,0,0]); e=np.zeros(5); e[L]=1
    c=1/np.sqrt(b@b+DELTA**2)
    pos=(positivity(c*(b+DELTA*e)),positivity(c*(b-DELTA*e)))
    rows={tt:dict(dret=0.0,bret=0.0,Ap=0.0,Am=0.0,Fp=0.0,Fm=0.0) for tt in TEP}
    worst=0.0; worstN=0.0
    for k,w in zip(ks,wE):
        t,Y=evolve(k,n,ts,LM,rtol,atol,[c*b,c*DELTA*e])
        U_b,U_d=Y[0],Y[1]
        for sgn in (1,-1):
            v=U_b+sgn*U_d; A=np.abs(v[0])**2; Ap=2*np.real(np.conj(v[0])*(-1j*k*(1/np.sqrt(3))*v[1]))
            Nrm=np.sum(np.abs(v)**2,axis=0)
            den=4*(k*k/3)*A*(1-A); ok=den>1e-300
            worst=max(worst,float(np.max(Ap[ok]**2/den[ok])))
            denN=4*(k*k/3)*A*(Nrm-A); ok=denN>1e-300
            worstN=max(worstN,float(np.max(Ap[ok]**2/denN[ok])))
        for tt in TEP:
            i=np.argmin(abs(t-tt)); r=rows[tt]
            r['dret']+=w*np.sum(np.abs(2*U_d[:3,i])**2); r['bret']+=w*np.sum(np.abs(U_b[:3,i])**2)
            vp=U_b[:,i]+U_d[:,i]; vm=U_b[:,i]-U_d[:,i]
            r['Ap']+=w*abs(vp[0])**2; r['Am']+=w*abs(vm[0])**2; r['Fp']+=w*abs(vp[1])**2; r['Fm']+=w*abs(vm[1])**2
    res={}
    for tt in TEP:
        r=rows[tt]
        res[str(tt)]=dict(R_ret=float(np.sqrt(r['dret']/r['bret'])),
            R_A=float(abs(r['Ap']-r['Am'])/(0.5*(r['Ap']+r['Am']))),
            R_F=float(abs(r['Fp']-r['Fm'])/(0.5*(r['Fp']+r['Fm']))))
    return dict(n=n,ratio=ratio,tau_s=ts,L=L,LM=LM,rtol=rtol,pos_min=pos,bound_worst=worst,bound_worst_N=worstN,res=res)
if __name__=='__main__':
    mode=sys.argv[1]; out=[]
    if mode=='prod':
        jobs=[(n,r,L) for n in (3,6) for r in (0.1,0.25,0.5,1,2) for L in (3,4,1,2)]
        kw_={}
    else:
        jobs=[(n,r,L) for n in (3,6) for r in (0.5,1,2) for L in (3,4)]
        kw_=dict(LM=120) if mode=='convLM' else dict(rtol=1e-11,atol=1e-14)
    for j in jobs:
        t0=time.time(); d=run(*j,**kw_); out.append(d)
        print(j,'%.1fs'%(time.time()-t0),' '.join('%s:%.3e/%.3e/%.3e'%(tt,v['R_ret'],v['R_A'],v['R_F']) for tt,v in d['res'].items()),
              'pos %.3f %.3f bound %.6f %.6f'%(*d['pos_min'],d['bound_worst'],d['bound_worst_N']),flush=True)
    json.dump(out,open('witness_%s.json'%mode,'w'),indent=1)
