import Neutrinos.Shear
-- Deliberately false: the shear response at equal rates is 32/37, not 33/37.
-- norm_num reduces the claim to False.
example : Neutrinos.Shear.R00 1 = 33 / 37 := by
  norm_num [Neutrinos.Shear.R00]
