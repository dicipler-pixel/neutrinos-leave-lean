import Neutrinos.Memory
-- Deliberately false: without the box |y| < 1/4 the self-adjoint condition y^2 = -y
-- also holds at y = -1, so it does not force y = 0. nlinarith cannot prove it.
example (y : ℝ) (h : y ^ 2 = -y) : y = 0 := by
  nlinarith [h, sq_nonneg y, sq_nonneg (y + 1)]
