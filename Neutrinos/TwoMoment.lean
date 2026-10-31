/-
Neutrinos: connection energy of the two-moment chain (Jeromie Beasley, 31 October 2026).
L = [[0, -I c], [-I c, -kappa]] with c = k / sqrt 3. The self-commutator C = L L^H - L^H L
satisfies (1/8) sum |C_ij|^2 = kappa^2 k^2 / 3.
Developed with AI assistance.
-/
import Mathlib
import Neutrinos.Frobenius

namespace Neutrinos.TwoMoment

open Complex Neutrinos.Frobenius

/-- The two-moment generator with coupling `c` and damping `κ`. -/
noncomputable def L2 (c κ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![0, -I * (c : ℂ); -I * (c : ℂ), -(κ : ℂ)]

theorem L2_00 (c κ : ℝ) : L2 c κ 0 0 = 0 := by first | rfl | simp [L2]
theorem L2_01 (c κ : ℝ) : L2 c κ 0 1 = -I * (c : ℂ) := by first | rfl | simp [L2]
theorem L2_10 (c κ : ℝ) : L2 c κ 1 0 = -I * (c : ℂ) := by first | rfl | simp [L2]
theorem L2_11 (c κ : ℝ) : L2 c κ 1 1 = -(κ : ℂ) := by first | rfl | simp [L2]

theorem sc_00 (c κ : ℝ) : selfComm (L2 c κ) 0 0 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_two, Matrix.conjTranspose_apply, L2_00, L2_01, L2_10, L2_11,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_11 (c κ : ℝ) : selfComm (L2 c κ) 1 1 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_two, Matrix.conjTranspose_apply, L2_00, L2_01, L2_10, L2_11,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_01 (c κ : ℝ) : selfComm (L2 c κ) 0 1 = I * ((2 * c * κ : ℝ) : ℂ) := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_two, Matrix.conjTranspose_apply, L2_00, L2_01, L2_10, L2_11,
    star_zero, star_negI_mul, star_neg_real]
  push_cast
  ring

theorem sc_10 (c κ : ℝ) : selfComm (L2 c κ) 1 0 = -(I * ((2 * c * κ : ℝ) : ℂ)) := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_two, Matrix.conjTranspose_apply, L2_00, L2_01, L2_10, L2_11,
    star_zero, star_negI_mul, star_neg_real]
  push_cast
  ring

/-- Energy in terms of the coupling `c`: `(1/8) ‖[L, L^H]‖_F^2 = c^2 κ^2`. -/
theorem twoMomentEnergy_c (c κ : ℝ) :
    (1 / 8) * frobSq (selfComm (L2 c κ)) = c ^ 2 * κ ^ 2 := by
  rw [frobSq_two, sc_00, sc_01, sc_10, sc_11, norm_neg, norm_sq_I_mul_real, norm_zero]
  ring

/-- TwoMomentConnectionEnergy: for `L = [[0, -I k/√3], [-I k/√3, -κ]]`,
`(1/8) ‖[L, L^H]‖_F^2 = κ^2 k^2 / 3`. -/
theorem twoMomentConnectionEnergy (k κ : ℝ) :
    (1 / 8) * frobSq (selfComm (L2 (k / Real.sqrt 3) κ)) = κ ^ 2 * (k ^ 2 / 3) := by
  rw [twoMomentEnergy_c, div_pow, Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)]
  ring

end Neutrinos.TwoMoment
