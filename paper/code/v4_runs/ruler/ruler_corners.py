# SCRIPT: NU-V4-RULER-CORNERS  deterministic corner enumeration for the ruler check (replaces the 2000-draw sampling of ruler_state.py, control C4)
# Every statistic of ruler_state.py is recomputed at EVERY corner of every bracket: 10 all-higher thresholds, 4 shear-only, the anchor -> 2^15 = 32768 corners.
import numpy as np, json, os, math, itertools
here=os.path.dirname(os.path.abspath(__file__)); up=os.path.join(here,'..')
FL,INS=0.49773,0.52832
def tau_of(dc): G=(dc-FL)/(INS-FL); return np.log((1-G)/G)
def load(tag):
    d=json.load(open(os.path.join(up,'res_%s.json'%tag))); return d['dc'],d.get('lo',d['dc']-d['w']/2),d.get('hi',d['dc']+d['w']/2)
ALL={1/16:'F2_r1o16',0.25:'F_r025',0.5:'J_r05',1/1.2:'A1_all_r083',0.8:'K_r08_clean',1.0:'H1_r1',1.2:'A1_all_r12',1.25:'K_r125_clean',2.0:'J_r2',4.0:'F_r4',16.0:'F2_r16'}
SHR={0.25:'L_r025',1/1.2:'A1_shear_r083',1.2:'A1_shear_r12',4.0:'L_r4'}
rs_all=sorted(ALL); rs_sh=sorted(SHR)
theta=json.load(open(os.path.join(here,'ruler_state.json')))['theta']
X=lambda r:0.5*math.log(r)
# corner grid: one bit per bracket; bit=0 -> lo, bit=1 -> hi
names=[('all',r) for r in rs_all]+[('sh',r) for r in rs_sh]           # anchor is ('all',1.0)
los=np.array([load(ALL[r])[1] for r in rs_all]+[load(SHR[r])[1] for r in rs_sh]); his=np.array([load(ALL[r])[2] for r in rs_all]+[load(SHR[r])[2] for r in rs_sh])
Nb=len(names); C=1<<Nb; bits=((np.arange(C)[:,None]>>np.arange(Nb))&1).astype(float)   # (C,Nb)
dc=los+bits*(his-los)                                                                   # (C,Nb)
ia={r:names.index(('all',r)) for r in rs_all}; ish={r:names.index(('sh',r)) for r in rs_sh}; i1=ia[1.0]
tau=tau_of(dc); anc=tau[:,i1]
def slope(xs,T):  # free-intercept least squares slope, vectorised over corners; T (C,m)
    xs=np.asarray(xs); xm=xs.mean(); return ((T-T.mean(1,keepdims=True))*(xs-xm)).sum(1)/((xs-xm)**2).sum()
def run(name,xa,xsh):
    Ta=np.stack([tau[:,ia[r]]-anc for r in rs_all],1); Tsh=np.stack([tau[:,ish[r]]-anc for r in rs_sh],1)
    ba=slope([xa(r) for r in rs_all],Ta); bsh=slope([xsh(r) for r in rs_sh],Tsh); ratio=bsh/ba
    odd=np.stack([(tau[:,ia[r]]-tau[:,ia[1/r]])/(xa(r)-xa(1/r)) for r in [1.2,1.25,2.0,4.0,16.0]],1)
    sp=(odd.max(1)-odd.min(1))/np.abs(odd.mean(1))
    print(f'[{name}] RATIO shear/all ALL-CORNER range [{ratio.min():.4f}, {ratio.max():.4f}]   odd-rate spread ALL-CORNER range [{100*sp.min():.2f}%, {100*sp.max():.2f}%]  (corners: {C})')
    return ratio,sp
print('# every statistic over all 2^15 bracket corners (lo/hi of each of the 15 thresholds incl. the anchor)')
run('CHART x=(1/2)ln r',X,X)
for t in ['1.7','4.0']:
    ta={float(k):v for k,v in theta[t]['all'].items()}; tsh={float(k):v for k,v in theta[t]['shear'].items()}
    fa=lambda r:ta[min(ta,key=lambda q:abs(q-r))]; fs=lambda r:tsh[min(tsh,key=lambda q:abs(q-r))]
    ratio,sp=run(f'RULER (e) theta at tau*={t}',fa,fs)
    print(f'   R1 kill line [0.97,1.03]: holds at every corner = {bool(((ratio<0.97)|(ratio>1.03)).all())}   R2 kill line spread>1.2%: holds at every corner = {bool((sp>0.012).all())}')
