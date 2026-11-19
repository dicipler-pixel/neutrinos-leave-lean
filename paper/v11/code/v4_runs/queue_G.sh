# SCRIPT: NU-V4-QUEUE-G  independent check of the Open Math OS review's measurements: two runs either side of each quoted threshold
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
python3 - > log_G.txt 2>&1 <<'PY'
import sys,os;sys.path.insert(0,os.environ['SIMDIR']);sys.path.insert(0,'.')
from multiprocessing import Pool
def step(d):
    from run_step import run; o=run(d,fnu=0.409,N=400,K=32,eps0=0.1,eps_dec=1.0,eps_max=15.0,nexp=3); return ('step eps_b=1',d,o['status'],float(o['eps']))
def k5(d):
    from run_nuc_n import run; o=run(d,fnu=0.409,N=400,K=32,eps0=0.1,eps_dec=1.20,eps_max=15.0,nexp=3); return ('K5 n=3 eps_dec=1.20',d,o['status'],float(o['eps']))
jobs=[(step,0.5132),(step,0.5138),(k5,0.5165),(k5,0.5171)]
def go(a): return a[0](a[1])
with Pool(2) as p:
    for t,d,s,e in p.map(go,jobs): print(f'{t} delta={d}: {s} eps={e:.2f}',flush=True)
print('review: step eps_b=1 delta_c=0.513512 (expect 0.5132 dispersed, 0.5138 BH); K5 n=3 eps_dec=1.20 delta_c=0.516797 (expect 0.5165 dispersed, 0.5171 BH)')
PY
