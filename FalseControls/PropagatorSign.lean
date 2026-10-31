import Neutrinos.Propagator
-- Deliberately false: the collision factor is exp(-sigma t), not exp(+sigma t). The proved
-- theorem carries -σ * t, so this is a type mismatch.
example {n : ℕ} (X : Matrix (Fin n) (Fin n) ℂ) (σ t : ℝ) :
    NormedSpace.exp (t • (X - σ • (1 : Matrix (Fin n) (Fin n) ℂ)))
      = (Real.exp (σ * t)) • NormedSpace.exp (t • X) :=
  Neutrinos.Propagator.scalarCollisionPropagator X σ t
