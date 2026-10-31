import Neutrinos.KillLine
-- Deliberately false: Test D lies within 0.08 of 0.30. Its fraction is 472/3059, about
-- 0.154, which is 0.146 below 0.30, so the claim reduces to False.
example : |Neutrinos.KillLine.G (50245 / 100000) - 30 / 100| < 8 / 100 := by
  rw [Neutrinos.KillLine.G_D, abs_lt]
  constructor <;> norm_num
