import Neutrinos.KillLine
-- Deliberately false: Test B lies within 0.08 of 0.431. Its fraction is 970/3059, about
-- 0.317, which is 0.114 below 0.431, so the claim reduces to False.
example : |Neutrinos.KillLine.G (50743 / 100000) - 431 / 1000| < 8 / 100 := by
  rw [Neutrinos.KillLine.G_B, abs_lt]
  constructor <;> norm_num
