# Surgery brief: v9 -> v10 of "What the Neutrino State Must Keep" (Jeromie Beasley)

## What happened
v9 was closed while one run was unfinished: the r = 0.8 threshold on the third (finest) resolution level. v9 therefore states the third-level rate only as a conditional extrapolation. That run has now finished. v10 must state the measurement and remove every statement it makes out of date. Nothing else in the paper may change.

## The new facts (raw files: <session>/nu6/A6_refine2/res_L3_r08.json, res_L3_r125.json, RUNLOG.txt, PREREGISTERED.txt, oddrate.py)
- r = 0.8, level 3 (N = 900, N_mu = 72, Courant 0.1, cH 0.00125): bracket [0.51178143, 0.51179393], delta_c = 0.51178768 +- 0.00000625.
- r = 1.25, level 3 (already in v9): bracket [0.50994187, 0.50995437], delta_c = 0.50994812 +- 0.00000625.
- Stage-correct thresholds at the coarser levels (v9 text and Appendix B.19/B.27): r = 1.25: level 1 0.50984158, level 2 0.50991687; r = 0.8: level 1 0.51169233, level 2 0.51175643.
- References: delta_F = 0.49773, delta_I = 0.52832. Offset tau(d) = ln[(delta_I - d)/(d - delta_F)]; odd rate = [tau(d_1.25) - tau(d_0.8)] / ln 1.25.
- Rates: level 1 1.1102, level 2 1.1020, level 3 1.1013 (over the corners of the two level-3 brackets: 1.0938 to 1.1088). Level 2 -> 3 change -0.0007; level 1 -> 2 change -0.0082 (the line set before the first refinement was 0.005).
- Shrink of the threshold shift, level 2->3 over level 1->2: r = 1.25: 0.415 (0.332 to 0.498); r = 0.8: 0.488 (0.390 to 0.585).

## The author's decision on the headline
The headline rate becomes 1.10 +- 0.01 (was 1.11 +- 0.01, which the author held only until this run landed).

## Rules of the surgery
- Change only sentences made false or out of date by the new facts or by the headline decision. Keep the author's wording and length wherever it is still true. No narration of what was changed ("previously", "v9 said"): the paper reads as one complete thought.
- A statement of what was actually run or used in an earlier test (for example a prediction that was computed with rate 1.11, or a figure drawn from first-level data) stays if it is still true as a statement of what was done; say so explicitly if you judge it must change.
- Every new number must be recomputable from the raw files.
- Source to operate on: <session>/nu6/paper_v9_frozen/ (neutrinos_v9.tex, sec_new_*.tex, app_new_*.tex, code/A6/), plus the README (<session>/nu6/harness/README_v9.md) and Zenodo description (<session>/out_v9/ZENODO_DESCRIPTION_v9.txt).

<session> = <session>
