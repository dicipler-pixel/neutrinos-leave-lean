# SCRIPT: A5-T1-ORDER  rate-order swap: same int sigma over a window, different order; readouts at e*=1.7, 4
import os; os.environ['OMP_NUM_THREADS']='1'
import numpy as np, json, time
from scipy.integrate import quad
from chain_lib import *
LM=60; EP=np.array([1.7,4.0]); W2=0.89
t1=time.time()
def readout(sig,breaks=(),dvec=None):
    A=np.zeros(2); P=np.zeros((3,2)); V=[]
    for k,w in zip(KS,WE):
        wl=evolve(k,sig,LM,EP,breaks=breaks,dvec=dvec)
        v=to_complex(wl[:3]); V.append(v)
        A+=w*wl[0]**2; P+=w*np.abs(v)**2
    return A,P,np.array(V)   # V[k, l, epoch]
Ai,_,_=readout(lambda t:0.0)
def g_of(A): return (1-A)/(1-Ai)
def cmp(name,sigF,sigR,ta,tb,brF=(),brR=(),dvec=None,r=1.0):
    AF,PF,VF=readout(sigF,brF,dvec); AR,PR,VR=readout(sigR,brR,dvec)
    dv2=np.einsum('k,kle->e',WE,np.abs(VF-VR)**2); n2=np.einsum('k,kle->e',WE,np.abs(VF)**2)
    gF,gR=g_of(AF),g_of(AR)
    s1=lambda f: quad(f,ta,tb,limit=400,points=[ta,tb])[0]
    ce=lambda f: s1(lambda t: f(t)**2/3+4*((r-1)*f(t))**2/15)   # per k^2
    row=dict(name=name,W=[ta,tb],r=r,
        optdepth=[s1(sigF),s1(sigR)], conn_energy_int_per_k2=[ce(sigF),ce(sigR)],
        sigma_at_readout=[[sigF(e) for e in EP],[sigR(e) for e in EP]],
        A=[AF.tolist(),AR.tolist()], P_l=[PF.tolist(),PR.tolist()],
        R_diff=np.sqrt(dv2/n2).tolist(), g=[gF.tolist(),gR.tolist()], dg=(gR-gF).tolist(),
        g2=[float(W2*gF[0]+(1-W2)*gF[1]),float(W2*gR[0]+(1-W2)*gR[1])])
    print(name,'W',[ta,tb],'r',r,'| optdepth %.6g %.6g | connE/k2 %.6g %.6g'%(*row['optdepth'],*row['conn_energy_int_per_k2']),flush=True)
    for i,e in enumerate(EP):
        print('   e*=%.1f  A %.5f -> %.5f | P0 %.5f %.5f P1 %.5f %.5f P2 %.5f %.5f | R_diff %.3e | g %.4f -> %.4f (dg %+.4f) | sigma(e*) %.3g %.3g'%(
            e,AF[i],AR[i],PF[0,i],PR[0,i],PF[1,i],PR[1,i],PF[2,i],PR[2,i],row['R_diff'][i],gF[i],gR[i],gR[i]-gF[i],sigF(e),sigR(e)),flush=True)
    print('   g2 %.4f -> %.4f'%tuple(row['g2']),flush=True)
    return row
out=dict(A_inst=Ai.tolist(),family_R=[],family_S=[])
# family R: time reversal inside W
for name,n,ed,ta,tb,r in [('R1',3,1,0.5,1.5,1),('R2',3,1,0.25,1.5,1),('R3',6,1,0.5,1.5,1),('R4',3,2,1.0,3.5,1),
                          ('R5',3,1,0.5,1.5,4.0),('R6',3,1,0.5,1.5,0.25)]:
    s=sigma_powerlaw(ed,n); sR=reversed_in_window(s,ta,tb)
    dv=None if r==1 else damp_vec(LM,r)
    out['family_R'].append(dict(n=n,ed=ed,**cmp(name,s,sR,ta,tb,(ta,tb),(ta,tb),dv,r)))
# family S: n=6 v5.1 histories against n=3 rescaled to equal optical depth on W
for (ta,tb) in [(TAU0,4.0),(0.5,4.0),(1.0,4.0)]:
    for ed6 in (1,2,3):
        I6=ed6**6/6*(ta**-6-tb**-6); ed3=(3*I6/(ta**-3-tb**-3))**(1/3)
        row=cmp('S_W[%g,%g]_ed6=%g'%(ta,tb,ed6),sigma_powerlaw(ed3,3),sigma_powerlaw(ed6,6),ta,tb)
        row.update(ed3=ed3,ed6=ed6); print('   (n=3 member ed3 = %.5f; first member n=3, second n=6)'%ed3,flush=True)
        out['family_S'].append(row)
json.dump(out,open('t1_order.json','w'),indent=1)
print('time %.0fs'%(time.time()-t1))
