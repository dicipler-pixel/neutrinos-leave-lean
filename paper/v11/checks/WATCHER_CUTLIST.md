# WATCHER cut list, phase 1 (v9 -> v10), written without reading the surgeon's plan

Paths: S = <session>
Source read: S/nu6/paper_v9_frozen/{neutrinos_v9.tex, sec_new_mcc.tex, sec_new_door.tex, sec_new_gramian.tex, app_new_evidence.tex, app_new_proofs.tex}, S/nu6/harness/README_v9.md, S/out_v9/ZENODO_DESCRIPTION_v9.txt, S/nu6/harness/claims.py.
My recompute script: S/nu6/harness10/watcher_work/recompute.py (run: python3 recompute.py S/nu6).

## 1. Recomputed numbers (all reproduce; none failed)

Code (core of recompute.py):

    DF, DI = 0.49773, 0.52832
    tau  = lambda d: log((DI-d)/(d-DF));  rate = lambda a,b: (tau(a)-tau(b))/log(1.25)
    L = {1:(0.50984158,0.51169233), 2:(0.50991687,0.51175643), 3:(res_L3_r125['dc'], res_L3_r08['dc'])}
    corners = [rate(a,b) for a in (r125 lo,hi) for b in (r08 lo,hi)]

Output:

    r08  lo 0.51178143 hi 0.51179393 dc 0.51178768 half 0.00000625  (N 900, K 72, cfl 0.1/0.1, cH 0.00125, rr 0.8)
         bracket = highest dispersed / lowest BH in its own log; 7 runs, only outcomes 'dispersed','BH', no flags
    r125 lo 0.50994187 hi 0.50995437 dc 0.50994812 half 0.00000625  (same grid, rr 1.25)
    level 1 rate 1.11021   level 2 rate 1.10198   level 3 rate 1.10132
    L3 corners 1.09382 .. 1.10883 (half-spread 0.00750)
    s12 -0.00823   s23 -0.00066   s23 over corners -0.00816 .. +0.00685
    fluid reference +-7.8e-5: R3 = 1.10509 / 1.09760 (+-0.0038, as at the other levels)
    r=1.25 shift12 +7.529e-05 shift23 +3.125e-05 shrink 0.415 (0.332..0.498)  order 2.17 (1.72..2.72)
    r=0.8  shift12 +6.410e-05 shift23 +3.125e-05 shrink 0.488 (0.390..0.585)  order 1.77 (1.32..2.32)
    first order cell size : 0.50996706 outside ; 0.51179916 outside   (PREREGISTERED prints 0.51179917, from unrounded level-1/2 midpoints)
    second order cell size: 0.50995033 inside  ; 0.51178492 inside
    first order time step : 0.50994197 inside (lower edge) ; 0.51177780 OUTSIDE (3.6e-6 below the dispersed edge 0.51178143)
    Richardson as fixed: p_obs 6.24, R_inf 1.10126 ; two-level p=1 1.10001, p=2 1.10080
    preregistered bracket part (8 range-end combinations, = A6_refine2/richardson.py): defined in 2 of 8, err_bracket 0.041
    budget at level 3: 0.0075 (bracket) , 0.0038 (fluid), 0.0036 (pair spread): 0.0091 quadrature, 0.0149 linear
    v9's conditional (r=0.8 shrinking by the r=1.25 factor): 1.0986 (1.0954..1.1017); measured 1.1013 lies inside that range

Every number in the brief is reproduced: brackets, 1.1102 / 1.1020 / 1.1013, corners 1.0938 to 1.1088, changes -0.0082 and -0.0007, shrink 0.415 (0.332-0.498) and 0.488 (0.390-0.585).
A6_refine2/level3_rates.py (new, written 15:56 local during this phase) reruns to its stored level3_rates_out.txt byte for byte and agrees with the above.

### PREREGISTERED.txt (first 4675 bytes, byte-identical to the frozen v9 copy; written 2026-11-11T20:44Z before any run)
Predicted (a): s23 = s12 (2/3)^p. p=1: R3 1.0965, thresholds 0.50996706 / 0.51179917. p=2: R3 1.0983, thresholds 0.50995033 / 0.51178492. p=3: 1.0995. Time step dominating (p_t=1): s23 -0.0027.
Kill line (b): if |R3 - 1.10198| > 0.00823 the rate is NOT converging and the paper must say so. Flag (not a kill): sign change of s23.
Richardson: p_obs = ln(s12/s23)/ln 1.5, R_inf = R3 + s23/(q^p_obs - 1); if p_obs outside [0.5, 4], reported but marked untrustworthy.
Deviation (appended 07:07Z 13 Nov): bisection stopped at width 1.25e-5 instead of 1e-6.

Finished r = 0.8 result against each line, in the file's terms:
- Kill line (b): |R3 - R2| = 0.00066 < 0.00823. PASSES at midpoints. At the worst bracket corner 0.00816: passes, with 0.00007 to spare.
- Sign-change flag: no change at midpoints (both negative); over the corners s23 takes both signs (not resolved).
- Prediction (a), rate: measured 1.1013 [1.0938, 1.1088]; the midpoint shift (-0.0007) is smaller than every predicted shift (-0.0055, -0.0037, -0.0024, -0.0027), and all predicted R3 lie inside the corner range, so the rate does not pick an order.
- Prediction (a), thresholds: p=2 inside both brackets; p=1 outside both. Time step alone (factor 1/3): inside for r=1.25, outside for r=0.8.
- Richardson: p_obs = 6.24, OUTSIDE [0.5, 4]: by the file's own rule R_inf = 1.1013 is "reported but marked untrustworthy". No extrapolated rate may be quoted as a result.
- Tolerance: FAILS the preregistered 1e-6 width (declared deviation, 1.25e-5).

## 2. Sentences to change (18 items)

Line numbers are in the frozen v9 files. "->" is my proposed text.

### neutrinos_v9.tex

C1. l.15. `\date{13 November 2026 \quad (version 9 of \emph{When the Neutrinos Leave})}` -> version 10 (date as the author sets it). Bookkeeping.

C2. l.22 (abstract). "at a rate of $1.11\pm0.01$ inside the window where the split operator is a Markov generator;" Headline decision. -> "at a rate of $1.10\pm0.01$ inside the window where the split operator is a Markov generator;"

C3. l.22 (abstract). "and the $\pm0.01$ is a finite-resolution budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step, and if the $r=0.8$ threshold shrinks alike the rate extrapolates to $1.094$--$1.098$." The r=0.8 run is finished; the conditional and the extrapolation are gone (Richardson order outside the preregistered range); the budget is now led by the third-level brackets, not a resolution shift. -> "and the $\pm0.01$ is an error budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shifts of the two thresholds to $0.42$ and $0.49$ of the previous step and gives $1.101$, against $1.102$ at the second level, with a bracket range of $1.094$--$1.109$."

C4. l.236, last sentence. "Every central inner value, $1.1020$ to $1.1102$, lies in" (then the equation). False under 1.10 +- 0.01: 1.1102 is 0.0002 above 1.11. See trap T1. -> "The values at the two finer levels, $1.1020$ and $1.1013$ (below), and the whole bracket range of the finest, lie in"

C5. l.238. `\text{odd rate}=1.11\pm0.01,` -> `\text{odd rate}=1.10\pm0.01,`

C6. l.240, sentence 1. "but the $\pm0.01$ is now the error budget itself, dominated by resolution, and not a margin around a converged number." "but" no longer follows C4, and the leading term is the third-level bracket range. -> "the first-level values, $1.1066$ and $1.1102$, sit at its upper edge. The $\pm0.01$ is the error budget itself, led by the third-level brackets, and not a margin around a converged number."

C7. l.240. "At $r=1.25$ it puts the threshold at $0.5099481\pm0.0000063$, a further rise of $3.1\times10^{-5}$ against $7.5\times10^{-5}$ for the previous step." One threshold of two. -> "It puts the thresholds at $0.5099481\pm0.0000063$ ($r=1.25$) and $0.5117877\pm0.0000063$ ($r=0.8$), further rises of $3.1\times10^{-5}$ each against $7.5$ and $6.4\times10^{-5}$ for the previous step."

C8. l.240. "The shift shrank to $0.42$ of the previous one (range $0.33$--$0.50$)." -> "The shifts shrank to $0.42$ (range $0.33$--$0.50$) and $0.49$ (range $0.39$--$0.59$) of the previous ones."

C9. l.240. "First order in the cell size predicted $0.50996706$, outside the bracket; second order in the cell size predicted $0.50995033$ (a factor $0.44$) and first order in the time step $0.50994197$ (a factor $0.33$), both inside, the second at its lower edge." -> "First order in the cell size predicted $0.50996706$ and $0.51179917$, both outside the brackets; second order in the cell size (a factor $0.44$) predicted $0.50995033$ and $0.51178492$, both inside; first order in the time step (a factor $0.33$) predicted $0.50994197$, at the lower edge of the $r=1.25$ bracket, and $0.51177780$, below the $r=0.8$ bracket."

C10. l.240. "So the bracket excludes an error purely first order in the cell size, but does not separate second order in space from first order in time, or from a mix of first-order errors in both \grade{measured; Appendix B.27}." At r=0.8 pure first order in time is now excluded. -> "So the brackets exclude an error purely first order in the cell size, and at $r=0.8$ one purely first order in the time step; they agree with second order in the cell size and do not exclude a mix of first-order errors in both \grade{measured; Appendix B.27}."

C11. l.240. "Under either reading, if the $r=0.8$ threshold shrinks by the same factor, the third-level rate is $1.099$ and the extrapolated rate $1.094$--$1.098$, just below the band; the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation is untested." Wholly out of date. -> "The third-level rate is $1.1013$, range $[1.0938,1.1088]$ over the corners of the two brackets: a change of $-0.0007$ from the second level against $-0.0082$ for the previous step, inside the kill line written first, which was a change larger than the previous one. The third-level brackets are $1.25\times10^{-5}$ wide, since runs this close to threshold no longer finish in one compute window, so the change is known only to $\pm0.0075$ and its sign is not resolved; the order read from the three central values, $6.2$, lies outside the range $0.5$ to $4$ set before the runs for an extrapolation, and none is quoted. With the reference shift and the pair spread the budget is $0.0091$ in quadrature, $0.015$ added linearly."

C12. l.262 (caption of Figure fig:link). "Lines: rate one (dashed) and the inner-pair rate $1.11$." The line and the plotted points are first-level, step-held data; the caption is true as a statement of what is drawn but now reads against the headline. Judgment call, see T3. -> "Lines: rate one (dashed) and the first-level inner-pair rate $1.11$."

C13. l.293 (Summary). "at a rate of $1.11\pm0.01$ inside the admissible window, and at $1.19$--$1.20$ when the shear alone is damped." -> "$1.10\pm0.01$" (rest unchanged).

C14. l.293 (Summary). "and the rate is a measured number at finite resolution, $1.11\pm0.01$, the $\pm0.01$ a resolution budget rather than a converged value or a statistical interval, extrapolating to $1.094$--$1.098$ if the unfinished third-level run follows the finished one, with no closed form attached." -> "and the rate is a measured number at finite resolution, $1.10\pm0.01$, the $\pm0.01$ an error budget rather than a converged value or a statistical interval, $1.102$ and $1.101$ at the two finest of three grid levels, with no closed form attached."

### sec_new_mcc.tex

C15. l.11. "His physical model lives far outside the window where the rate $1.11$ was measured," Presents 1.11 as the measured rate. -> "His physical model lives far outside the window where the rate was measured," (drop the number; l.19 still says which rate the frozen law used).

### app_new_evidence.tex

C16. l.68 (B.27). "Predictions and kill line written before the runs, with the appended timing and the change of tolerance; the queue scripts; the run log; the $r=1.25$ result." -> "Predictions and kill line written before the runs, with the appended timing, the change of tolerance and the results; the queue scripts; the run log; the two results; the script that computes the rates, and its output." Plus the listings in section 5.

### README (S/nu6/harness/README_v9.md)

C17. l.1, 3, 7, 8, 9, 10, 23: "version 9", "Version 9 of", and the v9 file names (PDF, HTML, ZENODO_DESCRIPTION_v9.txt, neutrinos_v9.tex) -> v10 names. l.18: "`guard.py` maps every sentence changed from version 8 to a ledger item ... `REVIEW_LEDGER_v8_to_v9.md` and `WATCHER_REPORT*.md` hold the record" describes the v9 check only; add the v10 record (this harness10 folder) or the line is incomplete for v10. l.15 (`lean_build_v9.log`) STAYS if the Lean sources are untouched: it names the actual build.

### Zenodo description (S/out_v9/ZENODO_DESCRIPTION_v9.txt)

C18. l.2 "(version 9 of ...)" -> version 10. l.9: "at a rate of 1.11 ± 0.01, a finite-resolution estimate whose ± 0.01 is a resolution budget, not a statistical interval. A third grid level shrinks the resolution shift of the r = 1.25 threshold to 0.42 of the previous step; if the r = 0.8 threshold shrinks alike, the rate extrapolates to 1.094–1.098." -> "at a rate of 1.10 ± 0.01, a finite-resolution estimate whose ± 0.01 is an error budget, not a statistical interval. A third grid level shrinks the resolution shifts of the two thresholds to 0.42 and 0.49 of the previous step and gives 1.101, against 1.102 at the second level."

## 3. Mentions that STAY

- neutrinos l.219-220 (table): odd rate 1.1006, 1.1128 ... with ranges. First-level, step-held runs; true as measured.
- l.222 "Inside the admissible window it lies at $1.10$--$1.11$": describes that table (1.1006, 1.1128).
- l.234 "The inner odd rates become $1.1066$ ... and $1.1102$, range $[1.1098,1.1106]$ ... differ by $0.0036$, against $0.012$ before": first-level stage-correct values, unchanged.
- l.22 abstract "the two inner pairs agree to $0.004$": first-level stage-correct, true.
- l.236 up to the last sentence: fluid reference +-0.0038; second level 0.50991687, 0.51175643, 1.1020, range [1.1016,1.1024], shift -0.0082 failing the 0.005 line; "which one is untested" (no run varied the radial grid or the time step alone; the third level refines both again); "budget is 0.0097 in quadrature, 0.016 added linearly" (the two-level budget, true as computed; C11 adds the three-level one).
- l.240 "A third level ($N=900$, $N_\mu=72$, ...) was run with its predictions and kill line written first." True. "Cells and angle bins shrink by $1.5$ per level and the Courant-limited time step by $3$." True.
- l.240 "how the odd rate depends on the start time is untested" and "The rate is a measured number with no closed form attached": untouched by the new run.
- l.245, 247, 249 shear-only table: "all $\ell\ge2$, same pair" 1.1006 and 1.1177, and 1.1928 against 1.1066: first-level values.
- l.251 angular resolution (1.1177 to 1.1170): a separate test.
- l.523 Lean `testK_*`: odd rate in [1.112,1.114] over the first-level step-held bracket pair. A theorem about that bracket; stays. l.524 `testJ_straddles` (1.108, 1.128) and l.526 `testL_*`: stay.
- sec_new_mcc l.13 "the frozen law of Section sec:link" and l.19 "the frozen law at rate $1.11$", and Figure fig:mcc caption "the frozen link law $+0.0010$": the prediction was computed and frozen with 1.11 (code_v6/A2_step3_predict.py l.115, A2_PREREGISTERED.txt l.42, 48). True as what was run. With 1.10 the predicted threshold moves by about 5e-5 against the quoted +-0.0003, so "a third of what the frozen law predicted" holds either way.
- code_v6/A2_*, A2b_PREREGISTERED.txt, A1_PREREGISTERED.txt, code/v4_runs/make_fig7_link_v5.py: archived scripts and preregistrations that used 1.11; never edited.
- sec_new_door.tex l.11 "A third restart surface", l.28 "angular refinement"; sec_new_gramian.tex: unrelated to the rate. No change.
- README l.13 "`code/A6/` holds the third resolution level": still true.
- Appendix C preamble (commit 9cd71fa, 87 theorems): stays, provided no Lean file is changed.

## 4. Traps

T1. Band sentence (l.236/238). Under 1.10 +- 0.01 = [1.09, 1.11] the level-1 value 1.1102 is outside by 0.0002, as are the step-held 1.1128 and the Lean bracket [1.112, 1.114]. Any sentence of the form "every value lies in the band" is false. Fix: say which values lie inside (levels 2 and 3 and the whole level-3 corner range 1.0938-1.1088) and that the first-level values sit at the upper edge (C4, C6).
T2. The band is not a hard bound either: level-3 corners with the fluid reference shifted run 1.0901 to 1.1126. The +-0.01 matches the quadrature budget (0.0091), not the linear one (0.0149). Do not write "bound" or "contains".
T3. Figure fig:link (figs/fig7_link_v5.png): the legend inside the image reads "rate 1.11 (inner pairs)" and the line is drawn at 1.11. Data plotted are the eleven first-level step-held thresholds, whose inner pairs give 1.1006 and 1.1128. No redraw needed for honesty (a 1.10 line would differ by 0.015 at the plot edge, under a marker width); minimal fix is the caption word "first-level" (C12). A redraw with a 1.10 line is the alternative; the author's call.
T4. No extrapolated rate. The preregistered Richardson order is 6.24, outside [0.5, 4]: "reported but marked untrustworthy". Replacing "1.094-1.098" by any new "extrapolates to" number would break the preregistration. The preregistered bracket part of the error is 0.041 (defined in 2 of 8 combinations), which says the same thing.
T5. Do not write "converged" or "the rate has stopped moving": s23 over the bracket corners is -0.0082 to +0.0069, sign unresolved; the kill line passes at the worst corner by 0.00007 only. Do write that the kill line passes.
T6. "Shrinks alike" / "by the same factor" is not what was measured: 0.415 against 0.488 (ranges overlap, 0.332-0.498 and 0.390-0.585). Quote both.
T7. The r=1.25 clause "first order in the time step ... inside, at its lower edge" is true only for r=1.25; for r=0.8 the same prediction (0.51177780) is outside. The v9 conclusion "does not separate second order in space from first order in time" is now false for r=0.8 (C9, C10).
T8. "Three systematics are larger than the brackets" (l.236) is true of the level-1 and level-2 brackets (rate range +-0.0004) and not of level 3 (+-0.0075, the largest term now). It stays where it is only because it precedes the third level; the new text must give the third-level range (C11) and must not call the budget "dominated by resolution" (C3, C6, C14, C18: "resolution budget" -> "error budget").
T9. First-order cell-size prediction for r=0.8: PREREGISTERED.txt prints 0.51179917 (unrounded midpoints); level3_rates.py prints 0.51179916 (8-digit inputs). Quote one; I used the preregistered 0.51179917.
T10. A6_refine2/PREREGISTERED.txt was appended at 15:56 local (21:56Z by file time; my clock read 21:58Z two minutes later) with a block headed "RESULT (appended 2026-11-13T22:05Z ...". The stamp is about nine minutes ahead of the real write time. In an append-only preregistration file the stamp should be the true time. Same block: "about 1.0993 (time step, p_t = 1)" is 1.0992 unrounded (1.10198 - 0.00823/3 = 1.09923). The first 4675 bytes are unchanged (checked against the frozen copy); a pre-append copy PREREGISTERED_before_result_2026-11-13.txt sits beside it.
T11. level3_rates.py's "over the four corners" Richardson line is not the preregistered part (i) (eight range-end combinations, as richardson.py does). If any Richardson spread is printed in the paper it must be the preregistered one, from richardson.py; my advice is to print none (T4).
T12. Abstract l.22 and Appendix C say every verdict's arithmetic is machine-checked in Lean. The third-level kill-line verdict is not in Lean (nor was the second-level 0.005 line in v9). Not made false by this surgery; do not add a claim that it is. If a Lean theorem is added for the level-3 corner range, Appendix C's count (87), commit and log all change: out of scope unless the author asks.
T13. checks/claims.py (S/nu6/harness/claims.py) will fail on v10: C6 requires the string `1.094$--$1.098`, C11 recomputes the removed extrapolation and requires `$1.099$`; defaults name neutrinos_v9.tex and read only res_L3_r125.json. It ships in the archive as "how this version was checked", so it needs a v10 copy (new file name, v9 copy left standing) whose C6/C11 check the measured level-3 numbers from both result files.
T14. The frozen code/A6/RUNLOG.txt stops at line 17 (first r=0.8 run); the archive needs the full 31-line log. Built files (flat_v9.tex, neutrinos_v9.html, raw_v9.html, PDF) are regenerated, not hand-edited; all new outputs under v10 names, v9 files left standing.
T15. sec_new_mcc l.11 (C15) is a judgment call; if the author prefers to keep "the rate $1.11$" there, the honest form is "the first-level rate".

## 5. Archive and appendix additions; figures

Add to code/A6/ of the v10 source (copies from S/nu6/A6_refine2/):
- res_L3_r08.json (new result)
- RUNLOG.txt (full, 31 lines; replaces the truncated copy in the v10 tree only)
- PREREGISTERED.txt with the appended r=0.8 result block (after T10 is settled); the frozen v9 copy stays as it is
- level3_rates.py and level3_rates_out.txt (every new number in C3-C11, C14, C18 comes from these; rerun reproduces the stored output)
- oddrate.py is byte-identical to code_v6/A1_oddrate.py (already listed in B.19); richardson.py only if a Richardson number is printed
- optional: log_L3_r08.txt, log_L3_r125.txt (per-run lines; the same lines are in RUNLOG.txt)
B.27 listings to add after l.73 of app_new_evidence.tex: `\lstinputlisting{code/A6/res_L3_r08.json}`, `code/A6/level3_rates.py`, `code/A6/level3_rates_out.txt`.
README: no new line needed beyond C17 (l.13 already covers code/A6/).
Figures: none needs redrawing. No figure plots the second or third level. Figure fig:link needs only the caption word (T3), unless the author chooses the redraw.
