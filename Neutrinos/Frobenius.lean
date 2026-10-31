/-
Neutrinos: Frobenius norm and self-commutator (Jeromie Beasley, 31 October 2026).
Definitions shared by the connection-energy files.
Developed with AI assistance.
-/
import Mathlib

namespace Neutrinos.Frobenius

open Complex
open scoped Matrix

/-- The squared Frobenius norm `sum_ij |M_ij|^2`. -/
noncomputable def frobSq {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) : ℝ :=
  ∑ i, ∑ j, ‖M i j‖ ^ 2

/-- The self-commutator `[L, L^H] = L L^H - L^H L`. -/
noncomputable def selfComm {n : ℕ} (L : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  L * Lᴴ - Lᴴ * L

theorem frobSq_two (M : Matrix (Fin 2) (Fin 2) ℂ) :
    frobSq M = ‖M 0 0‖ ^ 2 + ‖M 0 1‖ ^ 2 + ‖M 1 0‖ ^ 2 + ‖M 1 1‖ ^ 2 := by
  simp only [frobSq, Fin.sum_univ_two]
  ring

theorem frobSq_three (M : Matrix (Fin 3) (Fin 3) ℂ) :
    frobSq M = ‖M 0 0‖ ^ 2 + ‖M 0 1‖ ^ 2 + ‖M 0 2‖ ^ 2
      + (‖M 1 0‖ ^ 2 + ‖M 1 1‖ ^ 2 + ‖M 1 2‖ ^ 2)
      + (‖M 2 0‖ ^ 2 + ‖M 2 1‖ ^ 2 + ‖M 2 2‖ ^ 2) := by
  simp only [frobSq, Fin.sum_univ_three]
  ring

/-- The norm squared of `I * x` for real `x`. -/
theorem norm_sq_I_mul_real (x : ℝ) : ‖I * (x : ℂ)‖ ^ 2 = x ^ 2 := by
  rw [norm_mul, Complex.norm_I, Complex.norm_real, one_mul, Real.norm_eq_abs, sq_abs]

/-- The conjugate of `-I x` for real `x` is `I x`. -/
theorem star_negI_mul (x : ℝ) : star (-I * (x : ℂ)) = I * (x : ℂ) := by
  first
  | simp
  | (apply Complex.ext <;> simp [Complex.star_def])

/-- The conjugate of `-x` for real `x` is `-x`. -/
theorem star_neg_real (x : ℝ) : star (-(x : ℂ)) = -(x : ℂ) := by
  first
  | simp
  | (apply Complex.ext <;> simp [Complex.star_def])

end Neutrinos.Frobenius
