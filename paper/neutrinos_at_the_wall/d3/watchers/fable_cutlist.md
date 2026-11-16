# Cut list for "The Neutrinos at the Wall" d2 (watcher: Fable, 15 Nov 2026)

Line numbers are in `out_naw/neutrinos_at_the_wall_d2.tex`. My recomputation: `watch/run/fable_check.py`.

**Read in full:** d2 tex; wall_checks.py/.out; fig_wall.py; LEDGER; pocket-record README, LOG, PUBLISH, audit, three records, every experiment .py/.out, sec_physics.tex, cards N1/N2/N3 js, mixer LH-MATH-V1 (s2.js).
**Grep or partial only:** mixer LH-MIXER-V2 (string literals only); McCormick's paper text; v10 tex (door and Gramian sections read, rest grepped); d1 (diffed the check script, did not reread the tex); card stills and mp4 not viewed; engine.js not read.
**Reran:** wall_checks.py (byte-identical to .out); all ten pocket/abundance scripts (byte-identical); mixer self-test under node (24/24 pass).

## A. Serious

**1. The carried angular record is contradicted by the pocket record, and d2 still rests on it.**
Lines 36, 51, 232-235, 252-253, 260, 266, 272.
- LOG.md, 15 Nov: "the draft-1 prediction of a carried *angular* record does not survive standard physics. It is to be replaced." Open item 4 says d2 should replace it with the flavour-asymmetry and spectral record. d2 (built 14 Nov) did not.
- B_rebirth.out: a directly damped record survives 9.7e-2 from 2 MeV, 1.1e-18 from 5 MeV, 2.4e-145 from 10 MeV.
- A_census.out: no exact pocket in the moment chain under any of the three collision models.
- Internal conflict: line 186 says structure planted while coupled is erased by exp[-eps_dec^n/(n tau_s^n)], yet line 232 has a recurrent start "deliver the neutrinos to decoupling already carrying a record" with no mechanism through the coupled era.
- Fix: rewrite §6.3, Prediction 1, abstract paragraph 4, Summary bullet 5 and Tests rows 6-7. Keep the door (§5) as a measured sensitivity to structure present at decoupling. State that an angular record does not survive a hot coupled phase.

**2. Prediction 2 (even-led record) is refuted by the record's own test.**
Lines 236-239, 253.
- README: "the parity test (refuted)". LOG, G: "no consistent even/odd rule, so D's hint was an accident."
- G_parity.out, returned amplitude l3 vs l4: k=0.8, 2.3e-2 vs 2.3e-2; k=1.5, 9.9e-4 vs 1.3e-2; k=2.5, 3.1e-2 vs 5.3e-3. The sign of the preference flips.
- D_fold.out: a hot fold erases both (3e-8, 7e-11).
- Fix: withdraw Prediction 2 and Tests row 7; report G as a negative result. The survival-principle sentence (lines 104, 224) can stay as a statement of [BH], not as a neutrino prediction. Card N2 also says "odd readings cancel".

**3. The black-hole mass is inverted.**
Lines 34, 214; also wall_checks.py section 5 and sec_physics.tex.
- eps = 1/(aH r_m) grows as 1/T, and M_H is the horizon mass at eps = 1 (McCormick eq. 19; v10 line 29). A run with eps_dec = 2 and T_dec = 1 MeV crossed the horizon at T_H = 2 MeV, so M = M_H(T_dec)/eps_dec^2 = 1.5e5/4 = 3.7e4 M_sun, not 6e5.
- Cross-check: McCormick says holes heavier than about 1e6 form while neutrinos already stream (small eps_dec), so larger eps_dec means lighter.
- This is my derivation from the definitions; I ran no code for it.
- Also lines 214, 234: d2 says the step "begins" near 6e5 and spans 1e5-1e7. McCormick's abstract puts the rise between horizon masses 1e4 and 1e6. His 6e5 is where the full-history threshold peaks, a different statement.
- Fix: M = M_H(T_dec)/eps_dec^2, about 4e4 M_sun, inside his 1e4-1e6 range; correct abstract, §5.3, Prediction 1, script.

**4. §6.1 overstates the match to the fold theorem.**
Lines 219, 281.
- Theorem 2 needs a metric regular in the signed coordinate and singular in the even one (dλ² = dX²/4X). The radiation era is the reverse: proper time gives dt² = dX², regular in the even coordinate, and a1²η²dη², vanishing, in the signed one.
- What d2 calls "the coefficient blow-up" is da/dt, not a metric coefficient.
- The 4-metric a²(-dη²+dx²) is degenerate at η = 0 and the density diverges there. "Nothing breaks" is too strong.
- Fix: say the map η → t is a Whitney fold and a(η) is odd and analytic; drop "exactly the setting of Theorem 2"; state the degeneracy, and that continuation through it is Boyle-Finn-Turok's and holds for conformally invariant matter.

**5. "Held, just inside the line" is not decided by the data.**
Lines 22, 125, 127.
- Current inputs: m3/m2 = 5.8069 ± 0.0523, range 5.755-5.859, wall 5.8284. At -1σ a turn of 43°, centre 23.4°, at +1σ a run of 0.49.
- NuFIT 6.0: 48° / 17.4° / run 0.72.
- On Hypothesis 1 itself the turn is 0.
- Fix: give the range, say the data cannot yet tell turn from run, and soften "held at the edge".

**6. New pocket-record results that d3 should carry, with their limits.**
- J: flavour asymmetry behind the electron thermal potential survives 0.236 / 0.634 / 0.867 at cover ×1 / ×10 / ×100, independent of T_max above 10 MeV; leak window 2-6 MeV; fire ×10 gives 0.000. Observables named in the README: helium abundance and N_eff.
- H: spectral distortion survives 0.976 (from 2 MeV), 0.554 (5 MeV), 0.004 (10 MeV) at inelastic share 0.001. The script's last printed line contradicts its own table (LOG notes this); do not quote that line.
- E: leak k²(c²+c²)/σ. It matches four digits only for σ ≥ 30 (σ = 10: 0.05055 vs 0.05043; σ = 1: 0.472 vs 0.504).
- F: slowest decay 0.118 → 0.0113 for κ_n 1 → 100.
- I: one cut makes a protected mode in 15.5 / 4.8 / 1.4 % of 6 / 8 / 10-node networks.
- Abundance correction: the earlier "-53%" is withdrawn.
- Cautions: J is a two-flavour averaged toy with θ = 0.15 and the atmospheric splitting only; the solar channel is absent. The README credits Dolgov et al. 2002, which from my memory (unchecked) found near-complete flavour equilibration. Cite it and say J is not a kinetic calculation. B's second part (0.967-0.936) is for a hypothetical pocket that census A says the chain does not have.

## B. Numbers and tests

**7. Tests table is internally inconsistent.** Lines 249-251.
- "m1 > 1.5 meV or Σ > 62 meV": Σ = 62 corresponds to m1 = 2.6 meV; at m1 = 1.5, Σ = 60.6.
- "m_ββ above 4 meV": with m1 up to 1.5 meV allowed, the range is 0.5-4.8 meV (m_β 8.85-8.98). The 1.5-3.7 range holds at m1 = 0 and central angles only.
- The 1.5 meV bound is a 2σ line while the ratio row uses 3σ; at 3σ it is 1.9 meV (1σ: 0.9).
- Σ, m_β and m_ββ follow from m1 ≈ 0 plus the measured splittings (minimum normal-ordering Σ = 58.95; wall 59.1). Only the ratio 33.97 tests the wall. I get 33.72 ± 0.61 measured.

**8. Koide numbers do not match the paper's own script.** Line 111: Q = 0.6666644634, cos² = 0.50000165. wall_checks.out: 0.666660511, 0.500004616. The paper's values need m_τ = 1776.93; the script uses 1776.86. Pick one, cite PDG.

**9. "Every number ... is computed by the scripts" (line 17) is false.** Not produced by wall_checks.py or fig_wall.py: ± 0.079 and -0.15σ (I confirm 0.0792, -0.15); the NuFIT 6.0 2 meV bound (I get 2.01); the Koide values; random-orientation ℓ=3 0.6-3.8% (only in abundance.out); "three to eleven times" (I confirm 3.1-11.2); quark step ratios (hard-coded in fig_wall.py, no source, and scale-dependent); Σ limits 58 and 62; "factor of about 1.1"; 0.26 eV. Line 296 says NAW-CHECKS-01; the file header says NAW-CHECKS-02.

**10. Table at lines 141-146 mixes data sets.** Ratio row leads with current data, the Δm²31 row uses NuFIT 6.0 (2.534), the grade line says NuFIT 6.0. With JUNO's 7.50 the wall predicts 2.548e-3 against 2.529e-3.

**11. Data provenance.**
- JUNO 7.50 ± 0.12 confirmed through two third-party papers (arXiv:2511.14593; I read part of each page). d2 cites it only through Alikhanov; cite JUNO.
- NuFIT 6.1 Δm²31 = 2.529 ± 0.021: I could not verify; it is not in the bibliography.
- Alikhanov arXiv:2601.18781: untested, fetch blocked.
- NuFIT 6.0 has two tables. 2.534 and 0.02195 look like the set without SK atmospheric data (my memory, partly supported by a paper giving 0.0222 for the with-SK set). With the other set (2.513, from memory) I get 5.792, -0.47σ. Name the table.
- Line 254: the cosmological bound behind "factor of about 1.1" is uncited; untested.

**12. Gaussian abundance caveat missing.** Lines 34, 203-211. McCormick's abstract says CMB spectral distortions already exclude Gaussian perturbations of this size at these masses. d2 uses a Gaussian β and lists μ-distortion only as a future test.

## C. Framing, claims, small items

**13. Big-bang wording in the author's own voice.**
- Line 281: "with the bang at η = 0". Use "the apparent beginning".
- Line 170: "As the universe cools". Lines 32, 173: neutrinos "first species to cross ... at about 1 MeV". Line 214: M_H(T) history. Label these as the hot radiation phase of McCormick's setting, used as a tool (audit §D: "They stay labelled as his setting").
- Lines 150, 221 attribute "the bang" to Boyle-Finn-Turok; acceptable.
- Hypothesis 2 and the Lineage quote are correctly his.

**14. Lean claim on Theorem 1 (line 75).** "Machine-checked in Lean (line_ratio, five_inside_seven_outside)": the mixers say Lean covers ratios 5 and 7 and was "not re-run here". Whether Lean proves tr K = 2 - 4 sinh⁴(r/2) is untested by me; no Lean file was available. Say what each named statement proves.

**15. Mixer v2 (15 Nov) material d2 lacks.** All verified by its self-test.
- General form g = sinh(h_a) sinh(h_b); "for unequal steps the square changes at g = 1, not where either face alone crosses the wall". Proposition 2 covers equal steps only, and d2 never says why the two perpendicular steps are both m3/m2.
- On the wall R = T = ½, and (W + I)² = 0, the Jordan block.
- Thomas turn tan(θ/2) = Γ_aΓ_b, which on the wall is 53.13° (cos = 3/5).
- The face meets the rim at cos ψ = Γ, the 45° ping-pong cap exactly at the wall (numerical; Lean at z = 7 only).
- 1 - 2C = Γ ties the wall to line 177: wall occupation C = 0.146, ħω = 1.763 kT.
- Lineage (line 289) cites only "Balls in One Ball v3". Keep the mixer's own "does not claim" limits.

**16. Small.**
- Line 127: "is 1 - 5e-8 from the rim" is garbled. It is at ball radius tanh(r/2) = 1 - 5e-8; in velocity, 1 - v = 1.25e-15.
- Line 191: "lapse and constraints to 1e-15"; v10 gives 2e-15 and 7e-15.
- Line 170: "hidden structure is wiped"; v10 reports a 0.3-0.5% coupled-era leak.
- Line 70: with a real trace below -2, K is hyperbolic.
- Line 278: the cross term is a commutator, traceless anyway.
- PDF Title and Author metadata are empty.
- Length is 14 pages against his 20-25.
- Cards N1/N2 footers say "draft 1" and NuFIT 6.0 only.
- Citations thin: McCormick (no arXiv number), Dave et al. (no title), BFT2 (no volume).

## D. Passed

- Byline in tex, PDF and HTML is "Jeromie Beasley". The pocket record's README, LICENSE and d1 tex say "Jeromie N. Beasley"; do not copy.
- No boxed text. All fonts Type 1, PDF and figure.
- Every bibitem cited, every cite defined.
- Recomputed and matching: wall 5.828427; 5.8069 ± 0.0523, -0.41σ; m2 8.65, m3 50.44, Σ 59.10; m_β 8.85; m_ββ 1.49-3.71 at m1 = 0; turns 23.44° and 17.43°; fixed points 0.9501 and 0.9626 (formula against the matrix eigenvector); run 7.95; K values; Γ = 0.918; abundance table; pair differences and shifts against v10's eight thresholds; Appendix A.1 and A.3 algebra.
