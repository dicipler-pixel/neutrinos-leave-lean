# What the Neutrino State Must Keep (version 6 of *When the Neutrinos Leave*)

Jeromie Beasley, 11 November 2026.

- `What_the_Neutrino_State_Must_Keep_v6_2026-11-11.pdf` — paper, proofs (A.1–A.15), evidence (B.1–B.25: every script, preregistration and run log), Lean statements. One PDF, Type 1 fonts.
- `What_the_Neutrino_State_Must_Keep_v6_2026-11-11.html` — the same content as one HTML page, figures embedded.
- `neutrinos_v6.tex` with `sec_new_gramian.tex`, `sec_new_door.tex`, `sec_new_mcc.tex`, `app_new_proofs.tex`, `app_new_evidence.tex` — LaTeX source (`pdflatex` three times from this folder).
- `code/`, `results/` — the version 5.1 scripts and outputs listed in Appendix B.1–B.18; `code_v6/` — the version 6 scripts, diffs, preregistrations and logs listed in B.19–B.25; `figs/` — every figure, `make_figs_v6.py` draws figures 8–11.
- `swarm/` — the brief and, for each of the seven runs (A1–A6), the preregistration written before the run and the final report.

New in version 6: the readout Gramian of the hidden moments (no kernel; spectrum ranks what a reduced state must keep), the matched-restart test in McCormick's full collapse (hidden structure planted at decoupling moves the threshold by up to 5.5e-3), McCormick's multigroup collision term as the split flux–shear link, and the stage-correct reruns behind the odd rate 1.11 ± 0.01.

Open at the time of this record: the third refinement level (A6, N = 900, N_mu = 72) is still running; `Neutrinos/SelfScatter.lean` is stated but not yet compiled in this session.

AI-assisted: the ideas and research direction are the author's; AI tools (Claude, Anthropic) were used for literature search, computation, drafting and typesetting.
