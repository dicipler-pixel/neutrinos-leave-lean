# AGENT B: what survives a hot rebirth? integrate the erasure exponent int kappa dt from T_max down to the 1 MeV wall
import numpy as np
# radiation era: kappa/H = (T/T_d)^3, dlna = -dT/T  =>  int kappa dt = int (kappa/H) dlna = [(Tmax/T_d)^3 - 1]/3
for name,Td in [("number/energy (e±, T_d≈1 MeV)",1.0),("momentum drag only, hypothetical T_d≈2 MeV",2.0)]:
    for Tm in [1.5,2,3,5,10]:
        X=max(0,((Tm/Td)**3-1)/3); print(f" {name:45s} T_max={Tm:4.1f} MeV: erasure exponent {X:8.2f}, survival {np.exp(-X):.2e}")
print("Zeno-sealed pocket: if the pocket's leak is k²c²/kappa_n instead of kappa, the exponent becomes int (k²c²/kappa_n) dt, which FALLS as T rises:")
for Tm in [2,5,10,100]:
    # leak/H = (k/aH)^2 c^2 / (kappa_n/H); take kappa_n/H=(T/1)^3 and k/aH = eps^-1 with eps = T_d/T times eps_d=2
    T=np.linspace(1,Tm,4000); epsd=2.0; leakH=(1/(epsd*1.0/T))**2*0.267/((T/1.0)**3+1e-9)
    X=np.trapezoid(leakH/T,T); print(f"   T_max={Tm:5.0f} MeV: Zeno leak exponent {X:.3f}, survival {np.exp(-X):.3f}")
