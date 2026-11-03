<div align="center">

# When the Neutrinos Leave: Lean proofs

**The exact finite-dimensional algebra behind *When the Neutrinos Leave: Decoupling History and the Threshold for Primordial Black Hole Formation* (version 3): a speed bound, two connection energies, a shear counterexample, a scalar-collision propagator and the arithmetic of the pre-registered verdicts, written for Lean.**

![Lean](https://img.shields.io/badge/Lean-v4.34.1-blue)
![sorry](https://img.shields.io/badge/sorry-0-2EA043)
![Code: MIT](https://img.shields.io/badge/code-MIT-lightgrey)
![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey)

Jeromie Beasley

</div>

---

The paper asks how the history of when neutrinos stop colliding and start streaming freely
changes the density a region must reach before it collapses into a primordial black hole. The
collapse itself is a heavy numerical calculation that this repository does not touch. What it
does check, with a computer proof assistant, is the small piece of exact mathematics underneath:
a few inequalities and identities about a short chain of matrices (the first two or three
Legendre moments of the neutrino distribution), and the plain arithmetic by which the paper
decides whether each test result matches its prediction. If a number or an inequality in those
parts were misstated, Lean would refuse to accept it.

**Status.** Verified by the workflow in `.github/workflows/build.yml`: all modules build, every
module is replayed in the independent kernel checker, 84 theorems use only the standard axioms
(`propext`, `Quot.sound`, `Classical.choice`), and all 11 false controls are rejected. First green
commit and run are recorded in [`PROVENANCE.md`](PROVENANCE.md).

## What is proved

| File | Theorems | Paper | What it does |
| :--- | :-: | :--- | :--- |
| [`Neutrinos/CrossLink.lean`](Neutrinos/CrossLink.lean) | 4 | speed bound | `\|2 Re(conj a * (-I h b))\| <= 2 ‖h‖ ‖a‖ ‖b‖`; with `A = ‖a‖²`, `R = ‖b‖²`, `A + R <= 1`: `(2 Re(...))² <= 4 ‖h‖² A (1 - A)`; for `h = k/√3` the energy `E_B = ‖h‖² = k²/3` |
| [`Neutrinos/Frobenius.lean`](Neutrinos/Frobenius.lean) | 5 | definitions | squared Frobenius norm, self-commutator `[L, L^H]`, and small helper identities |
| [`Neutrinos/TwoMoment.lean`](Neutrinos/TwoMoment.lean) | 10 | connection energy | for `L = [[0, -I k/√3], [-I k/√3, -κ]]`: `(1/8) ‖[L, L^H]‖_F² = κ² k²/3` |
| [`Neutrinos/SplitRate.lean`](Neutrinos/SplitRate.lean) | 21 | connection energy | for the `3 x 3` chain with couplings `a = k/√3`, `b = 2k/√15` and damping `(0, κ1, κ2)`: `(1/8) ‖[L, L^H]‖_F² = k² κ1²/3 + (4k²/15)(κ2 - κ1)²` |
| [`Neutrinos/Shear.lean`](Neutrinos/Shear.lean) | 10 | shear counterexample | the response `R00(κ2) = 1/(1 + (1/3)/(2 + (4/15)/(1 + κ2)))` equals `2(15κ2 + 17)/(35κ2 + 39)` for `κ2 > -1`; `R00(1) = 32/37`; `dR00/dκ2 = -5/1369` at `κ2 = 1`; the energy `a²κ1² + b²(κ2 - κ1)²` has derivative `0` there |
| [`Neutrinos/ShearComplex.lean`](Neutrinos/ShearComplex.lean) | 14 | shear counterexample | the same response as the `(0,0)` entry of the inverse of the explicit complex matrix `s I + i k M + D`: it equals `cf(κ2)` for `a² = 1/3`, `b² = 4/15`, `κ2 > -1`, and `32/37` at `κ2 = 1` |
| [`Neutrinos/Propagator.lean`](Neutrinos/Propagator.lean) | 6 | hidden propagator | `exp(t (X - σ 1)) = exp(-σ t) exp(t X)`; all `X - σ(t) 1` commute pairwise; the two-step product formula |
| [`Neutrinos/KillLine.lean`](Neutrinos/KillLine.lean) | 6 | pre-registered verdicts | `G = (dc - 49773/100000)/(52832/100000 - 49773/100000)`; Test D `G = 472/3059`, Test C `G = 1983/3059`, Test B `G = 970/3059`, and each tolerance comparison with `0.08` |
| [`Neutrinos/Memory.lean`](Neutrinos/Memory.lean) | 8 | *What the Present Must Keep* | the sign wall sits on the self-adjoint line (`y² = -y ↔ y = 0` for `\|y\| < 1/4`); a rank-one `r vᵀ` with `v·r = 0` squares to zero, so its trace form is null; the exact one-mode gap of the offset speed limit, `4(ċ² + \|ḃ\|²)c(1-c) - ċ² = 4(Im b̄ḃ)²`, and its sign; the one-mode speed limit `Ȧ² <= 4gA(1-A)`; the middle ladder rung `S₀² <= S₋₂ S₂`; the ledger's reading of a constant `log(λ+c) = log λ + log(1 + c/λ)` |
| | **84** | | |

The headline statements, exactly as written in Lean, are listed in
[`docs/STATEMENTS.md`](docs/STATEMENTS.md).

The shear counterexample in one line: at equal damping rates the connection energy is stationary
in `κ2` (derivative `0`) while the linear response is not (derivative `-5/1369`), so the energy
alone cannot control the response there.

## The joint paper

*What the Present Must Keep: the Weight Between, the Speed of the Record, and the Wall It Survives*
(version 1.0, 1 November 2026) joins this neutrino work to *The Weight Between*, *The Offset Speed
Limit*, *Light Keeps the Ledger* and *The Ledger Outlives the Metric*. Its finite statements that
are pure algebra are in [`Neutrinos/Memory.lean`](Neutrinos/Memory.lean); the analytic, contour and
variational steps are written proofs in the paper's Appendix A. The paper (version 1.1: PDF, HTML and source) is in [`paper/joint/`](paper/joint/).

## False controls

[`FalseControls/`](FalseControls/) holds eleven files, each stating something deliberately false.
Each must fail to compile, and fail for a mathematical reason rather than a typo:

| File | The false claim |
| :--- | :--- |
| `ResponseValue.lean` | `R00(1) = 33/37` |
| `ResponseDerivative.lean` | `-20/(35·1 + 39)² = 0` |
| `EnergyDerivative.lean` | the energy has derivative `-5/1369` at equal rates |
| `CrossLinkFactor.lean` | CrossLink with factor 1 instead of 2 (false: `a = b = 1`, `h = I` gives `2 > 1`) |
| `EnergyCoefficient.lean` | two-moment energy `κ² k²/2` instead of `κ² k²/3` |
| `SplitRateSecondLink.lean` | three-moment energy with `κ2²` in place of `(κ2 - κ1)²` |
| `PropagatorSign.lean` | collision factor `exp(+σ t)` instead of `exp(-σ t)` |
| `KillLineTestD.lean` | Test D lies within `0.08` of `0.30` |
| `KillLineTestB.lean` | Test B lies within `0.08` of `0.431` |
| `MemoryWallNoBox.lean` | `y² = -y` forces `y = 0` without the box (false: `y = -1`) |
| `MemoryGapFactor.lean` | the one-mode gap with `2` in place of `4` (false at `c = 1/2`, `b = 1/2`, `ḃ = i`) |

## How to check

```
lake update
lake exe cache get
lake build
lake env leanchecker Neutrinos.CrossLink     # and each other module
python3 scripts/verify.py                    # axiom audit, inventory, false controls
```

`scripts/verify.py` writes its report to `verification/`. The audit requires every theorem to
use only `propext`, `Classical.choice` and `Quot.sound`, and the source scan rejects `sorry`,
`axiom` and `native_decide`.

What is not proved is listed in [`LIMITATIONS.md`](LIMITATIONS.md). Where the pieces came from is
in [`PROVENANCE.md`](PROVENANCE.md); the use of AI is in [`AI_USE.md`](AI_USE.md).
