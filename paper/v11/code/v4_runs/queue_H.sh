# SCRIPT: NU-V4-QUEUE-H  the anchor: r = 1 measured with the split code at tolerance 1e-4
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
until grep -qs "RESULT\|Traceback" log_F2b.txt; do sleep 20; done
python3 trisect_split.py H1_r1 1.0 2.0 3 0.5095 0.5125 1e-4 15.0 0.409 1.0 > log_H1.txt 2>&1
