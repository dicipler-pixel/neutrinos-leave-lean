# AGENT I (loose): random networks of coupled modes. Some nodes touch the bath (damped = the 'normal layer'), the rest do not.
# Cut ONE link at random. Does the cut leave behind a protected mode (an eigenvalue with Re = 0 that the bath cannot reach)?
import numpy as np
rng=np.random.default_rng(7)
def protected(Hc,D,tol=1e-9):
    L=-1j*Hc-np.diag(D); w,V=np.linalg.eig(L); n=0; occ=[]
    for j in range(len(w)):
        if abs(w[j].real)<tol: n+=1; occ.append(np.abs(V[:,j])**2)
    return n,occ
stats={}
for N in [6,8,10]:
    made=0; trials=4000; examples=[]
    for t in range(trials):
        A=np.triu((rng.random((N,N))<0.45).astype(float),1); W=A*rng.choice([-1,1],size=(N,N))*rng.uniform(0.5,1.5,(N,N)); Hc=W+W.T
        D=np.where(rng.random(N)<0.5,rng.uniform(1,3,N),0.0)
        if D.sum()==0: continue
        n0,_=protected(Hc,D)
        links=np.argwhere(np.triu(Hc!=0,1))
        if len(links)==0: continue
        i,j=links[rng.integers(len(links))]; Hcut=Hc.copy(); Hcut[i,j]=Hcut[j,i]=0
        n1,occ=protected(Hcut,D)
        if n1>n0: made+=1; examples.append((i,j,D.round(1),occ[0].round(2)))
    stats[N]=made/trials
    print(f" N={N}: a single cut created a NEW protected mode in {100*made/trials:.1f}% of {trials} random networks")
    if examples: i,j,D,o=examples[0]; print(f"   example: cut link ({i},{j}); bath on nodes {list(np.nonzero(D)[0])}; protected mode lives on {list(np.nonzero(o>0.01)[0])} with weights {o[o>0.01]}")
# designed version: a pocket node P coupled to two bath-touching nodes with equal and opposite links -> a dark combination
print("designed interference pocket: nodes a,b (undamped) both linked to damped node d, with links +g and -g")
for g in [0.3,1,3]:
    Hc=np.array([[0,0,g],[0,0,-g],[g,-g,0.]]); D=np.array([0,0,2.0]); n,occ=protected(Hc,D); print(f"   g={g}: protected modes {n}, living on a,b with weights {occ[0][:2].round(3) if n else '-'}")
