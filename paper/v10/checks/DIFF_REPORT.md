# v9 -> v10 changed sentences

## replace [C1] (neutrinos_v10.tex)
- OLD: \date{13 November 2026 \quad (version 9 of \emph{When the Neutrinos Leave})}
+ NEW: \date{13 November 2026 \quad (version 10 of \emph{When the Neutrinos Leave})}

## replace [C2, C3] (neutrinos_v10.tex)
- OLD: $G$ runs from $0.777$ to $0.129$, and its offset $\ln[(1-G)/G]$ moves close to a straight line in the link rapidity $\tfrac12\ln r$, at a rate of $1.11\pm0.01$ inside the window where the split operator is a Markov generator; with the collision rate evaluated at every Runge--Kutta stage the two inner pairs agree to $0.004$, and the $\pm0.01$ is a finite-resolution budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shift of the $r=1.25$ threshold to $0.42$ of the previous step, and if the $r=0.8$ threshold shrinks alike the rate extrapolates to $1.094$--$1.098$.
+ NEW: $G$ runs from $0.777$ to $0.129$, and its offset $\ln[(1-G)/G]$ moves close to a straight line in the link rapidity $\tfrac12\ln r$, at a rate of $1.10\pm0.01$ inside the window where the split operator is a Markov generator; with the collision rate evaluated at every Runge--Kutta stage the two inner pairs agree to $0.004$, and the $\pm0.01$ is an error budget, not a converged value or a statistical interval; a third grid level shrinks the resolution shifts of the two thresholds to $0.42$ and $0.49$ of the previous step and gives $1.101$, against $1.102$ at the second level, with a bracket range of $1.094$--$1.109$.

## replace [C4] (neutrinos_v10.tex)
- OLD: Every central inner value, $1.1020$ to $1.1102$, lies in
+ NEW: The values at the two finer levels, $1.1020$ and $1.1013$ (below), and the whole bracket range of the finest, lie in

## replace [C5] (neutrinos_v10.tex)
- OLD: \text{odd rate}=1.11\pm0.01,
+ NEW: \text{odd rate}=1.10\pm0.01;

## replace [C6] (neutrinos_v10.tex)
- OLD: but the $\pm0.01$ is now the error budget itself, dominated by resolution, and not a margin around a converged number.
+ NEW: the first-level values, $1.1066$ and $1.1102$, sit near its upper edge, the second $0.0002$ above it.
+ NEW: The $\pm0.01$ is the error budget itself, led by the third-level brackets, and not a margin around a converged number.

## replace [C7, C8] (neutrinos_v10.tex)
- OLD: At $r=1.25$ it puts the threshold at $0.5099481\pm0.0000063$, a further rise of $3.1\times10^{-5}$ against $7.5\times10^{-5}$ for the previous step.
- OLD: The shift shrank to $0.42$ of the previous one (range $0.33$--$0.50$).
+ NEW: It puts the thresholds at $0.5099481\pm0.0000063$ ($r=1.25$) and $0.5117877\pm0.0000063$ ($r=0.8$), further rises of $3.1\times10^{-5}$ each against $7.5$ and $6.4\times10^{-5}$ for the previous step.
+ NEW: The shifts shrank to $0.42$ (range $0.33$--$0.50$) and $0.49$ (range $0.39$--$0.59$) of the previous ones.

## replace [C10, C9] (neutrinos_v10.tex)
- OLD: First order in the cell size predicted $0.50996706$, outside the bracket; second order in the cell size predicted $0.50995033$ (a factor $0.44$) and first order in the time step $0.50994197$ (a factor $0.33$), both inside, the second at its lower edge.
- OLD: So the bracket excludes an error purely first order in the cell size, but does not separate second order in space from first order in time, or from a mix of first-order errors in both \grade{measured;
+ NEW: First order in the cell size predicted $0.50996706$ and $0.51179917$, both outside the brackets; second order in the cell size (a factor $0.44$) predicted $0.50995033$ and $0.51178492$, both inside; first order in the time step (a factor $0.33$) predicted $0.50994197$, at the lower edge of the $r=1.25$ bracket, and $0.51177780$, below the $r=0.8$ bracket.
+ NEW: So the brackets exclude an error purely first order in the cell size, and at $r=0.8$ one purely first order in the time step; they agree with second order in the cell size and do not exclude a mix of first-order errors in both \grade{measured;

## replace [C11] (neutrinos_v10.tex)
- OLD: Under either reading, if the $r=0.8$ threshold shrinks by the same factor, the third-level rate is $1.099$ and the extrapolated rate $1.094$--$1.098$, just below the band; the $r=0.8$ third-level run was still in progress when this version was closed, so the extrapolation is untested.
+ NEW: The third-level rate is $1.1013$, range $[1.0938,1.1088]$ over the corners of the two brackets: a change of $-0.0007$ from the second level against $-0.0082$ for the previous step, inside the kill line written first, which was a change larger than the previous one.
+ NEW: The third-level brackets are $1.25\times10^{-5}$ wide, since runs this close to threshold no longer finish in one compute window, so the change is known only to $\pm0.0075$ and its sign is not resolved; the order read from the three central values, $6.2$, lies outside the range $0.5$ to $4$ set before the runs for an extrapolation, and none is quoted.
+ NEW: With the reference shift and the pair spread the budget is $0.0091$ in quadrature, $0.015$ added linearly.

## replace [C12] (neutrinos_v10.tex)
- OLD: Lines: rate one (dashed) and the inner-pair rate $1.11$.}\label{fig:link}\end{figure}
+ NEW: Lines: rate one (dashed) and the first-level inner-pair rate $1.11$.}\label{fig:link}\end{figure}

## replace [C13, C14] (neutrinos_v10.tex)
- OLD: And the anisotropic stress carries the threshold: with the shear relaxing at $r$ times the flux rate, the offset of the surviving share moves close to a straight line in the link rapidity $\tfrac12\ln r$, at a rate of $1.11\pm0.01$ inside the admissible window, and at $1.19$--$1.20$ when the shear alone is damped.
- OLD: The direction of the flux--shear mismatch, not its connection energy, is what the collapse reads; of the rulers tested, the law lives in the collision operator's own link rapidity, not in the displacement of the linear kept state; and the rate is a measured number at finite resolution, $1.11\pm0.01$, the $\pm0.01$ a resolution budget rather than a converged value or a statistical interval, extrapolating to $1.094$--$1.098$ if the unfinished third-level run follows the finished one, with no closed form attached.
+ NEW: And the anisotropic stress carries the threshold: with the shear relaxing at $r$ times the flux rate, the offset of the surviving share moves close to a straight line in the link rapidity $\tfrac12\ln r$, at a rate of $1.10\pm0.01$ inside the admissible window, and at $1.19$--$1.20$ when the shear alone is damped.
+ NEW: The direction of the flux--shear mismatch, not its connection energy, is what the collapse reads; of the rulers tested, the law lives in the collision operator's own link rapidity, not in the displacement of the linear kept state; and the rate is a measured number at finite resolution, $1.10\pm0.01$, the $\pm0.01$ an error budget rather than a converged value or a statistical interval, $1.102$ and $1.101$ at the two finest of three grid levels, with no closed form attached.

## replace [C16] (app_new_evidence.tex)
- OLD: Predictions and kill line written before the runs, with the appended timing and the change of tolerance; the queue scripts; the run log; the $r=1.25$ result.
+ NEW: Predictions and kill line written before the runs, with the appended timing, the change of tolerance and the results; the queue scripts; the run log; the two results; the scripts that compute the rates and the extrapolation fixed before the runs, and their output (\texttt{richardson.py} uses \texttt{oddrate.py}, listed in B.19 as \texttt{A1\_oddrate.py}).

## insert [C16] (app_new_evidence.tex)
+ NEW: \lstinputlisting{code/A6/res_L3_r08.json}
+ NEW: \lstinputlisting{code/A6/level3_rates.py}
+ NEW: \lstinputlisting{code/A6/level3_rates_out.txt}
+ NEW: \lstinputlisting{code/A6/richardson.py}
+ NEW: \lstinputlisting{code/A6/richardson_out.json}

## replace [C15] (sec_new_mcc.tex)
- OLD: His physical model lives far outside the window where the rate $1.11$ was measured, and at readout both rates are below $H$ ($\kappa_e/H\approx0.02$--$0.04$, $\kappa_n/H\approx0.16$--$0.27$ at $T_H=1$\,MeV): a large link rapidity on a weak link.
+ NEW: His physical model lives far outside the window where the rate was measured, and at readout both rates are below $H$ ($\kappa_e/H\approx0.02$--$0.04$, $\kappa_n/H\approx0.16$--$0.27$ at $T_H=1$\,MeV): a large link rapidity on a weak link.


Unregistered change blocks: 0
Registered snippets never matched: []