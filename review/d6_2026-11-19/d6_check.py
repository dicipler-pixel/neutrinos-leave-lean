# SCRIPT: NU-D6-REVIEW-01  arithmetic and linear-chain checks of neutrino_submission_d6.pdf
import numpy as np
fl, ins = 0.49773, 0.52832; den = ins-fl
G = lambda d, f=fl, i=ins: (d-f)/(i-f)
tau = lambda g: np.log((1-g)/g)
print("== G values ==")
for name,d,e in [("C",0.51756,0.00019),("B",0.50743,0.00011),("D",0.50245,0.00019),("H1",0.51074,0.00002),("S1",0.51077853,0)]:
    print(f" {name}: G={G(d):.4f} +- {e/den:.4f}")
print(" Test A broad:", round(G(0.45337,0.44805,0.47747),4), round(G(0.44938,0.44805,0.47747),4), "err", round(0.00013/(0.47747-0.44805),4))
g1 = G(0.51077853); t1 = tau(g1)
print("\n== link table (fixed-step), offsets from S1 ==")
rows = [(1/16,0.521485),(1/4,0.516498),(1/2,0.513656),(1/1.2,0.5115145),(0.8,0.5116957),(1.0,0.51074),(1.2,0.5100149),(1.25,0.5098407),(2,0.507973),(4,0.505442),(16,0.501673)]
X=[];Y=[]
for r,d in rows:
    g=G(d); off=tau(g)-t1; X.append(0.5*np.log(r)); Y.append(off)
    print(f" r={r:7.4f} Gamma={(r-1)/(r+1):+.3f} rap={0.5*np.log(r):+.3f} G={g:.3f} off={off:+.3f}")
X=np.array(X);Y=np.array(Y)
p=np.polyfit(X,Y,1); res=Y-np.polyval(p,X); print(f" line fit slope={p[0]:.4f} icpt={p[1]:+.4f} rms={np.sqrt(np.mean(res**2)):.4f}")
p0=np.sum(X*Y)/np.sum(X*X); print(f" through-origin slope={p0:.4f} rms={np.sqrt(np.mean((Y-p0*X)**2)):.4f}")
print(" shifts at r=1/4, 4 from S1:", round(G(0.516498)-g1,3), round(G(0.505442)-g1,3))
print("\n== odd rates ==")
odd=lambda dr,dir_,r,f=fl: (np.log((ins-dr)/(dr-f))-np.log((ins-dir_)/(dir_-f)))/np.log(r)
for r,a,b in [(1.2,0.5100149,0.5115145),(1.25,0.5098407,0.5116957),(2,0.507973,0.513656),(4,0.505442,0.516498),(16,0.501673,0.521485)]:
    ev = 0.5*(tau(G(a))+tau(G(b)))-t1
    print(f" r={r}: odd={-odd(a,b,r):.4f}  even part={ev:+.3f}")
print(" stage-correct r=1.2:", round(-odd(0.51000812,0.51151594,1.2),4), " r=1.25:", round(-odd(0.50984158,0.51169233,1.25),4))
for lv,a,b in [(1,0.50984158,0.51169233),(2,0.50991687,0.51175643),(3,0.5099481,0.5117877)]:
    print(f" level {lv}: odd={-odd(a,b,1.25):.4f}")
o1,o2,o3=[-odd(a,b,1.25) for a,b in [(0.50984158,0.51169233),(0.50991687,0.51175643),(0.5099481,0.5117877)]]
print(f" observed order p = ln((o1-o2)/(o2-o3))/ln(1.5) = {np.log((o1-o2)/(o2-o3))/np.log(1.5):.2f}")
for s in [+7.8e-5,-7.8e-5]: print(f" level3 with fluid ref shifted {s:+.1e}: {-odd(0.5099481,0.5117877,1.25,fl+s):.4f}")
print(" shear only r=1.2:", round(-odd(0.50995463,0.51157978,1.2),4), " r=4:", round(-odd(0.50523503,0.51709419,4),4))
print(" budget quad/lin:", round(np.sqrt(.0075**2+.0038**2+.0036**2),4), .0075+.0038+.0036)
print("\n== door ==")
f0=0.5107500
for nm,a,b in [("0.5 l3",0.5107685,0.5107510),("0.5 l4",0.5107685,0.5107500),("2 l3",0.5125833,0.5088395),("2 l3 N48",0.5125134,0.5090041),("2 l4",0.5096749,0.5117726),("2 Gram",0.5134352,0.5079300),("4 l3",0.5108796,0.5106358),("4 l4",0.5106759,0.5108241)]:
    print(f" {nm}: diff={a-b:+.4e}  +f shift {a-f0:+.3e}  -f shift {b-f0:+.3e}")
print(" l4/l3 =", round(2.0977/3.7438,3), " Gram/l3 =", round(5.5052/3.7438,3), " l3 diff / whole shift =", round(3.7438e-3/den,3), round(3.5093e-3/den,3))
print(" f=0 restart minus H1 =", f"{f0-0.51074:+.2e}", " minus S1 =", f"{f0-0.51077853:+.3e}")
print(" spread of three baselines:", round(0.431-G(0.51074),4))
print("\n== connection energy, Eq (4) and six-group shares ==")
for rho in [1.5,7]: print(f" rho={rho}: shear share = {(4/15*rho**2)/(1/3+4/15*rho**2):.4f}")
rng=np.random.default_rng(1)
for _ in range(3):
    k,k1,k2=rng.uniform(0.1,3,3); N=30; l=np.arange(N); c=(l[:-1]+1)/np.sqrt((2*l[:-1]+1)*(2*l[:-1]+3))
    mu=np.diag(c,1)+np.diag(c,-1); A=-1j*k*mu; D=-np.diag([0,k1]+[k2]*(N-2)); L=A+D
    C=L@L.conj().T-L.conj().T@L
    print(f" ||[L,L*]||^2/8={np.linalg.norm(C)**2/8:.10f}  Eq4={k*k*k1*k1/3+4*k*k/15*(k2-k1)**2:.10f}")
print("\n== kept-sector onset, 200 moments; non-orthogonality K ==")
def chain(kap,k=1.0,N=200):
    l=np.arange(N); c=(l[:-1]+1)/np.sqrt((2*l[:-1]+1)*(2*l[:-1]+3))
    return -1j*k*(np.diag(c,1)+np.diag(c,-1)) - kap*np.diag([0]+[1]*(N-1))
def least(kap):
    w,V=np.linalg.eig(chain(kap)); i=np.argmax(w.real); return w[i],V[:,i]
lo,hi=0.6,0.7
for _ in range(50):
    m=(lo+hi)/2; w,_=least(m)
    if abs(w.imag)>1e-9: lo=m
    else: hi=m
print(f" least-damped mode turns complex at kappa/k = {hi:.4f}  (2/pi = {2/np.pi:.4f})")
from scipy.optimize import brentq
for kap in [1.0,0.9,0.8,0.7]:
    w,v=least(kap); Kp=(np.vdot(v,v).real)**2/abs(v@v)**2
    s=brentq(lambda s: np.arctan(1/(s+kap))-1/kap, -kap+1e-12, 50)
    phi=1/kap
    print(f" kappa/k={kap}: chain pole {w.real:+.6f}{w.imag:+.1e}i  closed form {s:+.6f}  Petermann K={Kp:.5f}  4phi^2/sin^2(2phi)={4*phi**2/np.sin(2*phi)**2:.5f}")
print("\n== horizon mass ==")
G_N=6.674e-11; c=2.998e8; hbar=1.0546e-34; MeV=1.602e-13; Msun=1.989e30
T=1*MeV; rho=(np.pi**2/30)*10.75*T**4/(hbar*c)**3  # J/m^3
H=np.sqrt(8*np.pi*G_N*rho/(3*c**2)); MH=(4*np.pi/3)*(rho/c**2)*(c/H)**3/Msun
print(f" M_H(1 MeV, g*=10.75) = {MH:.3e} Msun")
for e in [0.5,1,2,3,4,8]: print(f"  eps_dec={e}: {MH/e**2:.2e}")
print("\n== small numbers ==")
print(" e^-42 =", f"{np.exp(-42):.2e}", " 4.8e-17/e^-42 = 10^", round(np.log10(4.8e-17/np.exp(-42)),2))
cs=0.519; f=(1-cs)/(1-1/np.sqrt(3)); print(f" annihilation f = {f:.3f}; 6.31% *f -> {6.31*f:.2f}%  /f -> {6.31/f:.2f}%  (+{(f-1)*100:.1f}%, {(1/f-1)*100:.1f}%)")
print(" two-moment EP / onset ratio pi/sqrt3 =", round(np.pi/np.sqrt(3),3))
print(" 29% less at eps=8:", round(1-0.045/0.063,3))
