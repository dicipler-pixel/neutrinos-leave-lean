# Watcher report: v9 of "What the Neutrino State Must Keep"

**Verdict: SLIPS FOUND.** Two fixes did not land everywhere (F1, F2), one new sentence overreaches the table it rests on (F3), the Lean audit in the log left out one module and the log is not in the package (F9), the ledger's vote tally is wrong in two rows (F6), and one harness check can never fail (F7). Every number in the changed sentences recomputes correctly.

Written 13 November 2026, 07:45 CST. No file other than this one was edited. No web use.

Paths are relative to `<session>/`. "PK" is `out_v9/When_the_Neutrinos_Leave_v9_package`.

---

## Findings in the paper text

### F1. Item 6 did not land in the related-work paragraph (medium)
- **File:** `nu6/paper_v9/neutrinos_v9.tex`, line 285.
- **What is wrong:** the sentence still says, with no qualifier and as a cause, "...the kept sector has no isolated eigenvalue for about half of the profile, **which is why the threshold is a law in the operator's link rapidity and not in the displacement of a kept state**." All three voters amended this claim to "of the rulers tested / among the coordinates compared". The abstract, line 257 and the Summary were changed; this one was not. It is in the PDF and the HTML.
- **Evidence:** `grep -n "which is why the threshold is a law" neutrinos_v9.tex` gives line 285. `grep -c` on the flattened PDF text and on the HTML gives 1 each.
- **Minimal fix:** end the sentence "...for about half of the profile; of the rulers tested, the threshold follows the operator's link rapidity and not the displacement of the linear kept state."
- **Why the harness missed it:** Item 6 is "text only" in the ledger, and C7 has no phrase for it.

### F2. The "within 10^1.1" line is still printed in the paper (medium)
- **File:** `nu6/paper_v9/code_v6/A5_PREREGISTERED.txt`, line 106, printed by `app_new_evidence.tex` line 50 (`\lstinputlisting`).
- **What is wrong:** the appendix prints "Terminal Gramian ratio 4.8e-17 (n=3) is within 10^1.1 of the survival factor." The body now says a factor of about 80, which is 10^1.92. The audit named this line, and voters A and B both said it is wrong. The paper now contradicts itself between Section 6 and its own appendix.
- **Evidence:** `grep -rn "10^1.1" nu6/paper_v9` hits `code_v6/A5_PREREGISTERED.txt:106`, `flat_v9.tex:5577`, `neutrinos_v9.html:8096`. Flattened PDF text: 1 hit. Arithmetic: 4.801e-17 / e^-42 = 83.5, log10 = 1.92.
- **Minimal fix:** leave the record line as written and append one dated line under it in the same file, in the way results are appended elsewhere: "Correction, 13 November 2026: 4.8e-17 / e^-42 = 83.5 = 10^1.92, not 10^1.1; inside the 10^(+-3) kill line of P2b." Then rebuild.
- **Why the harness missed it:** C2b tests the string `10^{1.1}` in the `.tex` parts only. Files pulled in by `\lstinputlisting` are never read.

### F3. New sentence at line 181 claims more than its table (medium)
- **File:** `nu6/paper_v9/neutrinos_v9.tex`, line 181 ("Reading").
- **What is wrong:** "planted at a quarter of the decoupling time or earlier, the hidden difference returns at 10^-9 or less" is true for the witness table (history eps_dec = 0.5; largest entry in the 0.25 row is 6e-10). It is stated without that scope. For McCormick's history (eps_dec = 2, planting at eps_s = 0.5, also a quarter) the paper's own new number in Section 6 gives a larger return.
- **Evidence (inference from the paper's numbers, not a new run):** snapshot ratio for eps_dec = 2 is 1.38e-13 (raw json, harness C2b). Its square root, 3.7e-7, is the amplitude ratio against planting at decoupling; times a decoupling return of about 0.08 this is about 3e-8, thirty times above 10^-9. The same arithmetic on eps_dec = 0.5 reproduces the table: sqrt(4.80e-17) x 0.081 = 5.6e-10 against the table's 6e-10, so the method is calibrated.
- **Minimal fix:** "...loses almost nothing: in the table above, planted at a quarter of the decoupling time or earlier, the hidden difference returns at 10^-9 or less."

### F4. Item 3 sentence: the eps_dec = 2 clause gives no factor (low)
- **File:** `nu6/paper_v9/sec_new_gramian.tex`, line 11, last sentence.
- **What is wrong:** the sentence opens "comes far closer to the survival factor", gives "about 80 above" for eps_dec = 0.5, then for eps_dec = 2 gives only "1.4e-13, against the same e^-42". That is 2.4e5 above e^-42. The sentence is true (the integrated ratio is 5.4e11 above), but a reader takes the second case as agreement of the same kind. Voter A's wording was that this history "carries the same leak".
- **Evidence:** harness C2b output: `eps_dec=2 1.38e-13 (/e^-42 = 2.40e+05)`.
- **Minimal fix:** "...and for the eps_dec = 2 history it is 1.4e-13, a factor of 2e5 above the same e^-42."
- **Related, no change needed:** `sec_new_door.tex` line 28, "where the linear survival factor gives 5e-10", is right as arithmetic (exp(-64/3) = 5.4e-10). The linear chain itself gives about 4e-7 for that history, still far below the 0.3 to 0.5 per cent in the text.

### F5. Summary still says "set before, it is erased" (low, wording carried over from v8)
- **File:** `nu6/paper_v9/neutrinos_v9.tex`, line 293.
- **What is wrong:** same kind of absolute as the "exact" of Item 5. The witness table has planting at half the decoupling time returning 8.6e-3 and 7.9e-3, marked on. The abstract says "set deep in the coupled era", which is right.
- **Minimal fix:** "set deep in the coupled era, it is erased."

### Changed sentences that are clean
Checked against data, vote majority, grammar and the rest of the paper:
- **Item 0** version line.
- **Item 1** abstract, line 236, line 240, Summary. Recomputed with the `oddrate.py` formula: level rates 1.1102 and 1.1020, shift -0.0082; third-level rate 1.0986 ("1.099"); extrapolation 1.0939 to 1.0979 over the factor range 0.33 to 0.50 ("1.094 to 1.098"); bracket [0.50994187, 0.50995437]; predictions 0.50996706 out, 0.50995033 and 0.50994197 in.
- **Item 2** lines 71 and 75. sin(2 phi) = 0 at phi = pi/2; overlap = 1/sqrt(K) on the 400-moment chain to 1e-6.
- **Item 4** line 257: wall 1.5048, 0.5135 on nodes, 0.4785 by integration.
- **Item 6** abstract, line 257, Summary.
- **Item 7** Section 6 and Summary. `A5_kinetic/t1_order_out.txt`: pairs R1, R2, R3, R5, R6 have all three summaries matched and still differ by 43 to 57 per cent in readout.
- **Item 8** line 192. Continuum windows rederived by hand: r - 3|r-1| >= 0 gives [3/4, 3/2]; shear alone gives [0.6, 1.2]. Bin windows [0.7250, 1.5500] and [0.5600, 1.2413]. The edge 0.20 in `sec_new_mcc.tex` line 11 is (1/2) ln 1.5, consistent.
- **Item 9a** 0.7766, matches the table's 0.777.
- **Item 9b** A.13 wording. The two remaining "common-frame" uses (`sec_new_mcc.tex` lines 21 and 26) describe runs that really used that target.
- **Item 12** citations: format only. I could not confirm the Hu journal reference offline.

No stale hit remains in the `.tex` parts, README or Zenodo text for: "exact only", "every scalar summary", "No scalar summary", "leaves the spectrum", "before it leaves", "non-orthogonal to its own left eigenvector", "factor of ten", "51%", "0.776", "set by grid resolution", "in the nonlinear collapse" as a claim, "version 8". The one "0.776" in the PDF is `G=0.7765` in a printed run log, which is correct.

Remaining "untested" uses are all current: radial grid against time step (236), the r = 0.8 extrapolation (240), start-time dependence (240), order pairs at the threshold (Section 6), realistic initial data (181), the solver channel candidate (door, 28).

One thing in unchanged v8 text, for the author: Section 6 line 15 says the memory form differs "by 0.06 to 0.16, at or past the 0.08 kill line". Three of the six pairs are below 0.08 (0.064, 0.063, 0.067).

---

## Findings in the ledger

### F6. Vote tally does not match the vote files in two rows (medium)
- **File:** `nu6/harness/REVIEW_LEDGER_v8_to_v9.md` (same file in `out_v9/`).
- **Evidence:** `grep -n -E '^## Item|^VOTE' votes/vote_*.md`.

| Item | Ledger (A / B / C) | Vote files (A / B / C) |
|---|---|---|
| I4 | ACCEPT / AMEND / AMEND | AMEND / ACCEPT / AMEND |
| I9a, I9b | ACCEPT x3 | ACCEPT / AMEND / ACCEPT |

- B's AMEND on Item 9 gives the same wording as the others, so the v9 text is unaffected.
- All other rows match: I1 AMEND x3; I2 ACCEPT x3; I3 ACCEPT x3; I5 ACCEPT/AMEND/ACCEPT; I6 AMEND x3; I7 AMEND/ACCEPT/ACCEPT; I8 AMEND x3; I10 ACCEPT/AMEND/ACCEPT.
- **Minimal fix:** correct the two rows.

The ledger's other counts hold: v8 fails 6 of 9 (rerun: C1, C2b, C3, C4, C5, C7 fail); 16 change blocks, 0 unregistered (guard rerun on a copy reproduces `DIFF_REPORT.md` byte for byte); 125 pages; 26 fonts, all Type 1.

---

## Findings in the harness

### F7. Check C8 can never fail (medium)
- **File:** `nu6/harness/claims.py`, check `C8 shifts r=1/4,4`.
- **What is wrong:** the pass condition is the literal `True`. It prints the numbers and compares nothing. "v9 passes all 9" is really 8 tests and one printout.
- **Evidence:** `check('C8 shifts r=1/4,4', ..., True, f'...')`. It also passes on v8.
- **Minimal fix:** condition `f'{G(d14)-0.4253:+.3f}'=='+0.188' and f'{G(d4)-0.4253:+.3f}'=='-0.173' and has('$+0.188$ and $-0.173$') and has('$-0.763$ and $+0.786$')`. The numbers themselves are right: +0.188, -0.173, -0.763, +0.786.

### F8. Weak spots that let F1 and F2 through (low to medium)
- **Listings are not read.** `tex_all()` loads only the main file and the `sec_new_*` / `app_new_*` parts. Anything printed through `\lstinputlisting` is invisible, so C7 and C2b pass while the PDF prints the slip (F2). Fix: also scan the files named in `\lstinputlisting{...}` for the forbidden phrases, with `10^1.1` added.
- **No check for Item 6.** Fix: add to C7 the phrases "which is why the threshold is a law", "written in the nonlinear collapse", "leaves the spectrum", "set by grid resolution".
- **C6 does not recompute the extrapolation.** It tests only that the strings `1.094$--$1.098` and `$0.42$` exist somewhere. `$0.42$` would match any 0.42. The rate 1.099 and the range 1.094 to 1.098 are never computed. I recomputed them and they are right.
- **C2a and C2b use bare substring tests** (`3\times10^{-7}`, `1.4\times10^{-13}`) that could be satisfied by another sentence. Fine today, fragile.
- **README and Zenodo text are not checked by anything.** I checked them by hand: version 9, 1.11 +- 0.01, 0.42, 1.094 to 1.098, 5.5e-3, 0.645k at 200 moments all match the paper.
- **`guard.py` tags by block.** A block is registered if any one sentence in it holds a registered snippet, so other changed sentences in the same block ride along. Its "unused" test is by item, not by snippet. Today this is harmless: all 21 snippets occur in v9 and I read every changed sentence. The guard does not cover the eight changed scripts, which the appendix prints.
- **C5 builds its own bin generator** instead of importing the solver's. It agrees with voter B's independent construction and with the dipole formula of A.13, so I accept it.
- **Checks that test what their "why" line says:** C1, C3, C4, C5.

---

## Findings in the package

### F9. Lean log: one module left out of the audit, and the log is not in the package (high for release)
- **State at 07:43 CST.** `nu6/harness/lean_build_v9.log` has 26 lines. `lake build` succeeded (8934 jobs, exit 0). The first audit ended `OK: 84 theorems, axioms used: ['Classical.choice', 'Quot.sound', 'propext'], 11 false controls rejected`, exit 0. A second `scripts/verify.py` run was in progress and had not written to the log.
- **What is wrong, 1:** the 84 leave out `Neutrinos.SelfScatter`. The config at commit 9cd71fa lists nine modules; the source has ten and 87 theorems. The three self-scattering theorems carry the paper's seventh claim. README says the log holds "axioms of every theorem"; for this log that is not yet true.
  - Evidence: `verification/report.json` has `theorems: 84` and no SelfScatter module; `grep -rhoE '^\s*(protected )?theorem ' PK/lean/Neutrinos | wc -l` gives 87; `git diff scripts/config.json` in `<lean-repo>` shows an uncommitted change adding the module and 87.
- **What is wrong, 2:** `PK/lean/scripts/config.json` is still the 84 version, so the package would repeat the gap.
- **What is wrong, 3 (changed while I was writing):** at 07:43 `PK/lean/` had no log. At 07:45 it holds `lean_build_v9.log` and a `verification/` folder, but both are the 84-theorem run: the log ends `OK: 84 theorems`, and `verification/report.json` has `theorems: 84` over nine modules. So the package now ships the audit that leaves SelfScatter out.
- **What is wrong, 4:** the log header says commit 9cd71fa, but the rerun uses a config that is not in that commit.
- **Minimal fix:** when the rerun ends, confirm it says `OK: 87 theorems` with the same three axioms and 11 controls. Then replace in `PK/lean/` the log, `scripts/config.json` and the `verification/` folder with the 87-theorem versions, and add one line to the log saying `config.json` differs from the commit (or commit it first).
- **False controls (from the first run; they do not depend on the config):** all 11 rejected, each for a mathematical reason, read from `verification/*.log`:
  - linarith failed: CrossLinkFactor, MemoryGapFactor, MemoryWallNoBox.
  - Type mismatch on the stated value (k^2/2 for k^2/3; -5/1369 for 0; wrong sign; missing -kappa_1): EnergyCoefficient, EnergyDerivative, PropagatorSign, SplitRateSecondLink.
  - Unsolved goal `False`: KillLineTestB, KillLineTestD, ResponseDerivative, ResponseValue.
- **Axioms (first run):** 84 of 84 inside {propext, Classical.choice, Quot.sound}.

### F10. Appendix C counts do not match what ships (low, v8 text)
- **File:** `nu6/paper_v9/neutrinos_v9.tex`, line 513.
- **What is wrong:** it cites builds at commits d181d6d and c372d3f, "all 100 theorems" and "all twelve false controls". The shipped tree and log are commit 9cd71fa, 87 theorems, 11 false controls. Unchanged from v8, but v9 now ships a log beside it that shows different counts.
- **Minimal fix:** one sentence naming the v9 build (commit, 87 theorems, 11 controls), or reconcile the counts.

### F11. Compiled caches with scratch paths are in the package (low)
- **Where:** `PK/paper/code_v6/__pycache__/` (7 files) and `PK/paper/code/main/__pycache__/` (1 file). The same two folders are in `nu6/paper_v9/`.
- **Evidence:** `find PK -name '*.pyc'`; `grep -rl /tmp/claude PK` lists `A5_chain_lib.cpython-313.pyc`.
- **Minimal fix:** delete both `__pycache__` folders before zipping.

### F12. `checks/` folder is not self-contained (low)
- `guard.py` defaults to `../paper_v8`, which is not in the package, so it fails as shipped.
- `VOTE_DOSSIER.md` carries the scratch paths.
- `DIFF_REPORT.md` is not shipped.
- README does not mention `checks/` at all.
- `claims.py` does run from the package: 9 checks, 0 failed.
- **Minimal fix:** a README line for `checks/` saying the guard needs the v8 source, and ship `DIFF_REPORT.md`.

### F13. Two scratch paths are printed in the paper's appendix (low, carried over from v8)
- **Where:** `PK/paper/code/wb_checks/wb_steve_03_out.txt` (RuntimeWarning lines), printed through the listing, so they appear in the PDF and HTML. v8 had seven such lines, v9 has two. Also in `wb_steve_05_out.txt`, `report.md`, `report_head.md`.
- These are output logs, not `.py` or `.js`, so the Item 10 repair as voted is complete.

### Package checks that passed
- All 101 `.py` files parse.
- No `/tmp`, `/home/claude`, `/mnt` or `/root` in any `.py`, `.js`, `.sh`, `.toml` or `.json`.
- The five path edits use `NU_WORK` / `NU_UPSTREAM`, and `os` is imported in each.
- `A5_t1_order.py`, `A5_t2_gramian.py`, `A5_t3_closures.py` import `A5_chain_lib`, which exists and imports cleanly; every name they use resolves.
- `results/A5_raw/` holds `t2_gramian.json` (identical to `nu6/A5_kinetic/`), `t2_gramian_out.txt` and 12 `G_*.npy`.
- `LICENSE` (MIT), `LICENSE-CC-BY-4.0.md` and `LICENSING.md` are present.
- `paper/LICENSE-McCormick` is byte-identical to the `LICENSE` in the local McCormick checkout at eb7c4de, so the sentence at line 460 is true.
- `PK/paper` matches `nu6/paper_v9` apart from build products.
- The PDF and HTML in the package, in `out_v9/` and from the build are the same bytes.
- README and Zenodo text say version 9; the two Zenodo copies are identical.

---

## Fix list, in order
1. F9: finish the 87-theorem audit; ship the log, updated config and report in `PK/lean/`.
2. F1: line 285.
3. F2: correction line in `A5_PREREGISTERED.txt`.
4. F3: "in the table above" at line 181.
5. F6: two ledger rows.
6. F7 and F8: make C8 a real test; scan listings; add the Item 6 phrases.
7. F4, F5, F10, F11, F12: small wording and package tidy.
