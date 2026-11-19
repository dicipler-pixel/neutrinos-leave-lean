# v4 runs: R_nu independence and the flux-shear link (4 November 2026)

Every prediction and kill line is in `PREREGISTERED_V4.txt`, written before the run it judges; results are appended
below each test, nothing above them edited. Runs use S. McCormick's code (doi:10.5281/zenodo.23808375/6), unchanged
except `ms_nuc_split.py`: the flux relaxes at kappa1, every l >= 2 moment at kappa2 = r kappa1 (r = 1 reproduces the
unmodified code), and the stiff time-step cap uses the larger rate.

Run: `SIMDIR=/path/to/PBH_neutrino_simulation/simulation bash queue_F.sh` (and likewise for E-K; `numba` required).
Logs `log_*.txt`, thresholds `res_*.json`.
