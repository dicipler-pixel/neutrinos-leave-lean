/-
Neutrinos: finite statements of "What the Present Must Keep" (Jeromie Beasley, 1 November 2026).
The sign wall sits on the self-adjoint line, its null direction is nilpotent, the exact gap of
the offset speed limit for one mode, the one-mode speed limit, the middle rung of the gap
ladder, and the ledger's reading of an added constant.
Developed with AI assistance.
-/
import Mathlib

namespace Neutrinos.Memory

open Complex

/-- Proposition 14(i): in the chart, `P = P^dagger` needs `w = conj z`, i.e. `y^2 = -y`;
inside the box `|y| < 1/4` this happens exactly on the line `y = 0`. -/
theorem selfadjoint_line_iff (y : ℝ) (hy : |y| < 1 / 4) : y ^ 2 = -y ↔ y = 0 := by
  constructor
  · intro h
    have hm : y * (y + 1) = 0 := by linear_combination h
    rcases mul_eq_zero.mp hm with h0 | h1
    · exact h0
    · exfalso
      have hb := abs_lt.mp hy
      linarith [hb.1]
  · intro h
    subst h
    ring

/-- Proposition 14(iii): a rank-one matrix `r v^T` with `v . r = 0` squares to zero. -/
theorem rank_one_nilpotent (r0 r1 v0 v1 : ℂ) (h : v0 * r0 + v1 * r1 = 0) :
    !![r0 * v0, r0 * v1; r1 * v0, r1 * v1] * !![r0 * v0, r0 * v1; r1 * v0, r1 * v1] = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  · simp [Matrix.mul_apply, Fin.sum_univ_two] <;> linear_combination r0 * v0 * h
  · simp [Matrix.mul_apply, Fin.sum_univ_two] <;> linear_combination r0 * v1 * h
  · simp [Matrix.mul_apply, Fin.sum_univ_two] <;> linear_combination r1 * v0 * h
  · simp [Matrix.mul_apply, Fin.sum_univ_two] <;> linear_combination r1 * v1 * h

/-- A nilpotent tangent `D^2 = 0` is a null direction of `q(D) = Re Tr(D^2) / 2`. -/
theorem nilpotent_null (D : Matrix (Fin 2) (Fin 2) ℂ) (h : D * D = 0) :
    (Matrix.trace (D * D)).re / 2 = 0 := by
  rw [h]
  simp

/-- Theorem 8, one accessible mode: the exact gap
`4 g S - tau_dot^2 = 4 (Im conj(b) b_dot)^2 / (c(1-c))^2`, written over the common
denominator. Here `b = br + i bi`, `b_dot = dr + i di`, idempotence gives
`|b|^2 = c(1-c)` and `2 Re(conj b * b_dot) = c_dot (1 - 2c)`. -/
theorem offset_gap_identity (c cd br bi dr di : ℝ)
    (h1 : br ^ 2 + bi ^ 2 = c * (1 - c))
    (h2 : 2 * (br * dr + bi * di) = cd * (1 - 2 * c)) :
    4 * (cd ^ 2 + (dr ^ 2 + di ^ 2)) * (c * (1 - c)) - cd ^ 2 = 4 * (br * di - bi * dr) ^ 2 := by
  linear_combination (-4 * (dr ^ 2 + di ^ 2)) * h1 + (2 * (br * dr + bi * di) + cd * (1 - 2 * c)) * h2

/-- The gap is never negative, so the speed limit holds for one mode. -/
theorem offset_gap_nonneg (c cd br bi dr di : ℝ)
    (h1 : br ^ 2 + bi ^ 2 = c * (1 - c))
    (h2 : 2 * (br * dr + bi * di) = cd * (1 - 2 * c)) :
    cd ^ 2 ≤ 4 * (cd ^ 2 + (dr ^ 2 + di ^ 2)) * (c * (1 - c)) := by
  have e := offset_gap_identity c cd br bi dr di h1 h2
  nlinarith [sq_nonneg (br * di - bi * dr)]

/-- Equation (14): the offset speed limit for one mode, written in the kept population.
If `(A_dot / (A(1-A)))^2 <= 4 g / (A(1-A))` then `A_dot^2 <= 4 g A (1 - A)`. -/
theorem one_mode_speed (A Ad g : ℝ) (hA0 : 0 < A) (hA1 : A < 1)
    (h : (Ad / (A * (1 - A))) ^ 2 ≤ 4 * g * (1 / (A * (1 - A)))) :
    Ad ^ 2 ≤ 4 * g * A * (1 - A) := by
  have hp : 0 < A * (1 - A) := mul_pos hA0 (by linarith)
  have hp0 : A * (1 - A) ≠ 0 := ne_of_gt hp
  have key : Ad ^ 2 = (Ad / (A * (1 - A))) ^ 2 * (A * (1 - A)) ^ 2 := by
    rw [div_pow, div_mul_cancel₀ _ (pow_ne_zero 2 hp0)]
  have hsq : 0 ≤ (A * (1 - A)) ^ 2 := sq_nonneg _
  have step := mul_le_mul_of_nonneg_right h hsq
  have tail : 4 * g * (1 / (A * (1 - A))) * (A * (1 - A)) ^ 2 = 4 * g * A * (1 - A) := by
    field_simp
  linarith [key, step, tail]

/-- The middle rung of the gap ladder: `S_0^2 <= S_{-2} S_2` for couplings `a_i` at
nonzero gaps `Delta_i` (Cauchy-Schwarz). -/
theorem ladder_middle_rung {n : ℕ} (a Δ : Fin n → ℝ) (hΔ : ∀ i, Δ i ≠ 0) :
    (∑ i, a i ^ 2) ^ 2 ≤ (∑ i, (a i / Δ i) ^ 2) * (∑ i, (a i * Δ i) ^ 2) := by
  have hcs := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (fun i => a i / Δ i) (fun i => a i * Δ i)
  have e : (∑ i, a i / Δ i * (a i * Δ i)) = ∑ i, a i ^ 2 := by
    apply Finset.sum_congr rfl
    intro i _
    field_simp [hΔ i]
  simpa [e] using hcs

/-- Proposition 10(c): the ledger reads an added constant. For a selected eigenvalue
`lam > 0` moved to `lam + c > 0`, `log (lam + c) = log lam + log (1 + c / lam)`. -/
theorem ledger_reads_constant (lam c : ℝ) (hl : 0 < lam) (hlc : 0 < lam + c) :
    Real.log (lam + c) = Real.log lam + Real.log (1 + c / lam) := by
  have hq : 0 < 1 + c / lam := by
    have : 1 + c / lam = (lam + c) / lam := by field_simp
    rw [this]
    exact div_pos hlc hl
  rw [← Real.log_mul (ne_of_gt hl) (ne_of_gt hq)]
  congr 1
  field_simp

end Neutrinos.Memory
