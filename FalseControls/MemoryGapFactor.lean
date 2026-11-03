import Neutrinos.Memory
-- Deliberately false: the exact gap with 2 in place of 4. At c = 1/2, cd = 0,
-- b = (1/2, 0), b_dot = (0, 1) both hypotheses hold, the left side is 1 and the right side
-- is 1/2, so no proof exists and nlinarith fails.
example (c cd br bi dr di : ℝ)
    (h1 : br ^ 2 + bi ^ 2 = c * (1 - c))
    (h2 : 2 * (br * dr + bi * di) = cd * (1 - 2 * c)) :
    4 * (cd ^ 2 + (dr ^ 2 + di ^ 2)) * (c * (1 - c)) - cd ^ 2 = 2 * (br * di - bi * dr) ^ 2 := by
  nlinarith [h1, h2, sq_nonneg (br * di - bi * dr)]
