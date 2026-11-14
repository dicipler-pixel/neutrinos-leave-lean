# SCRIPT: NU-V4-QUEUE-J  odd rate near the matched link: r = 2 and r = 1/2
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
python3 trisect_split.py J_r2 1.0 2.0 3 0.5050 0.5100 5e-5 15.0 0.409 2.0 > log_J2.txt 2>&1
python3 trisect_split.py J_r05 1.0 2.0 3 0.5120 0.5170 5e-5 15.0 0.409 0.5 > log_J05.txt 2>&1
tail -1 log_J2.txt; tail -1 log_J05.txt
