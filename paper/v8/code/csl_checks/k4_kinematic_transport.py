# SCRIPT: K4-KINEMATIC-LEAKY-TRANSPORT
# Mapping: paper Sec.6 + Sec.8 (leader = slowest-surviving positive channel; "transfer" outflow vs independent decay). Steve's contest is
# neutrino overdensity leaving at c versus plasma overdensity dispersing at c_s. Gravity-free linear kinematics of Steve's own collision
# model (Eq.7,10) with his gradual decoupling kappa = H (e_dec/e)^3  =>  conformal rate sigma(tau) = e_dec^3 / tau^4  (r_m = 1, tau = eps).
# State per wavenumber k: plasma (delta_g, theta_g) + neutrino Legendre hierarchy F_l; collisions relax F_l (l>=1) toward the plasma
# frame at sigma, momentum returned to plasma with weight R/(1-R). Gaussian profile delta(x)=(2/3)(1-(2/3)x^2)exp(-x^2) (gradient expansion,
# Eq.13 with K=exp(-x^2)); FT = (2/3)pi^1.5 (k^2/6) exp(-k^2/4). Diagnostic: total overdensity energy inside radius x_c.
#   E(tau) = int 4pi k^2 dk/(2pi)^3 dFT(k) [(1-R) dg + R dnu](k,tau) Theta(k),  Theta = 4pi (sin(k x_c)-k x_c cos(k x_c))/k^3.
#   G_K4(e_dec) = [E_PF - E_grad(e_dec)] / [E_PF - E_inst]   at tau = eps* ; PF = tight coupling (single fluid, delta = cos(c_s k tau)).
# PRIMARY (written before run): eps* = 4.0 (Steve's PF apparent-horizon time, not fitted), x_c = 1 (r_m).  Sensitivity: eps* in {1.7,3,4.5}, x_c in {0.5,2}.
# KILL: max_i |G_K4 - G_pub| > 0.10 at the primary setting.
# OPPOSITE (run once): the inverse selection, i.e. let the PLASMA channel lead: G_opp = [E_gam,PF - E_gam,grad]/[...] using the plasma
#   overdensity only (does the back-reaction on the plasma carry the selection?).
import numpy as np, time
from scipy.integrate import solve_ivp
R=0.409; N=60; edecs=[.25,.5,1,2,4,8]; Gp=np.array([.959,.867,.683,.431,.190,.063])
ks=np.linspace(0.05,9.0,160); w=np.diff(np.concatenate([[0],(ks[1:]+ks[:-1])/2,[ks[-1]]]))
dFT=lambda k:(2/3)*np.pi**1.5*(k**2/6)*np.exp(-k**2/4)
def build(k):
    n=2+N; A0=np.zeros((n,n)); A1=np.zeros((n,n)); iF=lambda l:2+l
    A0[0,1]=-4/3; A0[1,0]=k*k/4; A0[iF(0),iF(1)]=-k
    for l in range(1,N):
        A0[iF(l),iF(l-1)]+=k*l/(2*l+1)
        if l<N-1: A0[iF(l),iF(l+1)]+=-k*(l+1)/(2*l+1)
        A1[iF(l),iF(l)]-=1.0
    A1[1,1]-=R/(1-R); A1[1,iF(1)]+=R/(1-R)*(3*k/4); A1[iF(1),1]+=4/(3*k)
    return A0,A1
def run(ed,k,tgrid,inst=False):
    A0,A1=build(k); n=A0.shape[0]
    if inst: sig=lambda t:0.0; t0=0.1
    else:
        sig=lambda t:ed**3/t**4; t0=max(0.1,(ed**3/100.0)**0.25)
    y0=np.zeros(n); y0[0]=1; y0[2]=1
    f=lambda t,y:(A0+sig(t)*A1)@y; J=lambda t,y:(A0+sig(t)*A1)
    tt=[t for t in tgrid if t>t0]
    out=np.zeros((len(tgrid),2))
    # before t0 tight coupling: no change in gravity-free fluid with theta=0 (delta=cos(c_s k t) evolves!) -> evolve fluid analytically to t0
    cs=1/np.sqrt(3); y0[0]=np.cos(cs*k*t0) if not inst else 1.0; y0[2]=y0[0]
    if not inst:
        # fluid velocity: delta' = -(4/3) theta -> theta = -(3/4) delta' = (3/4) cs k sin(cs k t0)
        y0[1]=0.75*cs*k*np.sin(cs*k*t0)
        y0[3]=4/(3*k)*y0[1]       # F1 of neutrinos comoving with plasma
    sol=solve_ivp(f,(t0,max(tt)),y0,method='Radau',jac=J,t_eval=tt,rtol=1e-6,atol=1e-9)
    for j,t in enumerate(tt): 
        i=tgrid.index(t); out[i]=[sol.y[0,j],sol.y[2,j]]
    for i,t in enumerate(tgrid):
        if t<=t0: out[i]=[np.cos(cs*k*t)]*2 if not inst else [1.0,1.0]
    return out
tg=[1.7,3.0,4.0,4.5]
t_start=time.time()
cs=1/np.sqrt(3)
res={}
for ed in edecs+['inst']:
    arr=np.zeros((len(ks),len(tg),2))
    for ik,k in enumerate(ks): arr[ik]=run(0 if ed=='inst' else ed,k,tg,inst=(ed=='inst'))
    res[ed]=arr
print('integration time %.1f s'%(time.time()-t_start))
def Eof(arr,xc,which):
    th=4*np.pi*(np.sin(ks*xc)-ks*xc*np.cos(ks*xc))/ks**3
    wgt=4*np.pi*ks**2/(2*np.pi)**3*dFT(ks)*th*w
    g=arr[:,:,0]; n=arr[:,:,1]
    if which=='tot': f=(1-R)*g+R*n
    elif which=='gam': f=g
    return (wgt[:,None]*f).sum(axis=0)
pf=np.array([[np.cos(cs*k*t) for t in tg] for k in ks])
PF=np.stack([pf,pf],axis=2)
for xc in (1.0,0.5,2.0):
    for which in ('tot','gam'):
        Epf=Eof(PF,xc,which); Ei=Eof(res['inst'],xc,which)
        G=np.array([(Epf-Eof(res[ed],xc,which))/(Epf-Ei) for ed in edecs])   # shape (6,len(tg))
        for j,t in enumerate(tg):
            tag='PRIMARY' if (xc==1.0 and which=='tot' and t==4.0) else ('OPPOSITE' if (xc==1.0 and which=='gam' and t==4.0) else '')
            print('xc=%.1f %-3s eps*=%.1f G_K4='%(xc,which,t),np.round(G[:,j],3),' max|err| %.3f %s'%(np.max(np.abs(G[:,j]-Gp)),tag))
print('E_pf, E_inst (xc=1,tot):',np.round(Eof(PF,1.0,'tot'),5),np.round(Eof(res['inst'],1.0,'tot'),5))
