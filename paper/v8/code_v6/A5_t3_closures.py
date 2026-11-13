# SCRIPT: A5-T3-CLOSURES  linear-level closure comparison against the exact chain, v5.1 histories (comparators fixed in PREREGISTERED.txt)
import os; os.environ['OMP_NUM_THREADS']='1'
import numpy as np, json, time, sys
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from chain_lib import *
H=float(sys.argv[1]) if len(sys.argv)>1 else 1e-3
HIST=[(3,0.25),(3,0.5),(3,1),(3,2),(3,4),(3,8),(6,1),(6,2),(6,3)]
if len(sys.argv)>2: HIST=[HIST[int(i)] for i in sys.argv[2].split(',')]
TG=TAU0+np.arange(int(round((4.0-TAU0)/H))+1)*H; TG[-1]=4.0
i17=int(np.argmin(abs(TG-1.7))); i40=len(TG)-1
c0,c1,c2=cl(0),cl(1),cl(2)
LMX=60; KQQ=Kreal(LMX)[3:,3:]
def ode(rhs,jac,y0,sig):
    s=solve_ivp(rhs,(TAU0,4.0),y0,method='BDF',jac=jac,t_eval=TG,rtol=1e-10,atol=1e-13); assert s.success,s.message; return s.y
def run_CE2(k,sig):
    rhs=lambda t,y: np.array([-k*c0*y[1], k*c0*y[0]-(sig(t)+k*k*c1*c1/sig(t))*y[1]])
    jac=lambda t,y: np.array([[0,-k*c0],[k*c0,-(sig(t)+k*k*c1*c1/sig(t))]])
    y=ode(rhs,jac,np.array([1.0,0.0]),sig); w2=k*c1*y[1]/np.array([sig(t) for t in TG]); return np.vstack([y,w2])
def run_OP2(k,sig):
    def rhs(t,y):
        s=sig(t); return np.array([-k*c0*y[1], k*c0*y[0]-k*c1*y[2]-s*y[1], k*c1*y[1]-s*y[2]-k*k*c2*c2*y[3]*y[2], 1-s*y[3]])
    def jac(t,y):
        s=sig(t); return np.array([[0,-k*c0,0,0],[k*c0,-s,-k*c1,0],[0,k*c1,-s-k*k*c2*c2*y[3],-k*k*c2*c2*y[2]],[0,0,0,-s]])
    return ode(rhs,jac,np.array([1.0,0,0,0]),sig)[:3]
def run_MF(k,sig,Sg_kernel):
    """l<=2 kept; hidden l>=3 eliminated: dw2 += -k^2 c2^2 int exp(-(S(t)-S(r))) g(t-r) w2(r) dr; implicit trapezoid."""
    Nt=len(TG); E=expm(H*k*KQQ); e=np.zeros(KQQ.shape[0]); e[0]=1; g=np.zeros(Nt)
    for j in range(Nt): g[j]=e[0]; e=E@e
    Sk=Sg_kernel(TG); sv=np.array([sig(t) for t in TG])
    Y=np.zeros((3,Nt)); Y[0,0]=1.0; C=k*k*c2*c2
    def Aloc(s): return np.array([[0,-k*c0,0],[k*c0,-s,-k*c1],[0,k*c1,-s]])
    mem=np.zeros(Nt)   # m(t_i)
    I3=np.eye(3)
    for i in range(Nt-1):
        j=np.arange(i+1); Kr=np.exp(-(Sk[i+1]-Sk[j]))*g[i+1-j]; wq=np.full(i+1,H); wq[0]=H/2
        known=-C*np.sum(wq*Kr*Y[2,j])          # memory at t_{i+1} from r<t_{i+1} (trapezoid, last node weight H/2 implicit)
        Mimp=np.zeros((3,3)); Mimp[2,2]=-C*H/2  # r=t_{i+1}: exp(0) g(0)=1
        lhs=I3-H/2*(Aloc(sv[i+1])+Mimp)
        rhsv=Y[:,i]+H/2*(Aloc(sv[i])@Y[:,i]+np.array([0,0,mem[i]])+np.array([0,0,known]))
        Y[:,i+1]=np.linalg.solve(lhs,rhsv); mem[i+1]=known-C*H/2*Y[2,i+1]
    return Y
def trap(y): return np.sum(0.5*(y[1:]+y[:-1])*np.diff(TG))
Sref=Sigma_powerlaw(2.0,3)
t1=time.time()
Ainst=sum(w*evolve(k,lambda t:0.0,LMX,TG[[i17,i40]])[0]**2 for k,w in zip(KS,WE))
COMPS=['P1','M1lin','P2','M2lin','P3','P5','CE2','OP2','MFe','MFf']
res={}
for (n,ed) in HIST:
    sig=sigma_powerlaw(ed,n); Sg=Sigma_powerlaw(ed,n)
    num={c:0.0 for c in COMPS}; den=0.0; Ac={c:np.zeros(2) for c in COMPS+['EX']}
    for k,w in zip(KS,WE):
        ex=evolve(k,sig,LMX,TG,rtol=1e-10,atol=1e-13)[:3]
        tr={}
        for N in (1,2,3,5):
            y=evolve(k,sig,N,TG,rtol=1e-10,atol=1e-13); z=np.zeros((3,len(TG))); m=min(3,N+1); z[:m]=y[:m]; tr[N]=z
        Y={'P1':tr[1],'M1lin':tr[1],'P2':tr[2],'M2lin':tr[2],'P3':tr[3],'P5':tr[5],'CE2':run_CE2(k,sig),'OP2':run_OP2(k,sig),
           'MFe':run_MF(k,sig,Sg),'MFf':run_MF(k,sig,Sref)}
        den+=w*trap(np.sum(ex**2,0)); Ac['EX']+=w*ex[0,[i17,i40]]**2
        for c in COMPS:
            num[c]+=w*trap(np.sum((Y[c]-ex)**2,0)); Ac[c]+=w*Y[c][0,[i17,i40]]**2
    gex=(1-Ac['EX'])/(1-Ainst); row={}
    for c in COMPS:
        gc=(1-Ac[c])/(1-Ainst)
        row[c]=dict(E_traj=float(np.sqrt(num[c]/den)),E_A=np.abs(Ac[c]-Ac['EX']).tolist(),E_g=np.abs(gc-gex).tolist(),
                    E_g2=float(abs(0.89*(gc[0]-gex[0])+0.11*(gc[1]-gex[1]))),g=gc.tolist())
    row['EX']=dict(g=gex.tolist(),g2=float(0.89*gex[0]+0.11*gex[1]))
    res['n%d_ed%g'%(n,ed)]=row
    print('n=%d ed=%g  exact g(1.7)=%.4f g(4)=%.4f g2=%.4f   [%.0fs]'%(n,ed,gex[0],gex[1],row['EX']['g2'],time.time()-t1),flush=True)
    for c in COMPS:
        r=row[c]; print('   %-6s E_traj %.3e | E_A(1.7) %.2e E_A(4) %.2e | E_g(1.7) %.2e E_g(4) %.2e E_g2 %.2e'%(c,r['E_traj'],*r['E_A'],*r['E_g'],r['E_g2']),flush=True)
json.dump(dict(h=H,res=res),open('t3_closures_h%g_%s.json'%(H,sys.argv[2].replace(',','-') if len(sys.argv)>2 else 'all'),'w'),indent=1)
print('time %.0fs'%(time.time()-t1))
