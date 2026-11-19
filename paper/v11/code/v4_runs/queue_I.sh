# SCRIPT: NU-V4-QUEUE-I  time-step control: r = 1/4 with the stiff step shrunk by 4
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, doi:10.5281/zenodo.23808376)}"
cd "$(dirname "$0")"
python3 trisect_split_dt.py I_r025_dt4 1.0 2.0 3 0.5150 0.5180 1e-4 15.0 0.409 0.25 4.0 > log_I.txt 2>&1
cat log_I.txt
