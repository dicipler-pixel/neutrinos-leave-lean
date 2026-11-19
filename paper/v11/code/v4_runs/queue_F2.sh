# SCRIPT: NU-V4-QUEUE-F2  which odd law: r = 1/16 then r = 16
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
python3 trisect_split.py F2_r1o16 1.0 2.0 3 0.5100 0.5283 1e-4 15.0 0.409 0.0625 > log_F2a.txt 2>&1
python3 trisect_split.py F2_r16 1.0 2.0 3 0.4977 0.5100 1e-4 15.0 0.409 16.0 > log_F2b.txt 2>&1
