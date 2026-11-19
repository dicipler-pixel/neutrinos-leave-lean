# SCRIPT: TRISECT3  three-valued two-point bracket search for delta_c (collapse / disperse / undecided-or-error)
# Usage: trisect3.py TAG qshape eps_dec nexp lo hi tol eps_max kapcap N K
# Outcome of one run: 'C' (collapse = status BH), 'D' (disperse = status dispersed), 'U' (anything else: undecided at eps_max, crash).
# An 'U' point NEVER moves the bracket. It is retried once with eps_max*1.5; if still 'U' it is recorded in 'undecided' and reported.
import sys, json, time, os
from multiprocessing import Pool
sys.path.insert(0, os.environ['SIMDIR']); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def classify(status):
    return 'C' if status == 'BH' else ('D' if status == 'dispersed' else 'U')

def one(a):
    from run_nuc_n3 import run
    d, q, ed, n, em, kc, N, K = a
    t1 = time.time()
    try:
        o = run(d, fnu=0.409, N=N, K=K, eps0=0.1, eps_dec=ed, eps_max=em, qshape=q, nexp=n, kapcap=kc)
        info = dict(d=d, status=o['status'], eps=float(o['eps']), eps_max=em, rawmax=float(o['rawmax']), kapcap=kc,
                    capsteps=int(o['capsteps']), steps=int(o['steps']), eps_cap_last=float(o['eps_cap_last']), sec=time.time()-t1)
    except Exception as ex:
        info = dict(d=d, status='error:' + type(ex).__name__ + ':' + str(ex)[:80], eps=float('nan'), eps_max=em, rawmax=float('nan'),
                    kapcap=kc, capsteps=-1, steps=-1, eps_cap_last=float('nan'), sec=time.time()-t1)
    info['out'] = classify(info['status'])
    return info

def fmt(tag, i):
    return (f"{tag} delta={i['d']:.5f}: {i['out']} [{i['status']}] eps={i['eps']:.2f} eps_max={i['eps_max']} "
            f"rawmax(kappa/H)={i['rawmax']:.3e} cap={i['kapcap']:.1e} capped_steps={i['capsteps']}/{i['steps']} "
            f"cap_released_at_eps~{i['eps_cap_last']:.3f} ({i['sec']:.0f}s)")

def search(tag, q, ed, n, lo, hi, tol, em, kc, N, K, mapper, log_path=None, retry_factor=1.5):
    log = []; undecided = []; nonmono = False; t0 = time.time()
    while hi - lo > tol:
        a = lo + (hi - lo) / 3; b = lo + 2 * (hi - lo) / 3
        res = mapper(one, [(a, q, ed, n, em, kc, N, K), (b, q, ed, n, em, kc, N, K)])
        for i in res: print(fmt(tag, i), flush=True); log.append(i)
        # retry each undecided/error point ONCE with raised eps_max (the other core is used for the second one)
        bad = [k for k, i in enumerate(res) if i['out'] == 'U']
        if bad:
            rr = mapper(one, [(res[k]['d'], q, ed, n, em * retry_factor, kc, N, K) for k in bad])
            for k, i in zip(bad, rr):
                i['retry'] = True; print('RETRY ' + fmt(tag, i), flush=True); log.append(i)
                if i['out'] == 'U':
                    undecided.append((i['d'], i['status'], i['eps']))
                res[k] = i
        ia, ib = res
        oa, ob = ia['out'], ib['out']
        if oa == 'U' and ob == 'U':
            print(f'{tag} STOP: both points undecided/error after retry; bracket [{lo:.5f},{hi:.5f}] unchanged', flush=True); break
        if oa == 'D' and ob == 'C':     # ordinary case, delta_c between a and b
            lo, hi = a, b
        elif oa == 'C' and ob == 'D':
            print(f'{tag} STOP: non-monotonic outcomes (collapse at a, disperse at b); bracket unchanged', flush=True); nonmono = True; break
        elif oa == 'C':                 # a collapses (b is C or U): threshold below a
            hi = a
        elif ob == 'D':                 # b disperses (a is D or U): threshold above b
            lo = b
        elif oa == 'D':                 # a disperses, b undecided: threshold above a
            lo = a
        elif ob == 'C':                 # b collapses, a undecided: threshold below b
            hi = b
        if log_path:
            json.dump(dict(tag=tag, lo=lo, hi=hi, log=log, undecided=undecided), open(log_path, 'w'))
        print(f'{tag} bracket now [{lo:.5f},{hi:.5f}]', flush=True)
    res = dict(tag=tag, qshape=q, eps_dec=ed, nexp=n, kapcap=kc, N=N, K=K, lo=lo, hi=hi, dc=0.5 * (lo + hi), w=0.5 * (hi - lo),
               minutes=(time.time() - t0) / 60, undecided=undecided, nonmonotonic=nonmono, log=log)
    print(f'RESULT {tag}: delta_c = {0.5*(lo+hi):.5f} +- {0.5*(hi-lo):.5f} bracket [{lo:.5f},{hi:.5f}] ({res["minutes"]:.1f} min) undecided_points={undecided}', flush=True)
    return res

if __name__ == '__main__':
    tag = sys.argv[1]; q = float(sys.argv[2]); ed = float(sys.argv[3]); n = float(sys.argv[4])
    lo, hi, tol = float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]); em = float(sys.argv[8])
    kc = float(sys.argv[9]); N = int(sys.argv[10]); K = int(sys.argv[11])
    with Pool(2) as p:
        res = search(tag, q, ed, n, lo, hi, tol, em, kc, N, K, lambda f, args: p.map(f, args), log_path=f'state_{tag}.json')
    json.dump(res, open(f'res_{tag}.json', 'w'))
