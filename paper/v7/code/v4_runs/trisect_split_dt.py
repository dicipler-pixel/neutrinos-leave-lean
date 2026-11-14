# SCRIPT: NU-V4-TRISECT-SPLIT-DT  two trial amplitudes per round in parallel (thirds of the bracket)
import sys, json, time, os
from multiprocessing import Pool
sys.path.insert(0, os.environ['SIMDIR']); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_split_dt import run
def one(a):
    d,q,ed,n,em=a; o=run(d,fnu=FNU,N=400,K=32,eps0=0.1,eps_dec=ed,eps_max=em,qshape=q,nexp=n,rr=RR,dtk=DTK); return d,o['status'],float(o['eps'])
if __name__=='__main__':
    tag=sys.argv[1]; q=float(sys.argv[2]); ed=float(sys.argv[3]); n=float(sys.argv[4]); lo,hi,tol=float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]); em=float(sys.argv[8]); FNU=float(sys.argv[9]); RR=float(sys.argv[10]); DTK=float(sys.argv[11])
    log=[]; t0=time.time()
    with Pool(2) as p:
        while hi-lo>tol:
            a=lo+(hi-lo)/3; b=lo+2*(hi-lo)/3
            res=p.map(one,[(a,q,ed,n,em),(b,q,ed,n,em)])
            for d,s,e in res: print(f'{tag} delta={d:.5f}: {s} eps={e:.2f}',flush=True); log.append((d,s,e))
            (da,sa,_),(db,sb,_)=res
            if 'BH' not in (sa,sb) and 'dispersed' not in (sa,sb): break
            if sa=='BH': hi=da
            elif sb=='BH': lo,hi=da,db
            else: lo=db
    print(f'RESULT {tag}: delta_c = {0.5*(lo+hi):.5f} +- {0.5*(hi-lo):.5f} ({(time.time()-t0)/60:.1f} min)',flush=True)
    json.dump(dict(tag=tag,dc=0.5*(lo+hi),w=hi-lo,log=log),open(f'res_{tag}.json','w'))
