# Review ledger: v9 to v10 (13 November 2026)

A working record, not part of the paper.

## Why v10

v9 was closed while the r = 0.8 threshold on the third (finest) resolution level was still running, so it gave the third-level rate only as a conditional extrapolation. The run finished. v10 states the measurement and removes what it made out of date. Nothing else in the paper changed.

## The result

| Level | r = 1.25 threshold | r = 0.8 threshold | Odd rate |
|---|---|---|---|
| 1 | 0.50984158 | 0.51169233 | 1.1102 |
| 2 | 0.50991687 | 0.51175643 | 1.1020 |
| 3 | 0.5099481 ± 0.0000063 | 0.5117877 ± 0.0000063 | 1.1013 (1.0938 to 1.1088 over the bracket corners) |

- Change in the rate: −0.0082 from level 1 to 2, −0.0007 from level 2 to 3.
- Kill line written before the runs (a change larger than the previous one): passed, at the midpoints and at every corner.
- Extrapolation fixed before the runs: fitted order 6.2, outside its trusted range of 0.5 to 4. By the preregistration's own rule the value is marked untrustworthy, so the paper quotes none.
- The thresholds exclude an error purely first order in cell size (both), and at r = 0.8 one purely first order in the time step. Second order in cell size fits both.
- Headline: 1.10 ± 0.01 (was 1.11 ± 0.01, held only until this run landed).

## How the change was made

1. v9 was frozen as the "before" copy.
2. A watcher (a Fable 5.2 agent) recomputed every number from the run files and wrote its own list of sentences to change, without seeing mine (`WATCHER_CUTLIST.md`).
3. I wrote my list before reading the watcher's (`SURGEON_CUTLIST.md`).
4. The lists agreed on what to cut. The watcher's wording was more minimal, so it was used throughout, with one amendment at the headline equation.
5. After the cuts the watcher checked the result twice more (`WATCHER_REPORT_v10.md`).

## The cuts (watcher's numbering)

| Cut | Where | Change |
|---|---|---|
| C1 | date line | version 10 |
| C2, C13 | abstract, Summary | 1.11 ± 0.01 becomes 1.10 ± 0.01 |
| C3 | abstract | the conditional extrapolation becomes the measurement: shifts shrink to 0.42 and 0.49; 1.101 against 1.102; bracket range 1.094–1.109 |
| C4–C6 | §link, headline equation | "every central inner value lies in" becomes the two finer levels and the finest bracket range; equation 1.10 ± 0.01; first-level values near its upper edge, one 0.0002 above |
| C7–C10 | §link, third level | r = 0.8 threshold, factor and predictions stated beside r = 1.25; conclusion updated for the time-step exclusion |
| C11 | §link | the "if r = 0.8 shrinks alike … still in progress … untested" sentence becomes the measured rate, its range, the kill line, why no extrapolation is quoted, and the budget (0.0091 in quadrature, 0.015 linear) |
| C12 | Figure caption | "the first-level inner-pair rate 1.11" (the figure is drawn from first-level data; not redrawn) |
| C14 | Summary | the measurement replaces the conditional |
| C15 | McCormick section | "the window where the rate was measured" (number dropped) |
| C16 | Appendix B.27 | intro updated; new listings: `res_L3_r08.json`, `level3_rates.py` and output, `richardson.py` and output |
| C17, C18 | README, Zenodo description | version 10; the same statement of the rate |

Stays, on purpose: the first-level table and "1.10–1.11"; "the frozen law at rate 1.11" (what that test was computed with); the Lean bracket statement; every "untested" unrelated to this run.

## Slips the watcher caught, and what was done

| Slip | Done |
|---|---|
| Comma splice at the headline equation (in its own proposed wording); "at its upper edge" loose for 1.1066 | semicolon; "sit near its upper edge" |
| I corrected a wrong timestamp in the appended preregistration result by rewriting the block, against that file's no-edit rule | disclosed in an appended note; the first 4675 bytes of the file are unchanged |
| The preregistered error parts of the extrapolation were not reported; `richardson.py` was not in the archive | reported in the appended note (0.041, 0.001); script and output shipped and listed |
| My note described the four-corner picture, not the eight combinations `richardson.py` takes; "written before the runs" was loose | a second appended note states both exactly |
| Harness could pass with some text wrong | C11 now asserts the conclusion sentence, the kill-line clause, "its sign is not resolved", the upper-edge clause and the count of remaining 1.11 mentions; recomputes 0.0038 and 0.0036; reads README and Zenodo text |
| `guard.py` did not run from inside the package; `check_same_text.py` usage not stated | guard defaults to `../paper`; README gives both commands |

## Final state

- Claim harness: 12 of 12 on v10, also when run from inside the package.
- Change guard: 13 changed passages, 0 unregistered.
- PDF: 131 pages, no errors, Type 1 fonts only.
- HTML (plain and art edition): 1,575 maths elements, 0 errors; the art edition's text equals the plain one; all 11 figures are unchanged from v9 (the art edition's are the same figures recoloured).
- Lean: untouched since v9 (87 theorems, standard axioms only, 11 false controls rejected).

## Open

- Figure 4's caption says "black dots"; in the art edition those dots are cream. The wording is unchanged pending the author's call.
- The legend inside the Figure 7 image reads "rate 1.11 (inner pairs)"; the caption now says first-level. A redraw at 1.10 is the alternative.
- The third-level change is known only to ±0.0075, because the level-3 brackets are 1.25e-5 wide.
- From v9: the abstract's erasure factor is checked against the witness table only at n = 3 (and one n = 6 point); McCormick's paper section and equation numbers are unchecked; the mixer is still "The Standard Model in the Ball".
