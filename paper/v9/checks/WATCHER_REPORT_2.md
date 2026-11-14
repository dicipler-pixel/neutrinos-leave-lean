# Watcher report, second pass: v9 of "What the Neutrino State Must Keep"

**Verdict: SLIPS FOUND (two, both small; no wrong number and no failed fix).** All thirteen first-pass findings landed and are true. What remains is one release step (S1: the Lean commit the paper cites is not pushed) and one word in the new Appendix C sentence (S2). Three low notes follow.

Written 13 November 2026. No file other than this one was edited. No web use. "PK" is `out_v9/When_the_Neutrinos_Leave_v9_package`.

## Reruns

| Command | Result |
|---|---|
| `python3 claims.py ../paper_v9 neutrinos_v9.tex` | 12 checks, 0 failed |
| `NU_OLD=../paper_v8 NU_NEW=../paper_v9 python3 guard.py` | 20 change blocks, 0 unregistered, 0 unused registrations |
| `cd PK/checks && python3 claims.py` | 12 checks, 0 failed |
| `claims.py` on v8 (ledger says 8 of 12 fail) | 8 failed: C1, C2b, C3, C4, C5, C7, C9, C10. Matches |

## New slips

### S1. The cited Lean commit 9292b2c exists only locally (medium, release step)
- **Where:** `neutrinos_v9.tex` line 513 and `lean_build_v9.log` both name commit `9292b2c`.
- **What is wrong:** the commit is not on GitHub yet. A reader following the paper's repository link will not find it.
- **Evidence:** `git status -sb` in `<lean-repo>` gives `claude/v6-what-the-state-must-keep...origin/claude/v6-what-the-state-must-keep [ahead 1]`; `git branch -r --contains 9292b2c` is empty.
- **Minimal fix:** push the commit before the paper is released. No text change.

### S2. "also replayed" in the new Appendix C sentence (low)
- **Where:** `neutrinos_v9.tex` line 513: "An earlier build at commit c372d3f (4 November 2026) **also** replayed every proof in an independent kernel checker."
- **What is wrong:** "also" says the present audit replayed the proofs in an independent kernel checker. It did not: `scripts/verify.py` runs the axiom audit, the inventory, the false controls and the hashes only.
- **Evidence:** `grep -c -i -E 'lean4checker|replay' PK/lean/scripts/verify.py` gives 0.
- **Minimal fix:** delete "also".
- I cannot check the c372d3f claim itself; it is carried over from v8.

## Low notes (no change required)

- **README, `lean/` line.** It says the log holds the axioms of every theorem and the file hashes. The log holds the summary line; the per-theorem axioms and hashes are in `lean/verification/report.json` and `axioms.log`, which now ship. The line does not mention `verification/` or `lean_build_v9_first_84.log`. One clause would cover it.
- **`PK/checks/WATCHER_REPORT.md`** still has one `<lean-repo>` path (line 110). `PK/checks/claims.py` contains the literal `/tmp/claude-0` only as the string C10 searches for. No other session path is left anywhere in the package.
- **This report** is not yet in `PK/checks/`; README refers to `WATCHER_REPORT*.md`.

## Can a new check pass while the text is wrong?

- **C8** is now a real test: four values computed and each required in the text. The text test is a bare substring (`+0.188` and so on), which is loose but adequate here.
- **C9** catches any sentence containing "law lives in the", "law is a law in the" or "is a law in the operator" without "rulers tested". It found 4 sentences, all qualified. A reworded claim ("the threshold follows the rapidity") would pass unseen. I read the whole text for such rewordings and found none.
- **C10** scans all 130 listed files, but only for two strings (`10^1.1` and the session path). It is a regression test for those two slips, not a general listing check. It does confirm the note is present when the record line is.
- **C11** recomputes the third-level rate and the extrapolation from the stored bracket: 1.0986, and 1.0939 to 1.0979. This agrees with my own first-pass computation.
- **guard.py** still tags by block, but every block now has one registered snippet per changed sentence group and I read all 20.

## Each first-pass fix, verified

| Finding | Landed | True |
|---|---|---|
| F1 line 285 | "so its eigenprojector cannot serve as a ruler there; of the rulers tested, ..." in tex, PDF and HTML; old phrase gone | Yes: the mode is absent above k = 1.50 for about half the profile weight |
| F2 A5 listing | Note before the listing in `app_new_evidence.tex`; record line untouched | 4.8e-17 / e^-42 = 83.5 = 10^1.92 |
| F3 line 181 | "... 10^-9 or less in the table above" | Table's 0.25 row tops out at 6e-10 |
| F4 Gramian sentence | "1.4e-13, 2e5 above the same e^-42" | Computed 2.40e5 |
| F5 Summary | "set deep in the coupled era, it is erased"; old phrase gone from tex, PDF, HTML | Consistent with the abstract and the table |
| F6 ledger tally | I4 AMEND / ACCEPT / AMEND; I9a and I9b ACCEPT / AMEND / ACCEPT | Matches the vote files |
| F7 C8 | Real assertions | See above |
| F8 harness | C9, C10, C11 added | See above |
| F9 Lean | Log: build 8934 jobs, exit 0; `OK: 87 theorems`, three standard axioms, 11 false controls rejected, exit 0. Package has the log, the 87 config, `verification/` at 87 with 3 SelfScatter theorems, and the earlier 84 log | Commit diff 9cd71fa to 9292b2c touches only `scripts/config.json`; package sources match the checkout; no theorem has an axiom outside the three; all 11 control logs show a mathematical failure |
| F10 Appendix C | "all 87 theorems of the library", "all eleven false controls"; "100 theorems" and "twelve" gone | Yes, apart from S1 and S2 |
| F11 caches | No `__pycache__` in the package or in `nu6/paper_v9` | |
| F12 `checks/` | README documents it; `DIFF_REPORT.md`, ledger and first watcher report shipped | |
| F13 log paths | `wb_checks` logs read `$NU_WORK/a_wb`; no session path in PDF or HTML | Ledger records the change |

## Other checks, second pass
- PDF: 125 pages, 26 fonts, all Type 1. No undefined references in the LaTeX log; `\ref{sec:gramian}` in the new note resolves.
- PDF and HTML in `out_v9/`, in the package and from the build are the same bytes; `PK/paper` matches `nu6/paper_v9` apart from build products.
- Zenodo text unchanged and now true on the Lean line (log ships; every false control fails).
- Ledger counts updated and correct: 12 checks, v8 fails 8, 20 change blocks.
- New sentences read cleanly; no correction narration entered the body (the A5 note sits in the appendix beside the record it describes).

## Still open, as the ledger says
- The r = 0.8 third-level run.
- The abstract's erasure factor, checked quantitatively only for part of the witness table (voter A's side note).
- The Hu journal reference, which I cannot confirm offline.
