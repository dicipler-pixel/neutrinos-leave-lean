# v8 -> v9 changed sentences

## replace [I0] (neutrinos_v9.tex)
- OLD: \date{13 November 2026 \quad (version 8 of \emph{When the Neutrinos Leave})}
+ NEW: \date{13 November 2026 \quad (version 9 of \emph{When the Neutrinos Leave})}

## replace [I1, I9a] (neutrinos_v9.tex)
- OLD: $G$ runs from $0.776$ to $0.129$, and its offset $\ln[(1-G)/G]$ moves close to a straight line in the link rapidity $\tfrac12\ln r$, at a rate of $1.11\pm0.01$ inside the window where the split operator is a Markov generator; with the collision rate evaluated at every Runge--Kutta stage the two inner pairs agree to $0.004$, and the $\pm0.01$ is now set by grid resolution; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step.
+ NEW: $G$ runs from $0.777$ to $0.129$, and its offset $\ln[(1-G)/G]$ moves close to a straight line in the link rapidity $\tfrac12\ln r$, at a rate of $1.11\pm0.01$ inside the window where the split operator is a Markov generator; with the collision rate evaluated at every Runge--Kutta stage the two inner pairs agree to $0.004$, and the $\pm0.01$ is a finite-resolution budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step, and if the $r=0.8$ threshold shrinks alike the rate extrapolates to $1.094$--$1.098$.

## replace [I6] (neutrinos_v9.tex)
- OLD: The frozen memory form misses this effect entirely, and so does the intrinsic displacement of the linear kept-sector state at readout, which the two collision models move by almost the same angle: the law lives in the operator's link rapidity, and the difference between the models is written in the nonlinear collapse.
+ NEW: The frozen memory form misses this effect entirely, and so does the intrinsic displacement of the linear kept-sector state at readout, which the two collision models move by almost the same angle: of the rulers tested, the law lives in the operator's link rapidity, and the linear kept state at readout does not hold the difference between the models.

## replace [I2] (neutrinos_v9.tex)
- OLD: The mode is real all the way down; at $\kappa_c$ it reaches the branch cut of $g$, the segment $\mathrm{Re}\,s=-\kappa$, $|\mathrm{Im}\,s|\le k$, at its centre $s=-\kappa$, and leaves the spectrum:
+ NEW: The mode is real all the way down; at $\kappa_c$ it reaches the branch cut of $g$, the segment $\mathrm{Re}\,s=-\kappa$, $|\mathrm{Im}\,s|\le k$, at its centre $s=-\kappa$, and merges into the continuous spectrum:

## replace [I2] (neutrinos_v9.tex)
- OLD: Appendix A.3a}: the kept mode becomes infinitely non-orthogonal to its own left eigenvector before it leaves.
+ NEW: Appendix A.3a}: the normalised overlap of the kept mode with its own left eigenvector, $K^{-1/2}=\sin2\phi/2\phi$, falls to zero, and its spectral projector becomes infinitely ill-conditioned as the mode meets the cut.

## replace [I5, W-F3] (neutrinos_v9.tex)
- OLD: \paragraph{Reading.} A closure on density, flux and stress is exact only for structure set while the neutrinos are tightly coupled.
+ NEW: \paragraph{Reading.} For structure set while the neutrinos are tightly coupled, a closure on density, flux and stress loses almost nothing: planted at a quarter of the decoupling time or earlier, the hidden difference returns at $10^{-9}$ or less in the table above.

## replace [I5] (neutrinos_v9.tex)
- OLD: Whether realistic initial data carry such structure, and how far it moves the nonlinear threshold, are untested: the memory curves of Section~\ref{sec:memory} start with the hidden moments empty.
+ NEW: How far such structure moves the nonlinear threshold is measured for matched, planted perturbations in Section~\ref{sec:door}.
+ NEW: Whether realistic initial data carry it is untested: the memory curves of Section~\ref{sec:memory} start with the hidden moments empty.

## replace [I8] (neutrinos_v9.tex)
- OLD: \paragraph{Admissible ratios.} On the angle bins the split collision operator is a Markov generator only for $\tfrac34\le r\le\tfrac32$ (all moments $\ell\ge2$ at $\kappa_2$) and $0.6\le r\le1.2$ (shear alone at $\kappa_2$); outside those windows it has a negative off-diagonal entry and can, in principle, drive a nonnegative intensity negative.
+ NEW: \paragraph{Admissible ratios.} The split collision operator is a Markov generator for $\tfrac34\le r\le\tfrac32$ (all moments $\ell\ge2$ at $\kappa_2$) and $0.6\le r\le1.2$ (shear alone at $\kappa_2$), the conservative continuum windows; on the $32$ angle bins the exact windows are slightly wider, $0.725\le r\le1.55$ and $0.56\le r\le1.24$, and outside them the operator has a negative off-diagonal entry and can, in principle, drive a nonnegative intensity negative.

## replace [I1] (neutrinos_v9.tex)
- OLD: Refining the $r=1.25$ pair in radius, angle and time together ($N=600$, $N_\mu=48$, the Courant numbers and the Hubble step factor halved) raises both thresholds, by $7.5$ and $6.4\times10^{-5}$, to $0.50991687$ and $0.51175643$, and lowers the rate to $1.1020$, range $[1.1016,1.1024]$: a shift of $-0.0082$, larger than the line of $0.005$ set before the run.
+ NEW: Refining the $r=1.25$ pair in radius, angle and time together ($N=600$, $N_\mu=48$, the Courant numbers and the Hubble step factor halved) raises both thresholds, by $7.5$ and $6.4\times10^{-5}$, to $0.50991687$ and $0.51175643$, and lowers the rate to $1.1020$, range $[1.1016,1.1024]$: a shift of $-0.0082$, which fails the line of $0.005$ set before the run.

## replace [I1] (neutrinos_v9.tex)
- OLD: So the bracket excludes first order in space but does not separate second order in space from first order in time \grade{measured;
+ NEW: So the bracket excludes an error purely first order in the cell size, but does not separate second order in space from first order in time, or from a mix of first-order errors in both \grade{measured;

## replace [I4, I6] (neutrinos_v9.tex)
- OLD: The eigenprojector of the least-damped mode is not available as an alternative: at the readout rate $\kappa=0.958$ that mode exists only for $k<\kappa\pi/2=1.50$ (Section~\ref{sec:cut}), which carries $51\%$ of the profile weight on the $36$ nodes used here; for the other half the pole has met the branch cut and there is no isolated kept eigenvalue.
- OLD: So the law is a law in the operator's own link rapidity, and not in the displacement of the linear kept state: the difference between the two collision models is written after the readout epoch, in the nonlinear collapse \grade{measured;
+ NEW: The eigenprojector of the least-damped mode is not available as an alternative: at the readout rate $\kappa=0.958$ that mode exists only for $k<\kappa\pi/2=1.50$ (Section~\ref{sec:cut}), which carries about half of the profile weight ($0.51$ on the $36$ nodes used here, $0.48$ by direct integration); for the other half the pole has met the branch cut and there is no isolated kept eigenvalue.
+ NEW: So, of the rulers tested, the law is a law in the operator's own link rapidity, and not in the displacement of the linear kept state: the difference between the two collision models is not carried by the linear kept state at the readout epoch \grade{measured;

## replace [W-F1] (neutrinos_v9.tex)
- OLD: Section~\ref{sec:link} finds that at the readout scale the kept sector has no isolated eigenvalue for about half of the profile, which is why the threshold is a law in the operator's link rapidity and not in the displacement of a kept state.
+ NEW: Section~\ref{sec:link} finds that at the readout scale the kept sector has no isolated eigenvalue for about half of the profile, so its eigenprojector cannot serve as a ruler there; of the rulers tested, the threshold is a law in the operator's link rapidity and not in the displacement of a kept state.

## replace [W-F5] (neutrinos_v9.tex)
- OLD: The memory sits in the angular structure a fluid closure drops: set at or after decoupling, it returns into density, flux and stress; set before, it is erased.
+ NEW: The memory sits in the angular structure a fluid closure drops: set at or after decoupling, it returns into density, flux and stress; set deep in the coupled era, it is erased.

## replace [I1, I6, I7] (neutrinos_v9.tex)
- OLD: The direction of the flux--shear mismatch, not its connection energy, is what the collapse reads; the law lives in the collision operator's own link rapidity, not in the displacement of the linear kept state; and the rate is a measured number, $1.11\pm0.01$ with the error now set by grid resolution, with no closed form attached.
- OLD: The readout Gramian of the hidden moments has no kernel and ranks what must be kept, and collision histories that agree in every scalar summary still differ in the memory.
+ NEW: The direction of the flux--shear mismatch, not its connection energy, is what the collapse reads; of the rulers tested, the law lives in the collision operator's own link rapidity, not in the displacement of the linear kept state; and the rate is a measured number at finite resolution, $1.11\pm0.01$, the $\pm0.01$ a resolution budget rather than a converged value or a statistical interval, extrapolating to $1.094$--$1.098$ if the unfinished third-level run follows the finished one, with no closed form attached.
+ NEW: The readout Gramian of the hidden moments has no kernel and ranks what must be kept, and collision histories that agree in integrated opacity and integrated connection energy still differ in the memory.

## replace [I12] (neutrinos_v9.tex)
- OLD: \bibitem{Rom} P.~Romatschke, \emph{Retarded correlators in kinetic theory: branch cuts, poles and hydrodynamic onset transitions}, Eur.\ Phys.\ J.\ C (2016), arXiv:1512.02641.
- OLD: \bibitem{Hu} J.~Hu, \emph{Relaxation time approximation revisited and non-analytical structure in retarded correlators}, arXiv:2409.05131.
+ NEW: \bibitem{Rom} P.~Romatschke, \emph{Retarded correlators in kinetic theory: branch cuts, poles and hydrodynamic onset transitions}, Eur.\ Phys.\ J.\ C 76 (2016) 352, arXiv:1512.02641.
+ NEW: \bibitem{Hu} J.~Hu, \emph{Relaxation time approximation revisited and non-analytical structure in retarded correlators}, SciPost Phys.\ 20 (2026) 020, arXiv:2409.05131.

## replace [W-F10, W-S2] (neutrinos_v9.tex)
- OLD: A full build of the version-7 statements at commit \texttt{d181d6d} (12 November 2026, 8934 build jobs) completes with no \texttt{sorry}, and the three self-scattering theorems use only the standard axioms.
- OLD: The earlier build at commit \texttt{c372d3f} (4 November 2026) compiles every module, replays every proof in an independent kernel checker, finds that all 100 theorems of the repository use only the standard axioms (\texttt{propext}, \texttt{Quot.sound}, \texttt{Classical.choice}), and confirms that all twelve false controls are rejected.
+ NEW: A full build of the Lean sources at commit \texttt{9cd71fa} (13 November 2026, 8934 build jobs) completes with no \texttt{sorry}; the audit script (commit \texttt{9292b2c}, which changes only its configuration) then finds that all 87 theorems of the library use only the standard axioms (\texttt{propext}, \texttt{Quot.sound}, \texttt{Classical.choice}) and that all eleven false controls are rejected for a mathematical reason.
+ NEW: The log, with the toolchain and Mathlib pins, ships with the archive.
+ NEW: An earlier build at commit \texttt{c372d3f} (4 November 2026) replayed every proof in an independent kernel checker.

## replace [W-F2] (app_new_evidence.tex)
- OLD: \noindent\texttt{A5\_PREREGISTERED.txt}: predictions and results.
+ NEW: \noindent\texttt{A5\_PREREGISTERED.txt}: predictions and results, kept as written; its line on the terminal Gramian ratio says $10^{1.1}$ where the ratio, $4.8\times10^{-17}$ against $e^{-42}$, is $10^{1.92}$ (Section~\ref{sec:gramian}).

## replace [I9b] (app_new_proofs.tex)
- OLD: The dipole coefficient of the common-frame target is $c=q/(2\pi\sum_k\mu_k^2\Delta\mu)$, chosen so that $c\mu$ carries the group's flux; on the bins $c\mu=P_1I$.
+ NEW: The dipole coefficient of the per-group default target is $c=q/(2\pi\sum_k\mu_k^2\Delta\mu)$, chosen so that $c\mu$ carries the group's flux; on the bins $c\mu=P_1I$.

## replace [I3, W-F4] (sec_new_gramian.tex)
- OLD: The coupled-era suppression is not the survival factor alone: for this history it is $1.1\times10^{-7}/0.367=3\times10^{-7}$ against the squared survival factor $e^{-42}$ (and $2.5\times10^{-9}$ against the same $e^{-42}$ for $\epsilon_{\rm dec}=0.5$), because the damped rungs still leak through the conserved $\ell=0$ at order $(k/\sigma)^\ell$; the snapshot Gramian at the end of the horizon, which is the witness of Section~\ref{sec:witness}, follows the survival factor to within a factor of ten for the $\epsilon_{\rm dec}=0.5$ history, where it was measured.
+ NEW: The coupled-era suppression is not the survival factor alone: for this history it is $1.1\times10^{-7}/0.367=3\times10^{-7}$ against the squared survival factor $e^{-42}$ (and $2.5\times10^{-9}$ against the same $e^{-42}$ for $\epsilon_{\rm dec}=0.5$), because the damped rungs still leak through the conserved $\ell=0$ at order $(k/\sigma)^\ell$; the snapshot Gramian at the end of the horizon, which is the witness of Section~\ref{sec:witness}, comes far closer to the survival factor: for the $\epsilon_{\rm dec}=0.5$ history its ratio is $4.8\times10^{-17}$, a factor of about $80$ above $e^{-42}$ where the integrated ratio is $4\times10^{9}$ above, and for the $\epsilon_{\rm dec}=2$ history it is $1.4\times10^{-13}$, $2\times10^{5}$ above the same $e^{-42}$.

## replace [I7] (sec_new_gramian.tex)
- OLD: No scalar summary of the history, whether opacity, integrated connection energy or the operator at readout, can carry what the threshold reads; the order is part of the record.
+ NEW: These three summaries of the history, the integrated opacity, the integrated connection energy and the operator at readout, matched together, do not fix the linear readout or the memory form; the order is part of the record.


Unregistered change blocks: 0
Registered snippets never matched: []