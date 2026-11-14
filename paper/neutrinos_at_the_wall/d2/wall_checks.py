# SCRIPT: NAW-CHECKS-02  The Neutrinos at the Wall: every number in the paper not taken from v10's archived runs.
import numpy as np, math
from scipy.linalg import expm
from scipy.special import erfc; from scipy.optimize import brentq
s=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.array([[1,0],[0,-1]],complex)]
B=lambda r,i: expm(0.5*r*s[i])                       # SL(2,C) boost of rapidity r along axis i
print("1. Commutator of two equal perpendicular boosts: tr = 2 - 4 sinh^4(r/2)")
for r in [0.5,1.0,math.log(3+2*math.sqrt(2)),2.5]:
    K=B(r,0)@B(r,1)@np.linalg.inv(B(r,0))@np.linalg.inv(B(r,1)); print(f"   r={r:.6f} tr={np.trace(K).real:+.9f} formula={2-4*math.sinh(r/2)**4:+.9f}")
rw=math.log(3+2*math.sqrt(2)); print(f"   parabolic (tr=-2) at r=ln(3+2sqrt2)={rw:.9f}; Gamma=tanh(r/2)={math.tanh(rw/2):.9f}=1/sqrt2={1/math.sqrt(2):.9f}; z=e^r={math.exp(rw):.9f}")
print("2. Neutrino masses on the wall (m1=0, normal ordering); NuFIT 6.0 central values")
d21,d31,s12,s13=7.49e-5,2.534e-3,0.307,0.02195; z=3+2*math.sqrt(2)
m2=math.sqrt(d21); m3=z*m2; c13=1-s13
print(f"   m2={m2*1e3:.3f} meV m3={m3*1e3:.3f} meV sum={(m2+m3)*1e3:.2f} meV; predicted d31/d21={z*z:.4f} (measured {d31/d21:.3f}); predicted d31={m3**2:.4e}")
print(f"   m_beta={1e3*math.sqrt(s12*c13*m2**2+s13*m3**2):.2f} meV; m_bb in [{1e3*abs(m2*s12*c13-m3*s13):.2f},{1e3*(m2*s12*c13+m3*s13):.2f}] meV")
for m1 in [0,1e-3,2e-3,5e-3]:
    M2=math.sqrt(m1**2+d21); M3=math.sqrt(m1**2+d31); print(f"   m1={m1*1e3:.0f} meV: m3/m2={M3/M2:.4f} (wall {z:.4f})")

print("2b. Current inputs (first JUNO dm21, NuFIT 6.1 dm31, as used by Alikhanov 2026)")
d21b,e21,d31b,e31=7.50e-5,0.12e-5,2.529e-3,0.021e-3; rb=math.sqrt(d31b/d21b); eb=0.5*rb*math.sqrt((e21/d21b)**2+(e31/d31b)**2)
print(f"   ratio d31/d21={d31b/d21b:.3f}; m3/m2={rb:.4f} +/- {eb:.4f}; pull from wall {(rb-z)/eb:+.2f} sigma")
lo=brentq(lambda m1: (math.sqrt((m1**2+d31b)/(m1**2+d21b))-z)/eb+2,0,5e-3); print(f"   m1 where the pull reaches -2 sigma: {lo*1e3:.2f} meV")
print("9. Turn or run of the square of two equal steps (Two Trees Thm 5.3, 5.4; BallJoins J3)")
for lab,zz in [('nu, current',rb),('nu, NuFIT 6.0',math.sqrt(d31/d21)),('wall',z),('mu->tau',1776.86/105.6583755)]:
    gq=(zz-1)**2/(4*zz); Gm=(zz-1)/(zz+1)
    if gq<1:
        sq=math.sqrt(1-2*Gm*Gm); print(f"   {lab}: z={zz:.4f} g={gq:.5f} turn {math.degrees(4*math.acos(gq)):.2f} deg, fixed point tanh(rho/2)={math.sqrt((1-sq)/(1+sq)):.4f}")
    else: print(f"   {lab}: z={zz:.4f} g={gq:.5f} run length {4*math.acosh(gq):.4f}")
print("3. Koide: Q and the 45-degree cone")
me,mm,mt=0.51099895,105.6583755,1776.86
Q=(me+mm+mt)/(math.sqrt(me)+math.sqrt(mm)+math.sqrt(mt))**2; print(f"   Q={Q:.9f}; cos^2(angle to (1,1,1))=1/(3Q)={1/(3*Q):.9f}")
print("   generation steps z and Gamma: ",{k:(round(v,2),round((v-1)/(v+1),3)) for k,v in {'e->mu':mm/me,'mu->tau':mt/mm}.items()})
print("4. Kept-sector onset and non-orthogonality")
for phi in [0.5,1.0,1.4,1.55]: print(f"   phi=k/kappa={phi}: s+kappa=k cot(phi)/k={1/math.tan(phi):.4f}, K=4phi^2/sin^2(2phi)={4*phi**2/math.sin(2*phi)**2:.4f}")
print("5. Horizon mass and decoupling epoch (g*=10.75)")
G,c,hb,MeV,Ms=6.674e-11,2.998e8,1.0546e-34,1.602e-13,1.989e30
rho=(math.pi**2/30)*10.75*MeV**4/(hb*c)**3/c**2; H=math.sqrt(8*math.pi*G*rho/3); MH=4/3*math.pi*rho*(c/H)**3/Ms
print(f"   M_H(1 MeV)={MH:.3g} Msun; eps_dec 1,2,3,4 -> {[f'{e*e*MH:.2g}' for e in [1,2,3,4]]}")
print("6. Abundance from the measured door shifts (v10 Sec. 10)")
dc0=0.51075; sh={'l3 a':1.83e-3,'l3 b':-1.91e-3,'l4 a':-1.08e-3,'l4 b':1.02e-3,'G a':2.69e-3,'G b':-2.82e-3,'split':3.1e-4}
for b0 in [1e-6,1e-10,1e-16]:
    sg=brentq(lambda x: erfc(dc0/(math.sqrt(2)*x))-b0,0.01,1); f=lambda d: erfc((dc0+d)/(math.sqrt(2)*sg))/b0
    print(f"   beta0={b0:g}: "+", ".join(f"{k}:{f(d):.2f}" for k,d in sh.items())+f", random G:{(f(sh['G a'])+f(sh['G b']))/2:.3f}, random l4:{(f(sh['l4 a'])+f(sh['l4 b']))/2:.3f}")
print("7. Fold of the radiation era: a(eta) ~ eta, t ~ eta^2/2 => a ~ sqrt(2t); da/dt ~ 1/sqrt(2t) diverges, a(eta) odd and analytic")
for e in [0.1,0.01,-0.01]: print(f"   eta={e:+.2f}: a={e:+.3f}, t={e*e/2:.5f}, da/dt={1/e:+.1f}")
print("8. Fermion record: tau=hw/kT, Gamma=tanh(tau/2); at decoupling T=1 MeV, mean neutrino energy 3.15 T -> Gamma=",round(math.tanh(3.15/2),4))
