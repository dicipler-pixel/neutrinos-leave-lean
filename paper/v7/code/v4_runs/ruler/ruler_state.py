# SCRIPT: NU-V4-RULER-STATE  ruler (e): principal angle between kept-sector trajectories v_r(tau*) and v_1(tau*) (see PREREGISTERED_RULER.txt)
import numpy as np, json, os, math, sys
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
here=os.path.dirname(os.path.abspath(__file__)); up=os.path.join(here,'..')
FL,INS=0.49773,0.52832
def tau_of(dc): G=(dc-FL)/(INS-FL); return math.log((1-G)/G)
def load(tag):
    d=json.load(open(os.path.join(up,'res_%s.json'%tag))); return d['dc'],d.get('lo',d['dc']-d['w']/2),d.get('hi',d['dc']+d['w']/2)
ALL={1/16:'F2_r1o16',0.25:'F_r025',0.5:'J_r05',1/1.2:'A1_all_r083',0.8:'K_r08_clean',1.0:'H1_r1',1.2:'A1_all_r12',1.25:'K_r125_clean',2.0:'J_r2',4.0:'F_r4',16.0:'F2_r16'}
SHR={0.25:'L_r025',1/1.2:'A1_shear_r083',1.2:'A1_shear_r12',4.0:'L_r4'}
anc=load('H1_r1'); rng=np.random.default_rng(1)
kn,kw=roots_legendre(36); ks=0.5*(9.0-0.25)*(kn+1)+0.25; wk=0.5*(9.0-0.25)*kw; wE=wk*ks**2*np.exp(-ks**2/2); wE/=wE.sum()
LM=60; n=LM+1; M=np.zeros((n,n))
for l in range(1,n): M[l,l-1]=M[l-1,l]=l/np.sqrt(4.0*l*l-1)
tau0=0.02; TS=[1.7,4.0]; ed,p=2.0,3
def Dr(r,fam):
    d=np.full(n,r if fam=='all' else 1.0); d[0]=0.0; d[1]=1.0
    if fam=='shear': d[2]=r
    return d
def state(k,r,fam):
    d=Dr(r,fam)
    def rhs(t,v):
        K=ed**p/t**(p+1); x,y=v[:n],v[n:]
        return np.concatenate([-K*d*x+k*(M@y),-K*d*y-k*(M@x)])
    v0=np.zeros(2*n); v0[0]=1
    s=solve_ivp(rhs,(tau0,TS[-1]),v0,method='BDF',t_eval=TS,rtol=1e-9,atol=1e-12)
    return {t:(s.y[:n,i]+1j*s.y[n:,i]) for i,t in enumerate(TS)}
cache={}
def V(k,r,fam):
    key=(k,round(r,9),fam)
    if key not in cache: cache[key]=state(k,r,fam)
    return cache[key]
rs_all=sorted(ALL); rs_sh=sorted(SHR)
theta={t:{'all':{},'shear':{}} for t in TS}; A0={t:{'all':{},'shear':{}} for t in TS}
for fam,rs in [('all',rs_all),('shear',rs_sh)]:
    for r in rs:
        for t in TS:
            th=0.0; a=0.0
            for k,w in zip(ks,wE):
                v1=V(k,1.0,'all')[t]; vr=V(k,r,fam)[t]
                c=abs(np.vdot(v1,vr))/(np.linalg.norm(v1)*np.linalg.norm(vr)); th+=w*math.acos(min(1.0,c)); a+=w*abs(vr[0])**2
            theta[t][fam][r]=math.copysign(th,math.log(r)) if r!=1 else 0.0; A0[t][fam][r]=a
        print(f'{fam:5s} r={r:8.4f}  theta(1.7)={theta[1.7][fam][r]:+.5f} theta(4.0)={theta[4.0][fam][r]:+.5f}  A0(1.7)={A0[1.7][fam][r]:.5f} A0(4.0)={A0[4.0][fam][r]:.5f}',flush=True)
json.dump({'theta':{str(t):{f:{str(r):v for r,v in d.items()} for f,d in theta[t].items()} for t in TS},'A0':{str(t):{f:{str(r):v for r,v in d.items()} for f,d in A0[t].items()} for t in TS}},open(os.path.join(here,'ruler_state.json'),'w'),indent=1)
def stats(rs,tab,xf,corner=None):
    xs=np.array([xf(r) for r in rs]); ts=np.array([tau_of(corner[r] if corner else load(tab[r])[0])-tau_of(corner[1.0] if corner else anc[0]) for r in rs])
    A=np.vstack([np.ones(len(xs)),xs]).T; (a,b)=np.linalg.lstsq(A,ts,rcond=None)[0]; rms=float(np.sqrt(np.mean((ts-a-b*xs)**2)))
    odd={r:(ts[rs.index(r)]-ts[[rs.index(q) for q in rs if abs(q-1/r)<1e-9][0]])/(xs[rs.index(r)]-xs[[rs.index(q) for q in rs if abs(q-1/r)<1e-9][0]]) for r in rs if r>1 and any(abs(q-1/r)<1e-9 for q in rs)}
    return b,rms,odd
spread=lambda o:(lambda v:(v.max()-v.min())/abs(v.mean()))(np.array(list(o.values())))
def report(name,xa,xs_):
    ba,ra,oa=stats(rs_all,ALL,xa); bs,rs_,os_=stats(rs_sh,SHR,xs_); ratios=[];sp=[]
    for _ in range(2000):
        ca={r:rng.uniform(*load(ALL[r])[1:]) for r in rs_all}; cs={r:rng.uniform(*load(SHR[r])[1:]) for r in rs_sh}; ca[1.0]=rng.uniform(anc[1],anc[2]); cs[1.0]=ca[1.0]
        b1,_,o1=stats(rs_all,ALL,xa,ca); b2,_,_=stats(rs_sh,SHR,xs_,cs); ratios.append(b2/b1); sp.append(spread(o1))
    print(f'[{name}] all-higher slope {ba:.4f} rms {ra:.4f} odd '+' '.join(f'{r:g}:{v:.4f}' for r,v in sorted(oa.items()))+f' spread {100*spread(oa):.2f}% ({100*min(sp):.2f}-{100*max(sp):.2f})')
    print(f'[{name}] shear-only slope {bs:.4f} rms {rs_:.4f} odd '+' '.join(f'{r:g}:{v:.4f}' for r,v in sorted(os_.items()))+f'   RATIO {bs/ba:.4f} ({min(ratios):.4f}-{max(ratios):.4f})')
X=lambda r:0.5*math.log(r)
report('CHART',X,X)
for t in TS:
    ta=theta[t]['all']; tsh=theta[t]['shear']
    report(f'RULER (e) theta at tau*={t}',lambda r:ta[r],lambda r:tsh[r])
    report(f'   C2 swapped tau*={t}',lambda r:tsh[r] if r in tsh else ta[r],lambda r:ta[r])
    # C1: synthetic tau = theta read in x
    xa=np.array([X(r) for r in rs_all]); ya=np.array([ta[r] for r in rs_all]); b1=np.linalg.lstsq(np.vstack([np.ones(len(xa)),xa]).T,ya,rcond=None)[0][1]
    xs2=np.array([X(r) for r in rs_sh]); ys=np.array([tsh[r] for r in rs_sh]); b2=np.linalg.lstsq(np.vstack([np.ones(len(xs2)),xs2]).T,ys,rcond=None)[0][1]
    od={r:(ta[r]-ta[1/r])/(2*X(r)) for r in [1.2,1.25,2,4,16]}
    print(f'   C1 tau*={t}: theta read in x -> family ratio {b2/b1:.4f}, odd spread {100*spread(od):.2f}%')
    # memory-form control: offset of A0 (log-odds of kept population) as a ruler
    aa=A0[t]['all']; ash=A0[t]['shear']; lo=lambda a: math.log((1-a)/a)
    report(f'   control: memory-form A0 log-odds as ruler, tau*={t}',lambda r:lo(aa[r])-lo(aa[1.0]),lambda r:lo(ash[r])-lo(aa[1.0]))
