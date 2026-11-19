# SCRIPT: K3-EP-CROSSING-AND-G
# (i) Re-derive where the two-moment operator crosses its exceptional point under kappa = H (e_dec/e)^3 (e = eps).
#     Units r_m=1, conformal time tau = eps (radiation era: tau = eps r_m, a*H = 1/tau). Rate in conformal time: sigma = kappa/(aH)... 
#     precisely a*kappa = (kappa/H)*(aH) = (e_dec/e)^3 / tau = e_dec^3 e^-4.  Two-moment: e' = -k q, q' = -(k/3) e - sigma q,
#     eigenvalues l^2 + sigma l + k^2/3 = 0, EP when sigma = 2k/sqrt3. Take k = 2 (k ~ 2/r_m, the earlier note's choice).
#     Claim to test: eps_EP = (sqrt3/4)^(1/4) e_dec^(3/4) = 0.811 e_dec^0.75  (earlier note: 0.658 e_dec^1.5).
# KILL (before run): if a root-find of the actual 2x2 matrix does not reproduce 0.811*e_dec^0.75 to 1e-6, the re-derivation is wrong.
# (ii) Parameter-free G predictions from eps_EP and Steve's PF apparent-horizon time eps_AH = 4.0 (his number, not fitted to G):
#     A: G = 1 - eps_EP/eps_AH       B: G = ln(eps_AH/eps_EP)/ln(eps_AH/0.1)      C: G = 1 - (eps_EP/eps_AH)^2   (clip 0..1)
#     Primary = A (written first). KILL: max |G_pred - G_pub| > 0.10.  B, C reported as sensitivity only.
# OPPOSITE (run once): the inverse ruler  G' = eps_EP/eps_AH  (wrong direction) and the earlier-note law eps_EP = 0.658 e_dec^1.5 in A.
import numpy as np
from scipy.optimize import brentq
k=2.0; edec=np.array([.25,.5,1,2,4,8]); Gp=np.array([.959,.867,.683,.431,.190,.063])
def sigma(e,ed): return ed**3/e**4
def disc_gap(e,ed):
    s=sigma(e,ed); M=np.array([[0,-k],[-k/3,-s]]); w=np.linalg.eigvals(M); return abs(w[0]-w[1])   # 0 at EP
epn=[]
for ed in edec:
    # EP where discriminant sigma^2-4k^2/3 changes sign
    f=lambda e: sigma(e,ed)**2-4*k*k/3
    epn.append(brentq(f,1e-3,1e3))
epn=np.array(epn); print('eps_EP numeric      :',np.round(epn,4)); print('0.811*edec^0.75    :',np.round((np.sqrt(3)/4)**.25*edec**.75,4))
print('earlier note 0.658 edec^1.5:',np.round(0.658*edec**1.5,4))
slope=np.polyfit(np.log(edec),np.log(epn),1); print('fitted log-log slope of eps_EP vs edec: %.4f'%slope[0])
print('KILL (i):', 'did not fire' if np.allclose(epn,(np.sqrt(3)/4)**.25*edec**.75,rtol=1e-6) else 'FIRED')
eAH=4.0
def rep(name,G): print('%-34s'%name, np.round(G,3),' max|err| %.3f'%np.max(np.abs(G-Gp)))
print('published G                       ',Gp)
rep('A  1-eEP/eAH (primary)',np.clip(1-epn/eAH,0,1))
rep('B  ln(eAH/eEP)/ln(eAH/0.1)',np.clip(np.log(eAH/epn)/np.log(eAH/0.1),0,1))
rep('C  1-(eEP/eAH)^2',np.clip(1-(epn/eAH)**2,0,1))
rep('opposite  eEP/eAH',np.clip(epn/eAH,0,1))
rep('opposite  A with note eEP=.658e^1.5',np.clip(1-0.658*edec**1.5/eAH,0,1))
print('G/(1-G) published:',np.round(Gp/(1-Gp),3),'; successive ratios',np.round((Gp/(1-Gp))[:-1]/(Gp/(1-Gp))[1:],2))
print('log-log slope of G/(1-G) vs edec: %.3f'%np.polyfit(np.log(edec),np.log(Gp/(1-Gp)),1)[0])
