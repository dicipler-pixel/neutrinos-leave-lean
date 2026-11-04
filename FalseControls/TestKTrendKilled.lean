import Neutrinos.LinkVerdict
open Neutrinos.LinkVerdict
-- Deliberately false: with clean bracket edges, Test K kills the trend reading (its whole range above 1.113).
example : (5 / 4 : ℚ) ^ 1113 < kQmin ^ 1000 := by
  norm_num [kQmin, odds, kAhi, kBlo, dFluid, dInst]
