# SCRIPT: PBH-NU-FIGURES  draws the three figures from the run results and the memory curves
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
mc=json.load(open('code/main/memory_curve.json'))
ed3=[0.25,0.5,0.75,1,1.5,2,3,4,6,8]; ed6=[0.5,1,1.5,2,3,4]
G3=[mc['3_%g'%e]['two_epoch'] for e in ed3]; G6=[mc['6_%g'%e]['two_epoch'] for e in ed6]
steve_e=[0.25,0.5,1,2,4,8]; steve_G=[0.959,0.867,0.683,0.431,0.190,0.063]
# Fig 1
fig,ax=plt.subplots(figsize=(7.2,4.6))
ax.plot(ed3,G3,'-',color='#1f5fa8',lw=2,label='kept-sector memory, rate $\\propto\\epsilon^{-3}$ (one weight fitted here)')
ax.plot(ed6,G6,'--',color='#c0392b',lw=2,label='kept-sector memory, rate $\\propto\\epsilon^{-6}$ (prediction)')
ax.plot(steve_e,steve_G,'o',color='k',ms=7,label='McCormick, Gaussian, rate $\\propto\\epsilon^{-3}$')
ax.plot([4,8],[0.181,0.045],'s',color='#2e8b57',ms=8,label='this work, broad profile $\\alpha=0.3$, rate $\\propto\\epsilon^{-3}$')
ax.errorbar([2],[0.317],yerr=[0.004],fmt='D',color='#c0392b',ms=8,label='this work, Gaussian, rate $\\propto\\epsilon^{-6}$')
ax.plot([2],[0.431],'x',color='gray',ms=10,mew=2); ax.annotate('if only $\\epsilon_{dec}$ mattered',(2,0.431),(2.6,0.52),fontsize=9,color='gray',arrowprops=dict(arrowstyle='->',color='gray'))
ax.set_xscale('log'); ax.set_xticks([0.25,0.5,1,2,4,8]); ax.set_xticklabels(['0.25','0.5','1','2','4','8']); ax.minorticks_off(); ax.set_xlabel('decoupling time $\\epsilon_{dec}$'); ax.set_ylabel('surviving share of the free-streaming shift, $G$')
ax.set_ylim(0,1.02); ax.legend(fontsize=8.2,loc='lower left',frameon=False); ax.set_title('How much of the neutrino effect survives gradual decoupling',fontsize=11)
fig.tight_layout(); fig.savefig('figs/fig1_G.png',dpi=220)
# Fig 2: Legendre chain
fig,ax=plt.subplots(figsize=(7.2,2.6)); ax.axis('off')
xs=np.arange(6)*1.2
for i,x in enumerate(xs):
    ax.add_patch(plt.Circle((x,0),0.28,color=['#f4d03f','#e67e22','#c0392b','#8e44ad','#8e44ad','#8e44ad'][i],zorder=3))
    ax.text(x,0,'$\\ell=%d$'%i if i<5 else '$\\cdots$',ha='center',va='center',fontsize=10,zorder=4,color='white' if i>1 else 'k')
for i in range(5):
    lw=[6,4,0.8,0.8,0.8][i]; col=['#c0392b','#e67e22','#bbbbbb','#bbbbbb','#bbbbbb'][i]
    ax.plot([xs[i]+0.28,xs[i+1]-0.28],[0,0],color=col,lw=lw,zorder=2)
ax.text((xs[0]+xs[1])/2,0.45,'$k^2\\kappa_1^2/3$',ha='center',fontsize=10,color='#c0392b')
ax.text((xs[1]+xs[2])/2,0.45,'$\\frac{4k^2}{15}(\\kappa_2-\\kappa_1)^2$',ha='center',fontsize=10,color='#e67e22')
ax.text((xs[3]+xs[4])/2,0.45,'0',ha='center',fontsize=10,color='gray')
ax.text(xs[0],-0.6,'density\n(kept)',ha='center',fontsize=8.5); ax.text(xs[1],-0.6,'flux\nrate $\\kappa_1$',ha='center',fontsize=8.5); ax.text(xs[2],-0.6,'shear\nrate $\\kappa_2$',ha='center',fontsize=8.5); ax.text(xs[4],-0.6,'higher moments\nrate $\\kappa_2$',ha='center',fontsize=8.5)
ax.set_xlim(-0.5,xs[-1]+0.5); ax.set_ylim(-1.0,0.85)
ax.set_title('Where the non-normality of the neutrino collision operator lives',fontsize=11)
fig.tight_layout(); fig.savefig('figs/fig2_chain.png',dpi=220)
# Fig 3: clock set early
fig,ax=plt.subplots(figsize=(7.2,3.6))
ax.bar([0.8,2.8],[0.190,0.063],0.35,color='#555555',label='Gaussian (McCormick): collapses at $\\epsilon\\approx4$')
ax.bar([1.2,3.2],[0.181,0.045],0.35,color='#2e8b57',label='broad profile $\\alpha=0.3$ (this work): collapses at $\\epsilon\\approx7$-$9$')
ax.plot([0.8,1.2,2.8,3.2],[0.38,0.38,0.17,0.17],'_',ms=0)
ax.hlines([0.42],1.02,1.38,colors='#c0392b',linestyles='dotted',lw=2); ax.hlines([0.205],3.02,3.38,colors='#c0392b',linestyles='dotted',lw=2)
ax.text(1.2,0.44,'if the clock were the collapse time',ha='center',fontsize=8.5,color='#c0392b'); ax.text(3.38,0.235,'if the clock were the collapse time',ha='right',fontsize=8.5,color='#c0392b')
ax.set_xticks([1,3]); ax.set_xticklabels(['$\\epsilon_{dec}=4$','$\\epsilon_{dec}=8$']); ax.set_ylabel('$G$'); ax.set_ylim(0,0.6)
ax.legend(fontsize=8.5,frameon=False,loc='upper right',bbox_to_anchor=(1.0,0.98)); ax.set_title('The clock is set early: a late collapse does not change $G$',fontsize=11)
fig.tight_layout(); fig.savefig('figs/fig3_clock.png',dpi=220)
print('ok')
