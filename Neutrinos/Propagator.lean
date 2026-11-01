/-
Neutrinos: the scalar-collision propagator (Jeromie Beasley, 31 October 2026).
For a constant collision rate σ the hidden-block propagator factors as
exp(t (X - σ 1)) = exp(-σ t) exp(t X), because a scalar matrix commutes with everything.
For a time-dependent σ(t) all generators X - σ(t) 1 commute pairwise, which is the
commuting lemma that makes the time-ordered exponential exact.
Developed with AI assistance.
-/
import Mathlib

namespace Neutrinos.Propagator

open NormedSpace

variable {n : ℕ}

/-- A real scalar matrix `c • 1` commutes with every complex matrix. -/
theorem commute_real_smul_one (c : ℝ) (X : Matrix (Fin n) (Fin n) ℂ) :
    Commute X (c • (1 : Matrix (Fin n) (Fin n) ℂ)) := by
  show X * (c • (1 : Matrix (Fin n) (Fin n) ℂ)) = (c • (1 : Matrix (Fin n) (Fin n) ℂ)) * X
  first
  | rw [mul_smul_comm, smul_mul_assoc, mul_one, one_mul]
  | rw [Matrix.mul_smul, Matrix.smul_mul, mul_one, one_mul]

/-- The exponential of a real scalar matrix: `exp (c • 1) = (Real.exp c) • 1`. -/
theorem exp_real_smul_one (c : ℝ) :
    exp (c • (1 : Matrix (Fin n) (Fin n) ℂ)) = (Real.exp c) • (1 : Matrix (Fin n) (Fin n) ℂ) := by
  have h1 : c • (1 : Matrix (Fin n) (Fin n) ℂ) = Matrix.diagonal (fun _ => (c : ℂ)) := by
    ext i j
    simp only [Matrix.smul_apply, Matrix.one_apply, Matrix.diagonal_apply]
    split_ifs <;> simp [Complex.real_smul]
  have h2 : (Real.exp c) • (1 : Matrix (Fin n) (Fin n) ℂ)
      = Matrix.diagonal (fun _ => Complex.exp (c : ℂ)) := by
    ext i j
    simp only [Matrix.smul_apply, Matrix.one_apply, Matrix.diagonal_apply]
    split_ifs <;> simp [Complex.real_smul, Complex.ofReal_exp]
  have h3 : exp (fun _ : Fin n => (c : ℂ)) = fun _ => Complex.exp (c : ℂ) := by
    funext i
    rw [Pi.coe_exp]
    exact (congrFun Complex.exp_eq_exp_ℂ (c : ℂ)).symm
  rw [h1, h2, Matrix.exp_diagonal, h3]

/-- ScalarCollisionPropagator: for a constant rate `σ`,
`exp (t • (X - σ • 1)) = (Real.exp (-σ t)) • exp (t • X)`. -/
theorem scalarCollisionPropagator (X : Matrix (Fin n) (Fin n) ℂ) (σ t : ℝ) :
    exp (t • (X - σ • (1 : Matrix (Fin n) (Fin n) ℂ)))
      = (Real.exp (-σ * t)) • exp (t • X) := by
  have hsplit : t • (X - σ • (1 : Matrix (Fin n) (Fin n) ℂ))
      = t • X + (-σ * t) • (1 : Matrix (Fin n) (Fin n) ℂ) := by
    rw [smul_sub, smul_smul, sub_eq_add_neg, show -σ * t = -(t * σ) by ring, neg_smul]
  have hcomm : Commute (t • X) ((-σ * t) • (1 : Matrix (Fin n) (Fin n) ℂ)) :=
    commute_real_smul_one (-σ * t) (t • X)
  rw [hsplit, Matrix.exp_add_of_commute _ _ hcomm, exp_real_smul_one, mul_smul_comm, mul_one]

/-- The commuting lemma behind the time-dependent propagator: the generators `X - a • 1` and
`X - b • 1` commute for all real `a`, `b`. -/
theorem commute_shifted (X : Matrix (Fin n) (Fin n) ℂ) (a b : ℝ) :
    Commute (X - a • (1 : Matrix (Fin n) (Fin n) ℂ)) (X - b • (1 : Matrix (Fin n) (Fin n) ℂ)) := by
  have hXB : Commute X (b • (1 : Matrix (Fin n) (Fin n) ℂ)) :=
    commute_real_smul_one b X
  have hAX : Commute (a • (1 : Matrix (Fin n) (Fin n) ℂ)) X :=
    (commute_real_smul_one a X).symm
  have hAB : Commute (a • (1 : Matrix (Fin n) (Fin n) ℂ)) (b • (1 : Matrix (Fin n) (Fin n) ℂ)) :=
    commute_real_smul_one b (a • (1 : Matrix (Fin n) (Fin n) ℂ))
  exact Commute.sub_left (Commute.sub_right (Commute.refl X) hXB) (Commute.sub_right hAX hAB)

/-- For any real function `σ`, the generators `X - σ(s) • 1` and `X - σ(t) • 1` commute pairwise,
so the time-ordered product of exponentials needs no ordering. -/
theorem commute_generators (X : Matrix (Fin n) (Fin n) ℂ) (σ : ℝ → ℝ) (s t : ℝ) :
    Commute (X - σ s • (1 : Matrix (Fin n) (Fin n) ℂ)) (X - σ t • (1 : Matrix (Fin n) (Fin n) ℂ)) :=
  commute_shifted X (σ s) (σ t)

/-- The product of two step propagators over consecutive intervals with rates `σ₁`, `σ₂` equals
the exponential of the summed generators. -/
theorem two_step_propagator (X : Matrix (Fin n) (Fin n) ℂ) (σ₁ σ₂ t₁ t₂ : ℝ) :
    exp (t₁ • (X - σ₁ • (1 : Matrix (Fin n) (Fin n) ℂ)) + t₂ • (X - σ₂ • (1 : Matrix (Fin n) (Fin n) ℂ)))
      = exp (t₁ • (X - σ₁ • (1 : Matrix (Fin n) (Fin n) ℂ)))
        * exp (t₂ • (X - σ₂ • (1 : Matrix (Fin n) (Fin n) ℂ))) :=
  Matrix.exp_add_of_commute _ _ (((commute_shifted X σ₁ σ₂).smul_left t₁).smul_right t₂)

end Neutrinos.Propagator
