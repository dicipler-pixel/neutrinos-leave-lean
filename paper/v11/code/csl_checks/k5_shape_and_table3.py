# SCRIPT: K5-SHAPE-AND-TABLE3
# (a) Shape insensitivity (Steve Fig.3b/Table II alpha rows). Paper Sec.6 "tips swing, tail holds"/leader fixed by the map, start (shape) only sets amplitude.
#     Question: is the near-constancy of the C_l shift across alpha (9.3-10.0%) a dynamical (leader) fact, or already forced by Eq.15?
#     Test: take the five PERFECT-FLUID thresholds and the five FS thresholds, convert each to C_l by inverting Eq.15, recompute the C_l shifts.
#     KILL (before run): the mapping "shape-independence is dynamical evidence for a shared leader" is dead if the C_l shifts recomputed from
#     delta_c via Eq.15 reproduce Steve's quoted 9.3/9.4/9.6/9.9/10.0 within 0.1 pp (then it is bookkeeping of the coordinate, nothing more).
#     OPPOSITE: the same conversion with the OTHER coordinate held fixed (delta_c shift held at 6.15% for all alpha) -> what C_l spread would result.
import numpy as np
inv=lambda d:(4/3)*(1-np.sqrt(1-1.5*d)); fwd=lambda C:C-3/8*C**2
al=[0.3,0.5,1,2,4]; pf=np.array([.44805,.46687,.49773,.53274,.56819]); fs=np.array([.47747,.49682,.52832,.56342,.59734]); q=np.array([9.3,9.4,9.6,9.9,10.0])
rec=(inv(fs)/inv(pf)-1)*100
print('alpha',al); print('C_l,c (pf)',np.round(inv(pf),4)); print('recomputed C_l shift %',np.round(rec,2)); print('Steve quoted           ',q)
print('max |diff| = %.2f pp  -> KILL (bookkeeping) %s'%(np.max(np.abs(rec-q)),'FIRED = it IS bookkeeping' if np.max(np.abs(rec-q))<0.15 else 'did not fire'))
hold=np.array([(inv(p*1.0615)/inv(p)-1)*100 for p in pf]); print('OPPOSITE: if delta_c shift were 6.15% for every alpha, C_l shifts would be',np.round(hold,2),'(spread %.2f pp vs Steve %.2f pp)'%(np.ptp(hold),np.ptp(q)))
# (b) Table III: three-sample sign on ln M vs ln(d-dc) (paper Sec.8: a positive independent mixture of power laws is log-CONVEX; negative determinant = not that)
x=np.array([1e-1,3e-2,1e-2,3e-3,1e-3,3e-4,1e-4]); pfm=np.array([.679,.497,.390,.288,.215,.151,.105]); fsm=np.array([.799,.590,.470,.343,.255,.178,.123])
def det3(y,i,j,k): return y[i]*y[k]-y[j]**2
def d2ln(y,i,j,k): return np.log(y[i])+np.log(y[k])-2*np.log(y[j])
for name,y in (('PF',pfm),('FS',fsm)):
    print(name,'det y0y2-y1^2 on (1e-1,1e-2,1e-3): %+.4f  | second difference of ln M: %+.4f | on (3e-2,3e-3,3e-4): %+.4f'%(det3(y,0,2,4),d2ln(y,0,2,4),d2ln(y,1,3,5)))
loc=lambda y:np.diff(np.log(y))/np.diff(np.log(x))
print('local log-slopes PF',np.round(loc(pfm),3)); print('local log-slopes FS',np.round(loc(fsm),3)); print('ratio FS/PF',np.round(fsm/pfm,3))
# rounding-noise scale of the second difference (3-digit masses)
rng=np.random.default_rng(1); s=[]
for _ in range(20000):
    a=pfm+rng.uniform(-5e-4,5e-4,7); b=fsm+rng.uniform(-5e-4,5e-4,7); s.append(d2ln(b,0,2,4)-d2ln(a,0,2,4))
print('FS-minus-PF second difference %+.4f ; rounding-only spread (1 sd) %.4f'%(d2ln(fsm,0,2,4)-d2ln(pfm,0,2,4),np.std(s)))
print('threshold-uncertainty scale: 3e-5/1e-3=3%% in x at the 1e-3 point -> dlnM ~ 0.27*0.03 = %.4f per curve'%(0.27*0.03))
# (c) the G curve itself: three-sample sign in t=ln(e_dec), and balance-map structure
ed=np.array([.25,.5,1,2,4,8]); G=np.array([.959,.867,.683,.431,.190,.063])
print('G three-sample dets (e_dec triples):',[round(G[i]*G[i+2]-G[i+1]**2,4) for i in range(4)])
from scipy.optimize import least_squares
def fit(f,p0): 
    r=least_squares(lambda p:f(p,ed)-G,p0); return r.x,np.max(np.abs(r.fun))
cands={'logistic-in-log (balance map): 1/(1+(e/ec)^n)':(lambda p,e:1/(1+(e/p[0])**p[1]),[1.6,1.7]),
       'stretched exp: exp(-(e/e0)^m)':(lambda p,e:np.exp(-(e/p[0])**p[1]),[3,1]),
       'power-damped: (1+e/e0)^-m':(lambda p,e:(1+e/p[0])**-p[1],[1,1]),
       'gaussian-in-log: exp(-(ln e/s)^2/2) one-sided':(lambda p,e:np.exp(-0.5*(np.log(e)/p[0])**2*(e>1)),[2,0])}
for n,(f,p0) in cands.items():
    p,m=fit(f,p0); print('%-48s params %s  max|err| %.3f'%(n,np.round(p,3),m))
p,_=fit(*cands['logistic-in-log (balance map): 1/(1+(e/ec)^n)'])
print('logistic predictions (UNTESTED, proposed): G(0.1)=%.3f G(16)=%.4f G(32)=%.4f'%tuple(1/(1+(np.array([.1,16,32])/p[0])**p[1])))
