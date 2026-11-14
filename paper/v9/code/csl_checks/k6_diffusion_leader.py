# SCRIPT: K6-DIFFUSIVE-LEADER-G-CURVE
# STATUS DISCLOSURE: this model was written AFTER the Table II G column had been read (the log-log slope of G/(1-G) ~ -1.6 suggested the
# exponent); the derivation below is independent of the data except for the choice of decision time eps* and of the interpolation rule.
# Derivation (all from Steve's Eq.7,10 and the paper's gap-clock reading, Sec.6/8): units r_m = 1, comoving, conformal time tau = eps.
#   kappa = H (e_dec/e)^3  ->  scattering rate a*kappa = sigma(tau) = e_dec^3 / tau^4          [Steve Eq.10 + gradual-decoupling law]
#   neutrinos (speed 1) diffuse with D = 1/(3 sigma) while sigma*L >> 1, so the NEUTRINO channel's decay rate (its principal Metzler
#   eigenvalue, K1-H2 above) is gamma ~ D (pi/L)^2 and its displacement by tau is  l_diff^2 = c * Int D dtau = c * tau^5/(15 e_dec^3).
#   Free-streaming (instantaneous decoupling) displaces by l_ball = tau.  Series (resistance) interpolation 1/l = 1/l_diff + 1/l_ball and
#   G := l/l_ball = 1/(1 + l_ball/l_diff) = 1/(1 + sqrt(15/c) (e_dec/e*)^(3/2)).        [c = 1: l^2 = Int D dtau ; c = 2: 1-D rms ; c = 6: 3-D rms]
# PRE-STATED PASS (this script): max|G_pred - G_pub| <= 0.10 with eps* = 4.0 (Steve's PF apparent-horizon time) and c = 1. Because c is a convention
#   the other c are reported and the one-parameter best fit is reported so that the size of the freedom is visible.
# KILL for the exponent claim: a free-exponent fit must give n = 3/2 within its own 2-sigma bootstrap/fit uncertainty, else the diffusion scaling is dead.
# OPPOSITE: ballistic-limited regime reading G = 1 - l_diff/l_ball clipped, and G = exp(-l_ball/l_diff).
import numpy as np
from scipy.optimize import least_squares
ed=np.array([.25,.5,1,2,4,8]); G=np.array([.959,.867,.683,.431,.190,.063])
def V1(e,es=4.0,c=1.0): return 1/(1+np.sqrt(15/c)*(e/es)**1.5)
print('published   ',G)
for es in (3.5,4.0,4.5):
    for c in (1.0,2.0,6.0):
        g=V1(ed,es,c); print('V1 e*=%.1f c=%.0f'%(es,c),np.round(g,3),'max|err| %.3f'%np.max(np.abs(g-G)))
# one-parameter fits
r=least_squares(lambda p:1/(1+p[0]*(ed/4.0)**1.5)-G,[3.0]); A=r.x[0]; print('1-param (exponent 3/2, e*=4): A_fit=%.3f  (c-equivalent %.2f)  max|err| %.3f'%(A,15/A**2,np.max(np.abs(r.fun))))
r=least_squares(lambda p:1/(1+np.sqrt(15)*(ed/p[0])**1.5)-G,[4.0]); print('1-param (c=1): e*_fit=%.3f max|err| %.3f'%(r.x[0],np.max(np.abs(r.fun))))
# free exponent with covariance
def res(p): return 1/(1+p[0]*(ed/4.0)**p[1])-G
r=least_squares(res,[3.0,1.5]); J=r.jac; s2=np.sum(r.fun**2)/(len(ed)-2); cov=np.linalg.inv(J.T@J)*s2
print('free exponent fit: A=%.3f+-%.3f  n=%.3f+-%.3f  max|err| %.3f'%(r.x[0],np.sqrt(cov[0,0]),r.x[1],np.sqrt(cov[1,1]),np.max(np.abs(r.fun))))
print('KILL (exponent): n=1.5 is %.1f sd from fitted n'%(abs(r.x[1]-1.5)/np.sqrt(cov[1,1])))
# opposites
l=np.sqrt(1/15)*(ed/4.0)**-1.5*0+ (4.0**2.5)/np.sqrt(15*ed**3)   # l_diff with c=1, eps*=4
lb=4.0
print('OPP1 G=1-l_diff/l_ball clipped ',np.round(np.clip(1-l/lb,0,1),3),'max|err| %.3f'%np.max(np.abs(np.clip(1-l/lb,0,1)-G)))
print('OPP2 G=exp(-l_ball/l_diff)     ',np.round(np.exp(-lb/l),3),'max|err| %.3f'%np.max(np.abs(np.exp(-lb/l)-G)))
print('OPP3 quadrature G=(1+15 x^3)^-1/2',np.round((1+15*(ed/4.0)**3)**-.5,3),'max|err| %.3f'%np.max(np.abs((1+15*(ed/4.0)**3)**-.5-G)))
# predictions (new, untested)
for es,tag in ((4.0,'Gaussian'),(8.0,'alpha=0.3 (decided at eps~7-9, Steve Sec.III B)')):
    print('PREDICT %-48s'%tag,{e:round(float(V1(e,es,1.0)),3) for e in (0.1,1,2,4,8,16)})
# Rnu check: odds linear in R? G is defined as ratio so the model predicts the R_nu-independence of G
print('R_nu enters only through the overall (rate) scale -> G(e_dec) curve independent of R_nu (UNTESTED; Steve ran gradual decoupling only at R=0.409)')
