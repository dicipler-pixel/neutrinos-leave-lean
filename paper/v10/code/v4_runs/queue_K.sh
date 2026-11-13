# SCRIPT: NU-V4-QUEUE-K  matched-link limit: r = 1.25 and r = 0.8 at tolerance 1e-5
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
python3 trisect_split.py K_r125 1.0 2.0 3 0.5083 0.5113 1e-5 15.0 0.409 1.25 > log_K125.txt 2>&1
python3 trisect_split.py K_r08 1.0 2.0 3 0.5102 0.5132 1e-5 15.0 0.409 0.8 > log_K08.txt 2>&1
tail -1 log_K125.txt; tail -1 log_K08.txt
