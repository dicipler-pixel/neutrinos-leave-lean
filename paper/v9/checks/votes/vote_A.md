# Votes of Voter A on v8 of "What the Neutrino State Must Keep"

Scripts used are in harness/work_A/ (item1.py, item2.py, item8.py); the rest were one-line python3 calls, quoted below.

## Item 1
VOTE: AMEND

CHECK:
Why this decides it: if the A6 brackets and the stated levels reproduce the 0.42 factor, the 1.099 / 1.094–1.098 figures and the three predictions, then the numbers are right and only the framing is in question. I can then also see which error models the bracket actually rules out.
Ran `python3 work_A/item1.py`, which uses oddrate.py's tau and rate on A1's L1/L2 values and A6's res_L3_r125.json bracket [0.50994187, 0.50995437]:
```
shift23 3.125e-05  ratio 0.4151  (bracket ends 0.3320, 0.4981)
R1,R2 1.11021 1.10198
f 0.415 R3 1.0986 Rinf 1.0962
f 0.332 R3 1.0993 Rinf 1.0979
f 0.498 R3 1.0979 Rinf 1.0939
model 4/9 (2nd order space): R3 1.0983 Rinf 1.0954
model 1/3 (1st order time):  R3 1.0992 Rinf 1.0979
pred p1 0.50996706  p2 0.50995033  t1 0.50994197
budget quad 0.00973, linear 0.0156
```
prog_L3_r08.json shows only two runs, the two ends of the r = 0.8 bracket (0.51155643 dispersed, 0.51195643 BH). No r = 0.8 third-level threshold exists yet. A6 PREREGISTERED: p = 1 is excluded, and the kill line |R3 − R2| > 0.00823 can't be judged until r = 0.8 lands.

REASON: Every number in the text reproduces: 0.42 (0.33–0.50), the three predicted thresholds, 1.099 and 1.094–1.098, and the 0.0097/0.016 budget. The audit's framing points are right, though.
(i) The abstract presents ±0.01 as if it were a margin. It is a finite-resolution budget, and §5 already says so. The abstract and Summary should say it too.
(ii) Under the shrink-factor assumption, the conditional third-level rate (1.099) and the extrapolation (1.094–1.098) both fall below the band. That belongs beside the headline, with its assumption stated.
(iii) A mixed first-order error, part from the cell size (factor 2/3 per level) and part from the time step (1/3), gives any factor between 1/3 and 2/3. 0.42 is in that range. So the bracket excludes only a pure first-order spatial error.
(iv) "Untested" for the extrapolation should read "conditional": the run exists and is in progress.
The −0.0082 failure of the preregistered 0.005 line is already stated in §5 ("larger than the line of 0.005 set before the run"), so it needs no change. The 1.11 ± 0.01 headline is kept, as the author decided.

TEXT:
- Abstract: replace "and the $\pm0.01$ is now set by grid resolution; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step." with:
  "and the $\pm0.01$ is a finite-resolution error budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step, and if the $r=0.8$ threshold shrinks alike the rate extrapolates to $1.094$--$1.098$."
- §5 ("The error the brackets do not show"): replace "So the bracket excludes first order in space but does not separate second order in space from first order in time" with:
  "So the bracket excludes a pure first-order error in the cell size, but does not separate second order in space from first order in time, or from a mix of first-order spatial and temporal errors"
  and replace "the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation is untested." with:
  "the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation is conditional on it."
- Summary: replace "and the rate is a measured number, $1.11\pm0.01$ with the error now set by grid resolution, with no closed form attached." with:
  "and the rate is a measured number, $1.11\pm0.01$, a finite-resolution budget rather than a converged value (extrapolated $1.094$--$1.098$ if the $r=0.8$ threshold converges as the $r=1.25$ one does), with no closed form attached."

## Item 2
VOTE: ACCEPT

CHECK:
Why this decides it: K is defined in A.3a as (u^H u)^2/|u^T u|^2. The operator is complex symmetric, so the left eigenvector is l = conj(u). If K equals 1/(|<l,r>|/(|l||r|))^2 on the chain, then K → ∞ means the normalised left–right overlap → 0. That is the reverse of "infinitely non-orthogonal".
Ran `python3 work_A/item2.py` (the onset_exact.py chain at N = 400, with the left eigenvector computed independently from A^H):
```
kap 2.0  herm overlap 0.8415  K=1/ov^2 1.41228  closed 1.41228  |l-conj r| 5e-16  (A-A^T = 0)
kap 1.0  herm overlap 0.4546  K 4.8378   closed 4.8378
kap 0.8  herm overlap 0.2394  K 17.4499  closed 17.4499
kap 0.7  herm overlap 0.0982  K 103.657  closed 103.657
kap 0.66 herm overlap 0.0366  K 744.49   closed 744.49
kap 0.65 herm overlap 0.0210  K 2266.9   closed 2266.9   s = -0.6177 -> -kappa
```

REASON: K = 1/(normalised Hermitian overlap)^2 exactly, and the overlap tends to 0 at the onset. At the onset the mode becomes orthogonal to its left eigenvector, which is the Petermann-factor divergence, and its spectral projector becomes infinitely ill-conditioned. Below κ_c the pole is no longer on the physical sheet. The segment Re s = −κ, |Im s| ≤ k is the continuous spectrum of the full operator, so the mode does not "leave the spectrum": it stops being an isolated eigenvalue and merges into the continuous part.

TEXT:
- Line 71: "...at its centre $s=-\kappa$, and merges into the continuous spectrum, so that below $\kappa_c$ there is no isolated kept eigenvalue: Romatschke's hydrodynamic onset transition, $\tau_D=\pi/(2k)$~\cite{Rom,Hu}."
- Line 75: "which is $1$ for a fully coupled gas and diverges at the onset $\phi=\pi/2$ \grade{derived; Appendix A.3a}: the normalised overlap of the kept mode with its own left eigenvector, $K^{-1/2}$, falls to zero, and its spectral projector becomes infinitely ill-conditioned before the mode merges into the cut."

## Item 3
VOTE: ACCEPT (correct the factor; keep the sentence)

CHECK:
Why this decides it: the coupled/transition ratio of the terminal Gramians' top eigenvalues, divided by the squared survival factor exp[−2(ε_dec^n/n)(τ_c^{−n} − τ_t^{−n})], is exactly the "within a factor of ten" claim. Computing it for every history in t2_gramian.json also tests "where it was measured".
```
python3 -c "...t2_gramian.json: ratio of eigs[0], coupled/transition, integral and terminal..."
ed0.5_n3 integral ratio 2.47e-09 exponent -42.00 ratio/surv 4.3e+09
ed0.5_n3 terminal ratio 4.8e-17  exponent -42.00 ratio/surv 83.5
ed0.5_n6 integral ratio 4.99e-27 exponent -1365  log10(ratio/surv) 566.5
ed0.5_n6 terminal ratio 3.91e-28 exponent -1365  log10(ratio/surv) 565.4
ed2_n3   integral ratio 3.08e-07 exponent -42.00 ratio/surv 5.4e+11
ed2_n3   terminal ratio 1.38e-13 exponent -42.00 ratio/surv 2.4e+05
```

REASON: 4.8e−17 / e^−42 = 83.5, which is 10^1.92. That is not within a factor of ten, and the log's "10^1.1" is also wrong. The terminal Gramian was also computed for ε_dec = 2 and for n = 6, where it does not follow the survival factor at all, so "where it was measured" is false. What survives is the contrast for the ε_dec = 0.5, n = 3 history: the snapshot comes within about two orders of magnitude of the survival factor, while the integral Gramian sits nine orders above it. For the other histories the snapshot carries the leak as well. The surrounding sentence ("the coupled-era suppression is not the survival factor alone ... leak through the conserved ℓ = 0") stays as it is.

TEXT: replace the last clause from "the snapshot Gramian at the end of the horizon" with:
"the snapshot Gramian at the end of the horizon, which is the witness of Section~\ref{sec:witness}, comes within a factor of about $80$ of the squared survival factor for the $\epsilon_{\rm dec}=0.5$, $n=3$ history ($4.8\times10^{-17}$ against $e^{-42}=5.7\times10^{-19}$), and carries the same leak for $\epsilon_{\rm dec}=2$ ($1.4\times10^{-13}$) and for $n=6$."
(Side note, not voted: the abstract's "erased, by the factor $\exp[-\epsilon_{\rm dec}^n/(n\tau_s^n)]$" rests on the witness table, which checks this quantitatively only for n = 3 between 0.5 and 1. In light of this item it would be worth a look.)

## Item 4
VOTE: AMEND

CHECK:
Why this decides it: the "profile weight" is the weight vector wE in ruler_check.py and diag_modes.py, k^2 e^{−k^2/2} on 36 Gauss–Legendre nodes over [0.25, 9]. Summing it below the wall, and integrating the same density exactly, shows whether 51% is a property of the profile or of the nodes.
```
python3 -c "... roots_legendre(36) ... wE ...; quad(k^2 exp(-k^2/2), 0.25, wall)/quad(..., 0.25, 9)"
wall 1.5048228810695108  nodes below 9  node share 0.5135215
exact share 0.4785157
nodes near wall [1.4335 1.7025]
```

REASON: The wall falls between two nodes, so the 36-node sum (0.514) is off from the continuum share (0.479) by one node's weight. "About half" is true either way, and "the other half" can stay.

TEXT: "...that mode exists only for $k<\kappa\pi/2=1.50$ (Section~\ref{sec:cut}), which carries about half of the profile weight ($0.48$ of the profile, $0.51$ on the $36$ nodes used here); for the other half the pole has met the branch cut and there is no isolated kept eigenvalue."

## Item 5
VOTE: ACCEPT

CHECK:
Why this decides it: the witness table on the same page gives the residual return for coupled-era planting. Nonzero entries mean a closure on ℓ ≤ 2 is not exact there. sec_new_door.tex then reports nonlinear threshold runs on hidden structure, which would make "untested" stale for one half of the sentence.
Read the witness table: at τ_s/ε_dec = 0.1 the entries are 7e−15, 5e−19, 8e−24, 5e−31; at 0.25 they are 6e−10, 6e−11, 2e−15, 7e−20. sec_new_door.tex reports eight full-GR thresholds, with differences of 2.1–5.5e−3 at decoupling and 1.75–1.85e−5 in the coupled era, and says the coupled era "is not perfectly shut" (0.3–0.5% of the decoupling effect).

REASON: Tight coupling suppresses the return by many orders of magnitude, but it does not make the closure exact. The suppression is 10^−9 or smaller in the linear chain. In the full collapse a residual channel of 0.3–0.5% remains. The question of how far planted hidden structure moves the nonlinear threshold is answered in Section~\ref{sec:door}, so only the realistic-initial-data question stays open. The pairs tested are engineered matched perturbations, not realistic data.

TEXT: "\paragraph{Reading.} A closure on density, flux and stress misses almost nothing of structure set while the neutrinos are tightly coupled: the hidden difference returns at $10^{-9}$ or less. Structure set at or after decoupling survives in the finer angular moments and streams back into the visible ones by several per cent. The memory McCormick's runs record therefore has a place to live that no fluid closure contains. Matched perturbations of this kind move the nonlinear threshold itself (Section~\ref{sec:door}); whether realistic initial data carry such structure is untested: the memory curves of Section~\ref{sec:memory} start with the hidden moments empty."

## Item 6
VOTE: AMEND

CHECK:
Why this decides it: out_state.txt holds every coordinate actually compared. If only a few state rulers were tested, the claim has to be limited to those. If no run separates linear from nonlinear causation, "written after the readout epoch, in the nonlinear collapse" is an inference and not a measurement.
Read code/v4_runs/ruler/out_state.txt and out_primary.txt. Compared: the rapidity chart (rms 0.0142, odd spread 3.39%, family ratio 1.062), the state angle θ at τ* = 1.7 (rms 0.130, spread 35.9%, ratio 0.947), θ at τ* = 4 (rms 0.350), arc-length and chord rulers (spread 195% and 255%), and a memory-form log-odds control (spread 40%). The eigenprojector ruler was voided at the instrument (PREREGISTERED_RULER.txt: no isolated mode at κ = 0.958). The text's figures (5%, 6%, 36% against 3.4%, 0.13 against 0.014) reproduce.

REASON: The tested state and projector rulers fail and the rapidity chart holds, so the comparison stands as made. It does not cover every state-based coordinate. The kept-state ruler also leaves out the hidden ℓ ≥ 3 sector of the linear chain, which Sections~\ref{sec:witness} and~\ref{sec:gramian} show carries memory. So "written in the nonlinear collapse" isn't shown: what is shown is that the difference is not in the linear kept state at readout. The rest of the wording can stay.

TEXT:
- Abstract: "...which the two collision models move by almost the same angle: of the coordinates compared, the law is linear in the operator's link rapidity, and the difference between the models is not in the linear kept-sector state at readout."
- Line 257, end: "So, among the coordinates compared, the law is a law in the operator's own link rapidity, and not in the displacement of the linear kept state: the difference between the two collision models is not carried by the linear kept state at the readout epoch \grade{measured; Appendix~B.17}."
- Summary: "...the law is linear in the collision operator's own link rapidity, not in the displacement of the linear kept state or the other state rulers tested; ..."

## Item 7
VOTE: AMEND

CHECK:
Why this decides it: the "Order, with the opacity held fixed" paragraph itself lists which summaries were matched, and what was compared (linear readout and g_2, not the threshold).
Read sec_new_gramian.tex. Matched were optical depth, ∫(k^2/3)σ^2 dτ, and the operator at readout only "if the window closes before the readout" (R4 does not). Measured were the linear readout (33–72%) and g_2 (0.06–0.16). Its last sentence reads "Whether the threshold itself separates such a pair is untested."

REASON: "No scalar summary ... can carry what the threshold reads" claims something about all scalar summaries and about the threshold. The evidence covers three named summaries and linear readouts. "Every scalar summary" in the Summary overreaches the same way. Naming the summaries keeps the point and its force.

TEXT:
- sec_new_gramian.tex: "Integrated opacity, integrated connection energy and, where the window closes first, the operator at readout, matched together, do not fix the linear readout or the memory form: the order is part of the record. Whether the threshold itself separates such a pair is untested."
- Summary: "...and collision histories that agree in integrated opacity and integrated connection energy still differ in the memory."

## Item 8
VOTE: AMEND

CHECK:
Why this decides it: the split operator is a Markov generator on the bins exactly when every off-diagonal entry is nonnegative. Building the operators from discrete projections on McCormick's 32 midpoint bins and root-finding the sign change gives the exact windows.
Ran `python3 work_A/item8.py` with C = −r(I−P0) + (r−1)P1 for all ℓ ≥ 2, and C = −(I−P0) + (1−r)P2 for shear alone, with κ1 = 1:
```
all l>=2 0.725   all l>=2 1.55
shear 0.56       shear 1.2413
r=0.725: 0.0, r=1.55: -7e-18 (all l>=2 roots exact); at r=0.75,1.5 min off-diag +0.0028
shear at r=0.6: +0.0028, at r=1.2: +0.0053 (inside)
```
Continuum: all ℓ ≥ 2 gives r + (r−1)·3μμ' ≥ 0, so [3/4, 3/2]; shear alone gives 1 + 5(1−r)p2p2' ≥ 0 with p2 ∈ [−1/2, 1], so [0.6, 1.2].

REASON: Both stated windows are the continuum windows. The exact bin windows, [0.725, 1.55] and [0.56, 1.24], are slightly wider. So "outside those windows it has a negative off-diagonal entry" is false between the two sets of edges. Every pair the text calls admissible lies inside both, so no verdict changes.

TEXT: "\paragraph{Admissible ratios.} The split collision operator is a Markov generator for $\tfrac34\le r\le\tfrac32$ (all moments $\ell\ge2$ at $\kappa_2$) and $0.6\le r\le1.2$ (shear alone at $\kappa_2$), the conservative continuum windows; on McCormick's 32 bins the exact windows are slightly wider, $0.725\le r\le1.55$ and $0.56\le r\le1.24$, and outside them the operator has a negative off-diagonal entry and can, in principle, drive a nonnegative intensity negative." (The rest of the paragraph is unchanged.)

## Item 9
VOTE: ACCEPT (both)

CHECK:
(a) Why this decides it: G = (δ_c − 0.49773)/0.03059 from the table rows gives the abstract's endpoints directly.
`python3 -c "print((0.521485-0.49773)/0.03059,(0.501673-0.49773)/0.03059)"` gives 0.77656, 0.12890. The table prints 0.777 and 0.129.
(b) Why this decides it: if A.13's c is the coefficient that makes cμ = P1 I from the group's own flux, then it belongs to the per-group default target that sec_new_mcc.tex line 9 says the identity covers. On the bins, P1 I = (Σ w μ I / Σ w μ^2) μ = q/(2π Σ μ_k^2 Δμ) μ with q = 2π Σ μ_k I_k Δμ, which matches A.13's c.

REASON: (a) The abstract rounds 0.7766 to 0.776, while the table has 0.777. (b) The derivation is right, but it is mislabelled. A.13 calls it the "common-frame" target, while the main text says the identity holds for the per-group target and puts the common-frame (boosted) option outside it.

TEXT:
(a) Abstract: "$G$ runs from $0.777$ to $0.129$".
(b) A.13: "The dipole coefficient of the per-group default target, isotropy in the group's own frame to first order, is $c=q/(2\pi\sum_k\mu_k^2\Delta\mu)$, chosen so that $c\mu$ carries the group's own flux; on the bins $c\mu=P_1I$."

## Item 10
VOTE: ACCEPT (all five must be fixed before release; no new collapse runs needed)

CHECK:
Why this decides it: each claim is a file-existence or string check on the package.
- `grep "import chain_lib" paper_v8/code_v6/*.py`: A5_t1_order.py, A5_t2_gramian.py and A5_t3_closures.py all do `from chain_lib import *`. Only A5_chain_lib.py ships, so the three fail on import.
- Absolute scratch paths appear in 5 shipped .py files (code/main/make_figures_v3.py, make_fig6_door.py, code_v6/A2_step2_algebra.py, A2b_gate_operator.py, A2_step3_predict.py), plus some text and report files.
- `find paper_v8 -name "t2_gramian*" -o -name "G_ed*"` returns nothing. The raw outputs exist only in ../A5_kinetic/.
- `find paper_v8 -iname "LICENSE*"` returns nothing, while B.15 says "the licence file ships with the archive".
- Appendix C states the build results (commit d181d6d, 8934 jobs, no sorry) but no full build log is in the package.

REASON and fixes. All are packaging fixes and need no new runs:
1. chain_lib: ship the file as `chain_lib.py`, or change the three imports to `from A5_chain_lib import *`. Run each A5 script once from the unpacked package to confirm. These are linear-chain scripts that take minutes, not the collapse code.
2. Absolute paths: replace them with paths relative to the script (`os.path.dirname(__file__)`) or an environment variable with a relative default. Strip scratch paths from shipped text/report files, or mark them as provenance.
3. Raw Gramian outputs: add t2_gramian.json, t2_gramian_out.txt, the G_*.npy files and PREREGISTERED.txt from A5_kinetic to the zip. Item 3's correction depends on them, and readers need them to check it.
4. LICENCE: add McCormick's MIT LICENSE file verbatim next to the modified ms_nuc*.py files. MIT requires the notice to travel with copies. Also add a licence for the author's own code.
5. Lean log: include the full `lake build` output for commit d181d6d and the axiom-check output, or point to the CI log URL at that commit. Otherwise trim Appendix C's claim to what the log shown supports.
Also put the A6 third-level files (res_L3_r125.json, prog_L3_r08.json, RUNLOG.txt, PREREGISTERED.txt) in the zip, since the abstract cites them.
