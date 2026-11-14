# A4 restart test: report

**REPORT.md was not written.** The environment blocks report files from subagents, so the full report is below. Save it as `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A4_restart/REPORT.md` if you want the file. Every prediction, kill line and result is in `PREREGISTERED.txt` in that folder, appended in time order with timestamps. Nothing written there earlier was edited.

**Answer.** Yes. Hidden angular structure that a fluid closure cannot carry moves the black-hole threshold in the full GR system, and it does so as Jeromie's door predicts:
- **Planted at decoupling (eps_s = 2):** the l=3 pair's thresholds differ by 3.74e-3. That is about 200 bracket widths and well past the drift allowance.
- **Planted deep in the coupled era (eps_s = 0.5):** the difference is 1.75e-5, under one bracket width.
- **Opposite reading** (the collapse washes out l ≥ 3 whatever the timing): killed.

## Setup
- **Solver.** Copies of McCormick's `ms_nuc.py` and `ms_fluid.py` (commit eb7c4de; the physics is the same as the 41a0f83 version v5.1 used). One collision rate (the r=1 case), Gaussian profile, R_nu = 0.409, eps_dec = 2, n = 3, N = 400, Nmu = 32.
- **Driver `restart.py`.** It is McCormick's run_nuc loop with two changes:
  - kappa is re-evaluated at every SSPRK3 stage, as audit item 1 asks;
  - the step that would cross t_s is shortened so the run lands exactly on the restart surface, where the full state is saved.
- **Bracket rule.** Only a detected apparent horizon or McCormick's dispersal rule moves a bracket. A crash or breakdown never does.
- **CPU.** Each long run waited until fewer than 2 other python processes were running. The first screen run waited 37 minutes.
- **Baseline (no perturbation, restart at 2):** delta_c = 0.5107500 ± 0.93e-5. v5.1's value was 0.51074 ± 0.00002, so the stage-time kappa moves the threshold by less than one bracket.

## Perturbation
The task's uniform version, I → I(1 + a P_3) in every cell, was tried first. It was dropped as a verdict tool:
- A uniform a is irregular at r = 0, because a regular l-th angular moment must vanish like r^l at the centre.
- Near the centre, streaming across one cell is as fast as collisions, so the uniform pair measures a centre artefact. At eps_s = 2 the centre neutrino density moved by 91%. At eps_s = 0.5 the separation was about 1e6 times the survival law.
- Those numbers are in `linear_check_uniform_out.txt`. This uniform-a check was the step-4 short-run check.

Every verdict uses the coordinator's design D2:
- dI_ik = f · b(r_i) · m_i · (eps_i/4π) · p_l(mu_k).
- p_l is the discrete orthogonal polynomial on the 32 bins (orthogonal to 1, mu, mu² to 2e-17).
- b is a smooth bump that is identically zero for r ≤ 0.3 r_m and r ≥ 2 r_m.
- m_i is the cell's positivity margin; f = ±0.5.

**Positivity bounds on the 32-bin grid.**

| Direction | Isotropic grid | Actual state at eps_s = 2 |
|---|---|---|
| l=3 | \|a\| < 1/max\|p_3\| = 1.21498 | +0.8435 / −0.8325 |
| l=4 | +2.3509 / −1.3885 | +2.026 / −0.951 |

**Restart checks** (`check_restart_out.txt`, `check_bump_out.txt`). Between the +f and −f states, every cell and all three surfaces were compared:

| Quantity | Largest difference |
|---|---|
| Discrete l=0,1,2 components | ≤ 4.4e-16 of c_0 |
| e_nu, P_r, mass M | ≤ 9e-16 |
| q (relative to e_nu) | ≤ 1e-16 |
| Lapse (cells and edges) | ≤ 2e-15 |
| Constraint residual Γ² − (1 + U² − 2M/R) | ≤ 7e-15 |
| Fluid and metric arrays | bit-identical |

The perturbed l component differs by 0.08–0.17 of c_0.

## Screen
Paired runs at delta 0.5100 and 0.5115 (`screen_out.txt`). The noise floor is the restart's own shortened step, 1e-12 to 4e-8 in Cmax.
- Every pair separated by more than 1e4 times the noise floor, so every pair was selected for trisection.
- At eps_s = 2 the outcomes flipped at both deltas:
  - the +p_3 member dispersed at 0.5115;
  - the −p_3 member collapsed at 0.5100.

## Thresholds
w is the full bracket width; Δ is delta_c(+f) − delta_c(−f).

| eps_s, direction | delta_c(+f) | delta_c(−f) | Δ | Δ / w |
|---|---|---|---|---|
| 2, l3 | 0.5125833 | 0.5088395 | +3.744e-3 | 202 |
| 2, l3 at Nmu=48 | 0.5125134 | 0.5090041 | +3.509e-3 | — |
| 2, d (A5 L∞ direction) | 0.5134352 | 0.5079300 | +5.505e-3 | 297 |
| 2, l4 | 0.5096749 | 0.5117726 | −2.098e-3 | 204 |
| 0.5, l3 | 0.5107685 | 0.5107510 | +1.75e-5 | 0.95 |
| 0.5, l4 | 0.5107685 | 0.5107500 | +1.85e-5 | 1.0 |
| 4, l3 | 0.5108796 | 0.5106358 | +2.44e-4 | 13 |
| 4, l4 | 0.5106759 | 0.5108241 | −1.48e-4 | 8 |

- Bracket widths w are 8e-6 to 1.85e-5.
- **Drift allowance.** Rerunning the (2, l3) pair at Nmu = 48 moved the members by 7.0e-5 and 1.65e-4, so d_K = 1.65e-4. A difference counts as real only if the brackets stay apart after each is widened by d_K; in practice it must exceed about 3.5e-4.

## Verdicts against the kill lines
- **P1 (eps_s = 2 moves the threshold):** passes for l=3 and for l=4. Both differences are real.
- **P2 (eps_s = 0.5 agrees within 2 w):** passes for l=3 and for l=4.
- **P3 (eps_s = 4 moves the threshold):** not passed for either l, as preregistered.
  - The raw differences are 13 w and 8 w, with the same signs as at eps_s = 2.
  - They fail only on the drift allowance, which was measured on the (2, l3) pair. A drift measured on these pairs is untested.
  - The lean that the effect is smaller than at eps_s = 2 holds: about 6.5% for l=3.
- **P4 (the d direction moves more than p_3 at equal positivity margin):** passes. The ratio is 1.47 in threshold and 1.5–1.7 in Cmax during the screen. A5's linear chain predicted 2.47.
- **Opposite reading:** killed.
- **Sign:** none was predicted. Measured:
  - directions oriented like +p_3 (including d) raise the threshold;
  - +p_4 lowers it, by 0.56 of the p_3 shift (A5's chain gave 0.40).
  - Shifts from the baseline for l=3 are +1.83e-3 and −1.91e-3, so the response is close to odd in f.

## Points to flag
- **The coupled era does not erase as hard as the survival law says.** At eps_s = 0.5:
  - the Cmax separation is about 1e5 times the noise floor;
  - it holds under angular refinement (Nmu 48/32 gives a ratio of 0.86–0.89);
  - the linearised threshold shift, about 1.3e-5, is 0.3–0.5% of the shift at decoupling, against the law's 5e-10.

  It is a channel of the GR solver, not an angular-grid artefact; dependence on radial resolution is untested. One candidate, also untested: the fluid-frame shear and acceleration terms couple l=3 to l=2 at a rate set by the shear rather than by k, so the suppression is roughly S/κ per rung. The witness's flat chain has no such term. At the bracket resolution reached, the threshold verdict is still "agree".
- **Solver crashes.** Three trial runs ended in "crash" at eps ≈ 7.37, just before a horizon. Under the strict rule none of them moved a bracket.
- **One queue was stopped and rerun.** The (0.5, l4, −f) search was stopped by the 2-hour background limit and rerun from scratch; the partial log is kept as `*_killed`.
- **Minimum intensity stayed positive in every run** (lowest 4.5e-10).

## Files
All in `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A4_restart/`:
- **Preregistration and results:** `PREREGISTERED.txt`
- **Solver copies and driver:** `ms_nuc.py`, `ms_fluid.py`, `restart.py`
- **Run scripts:** `check_restart.py`, `check_bump.py`, `linear_check.py`, `screen.py`, `screen48.py`, `trisect.py`, `cpuwait.py`, `queue_T*.sh`
- **Outputs:** `check_restart_out.txt`, `check_bump_out.txt`, `linear_check_uniform_out.txt`, `screen_out.txt`, `screen_res.json`, `screen48_out.txt`, `log_*.txt`, `trisect_*.json`
- **Saved states:** `screen/`, `cache/`
- **A5's direction file (copy):** `restart_direction_A5.json`

Every script carries a `# SCRIPT:` line.