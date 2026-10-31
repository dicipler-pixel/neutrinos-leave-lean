import Neutrinos.CrossLink
-- Deliberately false: dropping the factor 2 in CrossLink. A counterexample is
-- a = b = 1, h = I: then conj a * (-I * h * b) = 1, so the left side is 2 while the
-- right side is 1. The proved bound with the factor 2 cannot give it, so linarith fails.
open Complex in
example (a b h : ℂ) :
    |2 * (starRingEnd ℂ a * (-I * h * b)).re| ≤ ‖h‖ * ‖a‖ * ‖b‖ := by
  have := Neutrinos.CrossLink.crossLink a b h
  linarith
