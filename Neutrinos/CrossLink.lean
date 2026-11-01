/-
Neutrinos: the cross-link inequality (Jeromie Beasley, 31 October 2026).
The core inequality behind the speed bound (A')^2 <= 4 E_B A (1 - A) for a tridiagonal
moment chain in which only the l = 1 moment talks to the monopole.
Developed with AI assistance.
-/
import Mathlib

namespace Neutrinos.CrossLink

open Complex

/-- The cross term `2 Re(conj a * (-I * h * b))` of the amplitude derivative. -/
noncomputable def cross (a b h : ℂ) : ℝ :=
  2 * (starRingEnd ℂ a * (-I * h * b)).re

/-- The norm of the product behind the cross term. -/
theorem norm_cross_product (a b h : ℂ) :
    ‖starRingEnd ℂ a * (-I * h * b)‖ = ‖a‖ * ‖h‖ * ‖b‖ := by
  rw [norm_mul, norm_mul, norm_mul, norm_neg, Complex.norm_I, Complex.norm_conj]
  ring

/-- CrossLink: `|2 Re(conj a * (-I h b))| <= 2 ‖h‖ ‖a‖ ‖b‖`. -/
theorem crossLink (a b h : ℂ) :
    |2 * (starRingEnd ℂ a * (-I * h * b)).re| ≤ 2 * ‖h‖ * ‖a‖ * ‖b‖ := by
  have h1 : |(starRingEnd ℂ a * (-I * h * b)).re| ≤ ‖starRingEnd ℂ a * (-I * h * b)‖ :=
    Complex.abs_re_le_norm _
  rw [norm_cross_product] at h1
  rw [abs_mul, abs_two]
  nlinarith [h1]

/-- Corollary: with `A = ‖a‖^2`, `R = ‖b‖^2` and `A + R <= 1`,
`(2 Re(conj a * (-I h b)))^2 <= 4 ‖h‖^2 A (1 - A)`. -/
theorem crossLink_sq (a b h : ℂ) (A R : ℝ) (hA : A = ‖a‖ ^ 2) (hR : R = ‖b‖ ^ 2)
    (hAR : A + R ≤ 1) :
    (2 * (starRingEnd ℂ a * (-I * h * b)).re) ^ 2 ≤ 4 * ‖h‖ ^ 2 * A * (1 - A) := by
  have h1 := crossLink a b h
  have h0 : 0 ≤ |2 * (starRingEnd ℂ a * (-I * h * b)).re| := abs_nonneg _
  have h2 : |2 * (starRingEnd ℂ a * (-I * h * b)).re| ^ 2 ≤ (2 * ‖h‖ * ‖a‖ * ‖b‖) ^ 2 :=
    pow_le_pow_left₀ h0 h1 2
  rw [sq_abs] at h2
  have h3 : (2 * ‖h‖ * ‖a‖ * ‖b‖) ^ 2 = 4 * ‖h‖ ^ 2 * A * R := by
    rw [hA, hR]; ring
  have h4 : 0 ≤ 4 * ‖h‖ ^ 2 * A := by
    rw [hA]; positivity
  have h5 : 4 * ‖h‖ ^ 2 * A * R ≤ 4 * ‖h‖ ^ 2 * A * (1 - A) :=
    mul_le_mul_of_nonneg_left (by linarith) h4
  linarith

/-- The same bound for the paper's coupling `h = k / sqrt 3`: `E_B = ‖h‖^2 = k^2 / 3`. -/
theorem crossLink_sq_k (a b : ℂ) (k : ℝ) (A R : ℝ) (hA : A = ‖a‖ ^ 2) (hR : R = ‖b‖ ^ 2)
    (hAR : A + R ≤ 1) :
    (2 * (starRingEnd ℂ a * (-I * ((k / Real.sqrt 3 : ℝ) : ℂ) * b)).re) ^ 2
      ≤ 4 * (k ^ 2 / 3) * A * (1 - A) := by
  have h := crossLink_sq a b ((k / Real.sqrt 3 : ℝ) : ℂ) A R hA hR hAR
  have hn : ‖((k / Real.sqrt 3 : ℝ) : ℂ)‖ ^ 2 = k ^ 2 / 3 := by
    rw [Complex.norm_real, Real.norm_eq_abs, sq_abs, div_pow, Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)]
  rw [hn] at h
  exact h

end Neutrinos.CrossLink
