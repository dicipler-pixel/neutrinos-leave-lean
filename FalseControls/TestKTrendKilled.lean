import Neutrinos.LinkVerdict
open Neutrinos.LinkVerdict
-- Deliberately false: with clean bracket edges from the first search, Test K kills the trend reading
-- (its whole odd-rate range above 1.113).
example : rateAtLeast 5 4 1113 1000 5283200000 4977300000 5098432099 5116938272 := by decide
