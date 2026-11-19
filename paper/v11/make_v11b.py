# v11b edits: exact-string replacements on the v11b copies; each old string must occur exactly once.
import os
D='/workspace/ink/D17/v11b'
FRAME_PARA=r"""

\paragraph{The author's position, and the conformal boundary.} The draft d4 of the companion paper~\cite{WallD4} states the position this frame writes in: the author does not hold that the universe began in a Big Bang, and there may be no first moment. His framework ``begins from memory, not from a metric, a clock, a particle ontology, or an assumed time coordinate''~\cite{DT}. That draft reads the apparent beginning as a passage between aeons in the sense of Penrose's conformal cyclic cosmology~\cite{CCC}; the comparison with Penrose was relayed on the author's behalf and is not a quotation of his \grade{author's interpretation}. Inside one aeon the flat radiation solution is already conformal to a regular metric, $a^2(-d\eta^2+d\mathbf x^2)=\check\Omega^2 g$ with $\check\Omega=a_1\eta$ and $g=-d\eta^2+d\mathbf x^2$, so the degeneracy at $\eta=0$ is the zero of the conformal factor and $g$ continues across it. The draft adds that Penrose's reciprocal hypothesis makes an empty previous aeon de Sitter space with $\Lambda=3a_1^2$ (checked symbolically there, not rechecked here). In the author's words, ``the wall is not a memory it the force of one via all teh dirac time work''. Read at the conformal boundary, the metric and the clock fail there but the record need not, which has the logical shape of Dirac Time's ``failure of one metric description $\not\Rightarrow$ failure of every spectral record''~\cite{DT}. That is an analogy, not an instance: the projector metric is not the spacetime metric, and no map from the neutrino kept sector to a projector family across the boundary is given \grade{reading}. Neutrinos are massive and a mass scale breaks conformal invariance, so what the neutrino mass scale does at the boundary is left open here, as in~\cite{WallD4}."""

SOURCES=r"""

\section{Further sources read for this version}\label{sec:v11bsources}
Each item names its repository and commit. Connections to this paper are readings \grade{reading}; nothing below was rerun.

\paragraph{The black-hole recovery ledger.} Branch \texttt{claude/bh-recovery-20261116} of \texttt{dicipler-pixel/event-horizon-lean}, commit \texttt{7c3d5f6}, adds only a recovery manifest and reading ledgers to \texttt{main@7dd6164}; it adds no Lean statement, so the statements of Section~\ref{sec:bhreadings} are unchanged. Two of its entries bear on this paper. First, the manifest lists an edition~11 of~\cite{BH} (26 October 2026, 59~pp) with a new section ``Black holes as orientation records'' as \emph{not recovered}; only a draft of that section (25 October) survives. The orientation-record reading of Section~\ref{sec:bhreadings} therefore rests on edition~10. Second, its ledger of the 2 November neutrino crossings records the matched-load ``missing half of the ledger'' as ``FAIL, all variants'', and many-moment critical-damping values $\kappa^*/k=0.66492$, $0.65199$, $0.64495$, $0.64112$ at $N=50$, $100$, $200$, $400$, ``not converged, drifting down''. Those values are the ledger's, not recomputed here; this paper uses the exact onset $\kappa=2k/\pi$ (Section~\ref{sec:cut}), and $2/\pi=0.63662$.

\paragraph{The wall $\Gamma^2=\tfrac12$ in Lean.} The value of the wall is stated in Lean as \texttt{line\_ratio}, $\Gamma(3+2r)^2=\tfrac12$ when $r^2=2$ and $r>0$ (``J3''), with the commutator trace in reflect/transmit form, $2-4\sinh^4(r/2)=2-4(R/T)^2$, as \texttt{trace\_reflect\_transmit} (``J4''), in \texttt{research/2026-11-10/BallJoins.lean} on branch \texttt{claude/votkp-research-20261110} of \texttt{dicipler-pixel/votkp-lean} (tip \texttt{3565281}; the file was last changed in \texttt{629f3bf}). That file lies outside the libraries the repository's build targets, so its proof check does not cover it, and it was not compiled here. Neither statement is the sharp claim that two equal perpendicular steps turn parabolic exactly at $\Gamma^2=\tfrac12$; that remains the algebra of~\cite{SMball} used in Section~\ref{sec:link}.

\paragraph{The ledger outlives the metric.} \texttt{dicipler-pixel/gravity-ledger-lean}, commit \texttt{885932f} (30 theorems), proves that every tangent to an idempotent is off-diagonal, that a moving signed metric has an indefinite side (\texttt{moving\_metric\_indefinite\_side}), and that the overlap of equal-trace idempotents has an exact quadratic limit (\texttt{overlap\_quadratic\_limit}). In the frame of Section~\ref{sec:frame} this is the finite algebra behind ``the ledger outlives the metric'': the overlap of the kept projector stays controlled where a metric reading changes sign.

\paragraph{The square case.} \texttt{dicipler-pixel/square-case-lean}, commit \texttt{6769949} (63 theorems), proves that the intrinsic flow keeps a tangent on a binary-collision wall (\texttt{intrinsic\_preserves\_wall\_tangent}) and that for orthogonal projections of equal rank $k$, $\mathrm{Tr}(PQ)=k-\tfrac12\|P-Q\|_F^2$. The first is the wall-side half of one-way transport (what is in the wall stays in it); the second is the overlap used when the kept sector is compared across the cut.

\paragraph{The three-body fold.} \texttt{dicipler-pixel/three-body-lean}, commit \texttt{1f3ddcd}, proves the fold $\lambda_{\min}(\pi/2+\varepsilon)=\sin^2\varepsilon$ with $\lambda_{\min}/\varepsilon^2\to1$ (\texttt{fold\_lambda}, \texttt{fold\_quadratic}) and the shifted ledger minimum (\texttt{ledger\_min}): the same quadratic touch as the fold of~\cite{BH}. Its report \emph{3-6-9: straw man to the max} (28 October 2026) does not concern neutrinos and is not used.

\paragraph{Other branches read.} The five \texttt{test-*} branches of \texttt{dicipler-pixel/dirac-time-lean} (26 September 2026) each carry a sibling library (Elemental Peeling, the gravity ledger, the light ledger, Universal Projector Geometry, Yang--Mills) for build testing, not new Dirac Time statements. The UPG branch (\texttt{4c76b9e}) states when a retained sector evolves on its own, the question the cut of Section~\ref{sec:cut} answers for the neutrinos. Branch \texttt{atlas-207-coverage-2026-10-23} of \texttt{dicipler-pixel/relational-atlas-lean} is already merged into \texttt{main@060c904}."""

E=[
 ('neutrinos_v11.tex','date line: drop "draft for the author\'s review"; v11 label kept (provisional, v13 vs v11 undecided)',
  r"in full, with corrections; draft for the author's review)}", r"in full, with corrections)}"),
 ('sec_v11_frame.tex','frame: add the author\'s position and the conformal boundary (from Wall d4 §6.1, 6.3, 6.4)',
  r"by which a record at decoupling reaches matter.", r"by which a record at decoupling reaches matter."+FRAME_PARA),
 ('sec_v11_added.tex','new section: further sources read (EH-lean recovery branch, BallJoins J3/J4, gravity-ledger, square-case, three-body, dirac-time test branches, relational-atlas branch)',
  r"read the same way.", r"read the same way."+SOURCES),
 ('neutrinos_v11.tex','bibliography: add Wall d4',
  r"\end{thebibliography}", "\\bibitem{WallD4} J.~Beasley, \\emph{The Neutrinos at the Wall}, draft d4, 19 November 2026 (unpublished; revises draft 3 of 15 November 2026, commit \\texttt{aa8d6ec}).\n\\end{thebibliography}"),
]
log=['# Changes from v11 to v11b\n','Applied by make_v11b.py to copies of the v11 files in /workspace/ink/D17/v11b/. Each old string was asserted to occur exactly once.\n',
 '**Label:** the paper keeps the "v11" label. It is provisional: the author has not yet chosen between v13 and v11.\n']
for i,(f,why,old,new) in enumerate(E,1):
    p=os.path.join(D,f); s=open(p).read(); n=s.count(old)
    assert n==1,(f,old[:50],n)
    open(p,'w').write(s.replace(old,new))
    log.append(f'\n## B{i} {f}: {why}\n\n**old:**\n```latex\n{old}\n```\n**new:**\n```latex\n{new.strip()}\n```\n')
open(os.path.join(D,'changes_v11_to_v11b.md'),'w').write(''.join(log))
print('applied',len(E))
