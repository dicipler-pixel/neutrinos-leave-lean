# AGENT J: a flavour record (asymmetry stored as P_z) in a ditch covered by the electron sea. The fire = collisions Γ (flavour-
# blind, can't change P_z alone); the cover = thermal potential V (blocks oscillation). Leak = oscillation + collisions together:
# Stodolsky rate  Γ_conv = (Γ/2)·Δ²s² / [ (Δc + |V|)² + Δ²s² + (Γ/2)² ]   (s = sin 2θ, c = cos 2θ; thermal V has no resonance)
# Units: rates per Hubble time, T in MeV. Atmospheric Δ/H ≈ 9.3e5/T³; Γ/H = T³ (weak rate); V/Δ = h·(T/T*)^6 with T* = 5 MeV.
import numpy as np
s2=np.sin(2*0.15)**2; c=np.cos(2*0.15)
def survival(Tmax,h=1.0,g=1.0,Tend=0.5,Tstar=5.0):
    T=np.geomspace(Tmax,Tend,20000); D=9.3e5/T**3; G=g*T**3; V=h*D*(T/Tstar)**6
    rate=(G/2)*D*D*s2/((D*c+V)**2+D*D*s2+(G/2)**2)
    X=np.trapezoid(rate/T,T[::-1]) if False else -np.trapezoid(rate,np.log(T))   # d ln a = -d ln T
    return np.exp(-X)
print("flavour record surviving from T_max down to 0.5 MeV")
print("            heat on the cover h:   x0.1        x1         x10        x100")
for Tm in [3,5,10,30,100]:
    print(f" T_max={Tm:5.0f} MeV:              "+"   ".join(f"{survival(Tm,h):.3f}" for h in [0.1,1,10,100]))
print("where the leak happens (cover x1): rate per ln a at temperature T")
for T in [30,10,5,3,2,1,0.7]:
    D=9.3e5/T**3; G=T**3; V=D*(T/5)**6; r=(G/2)*D*D*s2/((D*c+V)**2+D*D*s2+(G/2)**2); print(f"   T={T:5.1f} MeV: cover/oscillation V/Δ = {V/D:9.2e}, fire Γ/Δ = {G/D:9.2e}, leak per ln a = {r:9.3e}")
print("heat the fire too (collisions x10) with cover x1:", f"{survival(30,1,10):.3f}", " vs fire x1:", f"{survival(30,1,1):.3f}")
