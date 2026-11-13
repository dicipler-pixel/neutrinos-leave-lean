# SCRIPT: NU-V4-RULER-CHECK  intrinsic-ruler check of the measured threshold offsets (see PREREGISTERED_RULER.txt)
import numpy as np, json, os, sys, math
from scipy.special import roots_legendre
here=os.path.dirname(os.path.abspath(__file__)); up=os.path.join(here,'..')
rng=np.random.default_rng(1)
FL,INS=0.49773,0.52832
def tau_of(dc): G=(dc-FL)/(INS-FL); return math.log((1-G)/G)
def load(tag):
    d=json.load(open(os.path.join(up,'res_%s.json'%tag))); lo=d.get('lo',d['dc']-d['w']/2); hi=d.get('hi',d['dc']+d['w']/2); return d['dc'],lo,hi
ALL={1/16:'F2_r1o16',0.25:'F_r025',0.5:'J_r05',1/1.2:'A1_all_r083',0.8:'K_r08_clean',1.0:'H1_r1',1.2:'A1_all_r12',1.25:'K_r125_clean',2.0:'J_r2',4.0:'F_r4',16.0:'F2_r16'}
SHR={0.25:'L_r025',1/1.2:'A1_shear_r083',1.2:'A1_shear_r12',4.0:'L_r4'}
anc=load('H1_r1')
# ---------- chain ----------
LM=int(os.environ.get('LM','60')); n=LM+1
M=np.zeros((n,n))
for l in range(1,n): M[l,l-1]=M[l-1,l]=l/np.sqrt(4.0*l*l-1)
S=np.diag([(-1.0)**l for l in range(n)])
kn,kw=roots_legendre(36); ks=0.5*(9.0-0.25)*(kn+1)+0.25; wk=0.5*(9.0-0.25)*kw; wE=wk*ks**2*np.exp(-ks**2/2); wE/=wE.sum()
if os.environ.get('SINGLEK'): ks=np.array([float(os.environ['SINGLEK'])]); wE=np.array([1.0])
KAP=float(os.environ.get('KAP','0.958'))
def Dr(r,fam):
    d=np.full(n,r if fam=='all' else 1.0); d[0]=0.0; d[1]=1.0
    if fam=='shear': d[2]=r
    return d
def proj(k,r,fam,rank):
    L=-1j*k*M-KAP*np.diag(Dr(r,fam))
    ev,R=np.linalg.eig(L); Lf=np.linalg.inv(R)       # rows of Lf are left eigenvectors (biorthonormal to R)
    o=np.argsort(-ev.real); ev,R,Lf=ev[o],R[:,o],Lf[o,:]
    if rank=='pair':
        idx=[0] if abs(ev[0].imag)<1e-9 else ([0,1] if abs(ev[0].real-ev[1].real)<1e-7 else [0])
    elif rank=='one': idx=[0] if abs(ev[0].imag)<1e-9 else [0 if ev[0].imag>0 else 1]
    P=sum(np.outer(R[:,i],Lf[i,:]) for i in idx)
    m=len(idx); gap=ev[m].real-ev[0].real if m<n else 0.0
    return P,gap,ev[0]
def rulers(fam,rank,us):
    """s_a (arc length, Hermitian), s_b (chord), q (biorth form along the path), theta (principal angle), each profile-averaged; indexed by u=ln r."""
    sa=np.zeros(len(us)); sb=np.zeros(len(us)); qmin=np.zeros(len(us)); th=np.zeros(len(us)); worst_gap=1e9; chk=0.0
    i1=int(np.argmin(abs(us)))
    for k,w in zip(ks,wE):
        Ps=[]; 
        for u in us:
            P,gap,ev=proj(k,math.exp(u),fam,rank); Ps.append(P); worst_gap=min(worst_gap,gap)
            chk=max(chk,np.abs(P@P-P).max(),abs(np.trace(P).real-round(np.trace(P).real)))
        Ps=np.array(Ps); du=us[1]-us[0]
        dP=np.gradient(Ps,du,axis=0)
        g=0.5*np.sum(np.abs(dP)**2,axis=(1,2))            # (1/2)||dP/du||_F^2
        q=0.5*np.real(np.einsum('uij,uji->u',dP,dP))       # (1/2) Re Tr V^2
        arc=np.concatenate([[0],np.cumsum(np.sqrt(g[1:])*du)]); arc-=arc[i1]
        sa+=w*arc
        chord=np.array([np.linalg.norm(P-Ps[i1])/math.sqrt(2) for P in Ps]); sb+=w*np.sign(us)*chord
        qmin+=w*q
        # principal angle via the Hermitian part: use range of P (right eigvecs) vs range at r=1
        for j,P in enumerate(Ps):
            A=np.linalg.svd(P,full_matrices=False)[0][:,:int(round(np.trace(P).real))]
            B=np.linalg.svd(Ps[i1],full_matrices=False)[0][:,:int(round(np.trace(Ps[i1]).real))]
            sv=np.linalg.svd(A.conj().T@B,compute_uv=False); th[j]+=w*np.sign(us[j])*math.sqrt(np.sum(np.arccos(np.clip(sv,0,1))**2))
    return dict(a=sa,b=sb,q=qmin,theta=th,gap=worst_gap,chk=chk)
us=np.linspace(math.log(1/16),math.log(16),641)
def interp(arr,r): return float(np.interp(math.log(r),us,arr))
# ---------- data ----------
def family_points(tab):
    rs=sorted(tab); return rs,[load(tab[r]) for r in rs]
def tau_off(pt,a): return tau_of(pt)-tau_of(a)
def stats(rs,pts,xfun,corner=None):
    """slope of tau against xfun(r) (least squares with intercept) and odd rates per unit of xfun; corner: None=mid, else dict r->dc"""
    xs=np.array([xfun(r) for r in rs]); ts=np.array([tau_off(corner[r] if corner else p[0], corner.get(1.0,anc[0]) if corner else anc[0]) for r,p in zip(rs,pts)])
    A=np.vstack([np.ones(len(xs)),xs]).T; (a,b),res,_,_=np.linalg.lstsq(A,ts,rcond=None); rms=float(np.sqrt(np.mean((ts-a-b*xs)**2)))
    odd={}
    for r in rs:
        if r>1 and (1/r) in rs or any(abs(1/r-q)<1e-9 for q in rs):
            q=[q for q in rs if abs(1/r-q)<1e-9]
            if r>1 and q:
                i,j=rs.index(r),rs.index(q[0]); odd[r]=(ts[i]-ts[j])/(xs[i]-xs[j])
    return b,rms,odd
def spread(odd): v=np.array(list(odd.values())); return float((v.max()-v.min())/abs(v.mean()))
def report(name,xall,xshr):
    ra,pa=family_points(ALL); rsh,psh=family_points(SHR)
    ba,rmsa,odda=stats(ra,pa,xall); bs,rmss,odds=stats(rsh,psh,xshr)
    # corner sampling
    ratios=[];spreads=[]
    for _ in range(2000):
        ca={r:rng.uniform(p[1],p[2]) for r,p in zip(ra,pa)}; cs={r:rng.uniform(p[1],p[2]) for r,p in zip(rsh,psh)}; ca[1.0]=rng.uniform(anc[1],anc[2]); cs[1.0]=ca[1.0]
        b1,_,o1=stats(ra,pa,xall,ca); b2,_,o2=stats(rsh,psh,xshr,cs); ratios.append(b2/b1); spreads.append(spread(o1))
    print(f'[{name}] all-higher: slope {ba:.4f} rms {rmsa:.4f}  odd rates '+' '.join(f'r={r:g}:{v:.4f}' for r,v in sorted(odda.items()))+f'  spread {100*spread(odda):.2f}% (corners {100*min(spreads):.2f}-{100*max(spreads):.2f}%)')
    print(f'[{name}] shear-only: slope {bs:.4f} rms {rmss:.4f}  odd rates '+' '.join(f'r={r:g}:{v:.4f}' for r,v in sorted(odds.items())))
    print(f'[{name}] slope ratio shear/all = {bs/ba:.4f}  (corners {min(ratios):.4f}-{max(ratios):.4f})')
    return bs/ba,spread(odda),(min(ratios),max(ratios)),(min(spreads),max(spreads))
print('kappa',KAP,'LM',LM,'profile',len(ks),'k nodes')
X=lambda r: 0.5*math.log(r)
base=report('CHART x=1/2 ln r',X,X)
GAM=lambda r:(r-1)/(r+1); report('C3 chart control Gamma12',GAM,GAM)
RA=rulers('all','pair',us); RS=rulers('shear','pair',us)
print(f'eigen controls: worst |P^2-P|,trace dev {RA["chk"]:.2e}/{RS["chk"]:.2e}; min real-part gap to next mode {RA["gap"]:.4f}/{RS["gap"]:.4f}')
print('biorthogonal form q along the path (profile avg): all-higher min %.3e max %.3e; shear-only min %.3e max %.3e'%(RA['q'].min(),RA['q'].max(),RS['q'].min(),RS['q'].max()))
for key,lab in [('a','(a) arc length'),('b','(b) chord'),('theta','(d) principal angle')]:
    print('--- ruler',lab,'  s(r) all-higher:',' '.join(f'{r:g}:{interp(RA[key],r):+.4f}' for r in [1/16,.25,.5,1/1.2,.8,1.2,1.25,2,4,16]),' shear-only:',' '.join(f'{r:g}:{interp(RS[key],r):+.4f}' for r in [.25,1/1.2,1.2,4]))
    res=report('RULER '+lab,lambda r,k=key:interp(RA[k],r),lambda r,k=key:interp(RS[k],r))
    print('   C2 wrong ruler:'); report('   swapped',lambda r,k=key:interp(RS[k],r),lambda r,k=key:interp(RA[k],r))
    # C1 positive control
    rs=sorted(ALL); ts=np.array([interp(RA[key],r) for r in rs]); xs=np.array([X(r) for r in rs]); A=np.vstack([np.ones(len(xs)),xs]).T; b1=np.linalg.lstsq(A,ts,rcond=None)[0][1]
    rsh=sorted(SHR); ts2=np.array([interp(RS[key],r) for r in rsh]); xs2=np.array([X(r) for r in rsh]); A2=np.vstack([np.ones(len(xs2)),xs2]).T; b2=np.linalg.lstsq(A2,ts2,rcond=None)[0][1]
    od={r:(interp(RA[key],r)-interp(RA[key],1/r))/(X(r)-X(1/r)) for r in [1.2,1.25,2,4,16]}
    print(f'   C1 positive control (tau = s read in x): family ratio {b2/b1:.4f}, odd-rate spread {100*spread(od):.2f}%  -> must differ from 1 and exceed 1.2%')
    key2=key
# rank-1 comparison on ruler (a)
RA1=rulers('all','one',us); RS1=rulers('shear','one',us)
report('RULER (a) rank-1 comparison',lambda r:interp(RA1['a'],r),lambda r:interp(RS1['a'],r))
