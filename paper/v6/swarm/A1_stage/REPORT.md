# A1 — the 1.11 law on stage-correct collision histories (complete)

## What was run
- **The one change:** in a copy of v5.1's `run_split_v2.py` / `run_shear_v2.py` (now `run_split_stage.py` / `run_shear_stage.py`), kappa(t) = (1/2t) min[(eps_dec/eps)^3, 5e5] is now evaluated at each SSPRK3 stage time (t, t+dt, t+dt/2). Before, it was computed once per step. The stiff time-step cap still uses the stage-start kappa. The solvers `ms_nuc_split.py` and `ms_nuc_shear.py` are byte copies of v5.1's. `ms_fluid.py` is McCormick's file at 41a0f83, identical at HEAD and left unchanged, so it has no SCRIPT line.
- **Physics as in v5.1:** eps_dec = 2, n = 3, Gaussian profile, R_nu = 0.409, eps0 = 0.1, N = 400, Nmu = 32, Courant 0.4, cH = 0.005.
- **Endpoint rule as in v5.1:** a run moves a bracket only if it ends in a detected horizon (2M/R >= 1 with U < 0) or disperses. A crash or BH_breakdown is retried once at Courant 0.3 (0.15 on the refined grid). If the retry also fails, the run is reported and skipped.
- **Search method:** the house rule allows one simulation process at a time, so v5.1's two-points-per-round trisection became sequential bisection under the same endpoint rule. Each search started from v5.1's midpoint +- 3e-4. Both starting ends were run first (lower end dispersed, upper end formed a horizon in every search). Every threshold was closed to a bracket width <= 1e-6.
- **Pre-registration:** `PREREGISTERED.txt` was written at 14:05Z, before every search. Results are appended under each test.
- **Positivity:** the minimum intensity stayed positive in all 118 logged search runs (lowest 4.9e-10).

## Regression (r = 1, delta = 0.5109)
- The v5.1 runner forms a black hole at eps = 6.6147, reproducing v5.1's 6.61. The stage-correct runner forms one at eps = 6.6176, a shift of +2.9e-3. Steps went from 61651 to 61677.
- Maximum relative field differences between the two runners:
  - eps = 1 to 2: about 1e-6
  - eps = 4: 1.2e-4 (e and I)
  - eps = 6: 3.4e-3 (e), 2.7e-3 (I), 4.9e-4 (U), 1.1e-5 (R)
  - at stop: 4.7e-3 (e), 4.4e-3 (U), 3.3e-3 (I), 4.4e-4 (R)

## Verdicts against the pre-registered lines
- **S1 (a): survives.** The inner odd rates moved +0.0060 (r = 1.2 pair: 1.1006 -> 1.1066, range [1.1061, 1.1072]) and -0.0026 (r = 1.25 pair: 1.1128 -> 1.1102, range [1.1098, 1.1106]). Both moves are under 0.01.
- **S1 (b): survives.** After the fix the two pairs differ by 0.0036 (v5.1: 0.0122), under 0.01.
- **Opposite reading: holds.** The pair difference fell below 0.005. On the reading stated before the runs, the old 0.012 spread was mostly the first-order collision-history error, not a per-point systematic. The stage fix moved the four inner thresholds by only 0.9 to 6.7e-6, but at |ln r| = 0.18 to 0.22 that is enough to move the rates.
- **S2 (shear only, r = 1.2 and 1/1.2): survives.** The rate went from 1.1895 to 1.1928 (range [1.1922, 1.1933]), a move of +0.0033, under 0.01. The gap to the all-l>=2 family is 0.0862 (v5.1: 0.0889), above 0.05.
- **S3 (simultaneous refinement, r = 1.25 and 0.8): FAILS.** The refinement used N = 600, Nmu = 48, cH and Courant halved, and the stiff cap unchanged as specified.
  - Both thresholds rose: +7.53e-5 at r = 1.25 and +6.41e-5 at r = 0.8. The rate moved because they rose by different amounts.
  - The odd rate went from 1.1102 to 1.1020 (range [1.1016, 1.1024]). The shift is -0.0082 (corner range [-0.0090, -0.0074]), more than the pre-registered 0.005.
  - In v5.1, Nmu alone (32 -> 48 at the r = 4 pair) moved the rate by under 0.001. So this shift most likely comes from the radial grid or the time step. Which one is untested.
- **Re-judging +-0.01 with the S3 shift carried as a resolution error:**
  - Every central inner value lies between 1.102 and 1.110: 1.1066 and 1.1102 at N = 400, 1.1020 refined. The band 1.11 +- 0.01 still contains all of them.
  - The error budget is now pair spread 0.0036, fluid reference +-0.0038 (common to all rates), and resolution 0.0082. That is 0.0097 in quadrature and 0.016 summed linearly.
  - So +-0.01 is no longer a margin around a known number. It is the error budget itself, and resolution dominates it. With only one refinement level, whether the rate has converged is untested.
  - A statement the numbers support: the inner odd rate is 1.10 to 1.11 on the N = 400 grid, and refinement lowers it by about 0.008. Keeping "1.11 +- 0.01" or restating it as about 1.105 +- 0.01 (resolution-dominated) is your call.
- **r = 1 anchor, flagged and checked (control C1):**
  - The stage-correct r = 1 threshold is 0.51077853, outside v5.1's bracket. G(1) = 0.42656.
  - The v5.1 runner, under the same driver, gives 0.51075683, inside v5.1's bracket. G = 0.42585.
  - So of the +3.8e-5 move, +2.2e-5 is the stage fix and +1.6e-5 is the distance from v5.1's tolerance-1e-4 midpoint to the true threshold.
  - The stage fix moves r = 1 more than any inner threshold. This changes G(1) by +0.0007 and the even parts by about 0.003 (tau(1) by -0.0029). It does not enter any odd rate.
- **Fluid reference shifted +-7.8e-5:** every odd rate moves by about +-0.0038 together. The values are in the table below.

## Run anomalies (all reported, none moved a bracket)
- Undecided after retry: S1 r = 1/1.2 at 0.51152391; S1 r = 0.8 (one point); S2 shear r = 1.2 (one point); S3 r = 0.8 at 0.51175620.
- The S3 r = 0.8 point needed more handling:
  - Its Courant 0.2 attempt did not end in a horizon or dispersal.
  - The 0.15 retry was cut at 33 min when the queue's 2-hour background window expired.
  - The rerun was stopped by hand at 70 min without ending.
  - Per the pre-stated rule, the 0.4 point was run instead (`run_point.py`) and dispersed, closing the bracket at width 7.0e-7.
- Another agent shared the 2 cores during S2 and S3, so wall times are inflated.

## Files (all in this folder)
- **Stage-correct runners:** `run_split_stage.py`, `run_shear_stage.py`
- **Solver copies:** `ms_nuc_split.py`, `ms_nuc_shear.py`, `ms_fluid.py`
- **v5.1 originals for regression and C1:** `orig/`
- **Search and tools:** `search.py` (resumable bisection), `run_point.py`, `regress.py`, `oddrate.py` (rates and four-corner ranges, with check `oddrate_v51_check.txt`), `make_report.py`, `queue.sh`, `queue2.sh`
- **Pre-registration:** `PREREGISTERED.txt`
- **Logs:** `RUNLOG.txt` (master), `log_S1_*.txt`, `log_S2_*.txt`, `log_S3_*.txt`, `log_C1_r1_v51runner.txt`, `log_regress.txt`, `point_S3_r08.txt`
- **Results:** `res_*.json` (brackets plus every run), `prog_*.json` (search state)

## Thresholds (stage-correct runner)

| search | r | bracket | delta_c | +- | reference delta_c (v5.1; N=400 stage for S3) | shift | G | runs | undecided after retry |
|---|---|---|---|---|---|---|---|---|---|
| S1_r1 | 1 | [0.51077824, 0.51077883] | 0.51077853 | 2.9e-07 | 0.51074074 | +3.78e-05 | 0.42656 | 12 (1 retried) | 0 |
| S1_all_r12 | 1.2 | [0.51000783, 0.51000841] | 0.51000812 | 2.9e-07 | 0.51001486 | -6.74e-06 | 0.40138 | 12 (0 retried) | 0 |
| S1_all_r083 | 0.8333 | [0.51151547, 0.51151641] | 0.51151594 | 4.7e-07 | 0.51151452 | +1.41e-06 | 0.45067 | 12 (1 retried) | 1 |
| S1_all_r125 | 1.25 | [0.50984129, 0.50984187] | 0.50984158 | 2.9e-07 | 0.50984070 | +8.84e-07 | 0.39593 | 12 (0 retried) | 0 |
| S1_all_r08 | 0.8 | [0.51169198, 0.51169268] | 0.51169233 | 3.5e-07 | 0.51169573 | -3.40e-06 | 0.45643 | 13 (1 retried) | 1 |
| S2_shear_r12 | 1.2 | [0.50995416, 0.50995510] | 0.50995463 | 4.7e-07 | 0.50995416 | +4.69e-07 | 0.39963 | 12 (1 retried) | 1 |
| S2_shear_r083 | 0.8333 | [0.51157949, 0.51158007] | 0.51157978 | 2.9e-07 | 0.51157480 | +4.98e-06 | 0.45276 | 12 (0 retried) | 0 |
| S3_fine_r125 | 1.25 | [0.50991658, 0.50991716] | 0.50991687 | 2.9e-07 | 0.50984158 | +7.53e-05 | 0.39839 | 12 (0 retried) | 0 |
| S3_fine_r08 | 0.8 | [0.51175608, 0.51175678] | 0.51175643 | 3.5e-07 | 0.51169233 | +6.41e-05 | 0.45853 | 13 (2 retried) | 1 |

## Odd rates (references 0.49773 / 0.52832; ranges are hard four-corner ranges)

| pair | odd rate | range | change vs v5.1 / vs N=400 | fluid ref +7.8e-5 | fluid ref -7.8e-5 | even part (vs r=1) |
|---|---|---|---|---|---|---|
| all l>=2, r=1.2 & 1/1.2 | 1.1066 | [1.1061, 1.1072] | +0.0060 | 1.1104 [1.1099, 1.1110] | 1.1028 [1.1023, 1.1034] | +0.0030 |
| all l>=2, r=1.25 & 0.8 | 1.1102 | [1.1098, 1.1106] | -0.0026 | 1.1141 [1.1137, 1.1144] | 1.1064 [1.1060, 1.1068] | +0.0027 |
| shear only, r=1.2 & 1/1.2 | 1.1928 | [1.1922, 1.1933] | +0.0033 | 1.1969 [1.1963, 1.1975] | 1.1887 [1.1881, 1.1893] | +0.0024 |
| refined N=600, Nmu=48, all l>=2, r=1.25 & 0.8 | 1.1020 | [1.1016, 1.1024] | -0.0082 | 1.1058 [1.1054, 1.1062] | 1.0982 [1.0979, 1.0986] | n/a (no refined r=1) |

r = 1 anchor: G(1) = 0.42656 (bracket G range [0.42655, 0.42657]); v5.1 0.4253 +- 0.0006.
Inner-pair difference (r=1.25 pair minus r=1.2 pair): +0.0036 (v5.1: +0.0122).
Shear-only minus all-l>=2 at r=1.2: +0.0862 (v5.1: +0.0889).
Refinement shift of the r=1.25 pair's odd rate: -0.0082.
