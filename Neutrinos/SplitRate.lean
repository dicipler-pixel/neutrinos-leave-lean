/-
Neutrinos: connection energy of the three-moment chain with split damping
(Jeromie Beasley, 31 October 2026).
L = [[0, -I a, 0], [-I a, -κ1, -I b], [0, -I b, -κ2]], a = k/√3, b = 2k/√15.
Developed with AI assistance.
-/
import Mathlib
import Neutrinos.Frobenius

namespace Neutrinos.SplitRate

open Complex Neutrinos.Frobenius

/-- The three-moment generator, off-diagonals `a` (0-1) and `b` (1-2), diagonal `(0, -κ1, -κ2)`. -/
noncomputable def L3 (a b κ1 κ2 : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![0, -I * (a : ℂ), 0;
     -I * (a : ℂ), -(κ1 : ℂ), -I * (b : ℂ);
     0, -I * (b : ℂ), -(κ2 : ℂ)]

theorem L3_00 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 0 0 = 0 := by first | rfl | simp [L3]
theorem L3_01 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 0 1 = -I * (a : ℂ) := by first | rfl | simp [L3]
theorem L3_02 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 0 2 = 0 := by first | rfl | simp [L3]
theorem L3_10 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 1 0 = -I * (a : ℂ) := by first | rfl | simp [L3]
theorem L3_11 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 1 1 = -(κ1 : ℂ) := by first | rfl | simp [L3]
theorem L3_12 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 1 2 = -I * (b : ℂ) := by first | rfl | simp [L3]
theorem L3_20 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 2 0 = 0 := by first | rfl | simp [L3]
theorem L3_21 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 2 1 = -I * (b : ℂ) := by first | rfl | simp [L3]
theorem L3_22 (a b κ1 κ2 : ℝ) : L3 a b κ1 κ2 2 2 = -(κ2 : ℂ) := by first | rfl | simp [L3]

theorem sc_00 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 0 0 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_02 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 0 2 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_20 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 2 0 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_11 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 1 1 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_22 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 2 2 = 0 := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  ring

theorem sc_01 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 0 1 = I * ((2 * a * κ1 : ℝ) : ℂ) := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  push_cast
  ring

theorem sc_10 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 1 0 = -(I * ((2 * a * κ1 : ℝ) : ℂ)) := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  push_cast
  ring

theorem sc_12 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 1 2 = I * ((2 * b * (κ2 - κ1) : ℝ) : ℂ) := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  push_cast
  ring

theorem sc_21 (a b κ1 κ2 : ℝ) :
    selfComm (L3 a b κ1 κ2) 2 1 = -(I * ((2 * b * (κ2 - κ1) : ℝ) : ℂ)) := by
  rw [selfComm, Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  simp only [Fin.sum_univ_three, Matrix.conjTranspose_apply, L3_00, L3_01, L3_02, L3_10, L3_11, L3_12, L3_20, L3_21, L3_22,
    star_zero, star_negI_mul, star_neg_real]
  push_cast
  ring


/-- Energy in terms of the couplings `a`, `b`:
`(1/8) ‖[L, L^H]‖_F^2 = a^2 κ1^2 + b^2 (κ2 - κ1)^2`. -/
theorem splitRateEnergy_ab (a b κ1 κ2 : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 a b κ1 κ2)) = a ^ 2 * κ1 ^ 2 + b ^ 2 * (κ2 - κ1) ^ 2 := by
  rw [frobSq_three, sc_00, sc_01, sc_02, sc_10, sc_11, sc_12, sc_20, sc_21, sc_22,
    norm_neg, norm_neg, norm_sq_I_mul_real, norm_sq_I_mul_real, norm_zero]
  ring

/-- SplitRateEnergy: with `a = k/√3`, `b = 2k/√15`,
`(1/8) ‖[L, L^H]‖_F^2 = k^2 κ1^2 / 3 + (4 k^2 / 15) (κ2 - κ1)^2`. -/
theorem splitRateEnergy (k κ1 κ2 : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 (k / Real.sqrt 3) (2 * k / Real.sqrt 15) κ1 κ2))
      = k ^ 2 * κ1 ^ 2 / 3 + (4 * k ^ 2 / 15) * (κ2 - κ1) ^ 2 := by
  have ha : (k / Real.sqrt 3) ^ 2 = k ^ 2 / 3 := by
    rw [div_pow, Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)]
  have hb : (2 * k / Real.sqrt 15) ^ 2 = 4 * k ^ 2 / 15 := by
    rw [div_pow, mul_pow, Real.sq_sqrt (show (0:ℝ) ≤ 15 by norm_num)]; ring
  rw [splitRateEnergy_ab, ha, hb]
  ring

/-- When the two damping rates agree the second link contributes nothing. -/
theorem splitRateEnergy_equal_rates (a b κ : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 a b κ κ)) = a ^ 2 * κ ^ 2 := by
  rw [splitRateEnergy_ab]; ring

end Neutrinos.SplitRate
