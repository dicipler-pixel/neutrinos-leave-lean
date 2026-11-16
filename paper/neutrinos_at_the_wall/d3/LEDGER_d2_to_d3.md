# The Neutrinos at the Wall — ledger, draft 2 to draft 3 (15 Nov 2026)

Final pass with two independent watchers (Fable and Sonnet). Each wrote a cut list of d2 before seeing any edits, then checked d3; their four reports are in `watchers/`.

## Changed
- **The carried record.** d2 took the hidden angular record as what crosses the fold. The pocket record (commit ac28179) shows a hot rebirth erases it (survival 1.7e-4 from 3 MeV, 2.4e-145 from 10 MeV; experiment B). Section 6 is rewritten:
  - what a hot rebirth erases (B), with the pocket census (A), Zeno sealing (E), McCormick flux sealing (F) and cut networks (I);
  - the fold itself (D, G);
  - the record no collision erases: the total lepton asymmetry (the offset mu). The flavour split under the electron cover (J) is carried with its limits: a two-flavour toy, while full three-flavour treatments (Dolgov et al. 2002; Castorina et al. 2012) equilibrate the flavours before nucleosynthesis.
  - The spectral record (H) is included.
- **Parity prediction withdrawn.** Experiment G shows no even/odd rule.
- **New prediction (graded weak):** a common neutrino chemical potential. Its status is from Ghedini et al. 2026: EMPRESS gives 0.041 (+0.036/−0.035) and LBT gives 0.006 ± 0.011.
- **Black-hole prediction** is now conditional on a passage below about 2 MeV, which the idealised radiation fold is not.
- **Black-hole mass corrected** (Fable). M = M_H(T_dec)/eps_dec², about 4e4 M_sun, not 6e5. This is the same inversion as in the v11/v12 physics section, `sec_physics.tex`, which still needs this correction.
- **Gaussian-abundance caveat added:** McCormick notes that CMB distortions exclude Gaussian perturbations of this size.
- **Turn or run:** the data do not decide (at ±1σ, a 43° turn or a run of length 0.49; 34% of the weight lies on the run side).
- **m_ββ and Σm** are now given for m1 up to 1.5 meV (0.5–4.8 meV; 59.0–60.6 meV), and the test lines are corrected.
- **Koide** recomputed with the PDG tau mass 1776.93 MeV, in the script.
- **NuFIT 6.0 table** named (IC19 without SK-atm), and the IC24 value given (5.792, −0.47σ). Both were verified against arXiv:2410.05380.
- **Lean claim scoped** to what the named statements cover.
- **Fold wording.** The density diverges at η = 0, so the fold is a statement about the clock and the scale factor. Standard-cosmology inputs are labelled as tools throughout. "Bang" is no longer in the author's voice.
- **New from Light at the Hypersurface v2:**
  - Proposition 3: the wall on the rim (tanh r_w = 2√2/3; the 45° caps);
  - the Thomas turn at the wall, cos = 3/5.
- **Script:** NAW-CHECKS-03 adds sections 2c and 10–14. All nine pocket experiments were rerun, byte-identical.

## Not changed / open
- fig_wall.py still hard-codes the quark step ratios; their source is SMball.
- JUNO and NuFIT 6.1 are cited only as quoted by Alikhanov.
- The full read of all prior black-hole work (answer 11) was not part of this pass.
- The pocket-record README, LICENSE and d1 tex still say "Jeromie N. Beasley".
- Cards N1/N2 footers say "draft 1". The N2 bars encode the withdrawn parity rule.
