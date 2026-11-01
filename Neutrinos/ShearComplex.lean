/-
Neutrinos: the complex resolvent form of the shear counterexample
(Jeromie Beasley, 31 October 2026).
R00 = [(s I + i k M + D)^{-1}]_{00} for the three-moment truncation with s = k = κ1 = 1,
M having off-diagonals a = 1/√3 and b = 2/√15, D = diag(0, 1, κ2). Proved here as
a statement about the inverse of the 3x3 complex matrix, for every real a, b with
a² = 1/3, b² = 4/15 and every κ2 > -1.
Developed with AI assistance.
-/
import Mathlib
import Neutrinos.Shear

namespace Neutrinos.ShearComplex

open Complex Neutrinos.Shear

/-- `s I + i k M + D` with `s = k = κ1 = 1`: diagonal `(1, 2, 1 + κ2)`, off-diagonals `i a`, `i b`. -/
noncomputable def Aresp (a b x : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![1, I * (a : ℂ), 0;
     I * (a : ℂ), 2, I * (b : ℂ);
     0, I * (b : ℂ), 1 + (x : ℂ)]

theorem A00 (a b x : ℝ) : Aresp a b x 0 0 = 1 := by first | rfl | simp [Aresp]
theorem A01 (a b x : ℝ) : Aresp a b x 0 1 = I * (a : ℂ) := by first | rfl | simp [Aresp]
theorem A02 (a b x : ℝ) : Aresp a b x 0 2 = 0 := by first | rfl | simp [Aresp]
theorem A10 (a b x : ℝ) : Aresp a b x 1 0 = I * (a : ℂ) := by first | rfl | simp [Aresp]
theorem A11 (a b x : ℝ) : Aresp a b x 1 1 = 2 := by first | rfl | simp [Aresp]
theorem A12 (a b x : ℝ) : Aresp a b x 1 2 = I * (b : ℂ) := by first | rfl | simp [Aresp]
theorem A20 (a b x : ℝ) : Aresp a b x 2 0 = 0 := by first | rfl | simp [Aresp]
theorem A21 (a b x : ℝ) : Aresp a b x 2 1 = I * (b : ℂ) := by first | rfl | simp [Aresp]
theorem A22 (a b x : ℝ) : Aresp a b x 2 2 = 1 + (x : ℂ) := by first | rfl | simp [Aresp]

/-- The determinant: `(1 + κ2)(2 + a²) + b²`. -/
theorem det_Aresp (a b x : ℝ) :
    (Aresp a b x).det = (((1 + x) * (2 + a ^ 2) + b ^ 2 : ℝ) : ℂ) := by
  rw [Matrix.det_fin_three]
  simp only [A00, A01, A02, A10, A11, A12, A20, A21, A22]
  push_cast
  linear_combination (-((b : ℂ) ^ 2 + (a : ℂ) ^ 2 * (1 + (x : ℂ)))) * Complex.I_sq

/-- The (0,0) entry of the inverse is the cofactor over the determinant. -/
theorem inv_00 (a b x : ℝ) :
    (Aresp a b x)⁻¹ 0 0
      = (Aresp a b x).det⁻¹ * (Aresp a b x 1 1 * Aresp a b x 2 2 - Aresp a b x 1 2 * Aresp a b x 2 1) := by
  rw [Matrix.inv_def, Ring.inverse_eq_inv', Matrix.smul_apply, Matrix.adjugate_fin_three]
  simp [smul_eq_mul]

/-- The cofactor: `2 (1 + κ2) + b²`. -/
theorem cofactor_00 (a b x : ℝ) :
    Aresp a b x 1 1 * Aresp a b x 2 2 - Aresp a b x 1 2 * Aresp a b x 2 1
      = ((2 * (1 + x) + b ^ 2 : ℝ) : ℂ) := by
  simp only [A11, A12, A21, A22]
  push_cast
  linear_combination (-((b : ℂ) ^ 2)) * Complex.I_sq

/-- The complex resolvent response equals the real Schur-form closed form `cf κ2`. -/
theorem resolvent_00_eq_cf (a b x : ℝ) (ha : a ^ 2 = 1 / 3) (hb : b ^ 2 = 4 / 15) (hx : -1 < x) :
    (Aresp a b x)⁻¹ 0 0 = ((cf x : ℝ) : ℂ) := by
  have h3 : (35 * x + 39 : ℝ) ≠ 0 := by
    have : (0 : ℝ) < 35 * x + 39 := by linarith
    exact ne_of_gt this
  have hD : ((1 + x) * (2 + a ^ 2) + b ^ 2 : ℝ) = (35 * x + 39) / 15 := by
    rw [ha, hb]; ring
  have hN : (2 * (1 + x) + b ^ 2 : ℝ) = (30 * x + 34) / 15 := by
    rw [hb]; ring
  have hreal : (2 * (1 + x) + b ^ 2) / ((1 + x) * (2 + a ^ 2) + b ^ 2) = cf x := by
    rw [hD, hN]
    unfold cf
    first
    | (field_simp; ring)
    | field_simp
  rw [inv_00, det_Aresp, cofactor_00, ← hreal]
  push_cast
  ring

/-- At `κ2 = 1` the complex resolvent response is exactly `32/37`. -/
theorem resolvent_00_at_one (a b : ℝ) (ha : a ^ 2 = 1 / 3) (hb : b ^ 2 = 4 / 15) :
    (Aresp a b 1)⁻¹ 0 0 = ((32 / 37 : ℝ) : ℂ) := by
  rw [resolvent_00_eq_cf a b 1 ha hb (by norm_num), cf_one]

end Neutrinos.ShearComplex
