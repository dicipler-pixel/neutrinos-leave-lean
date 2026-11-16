# AGENT H: is the neutrino ENERGY SPECTRUM a sealed pocket? Six energy groups (McCormick-like). Elastic scattering mixes angles
# but keeps each neutrino's energy (fast, rate ~E^2); inelastic exchange moves neutrinos between groups (slower, factor eps).
# Plant a spectral distortion (number moved between groups at fixed total) and ask how much survives a hot phase.
import numpy as np
from scipy.linalg import expm
E=np.array([1,2,3,5,8,12.]); G=len(E)
def exchange(eps,T):
    # inelastic kernel relaxing the group populations toward the thermal shape at T (detailed balance), rate eps*T^5-ish scale
    w=E**2*np.exp(-E/T); w/=w.sum(); R=np.zeros((G,G))
    for i in range(G):
        for j in range(G):
            if i!=j: R[i,j]=eps*w[i]*(E[i]*E[j])
    R-=np.diag(R.sum(0)); return R,w
for eps in [1.0,0.1,0.01,0.001]:
    surv=[]
    for Tmax in [2,5,10]:
        # integrate a cooling history from Tmax to 1 MeV; rate scale ~ (T/1)^5 * dt with dt ~ dlnT/(T^2) => weight (T)^3 per dlnT
        x=np.zeros(G); x[1]=+0.05; x[4]=-0.05; Ts=np.geomspace(Tmax,1,400)
        for a,b in zip(Ts[:-1],Ts[1:]):
            R,w=exchange(eps,a); x=expm(R*(a**3)*np.log(a/b))@x
        surv.append(np.abs(x).sum()/0.1)
    print(f" inelastic/elastic = {eps:6.3f}: distortion surviving from T_max = 2, 5, 10 MeV -> {np.round(surv,3)}")
print("elastic scattering alone never changes a group's population: the spectrum is an exact pocket against it;")
print("only the slower inelastic exchange erases it, so survival is set by that ratio, not by how hot the bath is.")
