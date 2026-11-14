# Surgeon's cut list, v9 -> v10 (written before any edit, and before reading the watcher's list)

Numbers are from `A6_refine2/level3_rates_out.txt`.

## To change

| # | Where | Now | Becomes | Why |
|---|---|---|---|---|
| S0 | `neutrinos_v9.tex` header line | version 9 | version 10 | new version |
| S1 | Abstract (L22) | "at a rate of 1.11 ± 0.01 inside the window" | "at a rate of 1.10 ± 0.01 inside the window" | headline decision |
| S2 | Abstract (L22) | "and the ±0.01 is a finite-resolution budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shift of the r = 1.25 threshold to 0.42 of the previous step, and if the r = 0.8 threshold shrinks alike the rate extrapolates to 1.094–1.098." | "and three grid levels give 1.110, 1.102 and 1.101, the last step moving the rate by 0.0007 where the step before moved it by 0.008; the ±0.01 is the bracket range of the finest level with the fluid reference, not a statistical interval." | the conditional is replaced by the measurement |
| S3 | §link L236, end | "Every central inner value, 1.1020 to 1.1102, lies in [eq. odd rate = 1.11 ± 0.01] but the ±0.01 is now the error budget itself, dominated by resolution, and not a margin around a converged number." | removed here; the equation moves to the end of the third-level account (S5) | the band must be stated after the third level, which now sets it |
| S4 | §link L240 | "Under either reading, if the r = 0.8 threshold shrinks by the same factor, the third-level rate is 1.099 and the extrapolated rate 1.094–1.098, just below the band; the r = 0.8 third-level run was still in progress when this version was closed, so the extrapolation is untested." | "At r = 0.8 it puts the threshold at 0.5117877 ± 0.0000063, a rise of 3.1e-5 against 6.4e-5, a factor 0.49 (range 0.39–0.59): second order in the cell size predicted 0.51178492, inside the bracket; first order in the cell size (0.51179917) and first order in the time step (0.51177780) both fall outside [measured; Appendix B.27]. The third-level rate is 1.1013, a shift of −0.0007 where the step before was −0.0082, inside the kill line set before the runs; over the corners of the two brackets it ranges from 1.094 to 1.109, so the shift is smaller than the brackets resolve and no order is fitted to the rate." | measurement replaces the conditional |
| S5 | §link, after S4 | (the equation, moved from S3) | "With the fluid reference and the pair spread the budget at the third level is 0.0091 in quadrature. The two finer levels and that range lie in [eq. odd rate = 1.10 ± 0.01], where the ±0.01 is a resolution and bracket budget, not a statistical interval; the first-level value, 1.1102, sits at its upper edge." | headline; states honestly that 1.1102 is at (0.0002 above) the edge |
| S6 | Fig. link caption (L262) | "the inner-pair rate 1.11" | "the first-level inner-pair rate 1.11" | the drawn line is the first-level fit; no redraw |
| S7 | Summary (L293) | "at a rate of 1.11 ± 0.01 inside the admissible window" | "at a rate of 1.10 ± 0.01 inside the admissible window" | headline |
| S8 | Summary (L293) | "the rate is a measured number at finite resolution, 1.11 ± 0.01, the ±0.01 a resolution budget rather than a converged value or a statistical interval, extrapolating to 1.094–1.098 if the unfinished third-level run follows the finished one, with no closed form attached." | "the rate is a measured number, 1.10 ± 0.01, steady to 0.001 between the two finer of three grid levels, the ±0.01 a resolution and bracket budget rather than a statistical interval, with no closed form attached." | measurement |
| S9 | `sec_new_mcc.tex` L11 | "far outside the window where the rate 1.11 was measured" | "far outside the window where the rate 1.10 was measured" | follows the headline |
| S10 | App. B.27 intro | "... the run log; the r = 1.25 result." | "... the run log; the two results; the rate script and its output." plus listings of `res_L3_r08.json`, `level3_rates.py`, `level3_rates_out.txt` | reproducibility |
| S11 | `code/A6/PREREGISTERED.txt`, `RUNLOG.txt` | as closed in v9 | current files: RESULT appended to the preregistration (append-only, as the file says); run log through the last run | the record of the finished run |
| S12 | Zenodo description | "at a rate of 1.11 ± 0.01, a finite-resolution estimate whose ± 0.01 is a resolution budget, not a statistical interval. A third grid level shrinks ... extrapolates to 1.094–1.098." ; "version 9" | "at a rate of 1.10 ± 0.01. Three grid levels give 1.110, 1.102 and 1.101; the ± 0.01 is a resolution and bracket budget, not a statistical interval." ; "version 10" | same |
| S13 | README | version 9 names | version 10 names; A6 line unchanged | version |

## To stay

- L219–222 (table of first-stage odd rates, "it lies at 1.10–1.11"): first-stage values, true as stated.
- L234 (stage-correct inner rates 1.1066 and 1.1102) and L236 up to "0.016 added linearly": the first and second level account, true as stated.
- L240, the r = 1.25 third-level sentences (0.5099481 ± 0.0000063, factor 0.42, the three predictions, "does not separate second order in space from first order in time, or a mix"): true for r = 1.25.
- L240 "how the odd rate depends on the start time is untested": still untested.
- `sec_new_mcc.tex` L19 "the frozen law at rate 1.11": states what the A2 prediction was computed with.
- App. C (L523) Lean statement "the odd rate lies in [1.112, 1.114] over the whole bracket pair": a theorem about the v5 bracket pair.
- Every other "untested" (L106, L140, L181, door, Gramian): unrelated to this run.
- No figure is redrawn.

## Open points for the watcher

- S5: is "sits at its upper edge" honest enough for 1.1102 against a band ending at 1.11?
- S9 against the L19 line that stays: consistent?
- Is the L236 budget sentence (0.0097 / 0.016, built on the −0.0082 shift) still right to keep once S5 gives the third-level budget?
