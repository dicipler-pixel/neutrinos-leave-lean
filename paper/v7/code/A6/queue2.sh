# SCRIPT: NU-V6-QUEUE-A6-V2 (r=0.8 tol 1.25e-5)  level 3 (N=900, Nmu=72, Courant 0.1, cH 0.00125) thresholds r=1.25 then r=0.8; one process at a time
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
F='"fnu":0.409,"N":900,"K":72,"eps0":0.1,"eps_dec":2.0,"eps_max":15.0,"nexp":3,"cfl_r":0.1,"cfl_mu":0.1,"cH":0.00125'
go() { [ -f res_$1.json ] || python3 search.py "$@"; }
go L3_r125 run_split_stage 0.50991687 2e-4 1e-6 "{$F,\"rr\":1.25}" 0.075
go L3_r08  run_split_stage 0.51175643 2e-4 1.25e-5 "{$F,\"rr\":0.8}" 0.075
echo "$(date +%H:%M:%S) QUEUE DONE" >> RUNLOG.txt
