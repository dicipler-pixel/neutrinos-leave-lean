# SCRIPT: A5-T2-GRAMIAN  readout Gramian of the hidden sector l>=3 (R = l<=2), parity-symmetrized, profile-summed
import os; os.environ['OMP_NUM_THREADS']='1'
import numpy as np, json, time, sys
from scipy.linalg import expm
from chain_lib import *

def gramian(ed, n, s, T=4.0, LM=60, dt=2e-3, ks=KS, ws=WE):
    N=LM+1; K=Kreal(LM); d=np.r_[0.0,np.ones(LM)]; Sg=Sigma_powerlaw(ed,n)
    nst=int(np.ceil((T-s)/dt)); tg=np.linspace(s,T,nst+1); h=tg[1]-tg[0]
    G=np.zeros((N-3,N-3)); GT=np.zeros((N-3,N-3))
    for k,w in zip(ks,ws):
        X=np.zeros((N,N-3)); X[3:,:]=np.eye(N-3)
        Gk=0.5*h*X[:3].T@X[:3]
        for i in range(nst):
            seff=(Sg(tg[i+1])-Sg(tg[i]))/h          # exact step-average rate
            X=expm(h*(k*K-seff*np.diag(d)))@X
            Gk+=(h if i<nst-1 else 0.5*h)*X[:3].T@X[:3]
        GTk=X[:3].T@X[:3]
        P=np.diag((-1.0)**np.arange(3,N))           # k -> -k
        G+=w*0.5*(Gk+P@Gk@P); GT+=w*0.5*(GTk+P@GTk@P)
    return G,GT

def summarize(G,label,ntop=3):
    lam,V=np.linalg.eigh(G); idx=np.argsort(lam)[::-1]; lam=lam[idx]; V=V[:,idx]
    ls=np.arange(3,3+G.shape[0])
    rows=[]
    for j in range(ntop):
        v=V[:,j]; v=v*np.sign(v[np.argmax(abs(v))]); wts=v**2
        par='odd' if wts[ls%2==1].sum()>0.999 else ('even' if wts[ls%2==0].sum()>0.999 else 'mixed')
        rows.append(dict(eig=float(lam[j]),parity=par,l_weights={int(l):float(x) for l,x in zip(ls[:10],wts[:10])},vec=v.tolist()))
    effrank=int(np.sum(lam>1e-3*lam[0]))
    print('  %s: top eigs %s | eff.rank(>1e-3 top) %d | min eig %.2e'%(label,' '.join('%.3e'%x for x in lam[:6]),effrank,lam[-1]),flush=True)
    for j,r in enumerate(rows):
        print('     v%d [%s] l-weights: %s'%(j,r['parity'],' '.join('%d:%.3f'%(l,x) for l,x in list(r['l_weights'].items())[:7])),flush=True)
    return dict(eigs=lam.tolist(),effrank=effrank,top=rows)

if __name__=='__main__':
    t1=time.time(); out={}
    confs=[('ed0.5_n3',0.5,3,[0.125,0.5,1.0]),('ed0.5_n6',0.5,6,[0.125,0.5,1.0]),('ed2_n3',2.0,3,[0.5,2.0,3.0])]
    for name,ed,n,ss in confs:
        for s,lab in zip(ss,['coupled','transition','free']):
            G,GT=gramian(ed,n,s)
            print('%s plant s=%g (%s)  [%.0fs]'%(name,s,lab,time.time()-t1),flush=True)
            out['%s_s%g'%(name,s)]=dict(ed=ed,n=n,s=s,epoch=lab,integral=summarize(G,'integral G'),terminal=summarize(GT,'terminal G_T'))
            np.save('G_%s_s%g.npy'%(name,s),G)
    json.dump(out,open('t2_gramian.json','w'),indent=1)
    print('time %.0fs'%(time.time()-t1))
