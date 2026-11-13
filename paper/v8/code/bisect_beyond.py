# SCRIPT: BEYOND-STEVE-BISECT  threshold bisection with gradual decoupling, profile alpha and rate exponent as inputs
import sys, json, time, os
sys.path.insert(0, os.environ['SIMDIR']); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_nuc_n import run
tag=sys.argv[1]; qshape=float(sys.argv[2]); epsd=float(sys.argv[3]); nexp=float(sys.argv[4])
lo,hi,tol=float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]); emax=float(sys.argv[8])
log=[]; t0=time.time()
while hi-lo>tol:
    mid=0.5*(lo+hi); t1=time.time()
    out=run(mid,fnu=0.409,N=400,K=32,eps0=0.1,eps_dec=epsd,eps_max=emax,qshape=qshape,nexp=nexp)
    print(f'{tag} delta={mid:.5f}: {out["status"]} eps={out["eps"]:.2f} ({time.time()-t1:.0f}s)',flush=True)
    log.append((mid,out['status'],float(out['eps'])))
    if out['status']=='BH': hi=mid
    elif out['status']=='dispersed': lo=mid
    else: break
print(f'RESULT {tag}: delta_c = {0.5*(lo+hi):.5f} +- {0.5*(hi-lo):.5f} ({(time.time()-t0)/60:.1f} min)',flush=True)
json.dump(dict(tag=tag,qshape=qshape,eps_dec=epsd,nexp=nexp,dc=0.5*(lo+hi),w=hi-lo,log=log),open(f'res_{tag}.json','w'))
