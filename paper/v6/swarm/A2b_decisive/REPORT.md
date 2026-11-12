# A2b: the two decisive simulations, flux-shear link law against timing for neutrino self-scattering

The tool refused to write `REPORT.md`, so the report is here. All other outputs are in `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A2b_decisive/`.

## Verdict
With the flux and every l ≥ 2 relaxing at the same rate (r = 1), and the isotropy history unchanged, the threshold is **δc = 0.51972 ± 0.00009**.

**Against the kill lines in `PREREGISTERED.txt`, the verdict is NEITHER.** The midpoint lands in the "neither" band (0.5197 < δc ≤ 0.5199):
- The bracket (0.519625 to 0.519813) lies entirely below the link-law line (0.5199), so **the link law is not favoured.**
- The bottom of the bracket reaches into the top of the timing band (≤ 0.5197). Timing describes almost all of it, but not quite.

**What the number says:**
- Going to r = 1 raises the threshold by only **+0.00031 ± 0.00018** from McCormick's run with self-scattering (0.51941). The link law predicted about +0.0010 (a result of 0.5204); timing predicted 0.
- The rise is definitely positive. In McCormick's archived run, δ = 0.5195625 formed a black hole; in this run, 0.519625 disperses.
- So most of the drop that self-scattering causes (0.52639 → 0.51941) comes from the isotropy history, i.e. timing. The flux-shear link carries a small, real remainder: r = 1 undoes 4.5% of the full self-scattering shift in G.

**New reference:** the instantaneous free-streaming threshold at T_H = 1 MeV with the full equation of state is **δ_inst = 0.53313 ± 0.00012**. A2's stand-in of 0.53379 was too high by 0.00066.

## 1. The r1 variant and its gates
McCormick's files are copied into `orig/` (unchanged apart from a `# SCRIPT:` line) and `r1/`.
- **What changed:** in `r1/ms_mg.py`, a new `nnmode = 2` sets the self-scattering target to κ_n(ε_s/4π − I) and adds κ_n,s q_s to the momentum handed to the plasma.
- **Driver changes:** `run_mg.py` passes `nnmode` through, and `bisect_mg.py` reads it as an integer.
- **CPU wait:** both bisection drivers call a wait before every run (until fewer than 3 other Python simulations are running). This does not change the bisection logic.

**Gates.** `gate_operator.py` takes the operator straight from the compiled `rhs()`. It uses an enormous uniform plasma density so the lapse A = 1 exactly; the collision term is then the only part that depends on the rates. Every gate passed.

| Check (one frozen group, N_μ = 32, κ_e = 0.7, κ_n = 1.9) | Result |
|---|---|
| Operator against −(κ_e+κ_n) diag(0,1,…,1) | largest error 5.3e−15 (entries 2.6) |
| Eigenvalues | 0, then 31 × −2.6 |
| Closed form on random anisotropic intensities, all cells | relative error 1.2e−15 |
| Energy moment of the collision term | 1.5e−16 (relative) |
| Momentum balance | neutrinos lose −0.1219742786974912, plasma receives −0.1219742786974893 (relative 1.5e−14) |
| Same test on the unmodified copy | −diag(0, κ_e, κ_e+κ_n, …) to 7.8e−15; plasma gets only κ_e q (A2's result reproduced) |
| Regression with κ_n = 0, run to ε = 0.6 (3340 steps); T0 = 10, δ = 0.52, G = 6, N = 300, K = 32 | r1 against the unmodified copy: I, e, ε, steps and peakC **bit-identical** (largest difference 0.0) |

## 2. Run 1: the r1 bisection
Settings: T0 = 10 MeV, mode=phys, G = 6, x from 0.4 to 20, N = 300, N_μ = 32, nnmode = 2, starting bracket 0.517–0.523. Only a detected horizon or dispersal moved a bracket end.

| δ | Outcome | ε at end | Time |
|---|---|---|---|
| 0.52000 | black hole | 6.10 | **353 s (first run)** |
| 0.51850 | dispersed | 5.53 | 300 s |
| 0.51925 | dispersed | 5.85 | 320 s |
| 0.519625 | dispersed | 6.23 | 343 s |
| 0.5198125 | black hole | 7.20 | 418 s |

- **δc = 0.51972 ± 0.00009**, T_H = 1.0029 MeV, 28.9 minutes in all.
- The bracket never needed widening, and no run came near the 90-minute limit.

## 3. Run 2: instantaneous free-streaming with the full equation of state
Settings: McCormick's `bisect_eos` with kind 'fs', T0 = 10, his defaults N = 400, K = 32.

| δ | Outcome |
|---|---|
| 0.533 | dispersed |
| 0.535 | black hole |
| 0.534 | black hole |
| 0.5335 | black hole |
| 0.53325 | black hole |

- Each run took 55–76 s.
- **δ_inst = 0.53313 ± 0.00012**, T_H = 1.0030 MeV.

## 4. A2's G predictions recomputed with δ_inst = 0.533125
These use A2's step3 and step4 scripts, copied, with δ_inst passed in.

Measured: G goes from 0.8114 (without self-scattering) to 0.6158 (with), a shift of −0.1956 ± 0.0053. The kill tolerance is 0.0978.

| Reading | Predicted shift in G | Miss (% of shift) | Predicted δc with self-scattering | Miss in δc | Verdict |
|---|---|---|---|---|---|
| Link law, rate 1.11 | −0.1804 | 7.8% | 0.51995 | +0.00054 | survives |
| Link law, rate 1.19 | −0.1961 | 0.2% | 0.51939 | −0.00002 | survives |
| Link law, rate 1.20 | −0.1980 | 1.2% | 0.51932 | −0.00009 | survives |
| Timing | −0.1606 | 17.9% | 0.52040 (0.52066 anchored) | — | survives |

- Using the eleven measured offsets directly instead of the straight-line law gives 0.51970, a miss of +0.00029.
- The R_ν-interpolated sensitivity reference (0.53377) gives 0.51957.

**What this means.** The size of the self-scattering shift does not separate the two readings: all four survive. Run 1 is what separates them. Once the isotropy history is held fixed, removing the link rapidity barely moves the threshold.

## 5. Context (not pre-registered; `step5_r1_readout.py`)
- **G values with the new δ_inst:** G(r1) = 0.6245, G(with self-scattering) = 0.6158, G(without) = 0.8114.
- **Against A2's prediction for r1:** r1 recovers 31% of the move A2 predicted (to 0.5204), or 25% against the anchored 0.52066.
- **Another way to read the link law:** subtracting the link rapidity u_eff = 0.8313 at rate 1.11 from the self-scattering run predicts 0.5260. Against that, r1 recovers 4.7%.
- **Implied rapidity:** if the whole r1 shift is read as link rapidity, it implies Δu = 0.034, against A2's 0.83.

## Files
- **Pre-registration and results:** `PREREGISTERED.txt` (written 14:09Z before any run; gates, Run 1, Run 2 and the recomputation appended at 14:50Z, 15:20Z and 15:30Z).
- **Code copies:** `orig/`, `r1/`.
- **Run results:** `r1/res_mg_r1_6_10.0.json`, `orig/res_eos_fs_10.0.json`.
- **Gate:** `gate_operator.py`, `gate_operator_r1.txt`, `gate_operator_orig.txt`.
- **Regression:** `regress.py`, `regress_compare.py`, `regress_compare.txt`, `regress_*.npz`.
- **Logs:** `log_regress.txt`, `log_bisect_r1.txt`, `log_bisect_fs.txt`.
- **Queue scripts:** `wait_cpu.sh`, `q_regress.sh`, `q_bisect_r1.sh`, `q_bisect_fs.sh`, `q_both.sh`.
- **Recomputation:**
  - A2 originals: `step3_predict.py`, `step4_compare.py`
  - Parameterised copies: `step3_predict_newdinst.py`, `step4_compare_newdinst.py`
  - Outputs: `step3_predictions_newdinst.json`, `step3_out_newdinst.txt`, `step4_out_newdinst.txt`
  - Section 5: `step5_r1_readout.py`, `step5_out.txt`