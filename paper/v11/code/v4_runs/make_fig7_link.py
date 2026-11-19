# SCRIPT: NU-V4-FIG7-LINK  the flux-shear link: G against Gamma12, and the offset of G against the link rapidity
import json, math, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, os
here=os.path.dirname(os.path.abspath(__file__)); fl,ins=0.49773,0.52832
runs={1/16:'F2_r1o16',0.25:'F_r025',0.5:'J_r05',0.8:'K_r08',1.0:'H1_r1',1.25:'K_r125',2.0:'J_r2',4.0:'F_r4',16.0:'F2_r16'}
r=np.array(sorted(runs)); G=np.array([(json.load(open(os.path.join(here,'res_%s.json'%runs[x])))['dc']-fl)/(ins-fl) for x in r])
Gam=(r-1)/(r+1); x=0.5*np.log(r); tau=np.log((1-G)/G); t1=tau[list(r).index(1.0)]
fig,ax=plt.subplots(1,2,figsize=(11,4.3))
ax[0].plot(Gam,G,'o',color='#1f5fa8',ms=7); ax[0].axhline(G[list(r).index(1.0)],color='0.6',lw=0.8,ls=':')
ax[0].set_xlabel(r'reflection coefficient of the flux–shear link, $\Gamma_{12}=(\kappa_2-\kappa_1)/(\kappa_2+\kappa_1)$')
ax[0].set_ylabel(r'surviving share $G$'); ax[0].set_title('The threshold reads the link')
xx=np.linspace(-1.45,1.45,200)
ax[1].plot(xx,np.sqrt(1.25)*xx,color='#d9822b',lw=1.6,label=r'rate $\sqrt{5/4}=c_0/c_1$')
ax[1].plot(xx,xx,color='0.5',lw=1,ls='--',label='rate 1 (plain peel law)')
ax[1].plot(x,tau-t1,'o',color='#1f5fa8',ms=7,label='measured')
ax[1].set_xlabel(r'link rapidity $\frac{1}{2}\ln(\kappa_2/\kappa_1)$'); ax[1].set_ylabel(r'offset of $G$: $\ln\frac{1-G}{G}-\ln\frac{1-G_1}{G_1}$')
ax[1].set_title('One straight line through the matched link'); ax[1].legend(frameon=False,loc='upper left')
for a in ax: a.grid(alpha=0.25)
plt.tight_layout(); plt.savefig(os.path.join(here,'..','..','figs','fig7_link.png'),dpi=160)
for a,b,c in zip(r,G,tau-t1): print(f'r={a:g} G={b:.4f} offset shift={c:+.4f}')
