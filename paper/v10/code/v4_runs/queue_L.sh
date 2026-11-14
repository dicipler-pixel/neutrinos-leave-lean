# SCRIPT: NU-V4-QUEUE-L  shear-only split: regression, then r = 4 and r = 1/4
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation}"
cd "$(dirname "$0")"
python3 -c "
import sys,os,time;sys.path.insert(0,os.environ['SIMDIR']);sys.path.insert(0,'.')
from run_shear import run
t=time.time();o=run(0.5109,fnu=0.409,N=400,K=32,eps0=0.1,eps_dec=2.0,eps_max=15.0,nexp=3,rr=1.0)
print('REGRESSION shear-only rr=1 delta=0.5109:',o['status'],round(float(o['eps']),2),f'{time.time()-t:.0f}s (unmodified: BH 6.61)',flush=True)" > log_L_regress.txt 2>&1
python3 trisect_shear.py L_r4 1.0 2.0 3 0.503 0.519 2e-5 15.0 0.409 4.0 > log_L4.txt 2>&1
python3 trisect_shear.py L_r025 1.0 2.0 3 0.503 0.519 2e-5 15.0 0.409 0.25 > log_L025.txt 2>&1
cat log_L_regress.txt; tail -1 log_L4.txt; tail -1 log_L025.txt
