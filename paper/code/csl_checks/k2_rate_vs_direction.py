# SCRIPT: K2-RATE-VS-DIRECTION-IN-R_NU
# Mapping under test (paper Sec.2, eq. split): a two-component overdensity (plasma share 1-R, neutrino share R) is a point
# (direction) on the chromatic sphere times a brightness (rate). Free streaming removes a fraction f of the NEUTRINO part.
#   Mapping D (direction): threshold shift  ~  chromatic (Fisher/sphere) distance between composition before and after.
#   Mapping B (rate)     : threshold shift  ~  loss of total brightness, 1/(1-f R) - 1  (collapsing mass diluted).
# WHY THIS DISCRIMINATES: for small R the sphere distance between (1-R,R) and (1-R,R s) grows like sqrt(R)
#   (sqrt-amplitude of the small channel), brightness loss grows like R. Steve's data (Table II, Eq.16-17) are linear in R_nu to 1-4%.
# KILL (before running): Mapping D is dead if, with its single scale fixed at R=0.409, it misses the Table II C_l shifts at
#   R=0.1 or 0.2 by more than 20% (relative). Mapping B is dead if it misses any of the five by more than 10% (relative).
# OPPOSITE run: Mapping D with the inverse reading (shift ~ 1/distance is nonsense) is not meaningful, so the opposite is
#   the OTHER channel of the same split (B), plus D with shares of the OTHER species (plasma-share loss, i.e. s>1 direction).
import numpy as np
R=np.array([.1,.2,.3,.409,.488]); data=np.array([2.3,4.7,7.0,9.6,11.5])/100
def dist(R,s):
    p=np.array([1-R,R]); q=np.array([1-R,R*s]); q=q/q.sum()
    return 2*np.arccos(np.clip(np.sum(np.sqrt(p*q)),-1,1))*2   # sphere of radius 2
for s in (0.0,0.5,0.8):                     # fraction lost = 1-s; scale fixed at R=0.409
    dd=np.array([dist(r,s) for r in R]); pred=dd/dd[3]*data[3]
    print('D  s=%.1f pred(%%)'%s, np.round(pred*100,2), ' rel.err', np.round(pred/data-1,2))
f=1-1/(1+data[3])  # solve 1/(1-fR)-1 = data[3] at R=.409 -> fR=data/(1+data)
f=(data[3]/(1+data[3]))/R[3]
predB=1/(1-f*R)-1
print('B  f=%.3f pred(%%)'%f, np.round(predB*100,2), ' rel.err', np.round(predB/data-1,3))
print('log-slope d ln(shift)/d ln R between R=.1 and .488: data %.3f ; D(s=0) %.3f ; B %.3f' % (
  np.log(data[-1]/data[0])/np.log(R[-1]/R[0]),
  np.log(dist(R[-1],0)/dist(R[0],0))/np.log(R[-1]/R[0]),
  np.log(predB[-1]/predB[0])/np.log(R[-1]/R[0])))
kD = np.max(np.abs((dist(R[0],0)/dist(R[3],0)*data[3])/data[0]-1))>0.2
kB = np.max(np.abs(predB/data-1))>0.10
print('KILL D (direction mapping) fired:',kD,'| KILL B (rate mapping) fired:',kB)
