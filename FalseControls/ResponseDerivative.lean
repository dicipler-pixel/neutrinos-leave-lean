import Neutrinos.Shear
-- Deliberately false: the response derivative formula -20/(35 x + 39)^2 at x = 1 is -5/1369,
-- not 0. If it were 0, the energy would control the response; it does not.
example : -20 / (35 * (1 : ℝ) + 39) ^ 2 = 0 := by
  norm_num
