# SCRIPT: PBH-NU-FIG6-DOOR  witness strength terrain (log10 R_ret at tau=4.0) from witness_prod.json
import json, math, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import os; HERE=os.path.dirname(os.path.abspath(__file__)); PAPER=os.path.normpath(os.path.join(HERE,'..','..'))
d=json.load(open(os.path.join(PAPER,'code','witness','witness_prod.json')))   # rebuilt from prod.log by code/witness/prod_log_to_json.py
ratios=[0.1,0.25,0.5,1,2]; Ls=[1,2,3,4]; FLOOR=-32
fig=plt.figure(figsize=(12,5.2))
for p,n in enumerate((3,6)):
    ax=fig.add_subplot(1,2,p+1,projection='3d')
    for r in d:
        if r['n']!=n: continue
        i=ratios.index(r['ratio']); j=Ls.index(r['L'])
        z=math.log10(r['res']['4.0']['R_ret'])
        col=cm.viridis((z-FLOOR)/(0-FLOOR))
        ax.bar3d(i-0.35,j-0.35,FLOOR,0.7,0.7,z-FLOOR,color=col,shade=True,edgecolor='k',linewidth=0.3)
    X,Y=np.meshgrid([-0.6,4.6],[-0.6,3.6]); ax.plot_surface(X,Y,np.full_like(X,-3.0),color='red',alpha=0.18)
    ax.set_xticks(range(5)); ax.set_xticklabels([str(x) for x in ratios])
    ax.set_yticks(range(4)); ax.set_yticklabels([str(l) for l in Ls])
    ax.set_zlim(FLOOR,0); ax.set_zticks([-30,-20,-10,-3,0])
    ax.set_xlabel('plant time / decoupling time',labelpad=8); ax.set_ylabel('moment holding the difference, l',labelpad=8); ax.set_zlabel('log$_{10}$ R$_{ret}$ at $\\tau$=4')
    ax.view_init(elev=22,azim=-128)
    ax.text2D(0.03,0.92,'n = %d'%n,transform=ax.transAxes,fontsize=13,weight='bold')
fig.text(0.5,0.02,'red plane: witness on (R$_{ret}$ = 10$^{-3}$)',ha='center',fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(PAPER,'figs','fig6_door.png'),dpi=300,facecolor='white')
