# v11b part 2: cite the papers behind three Lean repos (DOIs as printed in each repo's README).
import os
D='/workspace/ink/D17/v11b'
E=[
 ('sec_v11_added.tex','cite The Ledger Outlives the Metric', r"is the finite algebra behind ``the ledger outlives the metric''", r"is the finite algebra behind ``the ledger outlives the metric''~\cite{Ledger}"),
 ('sec_v11_added.tex','cite The Square Case', r"commit \texttt{6769949} (63 theorems), proves", r"commit \texttt{6769949} (63 theorems), the Lean companion of~\cite{SquareCase}, proves"),
 ('sec_v11_added.tex','cite the three-body paper', r"commit \texttt{1f3ddcd}, proves the fold", r"commit \texttt{1f3ddcd}, the Lean companion of~\cite{ThreeBody}, proves the fold"),
 ('neutrinos_v11.tex','bibliography: three entries',
  "\\bibitem{WallD4}", "\\bibitem{Ledger} J.~Beasley, \\emph{The Ledger Outlives the Metric}, Zenodo, doi:10.5281/zenodo.22023237 (DOI as given in \\texttt{gravity-ledger-lean}).\n\\bibitem{SquareCase} J.~Beasley, \\emph{The Square Case: Gram Reduction and Spectral Transport for $N=d+1$ Bodies}, Zenodo, doi:10.5281/zenodo.21855590 (DOI as given in \\texttt{square-case-lean}).\n\\bibitem{ThreeBody} J.~Beasley, \\emph{The Three-Body Problem, Operator-First: A Complete Spectral Anatomy of Relational Transport on the Shape Sphere}, Zenodo, doi:10.5281/zenodo.20764188.\n\\bibitem{WallD4}"),
]
log=[]
for i,(f,why,old,new) in enumerate(E,5):
    p=os.path.join(D,f); s=open(p).read(); n=s.count(old); assert n==1,(f,old[:50],n)
    open(p,'w').write(s.replace(old,new))
    log.append(f'\n## B{i} {f}: {why}\n\n**old:**\n```latex\n{old}\n```\n**new:**\n```latex\n{new}\n```\n')
open(os.path.join(D,'changes_v11_to_v11b.md'),'a').write(''.join(log)); print('applied',len(E))
