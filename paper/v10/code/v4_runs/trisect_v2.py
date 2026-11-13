# SCRIPT: NU-V4-TRISECT-V2  trisection in which only a detected horizon ('BH') or 'dispersed' moves the bracket.
# 'BH_breakdown' (numerical breakdown after 2M/R > 0.95) and 'crash' get one retry at CFL 0.3, then are reported and skipped.
# Every run reports min I over the run (positivity monitor) and max 2M/R.
import sys, json, time, os, importlib
from multiprocessing import Pool
sys.path.insert(0, os.environ['SIMDIR']); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def one(a):
    d,kw=a; mod=importlib.import_module(RUNNER); o=mod.run(d,**kw); s=o['status']; note=''
    if s not in ('BH','dispersed'):
        kw2=dict(kw,cfl_r=0.3,cfl_mu=0.3); o2=mod.run(d,**kw2); note=' (retry at CFL 0.3 after %s)'%s; o=o2; s=o['status']
    return d,s,float(o['eps']),float(o['Imin']),float(o['max2MR']),note
if __name__=='__main__':
    tag=sys.argv[1]; RUNNER=sys.argv[2]; lo,hi,tol=float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]); kw=json.loads(sys.argv[6])
    log=[]; t0=time.time()
    with Pool(2) as p:
        while hi-lo>tol:
            a=lo+(hi-lo)/3; b=lo+2*(hi-lo)/3
            res=p.map(one,[(a,kw),(b,kw)])
            for d,s,e,im,m2,note in res: print(f'{tag} delta={d:.8f}: {s} eps={e:.2f} minI={im:.3e} max2M/R={m2:.4f}{note}',flush=True); log.append((d,s,e,im,m2,note))
            ok=[(d,s) for d,s,*_ in res if s in ('BH','dispersed')]
            if not ok: print('both points undecided; stop',flush=True); break
            for d,s in ok:
                if s=='BH': hi=min(hi,d)
                else: lo=max(lo,d)
            if lo>=hi: print('inconsistent outcomes; stop',flush=True); break
    print(f'RESULT {tag}: delta_c = {0.5*(lo+hi):.8f} +- {0.5*(hi-lo):.8f}  bracket [{lo:.8f}, {hi:.8f}] ({(time.time()-t0)/60:.1f} min)',flush=True)
    json.dump(dict(tag=tag,dc=0.5*(lo+hi),w=hi-lo,lo=lo,hi=hi,log=log),open(f'res_{tag}.json','w'))
