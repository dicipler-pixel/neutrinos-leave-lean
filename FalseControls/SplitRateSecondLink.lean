import Neutrinos.SplitRate
-- Deliberately false: the three-moment energy has no term in the second damping rate alone;
-- it depends on the difference. Claiming a^2 kappa1^2 + b^2 kappa2^2 is rejected: the proved
-- theorem carries (kappa2 - kappa1)^2, so this is a type mismatch.
example (a b κ1 κ2 : ℝ) :
    (1 / 8) * Neutrinos.Frobenius.frobSq
      (Neutrinos.Frobenius.selfComm (Neutrinos.SplitRate.L3 a b κ1 κ2))
      = a ^ 2 * κ1 ^ 2 + b ^ 2 * κ2 ^ 2 :=
  Neutrinos.SplitRate.splitRateEnergy_ab a b κ1 κ2
