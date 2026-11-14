# Voter B

## Item 1
VOTE: AMEND
CHECK: Read line 22, 236, 240, 293. The text already states the -0.0082 shift failed the 0.005 line and that extrapolation is untested; what is missing is the plain label (estimate, not converged constant or confidence interval), the 1.094-1.098 value stated with its assumption beside the headline, and the narrower claim about what the bracket excludes. Why this decides: the item is about wording only, so the check is whether each of the audit's four points is already on the page.
REASON: Audit is right on three of four points (label, conditional extrapolation beside the headline, "excludes first order in space" is only about the pure form). The failed-preregistration point is already in the text. Number kept.
TEXT:
- Abstract: replace "and the $\pm0.01$ is now set by grid resolution; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step" with "a finite-resolution estimate, not a converged constant, whose $\pm0.01$ is a resolution budget and not a confidence interval; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step, and if the $r=0.8$ threshold shrinks the same way the rate extrapolates to $1.094$--$1.098$".
- Summary: "a rate of $1.11\pm0.01$" stays; replace "the rate is a measured number, $1.11\pm0.01$ with the error now set by grid resolution, with no closed form attached" with "the rate is a measured finite-resolution estimate, $1.11\pm0.01$ (a resolution budget, extrapolating to $1.094$--$1.098$ if the $r=0.8$ shift shrinks like the $r=1.25$ one), with no closed form attached".
- Line 240: replace "So the bracket excludes first order in space but does not separate second order in space from first order in time" with "So the bracket excludes the pure first-order spatial form, but not mixed-error models, and does not separate second order in space from first order in time"; replace "just below the band; ... so the extrapolation is untested" with "just below the band, on the assumption that the $r=0.8$ shift shrinks by the same factor; the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation is untested".

## Item 2
VOTE: ACCEPT
CHECK: Why decisive: K defined in onset_exact.py as (v^dag v)^2/|v^T v|^2; for a complex-symmetric operator the left eigenvector is conj(v) in the Hermitian pairing, so the normalised overlap is |v^T v|/(v^dag v) = 1/sqrt(K). Ran (code from onset_exact.py chain, N=400):
 kappa=2.0  K=1.4123 herm overlap=0.8415 1/sqrtK=0.8415 (4phi^2/sin^2 2phi = 1.4123)
 kappa=1.0  K=4.8378 overlap=0.4546 ; kappa=0.8 K=17.45 overlap=0.2394 ; kappa=0.7 K=103.66 overlap=0.0982 ; kappa=0.66 K=744.49 overlap=0.0366
So K grows because the overlap tends to zero; overlap = sin(2phi)/(2phi) exactly (0.8415 = sin1 at phi=1/2).
REASON: The sentence "infinitely non-orthogonal to its own left eigenvector" is ambiguous at best and reads reversed; the overlap vanishes. Also at kappa_c the pole reaches the cut centre and merges into the continuum; "leaves the spectrum" overstates.
TEXT:
- Line 71: "...at its centre $s=-\kappa$, and merges into the continuous spectrum: Romatschke's hydrodynamic onset transition..."
- Line 75: "...diverges at the onset $\phi=\pi/2$: the normalised overlap of the mode's left and right eigenvectors, $1/\sqrt K=\sin2\phi/2\phi$, tends to zero, so the spectral projector of the kept mode becomes ill-conditioned before the pole merges into the cut."

## Item 3
VOTE: ACCEPT
CHECK: Why decisive: compare the measured terminal-Gramian ratio against the squared survival factor for the eps_dec=0.5 history. From t2_gramian.json: terminal top eigenvalue at s=0.125 is 1.1292e-17, at s=0.5 is 0.23518; ran python: ratio = 4.8014e-17; squared survival exp[-2(ed^3/3)(1/0.125^3-1/0.5^3)] = exp(-42) = 5.7495e-19; ratio/factor = 83.5 (log10 = 1.92). So "within a factor of ten" is false; log's "10^1.1" is also wrong (1.9). Unsquared survival factor is 0.0 vs 7.6e-10, not the relevant object either. (Same pattern: n=6 terminal ratio 3.9e-28 against exp(-2*...) underflow, no meaningful comparison.)
REASON: The prereg P2b kill is 10^{+-3}, so 83.5 is inside the preregistered kill line, but the paper's wording claims a tighter agreement than measured.
TEXT: "...follows the survival factor to within a factor of about eighty for the $\epsilon_{\rm dec}=0.5$ history, where it was measured ($4.8\times10^{-17}$ against $e^{-42}=5.7\times10^{-19}$)." Also correct REPORT/PREREG line "within 10^1.1" to 10^1.9 if shipped.

## Item 4
VOTE: ACCEPT
CHECK: Why decisive: the weight below the wall depends on quadrature. Ran: wall k=pi/2*0.958=1.504823; 36 Gauss-Legendre nodes on [0.25,9] with weight k^2 exp(-k^2/2): 0.51352; scipy quad of the same on [0.25,1.504823] over [0.25,9]: 0.47852.
REASON: 51% is a coarse-node artefact; 48% by integration. "About half" is true for both.
TEXT: "...which carries about half of the profile weight ($0.51$ on the $36$ nodes used here, $0.48$ by direct integration); for the other half the pole has met the branch cut..."

## Item 5
VOTE: AMEND
CHECK: Why decisive: whether the witness table has nonzero residuals and whether sec_new_door covers the nonlinear threshold. Read neutrinos_v8.tex 160-181 and sec_new_door.tex: the witness table (tau_s/eps_dec = 0.1 ... entries like 7e-15, 5e-19, ...) is nonzero everywhere; sec_new_door.tex line 13 ff. reports eight restart thresholds (e.g. +1.83e-3 for +p3, planted at decoupling vs ~2e-5 coupled era). So "untested" is stale for matched perturbations; realistic initial data remain untested.
REASON: Tight coupling suppresses, does not zero, the hidden-structure effect; the nonlinear-threshold test now exists for matched planted structure.
TEXT: "A closure on density, flux and stress is accurate to the suppression factor for structure set while the neutrinos are tightly coupled. Structure set at or after decoupling survives in the finer angular moments and streams back into the visible ones by several per cent. The memory McCormick's runs record therefore has a place to live that no fluid closure contains. The effect on the nonlinear threshold is tested for matched planted perturbations in Section~\ref{sec:door}; whether realistic initial data carry such structure is untested: the memory curves of Section~\ref{sec:memory} start with the hidden moments empty." (use the actual label of the restart section.)

## Item 6
VOTE: AMEND
CHECK: Why decisive: what was actually compared. Read line 257 and abstract: tested rulers are the principal angle of the chain state (slope differences 5% vs 6%, odd-rate spread 36% vs 3.4%, residual 0.13 vs 0.014; models differ 0.0475 vs 0.0467 angle but thresholds 8%). That comparison supports "near-linear in rapidity, not in this tested angle" and no more; it cannot show every state coordinate fails or when the difference is generated.
REASON: Audit right; keep the comparison made.
TEXT:
- Line 257 end: "So the offsets are near-linear in the operator's own link rapidity and not in the displacement of the linear kept state tested here: the two collision models move that state by almost the same angle while their thresholds differ, so the difference between them is not carried by the linear state at readout and appears in the nonlinear collapse."
- Abstract: "the offsets follow the operator's link rapidity, not the tested angle of the linear kept state at readout; the difference between the models is not carried by that state and appears in the nonlinear collapse."
- Summary: "the offsets follow the collision operator's own link rapidity, not the displacement of the linear kept state tested here".

## Item 7
VOTE: ACCEPT
CHECK: Why decisive: the order test (sec_new_gramian line 15) names three summaries (integrated opacity, integrated connection energy, operator at readout, the last only when the window closes before readout) and measures linear readouts only; the same paragraph ends "Whether the threshold itself separates such a pair is untested." So universal wording is unsupported.
REASON: Replace "every/no scalar summary" with the specified ones.
TEXT:
- Summary: "collision histories with equal integrated opacity and equal integrated connection energy still differ in the memory".
- Gramian line 15: "Neither the integrated opacity, the integrated connection energy, nor the operator at readout (when the window closes before it) can carry what the linear readout reads; the order is part of the record. Whether the threshold itself separates such a pair is untested."

## Item 8
VOTE: AMEND
CHECK: Why decisive: off-diagonal sign on the actual 32 midpoint bins. Built the discrete orthonormal basis (Gram-Schmidt, weights dmu/2), projectors P_l, generator -(P1 + r(I-P0-P1)) for all l>=2, and -(I-P0+(r-1)P2) for shear alone, scanned r in [0.3,2.5] (22001 pts) for all off-diagonals >= 0. Output: all-l>=2: [0.725, 1.55]; shear alone: [0.56, 1.2412].
REASON: [3/4,3/2] is the conservative continuum window (inside the bin interval); 0.6-1.2 is likewise inside the bin shear window [0.56,1.24]. All inclusion claims (r=1.2,1/1.2,1.25,0.8 inside; 1/2, 2, 1/4, 4, 1/16, 16 outside) remain true on the bins.
TEXT: "On the $32$ angle bins the split collision operator is a Markov generator exactly for $0.725\le r\le1.55$ (all moments $\ell\ge2$ at $\kappa_2$) and $0.56\le r\le1.24$ (shear alone at $\kappa_2$); the conservative continuum windows are $\tfrac34\le r\le\tfrac32$ and $0.6\le r\le1.2$. Outside them it has a negative off-diagonal entry ..." (rest unchanged; "first window" -> "first window").

## Item 9
VOTE: AMEND
CHECK: (a) ran (0.521485-0.49773)/0.03059 = 0.77656; the table prints 0.777 and the run log 0.7765. (b) read app_new_proofs line 2 vs sec_new_mcc line 9: main text restricts the identity to the per-group default target and puts the boosted common-frame target outside it.
REASON: (a) 0.776 is a truncation; 0.777 matches table. (b) appendix wording contradicts main text.
TEXT: (a) abstract: "$G$ runs from $0.777$ to $0.129$". (b) A.13: "The dipole coefficient of the per-group default target is $c=q/(2\pi\sum_k\mu_k^2\Delta\mu)$, chosen so that $c\mu$ carries the group's own flux; on the bins $c\mu=P_1I$." (and drop any trailing sentence implying common-frame; the common-frame boosted target is outside the identity).

## Item 10
VOTE: AMEND
CHECK: code_v6/A5_t{1,2,3}_*.py do `from chain_lib import *`; only code_v6/A5_chain_lib.py exists. grep for /tmp, scratchpad, /home in code and code_v6 shows absolute paths in several drivers (make_figures_v3.py, make_fig6_door.py, A2_*.py, wb_checks logs). paper line 460 etc. mention a shipped licence; none in tree.
REASON: Must fix before release, no new collapse runs needed:
 1. Add chain_lib.py (copy of A5_chain_lib.py, or rename A5 scripts' import to A5_chain_lib) so A5 scripts run.
 2. Replace absolute scratch paths with paths relative to the script (Path(__file__).parent) or an argument.
 3. Ship A5_kinetic raw outputs (t2_gramian.json, t2_gramian_out.txt, PREREGISTERED.txt; the G_*.npy are small enough) since Items 3 and the Gramian claims rest on them.
 4. Add LICENSE (MIT) text, or change the paper's sentence to what ships.
 5. Lean log: regenerate a full build log from the existing Lean project (lake build) rather than the two-line stub; this is a rebuild of proofs, not the collapse code.
TEXT: no paper wording change beyond licence sentence if LICENSE is not added.
