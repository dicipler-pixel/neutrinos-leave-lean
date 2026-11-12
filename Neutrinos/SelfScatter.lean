import Neutrinos.SplitRate

/-!
# Self-scattering is the flux–shear link (v6, Appendix A.13)

McCormick's multigroup collision term, `-κe (I - P0) - κn (I - P0 - P1)`, is
`-diag(0, κe, κe + κn, …)` in the discrete Legendre basis: the split link with
`κ1 = κe`, `κ2 = κe + κn`. Its connection energy is therefore the split-rate
energy with the second jump equal to the self-scattering rate.
-/

namespace Neutrinos.SelfScatter

open Neutrinos.Frobenius Neutrinos.SplitRate

/-- With any streaming weights `a`, `b` (on the bins `a² = k²(1/3 - Δμ²/12)`,
`b² = (4k²/15)(1 - Δμ²)`), the self-scattering energy is `a² κe² + b² κn²`. -/
theorem selfScatterEnergy_ab (a b κe κn : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 a b κe (κe + κn))) = a ^ 2 * κe ^ 2 + b ^ 2 * κn ^ 2 := by
  rw [splitRateEnergy_ab]; ring

/-- In the continuum weights: `k² κe² / 3 + (4 k² / 15) κn²`. -/
theorem selfScatterEnergy (k κe κn : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 (k / Real.sqrt 3) (2 * k / Real.sqrt 15) κe (κe + κn)))
      = k ^ 2 * κe ^ 2 / 3 + (4 * k ^ 2 / 15) * κn ^ 2 := by
  rw [splitRateEnergy]; ring

/-- Without self-scattering the second link carries nothing. -/
theorem selfScatterEnergy_no_nn (a b κe : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 a b κe (κe + 0))) = a ^ 2 * κe ^ 2 := by
  rw [selfScatterEnergy_ab]; ring

end Neutrinos.SelfScatter
