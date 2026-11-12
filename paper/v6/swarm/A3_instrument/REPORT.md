I ran all four recorded runs (about 11 minutes each) and both archived edge pairs still split under nnmode=1. Prediction (i) was killed: the kept share separates the two fates before ε = 3. Prediction (ii) survives: the dominant group's link rapidity sits well above v5.1's admissible window in all four runs. The tool would not let me write `REPORT.md` as a file in the folder, so its content is below and the folder has no `REPORT.md`.

---

# A3: Jeromie Beasley's two-cut quantities in McCormick's multigroup model, read at threshold

Folder: `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A3_instrument/`

## What was run

**Code.** I copied McCormick's `run_mg.py`, `ms_mg.py`, `ms_fluid.py`, `ms_eos.py`, `run_eos.py`, `thermo_tables.npz` and `multigroup/weak_rates.json` (commit eb7c4de) into the folder. A second, unmodified set is in `orig/`, and its sha256 sums match the originals. `ms_mg.py` is unchanged.

The only change is in `run_mg.py` (marked `# SCRIPT: run_mg_rec`): a read-only recorder, switched on by `rec_every` and `rec_r`. Every 20 steps after the switch to transport, it calls McCormick's own `state()`, which has no side effects. It records at the centre cell (i = 0) and at the cell nearest r = r_m (i = 95, Lagrangian centre r = 0.9945):
- per flavour and group: e_s, q_s and P_r,s, and the local rates κ_e,s and κ_n,s;
- the discrete Legendre moments l = 0..4 and the full bin norm, per group, per flavour and for the whole gas;
- the lapse, Γ, R(r_m), T_b, H_b and the peak compaction.

**Bit-for-bit check.** nnmode=1, T0=10, δ=0.51925, run to ε = 0.6:
- The unmodified copy and the recorder copy (every 20 steps) both took 3342 steps.
- The intensities I and plasma energy densities e are identical, max|ΔI| = 0.0.
- I edited the recorder copy once more after the first check and repeated the check, with the same result.
- Files: `regress.py`, `log_regress.txt`.

**Runs.** All four used nnmode=1, mode=phys, G=6, x from 0.4 to 20, N=300, K=32, and every other option at McCormick's defaults. One process ran at a time.

| run | T0 | δ_m (archived edge) | outcome | ε at end | T_H (MeV) | wall time |
|---|---|---|---|---|---|---|
| T10_lo | 10 | 0.51925 | dispersed | 6.295 | 1.0029 | 11.2 min |
| T10_hi | 10 | 0.5195625 | BH | 6.139 | 1.0029 | 10.7 min |
| T5_lo | 5 | 0.52475 | dispersed | 6.052 | 0.5062 | 11.4 min |
| T5_hi | 5 | 0.525125 | BH | 6.339 | 0.5062 | 9.4 min |

- **Where the edges come from.** They are the last dispersed and last black-hole amplitudes of the archived nnmode=0 bisections, `res_mg_phys6_10.0.json` and `res_mg_phys6_5.0.json`.
- **They still split.** Both pairs split under nnmode=1, so the preregistered fallback (the ±0.001 pair of Table VIII) was not needed.
- **What that measures.** With the common-frame ν–ν target, the threshold lies in [0.51925, 0.51956] at T_H = 1 MeV and in [0.52475, 0.52513] at T_H = 0.51 MeV, from two runs per mass.

## Definitions (fixed in PREREGISTERED.txt before the runs)

- **Discrete Legendre moments.** p_l comes from Gram–Schmidt of 1, μ, …, μ⁴ on the 32 midpoint bins, with ⟨f,g⟩ = ½ Σ f g Δμ. So p_0 = 1 and I_0 = e_s/4π exactly. I_l = ⟨p_l, I⟩.
- **Kept share.** A = I_0² / ‖I‖², with the norm over all 32 bins. A_4 is the same with the norm cut at l ≤ 4.
  - It is computed per group, per flavour, and for the summed intensity.
  - This is v5.1's A = |v_0|² applied to the local angular chain rather than to a Fourier mode, so the comparison is structural only.
- **Link rapidity.** ρ_s = ½ ln[(κ_e,s + κ_n,s)/κ_e,s], and r_s = 1 + κ_n/κ_e, from the local rates.
  - With nnmode=1, the identification D = diag(0, κ_e, κ_e+κ_n, …) holds exactly only for the total momentum, because the ν–ν target is a common boosted frame.
- **Gas frame velocity.** v_L = 2q / [e + P_r + √((e+P_r)² − 4q²)], from the summed e, q and P_r in the plasma frame.
- **Speed-limit ratio.** R_SL = (dA/dτ)² / (4 E_B A(1−A)) for the whole-gas A, with τ the proper time of the cell.
  - I took E_B = 1/R(r_m)². That is k²/3 with k = √3/R(r_m), the rms k under v5.1's profile weight.
  - The bound's hypotheses do not hold in the GR model, so this is a reading only.
  - At the centre, 1−A is at roundoff level, so R_SL there is finite-difference noise.

## Numbers

Values at the r_m cell. Each collapsing/dispersing pair agrees to the digits shown until about ε ≈ 4; the T10_hi and T5_hi rows are in `log_readout.txt`.

| ε | run | v_L | 1−A | A_4 | \|I_1..4\|/I_0 | dominant slot | κ_e/H, κ_n/H | r_dom | ρ_dom |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 | T10_lo | 0.0040 | 0.0033 | 0.9967 | 0.009, 0.057, 0.004, 0.003 | 9 | 0.134, 0.908 | 7.76 | 1.025 |
| 1.7 | T10_lo | 0.0306 | 0.0358 | 0.964 | 0.068, 0.175, 0.035, 0.026 | 9 | 0.039, 0.267 | 7.88 | 1.032 |
| 2.5 | T10_lo | 0.0792 | 0.0961 | 0.906 | 0.172, 0.246, 0.103, 0.055 | 9 | 0.022, 0.158 | 8.23 | 1.054 |
| 4.0 | T10_lo | 0.1065 | 0.148 | 0.867 | 0.232, 0.217, 0.228, 0.011 | 10 | 0.029, 0.218 | 8.55 | 1.073 |
| 1.7 | T5_lo | 0.0519 | 0.0608 | 0.940 | 0.114, 0.214, 0.068, 0.032 | 9 | 0.0044, 0.032 | 8.24 | 1.055 |
| 2.5 | T5_lo | 0.1223 | 0.138 | 0.866 | 0.263, 0.241, 0.161, 0.034 | 9 | 0.0022, 0.019 | 9.61 | 1.131 |
| 4.0 | T5_lo | 0.1518 | 0.207 | 0.808 | 0.327, 0.204, 0.287, 0.076 | 10 | 0.0027, 0.029 | 12.08 | 1.246 |

- **Gas frame at r_m.**
  - v_L peaks at 0.110 (T_H = 1 MeV) and 0.162 (T_H = 0.51 MeV), near ε ≈ 3.5.
  - It turns negative, meaning infall, after about ε ≈ 5.3.
  - In the final compression |v_L| reaches 0.13–0.16, and the largest group flux ratio |q_s|/e_s reaches 0.29–0.38.
  - At the centre, |v_L| stays at or below 3×10⁻³.
- **Kept share at r_m.**
  - 1−A rises to 0.15–0.22 over the readout epoch.
  - From ε ≈ 2.5 on, the l = 2 and l = 3 parts of the summed intensity are each about as large as the dipole.
  - At the centre the distribution stays isotropic to 1−A ≲ 5×10⁻⁵.
- **Link rapidity over 1.7 ≤ ε ≤ 4.** The dominant slot at r_m is always ν_μ,τ group 3 or 4.

  | T_H | r_dom | ρ_dom | ν_e groups, r |
  |---|---|---|---|
  | 1 MeV | 7.88–8.58 | 1.03–1.07 | 2.47–2.63 |
  | 0.51 MeV | 8.24–12.15 | 1.06–1.25 | 2.54–3.39 |

  - At the centre, compression heating raises κ_e and r_dom drops to 4.6–7.5 (ρ 0.76–1.01). That is still above the window.
- **Both rates are below H at readout.**
  - At T_H = 1 MeV: κ_e/H = 0.02–0.04 and κ_n/H = 0.16–0.27.
  - At T_H = 0.51 MeV the rates are roughly ten times lower.
  - So the flux–shear link has a large rapidity but a small absolute rate.
- **Speed-limit ratio at r_m.**
  - The maximum over each whole run is 0.15 (T10_lo), 0.10 (T10_hi), 0.20 (T5_lo) and 0.11 (T5_hi).
  - It peaks near 0.04 around ε ≈ 1.2 and is at most 0.03 during 1.7–4.
  - It is below 1 everywhere, but per the definitions above that does not test the bound.

## Verdicts against the preregistered kill lines

### (i) First epoch where the collapsing and dispersing runs differ by more than 1%: killed

The criterion was the first record where |X_BH − X_disp| > 0.01 × the running max of |X_disp|, at r_m.

| quantity | T_H = 1 MeV | T_H = 0.51 MeV |
|---|---|---|
| v_L | 4.228 | 4.095 |
| 1−A | 2.907 | 2.926 |
| A itself | 4.488 | 4.157 |
| peak compaction | 3.777 | 3.645 |

**Setup failure at T_H = 0.51 MeV.** As written, the metric trips on the very first record (ε = 0.100). There both runs have X equal to zero within roundoff (10⁻¹⁹ for v_L, 10⁻¹⁶ for 1−A), so the scale is zero and the metric is undefined. The 0.51 MeV column excludes that one record.

- **Why it is killed:**
  - 1−A separates before ε = 3.0 at both T_H.
  - It leads v_L by 1.32 and 1.17 in ε, against the allowed gap of 0.5.
- **What held:**
  - v_L separates inside its predicted window [3.0, 5.5].
  - A itself separates only after ε = 4, as predicted.
- **What it shows.** The kept-share anisotropy 1−A is the earliest of these quantities to tell the two outcomes apart:
  - about 0.85 in ε before the peak compaction separates, and about 1.2–1.3 before the gas frame does;
  - its fractional difference is already 0.2% at ε = 1 and grows steadily, while v_L's is 0.02% there.
- **Caveat.** Part of this lead is because 1−A is second order in the anisotropy. Whether it is a causal lead is untested; that is the job of the restart test (A4).
- **Centre cell, T_H = 1 MeV:** 1−A separates at ε = 2.48 and v_L at 3.07.

### (ii) Link rapidity of the dominant group at readout: survives

- The dominant group's r is never inside 3/4 ≤ r ≤ 3/2 in any of the four runs. It is always above the window, at ρ = 1.03–1.25 against the window's upper edge of +0.203.
- My stated numerical ranges were too narrow at T_H = 0.51 MeV. I expected r of 6–9 for ν_μ,τ and 2.2–2.8 for ν_e; the runs reach 12.1 and 3.39. That misses the stated range but not the kill line.
  - The cause is the one I gave beforehand, only stronger than I allowed: the local factor (T_ν/T)⁴/χ_e grows as electron–positron pairs annihilate.
- **Consequence.** McCormick's physical model sits outside the window where v5.1 measured the odd rate 1.11 ± 0.01, at r ≈ 8–12. Applying v5.1's linear-in-rapidity law there would be an extrapolation; that is untested. v5.1's formal pairs reach only r = 16, where an even part appears.

## Files

All in `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A3_instrument/`:
- `PREREGISTERED.txt`: predictions timestamped 2026-11-11T14:06:02Z, with the results appended below them.
- Code: `run_mg.py` (the recorder copy), `ms_mg.py` (unchanged), and `orig/` (the unmodified copies).
- Regression check: `regress.py`, `log_regress.txt`, `regress_orig.npz`, `regress_mod.npz`.
- Runs: `drive.py`, `queue.sh`, `log_runs.txt`.
- Full recorder output, about 18 MB each: `raw_T10_lo.json`, `raw_T10_hi.json`, `raw_T5_lo.json`, `raw_T5_hi.json`.
- Analysis: `analyse.py` with `log_analyse.txt`, and `readout.py` with `log_readout.txt`.
- Compact time series: `A3_timeseries.json` (all four runs, Δε ≈ 0.02, 1.8 MB).
- Plots, made by `plots.py`; I viewed all three:
  - `fig_rm.png`: v_L, 1−A, link rapidity, moment ratios, R_SL and peak compaction against ε for the four runs, at r_m.
  - `fig_centre.png`: the same at the centre cell.
  - `fig_groups_rm.png`: kept share and link rapidity for each group at r_m.
- `mcc_paper.txt`: text extracted from McCormick's paper.