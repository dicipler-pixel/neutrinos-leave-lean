/-
Neutrinos: the shear counterexample (Jeromie Beasley, 31 October 2026).
With k = s = κ1 = 1 and three Legendre moments, the linear response at the monopole is
R00(κ2) = 1 / (s + a² / (s + κ1 + b² / (s + κ2))), a² = 1/3, b² = 4/15.
At κ2 = κ1 = 1 the response is 32/37 and it still changes with κ2 (derivative -5/1369),
while the connection energy a² κ1² + b² (κ2 - κ1)² is stationary there (derivative 0).
So the energy does not control the response at equal rates.
Developed with AI assistance.
-/
import Mathlib

namespace Neutrinos.Shear

open Complex

/-! ### The real (Schur) form -/

/-- `R00(κ2)` for `s = κ1 = k = 1`, `a² = 1/3`, `b² = 4/15`:
`1 / (1 + (1/3) / ((1 + 1) + (4/15) / (1 + κ2)))`. -/
noncomputable def R00 (x : ℝ) : ℝ :=
  1 / (1 + (1 / 3) / ((1 + 1) + (4 / 15) / (1 + x)))

/-- The closed form of the same rational function. -/
noncomputable def cf (x : ℝ) : ℝ := 2 * (15 * x + 17) / (35 * x + 39)

/-- Numerator `64/15` over denominator `74/15` at `κ2 = 1`. -/
theorem R00_one : R00 1 = 32 / 37 := by
  norm_num [R00]

theorem cf_one : cf 1 = 32 / 37 := by
  norm_num [cf]

theorem R00_eq_cf (x : ℝ) (hx : -1 < x) : R00 x = cf x := by
  have h1 : (1 : ℝ) + x ≠ 0 := by
    have : (0 : ℝ) < 1 + x := by linarith
    exact ne_of_gt this
  have h2 : (30 * x + 34 : ℝ) ≠ 0 := by
    have : (0 : ℝ) < 30 * x + 34 := by linarith
    exact ne_of_gt this
  have h3 : (35 * x + 39 : ℝ) ≠ 0 := by
    have : (0 : ℝ) < 35 * x + 39 := by linarith
    exact ne_of_gt this
  have e1 : (1 + 1 : ℝ) + 4 / 15 / (1 + x) = (30 * x + 34) / (15 * (1 + x)) := by
    first
    | (field_simp; ring)
    | field_simp
  have e2 : (1 : ℝ) + (1 / 3) / ((30 * x + 34) / (15 * (1 + x))) = (35 * x + 39) / (30 * x + 34) := by
    first
    | (field_simp; ring)
    | field_simp
  have e3 : (2 * (15 * x + 17) : ℝ) = 30 * x + 34 := by ring
  unfold R00 cf
  rw [e1, e2, one_div_div, e3]

/-- Derivative of the closed form at `κ2 = 1` is `-5/1369`. -/
theorem cf_hasDerivAt : HasDerivAt cf (-5 / 1369) 1 := by
  have hc : HasDerivAt (fun x : ℝ => 2 * (15 * x + 17)) 30 1 :=
    ((((hasDerivAt_id' (1 : ℝ)).const_mul 15).add_const 17).const_mul 2).congr_deriv (by norm_num)
  have hd : HasDerivAt (fun x : ℝ => 35 * x + 39) 35 1 :=
    (((hasDerivAt_id' (1 : ℝ)).const_mul 35).add_const 39).congr_deriv (by norm_num)
  have h := hc.div hd (by norm_num)
  exact h.congr_deriv (by norm_num)

/-- The response `R00` has derivative `-5/1369` in `κ2` at `κ2 = κ1 = 1`. -/
theorem R00_hasDerivAt : HasDerivAt R00 (-5 / 1369) 1 := by
  have hev : R00 =ᶠ[nhds (1 : ℝ)] cf := by
    filter_upwards [Ioi_mem_nhds (show (-1 : ℝ) < 1 by norm_num)] with x hx
    exact R00_eq_cf x (Set.mem_Ioi.mp hx)
  exact cf_hasDerivAt.congr_of_eventuallyEq hev

/-- The derivative formula `-20 / (35 κ2 + 39)^2` evaluated at `κ2 = 1` is `-5/1369`. -/
theorem R00_derivative_formula_at_one : -20 / (35 * (1 : ℝ) + 39) ^ 2 = -5 / 1369 := by
  norm_num

/-! ### The energy -/

/-- The connection energy `a² κ1² + b² (κ2 - κ1)²` at `κ1 = 1`, `a² = 1/3`, `b² = 4/15`. -/
noncomputable def shearEnergy (x : ℝ) : ℝ := (1 / 3) * 1 ^ 2 + (4 / 15) * (x - 1) ^ 2

/-- General form: `d/dκ2 (a² κ1² + b² (κ2 - κ1)²) = 2 b² (κ2 - κ1)`. -/
theorem energy_hasDerivAt (a2 b2 κ1 x0 : ℝ) :
    HasDerivAt (fun x : ℝ => a2 * κ1 ^ 2 + b2 * (x - κ1) ^ 2) (2 * b2 * (x0 - κ1)) x0 := by
  have hf : HasDerivAt (fun x : ℝ => (x - κ1) * (x - κ1))
      (1 * (x0 - κ1) + (x0 - κ1) * 1) x0 :=
    ((hasDerivAt_id' x0).sub_const κ1).mul ((hasDerivAt_id' x0).sub_const κ1)
  have hg := (hf.const_mul b2).const_add (a2 * κ1 ^ 2)
  have hfun : (fun x : ℝ => a2 * κ1 ^ 2 + b2 * (x - κ1) ^ 2)
      = fun x : ℝ => a2 * κ1 ^ 2 + b2 * ((x - κ1) * (x - κ1)) := by
    funext x; ring
  rw [hfun]
  exact hg.congr_deriv (by ring)

/-- The energy is stationary in `κ2` at `κ2 = κ1 = 1`. -/
theorem shearEnergy_hasDerivAt : HasDerivAt shearEnergy 0 1 := by
  have h := energy_hasDerivAt (1 / 3) (4 / 15) 1 1
  have h0 : (2 * (4 / 15) * ((1 : ℝ) - 1) : ℝ) = 0 := by norm_num
  rw [h0] at h
  exact h

/-- The energy derivative `2 b² (κ2 - κ1)` vanishes at `κ2 = κ1`. -/
theorem energy_derivative_zero_at_equal (b2 κ : ℝ) : 2 * b2 * (κ - κ) = 0 := by
  ring

/-- ShearCounterexample: at `k = s = κ1 = κ2 = 1` the response is `32/37`, it is not stationary
in `κ2` (derivative `-5/1369`), and the connection energy is stationary (derivative `0`). -/
theorem shearCounterexample :
    R00 1 = 32 / 37 ∧ HasDerivAt R00 (-5 / 1369) 1 ∧ HasDerivAt shearEnergy 0 1
      ∧ (-5 / 1369 : ℝ) ≠ 0 :=
  ⟨R00_one, R00_hasDerivAt, shearEnergy_hasDerivAt, by norm_num⟩

end Neutrinos.Shear
