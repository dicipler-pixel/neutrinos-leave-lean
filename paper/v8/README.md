# What the Neutrino State Must Keep — version 8

Jeromie Beasley, 13 November 2026. Version 8 of *When the Neutrinos Leave*.

## Contents

- `What_the_Neutrino_State_Must_Keep_v8_2026-11-13.pdf`: the paper, with proofs, scripts and run logs in the appendices.
- `What_the_Neutrino_State_Must_Keep_v8_2026-11-13.html`: the same paper as a web page.
- `ZENODO_DESCRIPTION_v8.txt`: the record description.
- `paper/`: LaTeX source (`neutrinos_v8.tex` with its `sec_new_*` and `app_new_*` parts), figures, and every script, preregistration and run log the appendices print (`code/`, `code_v6/`, `results/`).
  - `code/v7/onset_exact.py` checks the kept-sector pole and its non-orthogonality against the moment chain.
  - `code/v7/fig_onset.py` draws Figure 2.
  - `code/A6/` holds the third resolution level.
- `lean/`: the Lean 4 / Mathlib sources (`Neutrinos/`, `FalseControls/`, the lake files), the axiom check, and the build result (8934 jobs, no `sorry`).
  - The maintained repository is https://github.com/dicipler-pixel/neutrinos-leave-lean.
- `mixer/`: the interactive explorer page.

## Reproducing

- **Paper.** Compile `paper/neutrinos_v8.tex` with pdfLaTeX, twice.
- **Collapse runs.** These use S. McCormick's public code (https://github.com/quasilocal/PBH_neutrino_simulation, commit eb7c4de). The copied and changed files and the drivers are listed in Appendix B.
- **Lean.** Run `lake build` in a checkout of the repository.

AI-assisted: the ideas and research direction are the author's; AI tools (Claude, Anthropic) were used for literature search, computation, drafting and typesetting.
