import Neutrinos.TwoMoment
-- Deliberately false: the two-moment connection energy is kappa^2 k^2 / 3, not kappa^2 k^2 / 2.
-- The proved theorem carries 1/3, so this is a type mismatch.
example (k κ : ℝ) :
    (1 / 8) * Neutrinos.Frobenius.frobSq
      (Neutrinos.Frobenius.selfComm (Neutrinos.TwoMoment.L2 (k / Real.sqrt 3) κ))
      = κ ^ 2 * (k ^ 2 / 2) :=
  Neutrinos.TwoMoment.twoMomentConnectionEnergy k κ
