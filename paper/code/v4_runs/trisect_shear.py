# SCRIPT: NU-V4-TRISECT-SHEAR  trisect in which a crash never moves the bracket: one retry at CFL 0.3, else reported and skipped
import sys, json, time, os
from multiprocessing import Pool
sys.path.insert(0, os.environ['SIMDIR']); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_shear import run
def one(a):
    d,q,ed,n,em=a
    o=run(d,fnu=FNU,N=400,K=32,eps0=0.1,eps_dec=ed,eps_max=em,qshape=q,nexp=n,rr=RR); s=o['status']; note=''
    if s not in ('BH','dispersed'):
        o=run(d,fnu=FNU,N=400,K=32,eps0=0.1,eps_dec=ed,eps_max=em,qshape=q,nexp=n,rr=RR,cfl_r=0.3,cfl_mu=0.3); note=' (retry at CFL 0.3 after %s)'%s; s=o['status']
    return d,s,float(o['eps']),note
if __name__=='__main__':
    tag=sys.argv[1]; q=float(sys.argv[2]); ed=float(sys.argv[3]); n=float(sys.argv[4]); lo,hi,tol=float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]); em=float(sys.argv[8]); FNU=float(sys.argv[9]); RR=float(sys.argv[10])
    log=[]; t0=time.time()
    with Pool(2) as p:
        while hi-lo>tol:
            a=lo+(hi-lo)/3; b=lo+2*(hi-lo)/3
            res=p.map(one,[(a,q,ed,n,em),(b,q,ed,n,em)])
            for d,s,e,note in res: print(f'{tag} delta={d:.8f}: {s} eps={e:.2f}{note}',flush=True); log.append((d,s,e,note))
            ok=[(d,s) for d,s,e,_ in res if s in ('BH','dispersed')]
            if not ok: print('both points undecided; stop',flush=True); break
            for d,s in ok:
                if s=='BH': hi=min(hi,d)
                else: lo=max(lo,d)
            if lo>=hi: print('inconsistent outcomes; stop',flush=True); break
    print(f'RESULT {tag}: delta_c = {0.5*(lo+hi):.8f} +- {0.5*(hi-lo):.8f}  bracket [{lo:.8f}, {hi:.8f}] ({(time.time()-t0)/60:.1f} min)',flush=True)
    json.dump(dict(tag=tag,dc=0.5*(lo+hi),w=hi-lo,lo=lo,hi=hi,log=log),open(f'res_{tag}.json','w'))
