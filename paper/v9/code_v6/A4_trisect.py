# SCRIPT: A4-TRISECT  strict-endpoint trisection, one process, for one member (eps_s, l, f) of a restart pair
# usage: python3 trisect.py TAG eps_s l f lo hi wtarget [K]
import sys, os, json, time
import restart
from restart import run_member
from cpuwait import wait
tag = sys.argv[1]; eps_s = float(sys.argv[2]); l = int(sys.argv[3]); f = float(sys.argv[4])
lo, hi, wt = float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])
if len(sys.argv) > 8: restart.K = int(sys.argv[8])
def P(*a): print(*a, flush=True)
log = []
def trial(d):
    w = wait(P); t1 = time.time()
    o = run_member(d, eps_s, l, f, 'cache', mode='bump')
    log.append((d, o['status'], float(o['eps']), float(o['Imin']), float(o['max2MR'])))
    P(f'{tag} delta={d:.7f}: {o["status"]} eps={o["eps"]:.3f} Imin={o["Imin"]:.2e} ({time.time()-t1:.0f}s, waited {w:.0f}s)')
    json.dump(dict(tag=tag, eps_s=eps_s, l=l, f=f, K=restart.K, lo=lo, hi=hi, log=log), open(f'trisect_{tag}.json', 'w'), indent=1)
    return o['status']
t0 = time.time()
# endpoint verification: lo must disperse, hi must form a horizon; widen by the bracket width until they do
s = trial(lo)
while s != 'dispersed':
    if s == 'BH': hi = lo; lo = lo - 1.5e-3
    else: lo = lo - 2e-4                               # undecided/crash/breakdown: does not move the bracket; step aside
    s = trial(lo)
s = trial(hi)
while s != 'BH':
    if s == 'dispersed': lo = hi; hi = hi + 1.5e-3
    else: hi = hi + 2e-4
    s = trial(hi)
while hi - lo > wt:
    a = lo + (hi-lo)/3; b = lo + 2*(hi-lo)/3
    sa = trial(a)
    if sa == 'BH': hi = a; continue
    sb = trial(b)
    if sa == 'dispersed': lo = a
    if sb == 'BH': hi = b
    elif sb == 'dispersed': lo = b
    if sa not in ('BH', 'dispersed') and sb not in ('BH', 'dispersed'):
        P(f'{tag}: both trial points undecisive; bracket not moved; stopping'); break
dc = 0.5*(lo+hi)
P(f'RESULT {tag}: delta_c = {dc:.7f}  bracket [{lo:.7f}, {hi:.7f}]  width {hi-lo:.2e}  ({(time.time()-t0)/60:.1f} min)')
json.dump(dict(tag=tag, eps_s=eps_s, l=l, f=f, K=restart.K, lo=lo, hi=hi, dc=dc, w=hi-lo, log=log), open(f'trisect_{tag}.json', 'w'), indent=1)
