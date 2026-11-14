# What the Neutrino State Must Keep — version 9

Jeromie Beasley, 13 November 2026. Version 9 of *When the Neutrinos Leave*.

## Contents

- `What_the_Neutrino_State_Must_Keep_v9_2026-11-13.pdf`: the paper, with proofs, scripts and run logs in the appendices.
- `What_the_Neutrino_State_Must_Keep_v9_2026-11-13.html`: the same paper as a web page.
- `ZENODO_DESCRIPTION_v9.txt`: the record description.
- `paper/`: LaTeX source (`neutrinos_v9.tex` with its `sec_new_*` and `app_new_*` parts), figures, and every script, preregistration and run log the appendices print (`code/`, `code_v6/`, `results/`).
  - `code/v7/onset_exact.py` checks the kept-sector pole and its non-orthogonality against the moment chain.
  - `code/v7/fig_onset.py` draws Figure 2.
  - `code/A6/` holds the third resolution level.
  - `results/A5_raw/` holds the raw readout-Gramian outputs (`t2_gramian.json`, `G_*.npy`) behind the Gramian section.
- `lean/`: the Lean 4 / Mathlib sources (`Neutrinos/`, `FalseControls/`, the lake files), the axiom check, `lean_build_v9.log` (commit, toolchain and Mathlib pins, the `lake build` result of 8934 jobs with no `sorry`, and the summary of the audit by `scripts/verify.py`), and `verification/`, the audit's own output: the axioms of each of the 87 theorems, the false-control logs and the file hashes (`report.json`). `lean_build_v9_first_84.log` is the first run, before the self-scattering module was added to the audit.
  - The maintained repository is https://github.com/dicipler-pixel/neutrinos-leave-lean.
- `mixer/`: the interactive explorer page.
- `checks/`: how this version was checked. `claims.py` recomputes every disputed number from the archived data and checks the paper's text (`python3 claims.py`). `guard.py` maps every sentence changed from version 8 to a ledger item (it needs the version 8 source: set `NU_OLD`). `render.js` renders the HTML maths. `VOTE_DOSSIER.md` and `votes/` hold the independent vote. `REVIEW_LEDGER_v8_to_v9.md` and `WATCHER_REPORT*.md` hold the record.
- `LICENSING.md`, `LICENSE` (MIT, the code and proofs) and `LICENSE-CC-BY-4.0.md` (the written text), as in the repository. `paper/LICENSE-McCormick`: the MIT licence of S. McCormick's code, which covers the copied and changed solver files.

## Reproducing

- **Paper.** Compile `paper/neutrinos_v9.tex` with pdfLaTeX, twice.
- **Scripts.** Drivers read their working directory from the environment variable `NU_WORK` and McCormick's checkout from `NU_UPSTREAM` (both default to the current directory).
- **Collapse runs.** These use S. McCormick's public code (https://github.com/quasilocal/PBH_neutrino_simulation, commit eb7c4de). The copied and changed files and the drivers are listed in Appendix B.
- **Lean.** Run `lake build` in a checkout of the repository.

AI-assisted: the ideas and research direction are the author's; AI tools (Claude, Anthropic) were used for literature search, computation, drafting and typesetting.
