# When the Neutrinos Leave, v6 — shared brief for every agent

Author: Jeromie Beasley (byline: "Jeromie Beasley", first and last name only). His paper builds on
S. McCormick, "Free-streaming neutrinos raise the threshold for primordial black hole formation" (2026).
Talk about his work directly, as the work itself.

## Where things are (all local; never re-download)
- His latest paper, v5.1 (read the parts your task touches, in full):
  `S/nu51/zip/When_the_Neutrinos_Leave_v5_1/paper/neutrinos_leave_v5_1.tex`
  code: `.../paper/code/` (v4_runs/ms_nuc_split.py, ms_nuc_shear.py, run_split_v2.py, trisect_*.py,
  PREREGISTERED_V4.txt, log_*.txt; witness/; main/; wb_checks/), Lean: `.../lean/Neutrinos/*.lean`
- McCormick's current solver (commit eb7c4de, v1.1): `S/steve/src/` (simulation/*.py, README.md).
  v5.1 pinned upstream commit 41a0f83; the split solvers are copies of that era's ms_nuc.py.
- McCormick's new paper text (the 20-page PDF): `/mnt/user-data/attachments/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/98e6e69c-paper_2.pdf`
- Independent audit of both papers (11 Nov 2026), text: `S/nuaudit/audit.txt` (lines 92-400 = verdict,
  corrections and proposed tests; 1070-1450 = his corpus and the v5.1 review's qualifications).

S = /tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad

## What v5.1 established (his results; build on them, do not rebuild them)
- Collision operator as a cut: (1/8)||[L,L*]||^2 = k^2 k1^2/3 + (4k^2/15)(k2-k1)^2; sqrt(E_B) = k/sqrt3.
- Flux-shear link: with flux at k1 and shear+higher at k2 = r k1, eleven thresholds; offset
  tau_G = ln[(1-G)/G] moves ~linearly in the link rapidity (1/2) ln r, odd rate 1.11 +- 0.01 inside the
  admissible window 3/4 <= r <= 3/2; shear-only damping gives 1.19-1.20.
  References: delta_fluid = 0.49773, delta_inst = 0.52832, R_nu = 0.409, eps_dec = 2, n = 3, N=400, Nmu=32.
- Memory form, matched-pair witness (hidden l=3,4 structure planted at/after decoupling returns into
  l=0,1,2 by several per cent), kept-population speed limit dA^2 <= 4 E_B A(1-A).

## What the audit says needs doing (the reason for v6)
1. In the v5.1 runners the collision rate kappa(t) is computed once per SSPRK3 step and reused at the
   intermediate stages, so the collision history is first order. Re-evaluate kappa at each stage time and
   reconverge the inner pairs before keeping +-0.01.
2. McCormick's new model (App. C, Eq. C3) has plasma drag kappa_e on the dipole and neutrino
   self-scattering kappa_nu on the quadrupole and above: D = diag(0, k_e, k_e + k_nu, ...). This is exactly
   his split link with k1 = k_e, k2 = k_e + k_nu, so (1/8)||[H,H*]||^2 = k^2 (k_e^2/3 + 4 k_nu^2/15).
3. Instrument McCormick's multigroup solver (positive common-frame target, nnmode=1) and apply his
   two-cut quantities without refitting.
4. Causal test: matched states at a restart surface with equal l <= 2 moments and different l >= 3,
   evolved through the same GR system; does the collapse bracket move?

## House rules (his, binding)
- Every script carries a line `# SCRIPT: NAME` inside the file.
- Before any run that decides something, write the prediction and the kill condition into a
  `PREREGISTERED.txt` in your folder, with a timestamp; append results under it after the run, never
  edit what was written before.
- Try the opposite before calling anything dead. A setup error is reported as a setup error.
- Never overwrite an original file: copy McCormick's or his files into your folder and change the copy.
- Do not state a claim you have not checked; say "untested" otherwise.
- CPU: this machine has 2 cores and 7 GB. Run at most ONE simulation process at a time per agent.
  Numba caches compile; first run is slow.
- No web access needed. Do not touch Google Drive or push to GitHub.
- Write all outputs in your own folder. Finish with `REPORT.md` there: what was run, every number,
  verdicts against the pre-registered kill lines, file list. Return that report as your final message.
