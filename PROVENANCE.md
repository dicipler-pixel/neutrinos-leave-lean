# Provenance

**Paper.** *When the Neutrinos Leave: Decoupling History and the Threshold for Primordial Black
Hole Formation*, Jeromie Beasley, version 3, 31 October 2026.

**Built on.** Stephen McCormick's preprint *Free-streaming neutrinos raise the threshold for
primordial black hole formation* (2026), and his code record
[10.5281/zenodo.23808375](https://doi.org/10.5281/zenodo.23808375). The nonlinear collapse runs
and the threshold values that the paper's verdicts compare against come from that work; nothing
in this repository re-derives them.

**How the Lean files were made.** The eight modules under `Neutrinos/` were written for this
repository from the statements of version 3 (the cross-link inequality behind the speed bound,
the two- and three-moment connection energies, the shear counterexample, the scalar-collision
propagator and the arithmetic of the pre-registered verdicts). Every numerical value they assert
was first recomputed in exact rational arithmetic with SymPy, and the real Schur form of the
shear response was checked against the full complex `3 x 3` resolvent.

**Toolchain.** Lean v4.34.1, Mathlib v4.34.1, the same pins as the sibling repository
`votkp-lean`.

**Verification status.** First verified at commit `5b7b5cb55032cf7ffb46f67cc1dc591cb22419f1`
(GitHub Actions run 41253552358, 31 October 2026): every module built, every module replayed in
the independent kernel checker, 76 theorems audited using only the axioms `propext`,
`Quot.sound` and `Classical.choice`, and all 9 false controls rejected. The workflow in
`.github/workflows/build.yml` is the check of record and runs again on every push.
