# Vote dossier: v8 of "What the Neutrino State Must Keep" (Jeromie Beasley)

An outside audit of v8 raised the items below. You are one of three independent voters. For EACH item, vote:

- ACCEPT: the audit is right and the text must change (give the corrected wording, kept close to the author's own wording and length);
- DEFEND: the current text is right as it stands (say why, with a check);
- AMEND: the audit is partly right (give the corrected wording).

Rules:
- Check things yourself from the files; do not take the audit or the current text on trust. Where a number is involved, recompute it (python3 with numpy/scipy is available) and show the line you ran and its output.
- Before each check, say in one line why that check would decide the item.
- Do not use the web. Do not edit any file outside your own output file.
- Change only what is wrong: keep the author's wording, framing and length wherever they are correct. No hedging boilerplate, no "the original said" narration: the paper must read as one complete thought.
- Write your votes to the output file named in your instructions, one section per item, as:
  `## Item N` / `VOTE: ACCEPT|DEFEND|AMEND` / `CHECK:` (what you ran, output) / `REASON:` / `TEXT:` (replacement wording, or "unchanged").

Source (read-only): <session>/nu6/paper_v8/
- main file neutrinos_v8.tex (line numbers below), sections sec_new_*.tex, appendices app_new_*.tex
- code in code/, code_v6/, code/A6/; raw Gramian outputs in ../A5_kinetic/ (t2_gramian.json, t2_gramian_out.txt, G_*.npy, PREREGISTERED.txt)
- A6 third-level runs: ../A6_refine2/ (res_L3_r125.json, prog_L3_r08.json, RUNLOG.txt, PREREGISTERED.txt, oddrate.py)

## Item 1: the headline rate 1.11 ± 0.01
Text: abstract (line 22) and §5 (line 240, "The error the brackets do not show" and the A6 third-level paragraph), Summary (line 293).
Audit: the number is a finite-resolution empirical estimate, not a converged constant or a statistical confidence interval; the v6 refinement shift −0.0082 failed its preregistered 0.005 line; the conditional extrapolation 1.094–1.098 belongs beside the headline with its assumption stated; the coupled refinement excludes the pure first-order spatial prediction, not all mixed-error models.
Note: the author has decided to keep 1.11 ± 0.01 as the headline until the r = 0.8 third-level run (still running) lands. Vote on the WORDING around it, not on replacing the number.

## Item 2: K and the left/right eigenvector sentence
Text: line 71 ("... at its centre s = −κ, and leaves the spectrum") and line 75 ("the kept mode becomes infinitely non-orthogonal to its own left eigenvector before it leaves").
Audit: for unit left/right vectors K = 1/|<l,r>|^2, so the overlap tends to zero: the sentence is reversed. Say the spectral projector becomes ill-conditioned / the normalised left–right overlap tends to zero, and that the isolated eigenvalue merges into the continuous spectrum rather than "leaves the spectrum".
Check: the operator is complex symmetric (bilinear pairing). Compute on a truncated chain (code/v7/onset_exact.py) what K is and how the Hermitian overlap |<l,r>|/(|l||r|) behaves near the onset.

## Item 3: the snapshot Gramian "within a factor of ten"
Text: sec_new_gramian.tex line 11, last sentence ("the snapshot Gramian at the end of the horizon ... follows the survival factor to within a factor of ten for the ε_dec = 0.5 history, where it was measured").
Audit: A5 PREREGISTERED gives terminal ratio 4.8e−17; divided by e^−42 that is 83.5, not ≤ 10; the log's "within 10^1.1" is also inconsistent. Resolve from the raw outputs or remove.
Check: ../A5_kinetic/t2_gramian.json holds the terminal Gramian top eigenvalues per run (key "terminal"). The survival factor is exp[−ε_dec^n/(n τ_s^n)] (abstract), squared for a Gramian.

## Item 4: 51% of the profile weight
Text: line 257 ("... which carries 51% of the profile weight on the 36 nodes used here; for the other half ...").
Audit: 51% is a coarse-node result. Wall k = 1.504822881 at κ = 0.958; the 36 nodes give 0.5135; direct integration of k^2 exp(−k^2/2) on [0.25, 9] below the wall gives 0.4785. Use "about half" or report both.

## Item 5: "exact only for structure set while tightly coupled"; "untested"
Text: line 181 ("Reading" paragraph of the witness section).
Audit: the witness table has nonzero residuals; tight coupling strongly suppresses, does not make a closure exact. The same paragraph says the nonlinear threshold effect is "untested", which is stale given the later restart section (sec_new_door.tex). Distinguish tested matched perturbations from realistic initial conditions.

## Item 6: the rapidity "law lives in" claims
Text: line 257 (end: "So the law is a law in the operator's own link rapidity ... written after the readout epoch, in the nonlinear collapse"), abstract ("the law lives in the operator's link rapidity, and the difference between the models is written in the nonlinear collapse"), Summary.
Audit: the tested state/projector rulers fail and the offsets are near-linear in rapidity; that does not prove every state-based coordinate fails or that the difference is causally generated only after the readout. Keep it as the comparison actually made.

## Item 7: "every scalar summary" / "No scalar summary"
Text: Summary ("collision histories that agree in every scalar summary still differ in the memory"); sec_new_gramian.tex line 15 ("No scalar summary of the history, whether opacity, integrated connection energy or the operator at readout, can carry what the threshold reads").
Audit: replace with the specified summaries (integrated opacity, integrated connection energy, the matched end-point operator where applicable); the order test is on linear readouts, and the paper itself says the threshold comparison for reversed histories is untested.

## Item 8: the positivity window [3/4, 3/2]
Text: line 192 ("Markov generator only for 3/4 ≤ r ≤ 3/2 ... and 0.6 ≤ r ≤ 1.2 (shear alone)").
Audit: on the 32 midpoint bins the off-diagonal entries have sign r + (r−1) μ_i μ_j/<μ^2>; the exact nonnegative interval is [0.725, 1.55]; [0.75, 1.5] is the continuum window. Label it as the conservative continuum window. (Also check the shear-alone window 0.6–1.2 the same way.)

## Item 9: two incomplete v8 edits
(a) Abstract (line 22) has "G runs from 0.776 to 0.129"; the table gives r = 1/16 as (0.521485 − 0.49773)/0.03059.
(b) Appendix A.13 (app_new_proofs.tex line 2): "The dipole coefficient of the common-frame target is c = ..."; the main text (sec_new_mcc.tex line 9) says the identity is for the per-group default target, and the boosted common-frame option is outside it.

## Item 10: archive repairs
Audit: A5 scripts import chain_lib but the package has A5_chain_lib.py; several drivers carry absolute scratch paths; raw Gramian outputs absent from the zip; the paper says an MIT licence ships but no LICENSE file is in the zip; the Lean build log is two lines. Vote on which of these must be fixed before release and how (no new runs of the collapse code).
