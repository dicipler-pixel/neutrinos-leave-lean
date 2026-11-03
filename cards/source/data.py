# SCRIPT: CARDS-DATA  exact numbers for the P1-P4 card videos (k = 1 throughout; everything is in units of k)
import numpy as np, json, sys
from numpy.polynomial.legendre import leggauss, legval
cl = lambda l: (l+1)/np.sqrt((2*l+1)*(2*l+3))
def M(N, start=0):
    l = np.arange(start, start+N-1); c = cl(l)
    return np.diag(c,1)+np.diag(c,-1)
out = {}
# ---------- P1: free-streaming memory kernel, its running integral, Z_b(s), reflection S(w)
N = 1200; MQ = M(N, 1); lam, V = np.linalg.eigh(MQ); w1 = V[0]**2
c0 = cl(0)
t = np.linspace(0, 60, 2401)
K = c0**2*(w1[None,:]*np.cos(np.outer(t, lam))).sum(1)
R = np.concatenate([[0], np.cumsum(0.5*(K[1:]+K[:-1])*np.diff(t))])
s = np.linspace(0, 3, 301); Zb = np.where(s>0, 1/np.arctan(1/np.maximum(s,1e-12)) - s, 2/np.pi)
w = np.linspace(-4, 4, 801); sw = 1e-9 + 1j*w
Zw = 1/np.arctan(1/sw) - sw; Z0 = 1/np.sqrt(3); S = (Zw - Z0)/(Zw + Z0)
print('P1  R(60)=%.5f  mean R over t in [40,60]=%.5f  2/pi=%.5f  Zb(0)/Z0=%.5f |S(0)|=%.4f' % (R[-1], R[t>=40].mean(), 2/np.pi, (2/np.pi)/Z0, abs(S[400])))
out['P1'] = dict(t=t[::2].round(4).tolist(), K=K[::2].round(6).tolist(), R=R[::2].round(6).tolist(), rho=np.sinc(t[::2]/np.pi).round(6).tolist(),
                 s=s.round(3).tolist(), Zb=Zb.round(6).tolist(), w=w[::2].round(3).tolist(), Sre=S.real[::2].round(6).tolist(), Sim=S.imag[::2].round(6).tolist(),
                 Rlate=float(R[t>=40].mean()))
# ---------- P2: finite-N onsets (E3b recurrence) and the exact pole track
def nroots(N, k, kap, ns=4000):
    l = np.arange(N); c = cl(l); s = -kap + kap*np.linspace(1e-6, 1, ns); r = s + kap; sign = np.sign(r)
    for j in range(N-2, -1, -1):
        d = s + (kap if j > 0 else 0.0); r = d + k*k*c[j]**2/r; sign = sign*np.sign(r)
    return int(np.sum(sign[1:] != sign[:-1]))
def kstar(N):
    lo, hi = 0.5, 1.2
    for _ in range(36):
        m = 0.5*(lo+hi)
        if nroots(N, 1.0, m) > 0: hi = m
        else: lo = m
    return 0.5*(lo+hi)
Ns = [2, 4, 6, 8, 12, 16, 24, 50, 100, 200, 400, 800]
ks = [kstar(n) for n in Ns]
print('P2 onsets', [(n, round(k, 5)) for n, k in zip(Ns, ks)], '2/pi', round(2/np.pi, 6))
kap = np.linspace(2/np.pi+1e-6, 1.6, 300); sp = 1/np.tan(1/kap) - kap
out['P2'] = dict(N=Ns, kstar=[round(k, 6) for k in ks], kap=kap.round(5).tolist(), spole=sp.round(6).tolist())
# ---------- P3: the door, exact free streaming, a_l(t) = sqrt((2l+1)(2L+1)) * int dmu/2 P_l P_L e^{-i mu t}
x, wq = leggauss(160)
P = lambda l, x: legval(x, [0]*l+[1])
def door(L, t, lmax=12):
    ph = np.exp(-1j*np.outer(t, x))
    return np.array([np.sqrt((2*l+1)*(2*L+1))*(ph*(wq*P(l, x)*P(L, x))[None, :]).sum(1)/2 for l in range(lmax+1)])
tt = np.linspace(0, 8, 481)
P3 = dict(t=tt.round(4).tolist())
tl = np.logspace(-3, 0.3, 120); P3['tl'] = tl.round(6).tolist()
for L in (3, 4, 5):
    A = door(L, tt); P3['a%d' % L] = np.abs(A).round(6).tolist()
    a2 = np.abs(door(L, tl, 2)[2]); coef = np.prod([cl(j) for j in range(2, L)])/__import__("math").factorial(L-2)
    slope = np.polyfit(np.log(tl[:30]), np.log(a2[:30]), 1)[0]
    print('P3 L=%d slope %.4f  a2/(coef t^(L-2)) at t=1e-3: %.6f  coef %.6f' % (L, slope, a2[0]/(coef*tl[0]**(L-2)), coef))
    P3['a2l%d' % L] = a2.tolist(); P3['coef%d' % L] = float(coef); P3['slope%d' % L] = float(slope)
out['P3'] = P3
# ---------- P4: truncated chain L_N = -ikM - kappa(I-P0), k = kappa = 1
def LN(N):
    D = np.ones(N); D[0] = 0
    return -1j*M(N) - np.diag(D)
ev = {}; rows = []
for n in list(range(2, 41)) + list(range(42, 161, 2)):
    A = LN(n); lam = np.linalg.eigvals(A); ev[n] = [[round(float(z.real), 5), round(float(z.imag), 5)] for z in lam]
for n in list(range(2, 41)) + list(range(44, 401, 4)):
    A = LN(n); lam = np.linalg.eigvals(A); F = np.linalg.norm(A, 'fro')**2; S2 = float(np.sum(abs(lam)**2))
    As = A.conj().T; Em = np.linalg.norm(A@As - As@A, 'fro')**2/8; Ep = np.linalg.norm(A@A - As@As, 'fro')**2/8
    rows.append([n, round(F, 6), round(S2, 6), round(F-S2, 6), round(Em, 6), round(Ep, 6)])
print('P4 last rows', rows[-3:], ' dep2 at 200:', [r for r in rows if r[0] == 200])
out['P4'] = dict(ev=ev, rows=rows)
json.dump(out, open('cards_data.json', 'w'))
