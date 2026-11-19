# SCRIPT: NU-V4-QUEUE-M  angular resolution: Test F pair at N_mu = 48
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation}"
cd "$(dirname "$0")"
python3 trisect_clean_res.py M_r4_K48 1.0 2.0 3 0.5045 0.5065 2e-5 15.0 0.409 4.0 400 48 > log_M4.txt 2>&1
python3 trisect_clean_res.py M_r025_K48 1.0 2.0 3 0.5155 0.5175 2e-5 15.0 0.409 0.25 400 48 > log_M025.txt 2>&1
tail -1 log_M4.txt; tail -1 log_M025.txt
