# Review ledger: v8 to v9 (13 November 2026)

This is a working record, not part of the paper. It covers the independent audit of v8 and how each item was settled.

## How v9 was checked

1. **Vote.** Three independent voters, each a different model (Opus, Sonnet, Fable 5.2), worked from the same dossier (`harness/VOTE_DOSSIER.md`).
   - None of them saw my proposed fixes or each other's votes.
   - Each one recomputed the numbers before voting.
   - The votes are in `harness/votes/vote_A.md`, `vote_B.md` and `vote_C.md`.
2. **Claim harness.** `harness/claims.py` recomputes every disputed number from the archived data, then checks that the paper says it.
   - The archived data are the raw Gramian json, the A6 result files, the moment chain, the bin generators and the profile nodes.
   - The harness also fails on any phrase from a known slip.
   - v8 fails 8 of its 12 checks; v9 passes all 12.
3. **Diff guard.** `harness/guard.py` lists every sentence changed from v8 to v9, and each one must map to an item below.
   - The output is `harness/DIFF_REPORT.md`.
   - 20 change blocks, 0 unregistered.
4. **Watcher.** A separate Fable 5.2 agent, not one of the voters, read the vote record, the diff, the harness output and the build, looking for new slips.
5. **Build checks.**
   - pdfLaTeX run twice: 0 errors, 125 pages, all 26 fonts Type 1.
   - HTML rendered in a headless browser with MathJax 3.2.2: 1550 maths elements, 0 errors.
   - Fresh Lean build and full audit, logged in `lean_build_v9.log`.

## Votes and changes

| Item | Votes (A Opus / B Sonnet / C Fable) | v9 text | Check (harness) |
|---|---|---|---|
| I1 Headline wording | AMEND / AMEND / AMEND | 1.11 ± 0.01 kept (author's decision). Abstract and Summary call ±0.01 a finite-resolution budget, not a converged value or statistical interval, and give the conditional extrapolation 1.094–1.098 beside it. §5 says the −0.0082 shift "fails" the 0.005 line, and that the bracket excludes only an error purely first order in cell size, not second order in space, first order in time, or a mix | C6: bracket [0.50994187, 0.50995437]; predictions 0.50996706 (out), 0.50995033, 0.50994197 (in); ratio 0.415 (0.332–0.498) |
| I2 Left/right sentence | ACCEPT ×3 | "merges into the continuous spectrum"; the normalised left–right overlap K^(−1/2) = sin2φ/2φ falls to zero and the spectral projector becomes infinitely ill-conditioned | C3: on the 400-moment chain, the true left eigenvector's overlap = 1/√K = sin2φ/2φ to 1e−6 at κ = 2, 1, 0.8, 0.7 |
| I3 Snapshot Gramian | ACCEPT ×3 | "factor of ten" replaced. ε_dec = 0.5 snapshot ratio 4.8e−17, about 80 above e^−42, where the integrated ratio is 4e9 above. ε_dec = 2 snapshot 1.4e−13 against the same e^−42. "Where it was measured" removed (B, C: it was also measured at ε_dec = 2) | C2b: raw json 4.801e−17 (/e^−42 = 83.5), 1.38e−13; integrated 4.30e9 above. Both exponents are exactly 42 (coupled/transition: 128/3 − 2/3) |
| I4 Profile share | AMEND / ACCEPT / AMEND | "about half of the profile weight (0.51 on the 36 nodes used here, 0.48 by direct integration)" | C4: wall 1.504822881; nodes 0.5135; integral 0.4785 |
| I5 "Exact" closure, stale "untested" | ACCEPT / AMEND / ACCEPT | Tight coupling: the closure "loses almost nothing", with the hidden difference returning at 10^−9 or less when planted at ≤ ¼ ε_dec. Threshold effect "measured for matched, planted perturbations" (§ door); realistic initial data untested | witness table: coupled rows ≤ 6e−10 |
| I6 Rapidity ruler | AMEND ×3 | "of the rulers tested" (abstract, §5, Summary); "the linear kept state at readout does not hold the difference"; "written in the nonlinear collapse" removed | text only |
| I7 Scalar summaries | AMEND / ACCEPT / ACCEPT | Names the three matched summaries; says they "do not fix the linear readout or the memory form"; Summary: "agree in integrated opacity and integrated connection energy" | C7 forbidden phrases |
| I8 Positivity window | AMEND ×3 | [3/4, 3/2] and [0.6, 1.2] called the conservative continuum windows; exact 32-bin windows [0.725, 1.55] and [0.56, 1.24] stated. No run changes side | C5: bin generators scanned: [0.7250, 1.5500], [0.5600, 1.2413] |
| I9a Abstract G | ACCEPT / AMEND / ACCEPT (B's AMEND gives the same wording) | 0.777 | C1: 0.7766 |
| I9b A.13 target | ACCEPT / AMEND / ACCEPT (same wording) | "per-group default target" | C7 |
| I10 Archive | ACCEPT / AMEND / ACCEPT | A5 imports fixed to A5_chain_lib. Absolute scratch paths in 5 drivers replaced by `NU_WORK` / `NU_UPSTREAM` environment paths. Raw Gramian outputs shipped (`results/A5_raw/`). McCormick's MIT licence shipped (`paper/LICENSE-McCormick`), so the sentence at line 460 is now true. Author licences at top level. Full Lean build and audit log | py_compile of the changed drivers; A5 import check; `lean_build_v9.log` |
| I12 Citations | not voted (the audit's check) | Romatschke: EPJC 76 (2016) 352. Hu: SciPost Phys. 20 (2026) 020 | Romatschke volume and number are from the audit's link to the article. Hu's journal reference is confirmed by a search hit on SciPost's own page for this article |

## Slips caught by the process (not by the audit)

- My first harness check of the left eigenvector used the wrong pairing (the transpose instead of the conjugate transpose) and reported overlap 1. Fixed before use; the check now matches 1/√K.
- My first harness exponent for the squared survival factor was 42.67. The Gramian ratio is coupled over transition, so the exponent is 128/3 − 2/3 = 42 exactly; the paper's e^−42 was right.
- README: "Version 8" was left in the first line by a partial replace. Fixed.
- Voters B and C: "where it was measured" in the Gramian sentence was also wrong (snapshot stored for ε_dec = 2 as well).

## Watcher findings (Fable 5.2, first pass) and what was done

| Finding | Done |
|---|---|
| F9 Lean audit covered 84 theorems; `Neutrinos.SelfScatter` was missing from the audit config | Added to `scripts/config.json` (87 expected) and reran: 87 theorems, only the three standard axioms, 11 false controls rejected for a mathematical reason. Appendix C now states this build and audit |
| F1 §6 still had the unqualified "which is why the threshold is a law in the operator's link rapidity" | Now "so its eigenprojector cannot serve as a ruler there; of the rulers tested, …". New harness check C9 requires the qualifier on every such sentence |
| F2 the printed A5 preregistration still says 10^1.1 | Record kept as written; the appendix line before it gives the true 10^1.92. New check C10 scans every listed file |
| F3 "10^−9 or less" overreached beyond the witness table | Now "… in the table above" |
| F4 the ε_dec = 2 snapshot had no factor | Now "2×10^5 above the same e^−42" (computed 2.40e5) |
| F5 Summary "set before, it is erased" (from v8) | Now "set deep in the coupled era, it is erased" |
| F6 two tally rows were wrong in this ledger | Corrected from the vote files |
| F7 check C8 could not fail | Now asserts the computed values and their presence in the text |
| F8 harness blind spots | Added C9 (item 6 scope), C10 (printed listings) and C11 (third-level and extrapolated rates recomputed) |
| F10 Appendix C counts from older commits | Rewritten for the current build and audit |
| F11–F13 `__pycache__`, `checks/` undocumented, scratch paths in `wb_checks` logs | Caches removed; README documents `checks/`; log paths now read `$NU_WORK/a_wb` |

## Watcher second pass

All thirteen first-pass fixes were confirmed true; the harness gives 12/12 on v9 and 8/12 failed on v8; the guard finds 0 unregistered changes. Two new slips, both fixed:
- S1: Lean commit 9292b2c was local only. Pushed with this version.
- S2: Appendix C's "also replayed" implied the present audit replays proofs in a kernel checker. "also" removed.

Watcher notes on harness reach: C9 catches the known phrasings of the rapidity claim, and C10 the two known strings in listings. The watcher read the text for rewordings and found none.

## Open

- The r = 0.8 third-level threshold is still running.
- From voter A, not voted: the abstract's erasure factor exp[−ε_dec^n/(nτ_s^n)] is checked against the witness table quantitatively only for n = 3 (0.5 to 1) and for n = 6 at 0.5. Left as written.
- McCormick's paper section and equation numbers are still unchecked (not in his repository).
- Mixer: the package still carries "The Standard Model in the Ball". Its fit for this paper is the author's call.
