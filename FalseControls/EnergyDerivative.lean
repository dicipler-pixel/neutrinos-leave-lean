import Neutrinos.Shear
-- Deliberately false: the connection energy is stationary in the second damping rate at
-- equal rates (derivative 0), so it cannot have derivative -5/1369 there. The proved
-- statement carries derivative 0, so this is a type mismatch.
example : HasDerivAt Neutrinos.Shear.shearEnergy (-5 / 1369) 1 :=
  Neutrinos.Shear.shearEnergy_hasDerivAt
