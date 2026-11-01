# AI use

The research questions behind this library are Jeromie Beasley's. AI tools (Claude) were used to
search the literature, write the Lean proofs and organise this repository.

No statement here rests on an AI's say-so. Every proof is meant to be checked by the Lean kernel
and replayed by an independent kernel checker on every push, every theorem's axioms are audited,
and every false control must be rejected for the check to pass. Those checks run in the GitHub
Actions workflow. When the files were written, they had not been compiled on the machine that
wrote them (the Mathlib cache could not be downloaded there), so the first green run of the
workflow is the first evidence that they are correct. That first green run is recorded in
`PROVENANCE.md`. What the
statements mean, and what they do not claim, is set out in plain words in `README.md` and
`LIMITATIONS.md`.

Every numerical value the files assert (the response `32/37`, its derivative `-5/1369`, the
fractions `472/3059`, `1983/3059`, `970/3059`) was first recomputed in exact rational arithmetic
with SymPy, including a check of the Schur-complement form against the full complex resolvent.
