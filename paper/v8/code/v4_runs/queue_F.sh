# SCRIPT: NU-V4-QUEUE-F  regression then Test F searches
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
python3 -c "
import sys,os,time;sys.path.insert(0,os.environ['SIMDIR']);sys.path.insert(0,'.')
from run_split import run
t=time.time();o=run(0.5109,fnu=0.409,N=400,K=32,eps0=0.1,eps_dec=2.0,eps_max=15.0,nexp=3,rr=1.0)
print('REGRESSION rr=1 delta=0.5109:',o['status'],round(float(o['eps']),2),f'{time.time()-t:.0f}s (unmodified: BH 6.61)',flush=True)" > log_F_regress.txt 2>&1
python3 trisect_split.py F_r025 1.0 2.0 3 0.5023 0.5207 1e-4 15.0 0.409 0.25 > log_F025.txt 2>&1
python3 trisect_split.py F_r4 1.0 2.0 3 0.5023 0.5207 1e-4 15.0 0.409 4.0 > log_F4.txt 2>&1
