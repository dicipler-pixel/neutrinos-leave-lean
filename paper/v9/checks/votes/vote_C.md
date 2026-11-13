# Voter C: votes on v8 of "What the Neutrino State Must Keep"

Check scripts (all run, outputs quoted below):
`harness/work_C/chk.py` (items 2, 3, 4), `harness/work_C/chk1.py` (items 1, 8, 9a).
Run as `python3 harness/work_C/chk.py` and `python3 harness/work_C/chk1.py` from `nu6/`.

---

## Item 1
VOTE: AMEND

CHECK:
Why this decides it: the wording question is whether "1.11 ± 0.01" is a converged value with a margin, or a band that the finer levels are walking out of. Recomputing the level rates and the conditional third level from the stored thresholds shows which.
```
python3 harness/work_C/chk1.py
R1 1.1102107016966025 R2 1.1019781493907503 s12 -0.008232552305852181
inner 1.2 pair 1.1066158324544884 diff 0.0035948692421141626
shift ratio 0.4150617611908473 range 0.3320494089529728 0.4980741134287219
conditional R3 1.0985816370527144 s23 -0.0033965123380359508
 geometric factor 0.333 -> R_inf 1.0969
 geometric factor 0.415 -> R_inf 1.0962
 geometric factor 0.444 -> R_inf 1.0959
 geometric factor 0.500 -> R_inf 1.0952
fluid ref shift effect -0.003848741724912008
quadrature 0.009728309205612249 linear 0.0156
```
Also read: A6_refine2/PREREGISTERED.txt (kill line was "shift does not shrink", |R3 - R2| > 0.00823; the 0.005 line belongs to the earlier v6 refinement and was failed by -0.0082), res_L3_r125.json (bracket [0.50994187, 0.50995437], width 1.25e-5, a recorded deviation from the 1e-6 tolerance), prog_L3_r08.json (only the two end points done: bracket still [0.51155643, 0.51195643]).

REASON:
- Every number in the paragraph reproduces (1.1102, 1.1020, -0.0082, 0.0036, 0.0097/0.016, 0.42 with range 0.33-0.50, conditional third-level rate 1.099). My central extrapolation is 1.095-1.097; the text's 1.094-1.098 is a little wider and contains it, so it stands.
- The body text (line 240) is already mostly honest: it says the shift exceeded the 0.005 line and that the ±0.01 is "the error budget itself ... not a margin around a converged number". The audit is right on three points of wording only:
  1. The abstract and Summary say "the ±0.01 is now set by grid resolution", which reads as a converged number with a resolution-sized error bar. The two finished levels are 1.110 and 1.102, the trend is monotone downward, and the conditional third level (1.099) and its extrapolation (1.094-1.098) sit below the band's lower edge. The band must be named as a finite-resolution estimate wherever it is headlined, with the conditional extrapolation and its one assumption beside it.
  2. "larger than the line of 0.005 set before the run" should say plainly that the line was failed.
  3. "the bracket excludes first order in space" is too wide: what is excluded is an error purely first order in the cell size. A mixed error (first-order spatial part plus a faster-shrinking time part) is not excluded by one threshold at three levels.
- The number itself stays, per the author's decision.

TEXT:
Abstract, replace "at a rate of $1.11\pm0.01$ inside the window where the split operator is a Markov generator; with the collision rate evaluated at every Runge--Kutta stage the two inner pairs agree to $0.004$, and the $\pm0.01$ is now set by grid resolution; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step." with:

> at a rate of $1.11\pm0.01$ inside the window where the split operator is a Markov generator. This is an estimate at finite resolution, and the $\pm0.01$ is a resolution budget, not a statistical interval: with the collision rate evaluated at every Runge--Kutta stage the two inner pairs agree to $0.004$, one joint refinement of the grid lowers the rate by $0.008$, and a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step; if the $r=0.8$ threshold, whose third-level run is not finished, shrinks by the same factor, the rate extrapolates to $1.094$--$1.098$.

Line 240, replace "a shift of $-0.0082$, larger than the line of $0.005$ set before the run." with:

> a shift of $-0.0082$, which fails the line of $0.005$ set before the run.

Line 240, replace "So the bracket excludes first order in space but does not separate second order in space from first order in time" with:

> So the bracket excludes an error that is purely first order in the cell size; it does not separate second order in space from first order in time, and it does not exclude a mixture of the two

Line 240, replace "just below the band; the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation is untested." with:

> just below the band, which would then be an upper estimate of the continuum rate; the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation rests on that one assumption and is untested.

Summary (line 293), replace "and the rate is a measured number, $1.11\pm0.01$ with the error now set by grid resolution, with no closed form attached." with:

> and the rate is a measured number at finite resolution, $1.11\pm0.01$, the $\pm0.01$ being a resolution budget and the finer grids so far moving it down, toward $1.094$--$1.098$ if the unfinished third-level run follows the finished one, with no closed form attached.

All other sentences of the paragraph: unchanged.

---

## Item 2
VOTE: ACCEPT

CHECK:
Why this decides it: the operator is complex symmetric, so the left eigenvector is the complex conjugate of the right one. Computing both from the truncated chain and taking their Hermitian overlap shows directly whether the overlap grows or shrinks as K diverges.
```
python3 harness/work_C/chk.py   (400 moments, k = 1; left vector from eig of A^H, right from eig of A)
kap=2.000 s=-0.169512  herm overlap=0.841471  1/ov^2=1.4123    K=1.4123    exact=1.4123    resid l=conj(r): 5.1e-16
kap=1.000 s=-0.357907  herm overlap=0.454649  1/ov^2=4.8378    K=4.8378    exact=4.8378    resid l=conj(r): 2.4e-15
kap=0.800 s=-0.467727  herm overlap=0.239389  1/ov^2=17.4499   K=17.4499   exact=17.4499   resid l=conj(r): 3.6e-15
kap=0.700 s=-0.556808  herm overlap=0.098220  1/ov^2=103.6567  K=103.6567  exact=103.6567  resid l=conj(r): 5.9e-14
kap=0.660 s=-0.604298  herm overlap=0.036650  1/ov^2=744.4859  K=744.4859  exact=744.4859  resid l=conj(r): 7.2e-13
kap=0.645 s=-0.624589  herm overlap=0.013157  1/ov^2=5776.6241 K=5776.6241 exact=5774.1733 resid l=conj(r): 4.7e-12
```
K = 1/overlap^2 to every digit shown; the normalised left-right overlap falls from 0.84 to 0.013 as the onset is approached. Pole position: s = k cot(k/kappa) - kappa equals -kappa at phi = pi/2, the centre of the cut, which is in the continuous spectrum.

REASON: The formula and its divergence are right; the gloss is reversed. As K diverges the mode becomes orthogonal to its own left eigenvector (overlap = 1/sqrt K -> 0); what grows without bound is the norm of its spectral projector, sqrt K. And the eigenvalue does not leave the spectrum: it arrives at s = -kappa, a point of the continuous spectrum, and stops being an isolated eigenvalue. "Its non-orthogonality diverges" in the abstract and Summary is the standard name for K and stays.

TEXT:
Line 71, replace "at its centre $s=-\kappa$, and leaves the spectrum:" with:

> at its centre $s=-\kappa$, and merges into the continuous spectrum:

Line 75, replace "the kept mode becomes infinitely non-orthogonal to its own left eigenvector before it leaves." with:

> the overlap of the kept mode with its own left eigenvector, $1/\sqrt K$ for unit vectors, falls to zero, and its spectral projector grows without bound, as it meets the cut.

---

## Item 3
VOTE: ACCEPT

CHECK:
Why this decides it: the sentence is a statement about one ratio of two stored numbers against one exponential. Reading the terminal eigenvalues from the raw JSON and dividing settles it.
```
python3 harness/work_C/chk.py
ed0.5_n3_s0.125 terminal top 1.1291885609510952e-17 integral top 1.693721819472602e-09
ed0.5_n3_s0.5   terminal top 0.23518053560683314    integral top 0.6844607882382296
n 3 terminal ratio 4.8013691185687e-17 integral ratio 2.4745344782016856e-09
    sq surv rel 5.74952226429356e-19 (= e^-42.0)   term/rel 83.50900992916915  log10 1.9217
ed2 terminal ratio 1.3818817441358698e-13 sq surv 5.74952226429356e-19 ratio 240347  (integral ratio 3.08e-07)
```
Squared survival factor between the two plant epochs: exp[-2(0.5^3/3)(1/0.125^3 - 1/0.5^3)] = e^-42.0 = 5.75e-19, as the paper uses. t2_gramian_out.txt lines 6 and 15 give the same terminal tops (1.129e-17, 2.352e-01).

REASON: The audit is right: the snapshot ratio is 83.5 times the squared survival factor, 10^1.92, not within ten. The point of the sentence survives and is strong: the time-integrated Gramian sits 4e9 above the survival factor (2.5e-9 against 5.7e-19), the snapshot only 84 above. Two further things the raw file shows: (i) "where it was measured" is not the whole record, since the terminal Gramian was also stored for the eps_dec = 2 history, and there the snapshot ratio is 1.4e-13, 2.4e5 above e^-42; (ii) the n = 3, eps_dec = 0.5 integral ratio 2.5e-9 in the same sentence is confirmed. REPORT.md line 86 ("within a factor of about 10") carries the same error and should be corrected in the archive copy.

TEXT:
sec_new_gramian.tex line 11, replace the last clause "the snapshot Gramian at the end of the horizon, which is the witness of Section~\ref{sec:witness}, follows the survival factor to within a factor of ten for the $\epsilon_{\rm dec}=0.5$ history, where it was measured." with:

> the snapshot Gramian at the end of the horizon, which is the witness of Section~\ref{sec:witness}, follows the survival factor far more closely: for the $\epsilon_{\rm dec}=0.5$ history its ratio is $4.8\times10^{-17}$, a factor of $84$ above $e^{-42}$ where the integrated Gramian is $4\times10^{9}$ above; for the $\epsilon_{\rm dec}=2$ history it is $1.4\times10^{-13}$.

---

## Item 4
VOTE: AMEND

CHECK:
Why this decides it: the figure is a sum of profile weights below one wall; computing it on the 36 nodes and by direct integration shows how much of "51%" is the node spacing.
```
python3 harness/work_C/chk.py
wall 1.5048228810695108
36-node below wall 0.5135215356394718 nodes near wall [1.43348487 1.70249459]
integral 0.4785156539223116 on [0,inf) 0.4806425763072802
```

REASON: The text is true as worded ("on the 36 nodes used here" gives 0.5135), so it is not an error, but the audit is right that the second digit is a node effect: the wall falls between nodes at 1.433 and 1.702, and the integral itself gives 48%. "For the other half" and line 285's "about half of the profile" are both fine. Report both numbers, once.

TEXT:
Line 257, replace "which carries $51\%$ of the profile weight on the $36$ nodes used here; for the other half" with:

> which carries about half of the profile weight ($51\%$ on the $36$ nodes used here, $48\%$ by direct integration); for the other half

---

## Item 5
VOTE: ACCEPT

CHECK:
Why this decides it: "exact" is decided by whether the witness table has zeros in the coupled rows, and "untested" by whether a later section of the same paper tests it.
- Witness table (neutrinos_v8.tex, Section witness): coupled-era entries are 7e-15, 5e-19, 8e-24, 5e-31 at tau_s/eps_dec = 0.1 and 6e-10, 6e-11, 2e-15, 7e-20 at 0.25. Small, graded with the survival factor, not zero. (The n = 3, 0.25 entry squared against the 1 entry squared is (6e-10/0.081)^2 = 5.5e-17, matching the snapshot Gramian ratio 4.8e-17 of Item 3.)
- sec_new_door.tex: eight thresholds measured in the full collapse; decoupling differences 3.744e-3, -2.098e-3, 5.505e-3; coupled era 1.75e-5 and 1.85e-5; and its own Reading paragraph says the perturbation is "an engineered sensitivity, at half each cell's positivity margin, on one profile" and that cosmological initial data are a separate question.
- The door section also states the coupled era "is not perfectly shut" in the full solver (0.3-0.5% of the decoupling effect).

REASON: Both audit points hold. Tight coupling suppresses the hidden structure by the survival factor, it does not make the closure exact; and the full solver has a small coupled-era channel besides. "How far it moves the nonlinear threshold" is no longer untested for matched engineered perturbations: Section door measures it. What remains untested is whether realistic initial data carry such structure.

TEXT:
Line 181, replace the first sentence "A closure on density, flux and stress is exact only for structure set while the neutrinos are tightly coupled." with:

> A closure on density, flux and stress loses nothing that can be read later only for structure set while the neutrinos are tightly coupled, where the survival factor suppresses it to $10^{-10}$ and below.

Line 181, replace the last sentence "Whether realistic initial data carry such structure, and how far it moves the nonlinear threshold, are untested: the memory curves of Section~\ref{sec:memory} start with the hidden moments empty." with:

> How far such structure moves the nonlinear threshold is measured for matched, engineered perturbations in Section~\ref{sec:door}. Whether realistic initial data carry it is untested: the memory curves of Section~\ref{sec:memory} start with the hidden moments empty.

Middle sentences: unchanged.

---

## Item 6
VOTE: AMEND

CHECK:
Why this decides it: the claim's reach is set by what was compared. Reading line 257 against its own numbers shows which rulers were tested and at which epoch.
- Rulers tested: (1) the link rapidity; (2) the principal angle of the linear kept-sector trajectory at the first compaction maximum. A third, the eigenprojector of the least-damped mode, was not tested because it does not exist over about half the profile (Item 4 check: wall k = 1.5048, 48-51% below).
- Numbers quoted for the comparison: slopes differ 5% vs 6%, odd rates spread 36% vs 3.4%, residuals 0.13 vs 0.014, readout angles 0.0475 vs 0.0467 against an 8% threshold difference. I did not rerun the chain for these; the vote does not turn on their values but on what they can support.

REASON: The comparison made is sound and the author's conclusion from it is right as far as it goes: of the two rulers tested, the offsets are linear in the rapidity and not in the state angle, and the linear kept state at readout does not separate the two collision models. Two steps go beyond it. (a) "The law lives in the rapidity" as a bare statement covers every state-based coordinate; one state distance at one epoch was tested. (b) "The difference between the models is written after the readout epoch, in the nonlinear collapse" is a statement about where and when the difference is made; what is shown is only that the linear kept-sector state at readout does not hold it. It could sit in the hidden moments at readout (which the paper's own door section shows the threshold reads), not only in later nonlinear evolution. The paragraph heading and the framing stay.

TEXT:
Line 257, replace the final sentence "So the law is a law in the operator's own link rapidity, and not in the displacement of the linear kept state: the difference between the two collision models is written after the readout epoch, in the nonlinear collapse" with:

> So, of the rulers tested, the law is a law in the operator's own link rapidity, and not in the displacement of the linear kept state: at the readout epoch that state does not hold the difference between the two collision models, which must be carried by what it leaves out, the hidden moments and the nonlinear collapse

Abstract, replace "the law lives in the operator's link rapidity, and the difference between the models is written in the nonlinear collapse." with:

> of the two rulers tested the law lives in the operator's link rapidity, and the linear kept state at readout does not hold the difference between the models.

Summary (line 293), replace "the law lives in the collision operator's own link rapidity, not in the displacement of the linear kept state;" with:

> of the two rulers tested, the law lives in the collision operator's own link rapidity, not in the displacement of the linear kept state;

---

## Item 7
VOTE: ACCEPT

CHECK:
Why this decides it: "every scalar summary" is a universal; it is decided by listing what the test actually held equal and what it read.
- A5_kinetic/PREREGISTERED.txt, Test 1: three summaries are named and held equal: P1a optical depth, P1b time-integrated connection energy, P1c the instantaneous operator at readout (equal only "whenever W closes before e*": R1, R2, R3, R5, R6 at both epochs, R4 only at e* = 4). The readout P1d is the linear l <= 2 readout and the memory form g. No threshold was run.
- sec_new_gramian.tex line 15 itself ends "Whether the threshold itself separates such a pair is untested", which contradicts "can carry what the threshold reads" one sentence earlier.
- Family S (n = 3 against n = 6) matches optical depth only; its connection energies differ by construction.

REASON: Three named summaries were matched, not every scalar summary (a scalar that weights the rate by time, for one, is not order-blind and was not tried). And what they fail to carry is the linear readout and the memory form, not the threshold. The finding itself, that order is part of the record, stands untouched.

TEXT:
sec_new_gramian.tex line 15, replace "No scalar summary of the history, whether opacity, integrated connection energy or the operator at readout, can carry what the threshold reads; the order is part of the record." with:

> None of these three summaries of the history, the integrated opacity, the integrated connection energy or the operator at readout, carries what the linear readout holds; the order is part of the record.

(The next sentence, "Whether the threshold itself separates such a pair is untested.", unchanged.)

Summary (line 293), replace "collision histories that agree in every scalar summary still differ in the memory." with:

> collision histories that agree in integrated opacity, integrated connection energy and the operator at readout still differ in the memory.

---

## Item 8
VOTE: AMEND

CHECK:
Why this decides it: a Markov generator needs every off-diagonal entry nonnegative; on midpoint bins those entries are known in closed form, so the exact window is the root of their minimum over i != j, at each bin count used in the paper.
```
python3 harness/work_C/chk1.py
(all l>=2: N x offdiag = r + (r-1) mu_i mu_j/<mu^2>;  shear alone: 1 + (1-r) p2_i p2_j/<p2^2>, p2 = mu^2 - <mu^2>)
32   all: 0.7250 1.5500   shear: 0.5600 1.2413
48   all: 0.7337 1.5326   shear: 0.5739 1.2266
72   all: 0.7393 1.5214   shear: 0.5829 1.2174
4000 all: 0.7498 1.5004   shear: 0.5997 1.2003
```
An independent build of the operator from Gram-Schmidt projectors on the 32 bins, scanned in r at step 0.0005, gave the same windows: (0.725, 1.55) and (0.56, 1.241) (harness/work_C/chk.py).
Continuum by hand: all l >= 2 kernel r + 3(r-1) mu mu' >= 0 on the square gives [3/4, 3/2]; shear alone 1 + 5(1-r) P2 P2' with P2 in [-1/2, 1] gives [0.6, 1.2].

REASON: The audit is right for the all-l window and the same holds for the shear-alone window: on the 32 bins the exact windows are [0.725, 1.55] and [0.56, 1.24]; the quoted [3/4, 3/2] and [0.6, 1.2] are the continuum windows. So "on the angle bins ... only for" is wrong as a statement about the bins, though wrong on the safe side. The bin windows close onto the continuum ones as the bins are refined (48 and 72 bins are used in the refinement runs), so the continuum window is the right one to state, labelled as such. No verdict changes: 1.2, 1/1.2, 1.25, 0.8 are inside every window at every bin count; r = 1/2, 2 and the extreme pairs are outside every one; the shear-only pair 1.2, 1/1.2 is inside (1.2 is the continuum edge itself, inside on the bins). The "upper edge 0.20" in sec_new_mcc.tex (rapidity (1/2) ln 1.5 = 0.203) stays correct for the continuum window.

TEXT:
Line 192, replace "On the angle bins the split collision operator is a Markov generator only for $\tfrac34\le r\le\tfrac32$ (all moments $\ell\ge2$ at $\kappa_2$) and $0.6\le r\le1.2$ (shear alone at $\kappa_2$); outside those windows it has a negative off-diagonal entry and can, in principle, drive a nonnegative intensity negative." with:

> In the continuum the split collision operator is a Markov generator only for $\tfrac34\le r\le\tfrac32$ (all moments $\ell\ge2$ at $\kappa_2$) and $0.6\le r\le1.2$ (shear alone at $\kappa_2$). On the angle bins the windows are slightly wider, $0.725\le r\le1.55$ and $0.56\le r\le1.24$ on $32$ bins, and close onto the continuum ones as the bins are refined, so the continuum windows are the ones used here; outside the bin windows the operator has a negative off-diagonal entry and can, in principle, drive a nonnegative intensity negative.

Rest of the paragraph: unchanged.

---

## Item 9
VOTE: ACCEPT (both parts)

CHECK:
Why this decides it: (a) is one division; (b) is whether the appendix names the same target as the main text.
```
python3 harness/work_C/chk1.py
G(1/16) 0.7765609676364814 G(16) 0.1288983327884939
```
(a) (0.521485 - 0.49773)/(0.52832 - 0.49773) = 0.77656, which rounds to 0.777, the table's value (line 203). The abstract's 0.776 is a truncation. 0.129 is right.
(b) app_new_proofs.tex line 2 defines c "chosen so that c mu carries the group's flux", which is the per-group default target; sec_new_mcc.tex line 9 says the identity is for "this default target ... which keeps each group's own flux" and that the boosted common-frame option "is outside the identity". The appendix's label "common-frame target" names the option the main text excludes.

REASON: Both are leftovers of edits made in the main text and table but not carried to the abstract and the appendix.

TEXT:
(a) Abstract (line 22): "$G$ runs from $0.776$ to $0.129$" becomes

> $G$ runs from $0.777$ to $0.129$

(b) app_new_proofs.tex line 2: "The dipole coefficient of the common-frame target is $c=q/(2\pi\sum_k\mu_k^2\Delta\mu)$" becomes

> The dipole coefficient of the per-group default target is $c=q/(2\pi\sum_k\mu_k^2\Delta\mu)$

---

## Item 10
VOTE: ACCEPT (four must be fixed before release; the Lean log is a should)

CHECK:
Why this decides it: each complaint is a fact about the files; listing them settles it. No v8 zip is present in the nu6 scratch tree, so these checks are on the paper_v8 source directory the zip is built from; the zip itself was not inspected.
```
grep -rn chain_lib paper_v8/code_v6 --include=*.py
  A5_t2_gramian.py:5, A5_t3_closures.py:6, A5_t1_order.py:5:  from chain_lib import *
cmp A5_kinetic/chain_lib.py paper_v8/code_v6/A5_chain_lib.py   -> same (byte-identical)
grep -rn "/tmp/|/home/|/root/|/mnt/" code code_v6 --include=*.py --include=*.sh
  code/main/make_figures_v3.py:13, code/main/make_fig6_door.py:6,
  code_v6/A2_step2_algebra.py:15, code_v6/A2_step3_predict.py:8, code_v6/A2b_gate_operator.py:10
find paper_v8 -iname "*licen*"          -> nothing
neutrinos_v8.tex:460: "MIT licence, copyright S. McCormick; the licence file ships with the archive"
find paper_v8 -name "t2_gramian*" -o -name "G_*.npy"  -> nothing;  du A5_kinetic/G_*.npy t2_gramian.json t2_gramian_out.txt -> 488K total
find paper_v8 -iname "*.lean" -o -iname "*lean*log*"  -> nothing (paper_v8/build.log is the pdfTeX log)
```

REASON and what to do (none of this reruns the collapse code):
1. chain_lib import: MUST. The three A5 scripts fail at line 5 as packaged. Ship the library under the name the scripts import: add `code_v6/chain_lib.py` as a byte copy of `A5_chain_lib.py` (keep the A5-prefixed file if the appendix lists it). Do not edit the import lines, so the listed scripts stay the ones that ran.
2. Raw Gramian outputs: MUST. Item 3 was decided only from `t2_gramian.json` and `t2_gramian_out.txt`, and the paper's Gramian eigenvalues, the 2.5e-9 and the snapshot ratio all come from them. Add `t2_gramian.json`, `t2_gramian_out.txt` and the twelve `G_*.npy` (488K in all) from A5_kinetic, plus `t1_order.json`/`_out.txt` and the t2b/t2c outputs behind the same section. Correct REPORT.md line 86 if REPORT.md ships.
3. LICENSE: MUST. The paper says the licence file ships, and the MIT terms require the copyright and permission notice to go with every copy of ms_nuc.py and the files derived from it. Add McCormick's LICENSE file verbatim from his repository at the cited commit, next to the changed solvers, and name it in the README.
4. Absolute scratch paths: MUST for the five files above, by the smallest change: one line at the top of each replacing the scratch prefix with a path relative to the script (or one environment variable, default the archive root), and a README line saying which inputs each expects and that McCormick's `src/simulation` must be fetched from his repository for the A2 scripts. Say in the README that only the path lines differ from the files as run. Scratch paths inside stored logs and `_out.txt` records (code/wb_checks) are records of what ran and stay as they are.
5. Lean build log: SHOULD, not a blocker. The claim in Appendix C (commit d181d6d, 8934 jobs, no sorry, standard axioms) is checkable by anyone from the public repository, so the release does not depend on the log. But a two-line log does not show it; replace it with the full `lake build` output for that commit plus the `#print axioms` output for the three self-scattering theorems, with the Lean and Mathlib versions at the top. This is a Lean rebuild, not a collapse run. If that cannot be done before release, the paper's sentence stays as it is and the README says the log is a summary.

TEXT: Paper text unchanged, provided the LICENSE file is added (line 460 then becomes true as written). If the LICENSE file is not added, line 460 must lose "the licence file ships with the archive".
