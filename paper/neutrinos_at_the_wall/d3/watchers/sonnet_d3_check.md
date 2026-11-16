# Watcher check of d3 against the d2 cut list (Sonnet 5.5)

Checked: S/naw_d3/neutrinos_at_the_wall_d3.tex read in full (404 lines); wall_checks.py rerun with python3 -I, output identical to wall_checks.out (NAW-CHECKS-03). I recomputed the new numbers independently (Thomas turn, rim proposition algebra, hot-rebirth exponents, Σm, m_ββ, horizon mass). Fetched Ghedini et al. (arXiv:2606.28135): the quoted ξ_e values match Table IV (95%, SPA+DESI+EMPRESS 0.052 +0.045/-0.040; LBT 0.009 +0.015/-0.013). Not verified: Dave et al. title, Castorina, EMPRESS, Stodolsky, Dolgov2 (bibliographic details match my recollection, untested), Lean, NU10, the "Balls in One Ball v3" mixer. PDF: all Type 1 fonts, byline "Jeromie Beasley", no boxed text in the tex.

## 1. Status of my items (d2 numbering)

1 angular record: FIXED. Abstract l.36, Sec 6 l.246-292 (erasure 0.45/0.097/1.7e-4/1e-18/2.4e-145 reproduce; exponent (T³-1)/3 matches B.out), Pred. 2 conditional (l.286-289), Summary l.318-325.
2 parity: FIXED. Withdrawn at l.265 with the G numbers (k=0.8 equal, 1.5 even larger, 2.5 odd larger: correct). Tests row removed.
3 fold passage / "tens of per cent": FIXED. Qualifiers at l.34, l.287, l.318; l.265 says the cold fold goes into density. Small slip, see N6.
4 omitted pocket results: FIXED (A, B, D, E, F, G, H, I, J all appear, with toy-model caveat l.276, l.311, helium/N_eff test added). One honest extra: l.262 conditional pocket.
5 Koide: FIXED (PDG 1776.93, Q = 0.666664463, cos² = 0.500001652 now from script; μ→τ z = 16.8177).
6 m_ββ: FIXED (l.160, 301; 0.52-4.76 verified). 7 Σm lines: FIXED (60.6; 59.0-60.6 verified).
8 turn vs run: FIXED (l.138, 140; 43°, 0.49, 34%/44% verified).
9 look-elsewhere / citations: PARTLY. Sentence at l.135 added, NuFIT JHEP cited, SK-table row added and verified (5.7924 ± 0.0770, -0.47σ). Still no bibliography entry for JUNO's first measurement or NuFIT 6.1; the 6.1 value is unverified.
10 Lean overclaim: FIXED (l.75 states what Lean covers and that it was not re-run).
12 big-bang framing: MOSTLY FIXED (l.53, 185, 234, 312). Residuals in N3 below.
13 Lineage quote: FIXED (l.345, now "not sure there is a first moment"). 14 "nothing breaks": FIXED (l.234, 313; closed-universe aside added; "independently" dropped).
15 "exactly parabolic" vs turn: PARTLY (l.140 "within the errors"; Hypothesis 1 unchanged, acceptable).
16 README 10-47 vs 5-47: not a d3 item. 17 byline: d3 clean; repo README/LICENSE/old d1 still say "Jeromie N. Beasley" (not fixed, outside d3).
18 references: PARTLY. Dave, Romatschke titles added; still uncited: KATRIN (l.159), DESI/Planck Σm bounds (l.158), JUNO.
19 fig_wall.py hard-codes: NOT FIXED (script byte-identical to d2; quark z values and 16.82 hard-coded).
20 fonts/boxes/pages: OK, 18 pages. 21 mixer: PARTLY. Mixer2 (Light at the Hypersurface v2) now cited and its formulas used correctly; Lineage l.342 and bib l.386 still quote eye names of "Balls in One Ball v3" that do not occur in the file I was given. 22 cards: out of d3 scope (still show draft 1, NuFIT-6.0-only, N2 parity bars).

## 2. New errors or weaknesses introduced by d3

N1. **Correction narration inside the paper body.** l.229 "(Draft 2 wrote ε²M_H and 6×10⁵ M⊙; that inverted the scaling.)", l.246 "Draft 2 of this paper took...", l.265 "Draft 2's parity prediction ... withdrawn", abstract l.36 "the parity prediction of draft 2 is withdrawn", l.368 (H_spectrum last-line remark, acceptable in Appendix C only). The author's rule: final papers read as one complete thought, no version archaeology; corrections live in the ledger. Strip all "Draft 2" mentions; state results directly.
N2. **Horizon-mass scaling is now right, and I confirm it.** M = M_H(T_dec)/ε² = 3.7e4 M⊙ (ε ∝ 1/T, crossing at T = ε·T_dec). d2's ε²M_H was wrong. But the new "inside the range 10⁴-10⁶ M⊙ where McCormick's rise sets in" and "SMBH seeds proposed in this range" are unverified by me (McCormick, Dave).
N3. **Big-bang dependence in the new Sec 6, in the author's voice.** l.249 "Any phase hotter than about 1 MeV remakes the neutrinos, Γ/H ≃ (T/1 MeV)³" and l.274 sphalerons/electroweak scale, l.283 leptogenesis, l.285 CMB+DESI+BBN helium: all standard hot-big-bang thermal history. l.304 says cosmological models are not adopted and bounds are "a check rather than a verdict", but only for Σm; the ξ test (l.285, 302, 324) rests entirely on BBN helium and ΛCDM-fitted CMB. Needs one sentence saying the same for ξ, and that the hot-rebirth chain is evaluated in McCormick's standard coordinates as a tool.
N4. **Prediction 1 (common ξ) barely discriminates recurrence.** Oscillations equalise any large asymmetry from any source (l.276 cites Dolgov2/Castorina), so "flavours unequal at nucleosynthesis" (l.302) would refute oscillation physics, not recurrence; and l.285 concedes ξ=0 does not refute. Tests row grades as refutable what is close to unfalsifiable. Say so, or reword as consistency check. Also Ghedini's fit is a (1+2)ν scenario with ξ_e and ξ_x separate; d3 quotes ξ_e only and does not claim ξ_μ,τ measured (fine), but "data do not yet agree on ξ_e" is correct as stated.
N5. **Cross-sentence tension on the electron-sea "cover".** l.272 says the thermal potential holds the flavour split; l.276 says a full three-flavour treatment equilibrates the flavours, leaving only the total robust. Both stated, but l.36 (abstract) still says "the electron sea's thermal potential holds the flavour split while it is hot" without the caveat. Add "in a two-flavour toy model".
N6. **D-experiment numbers.** l.265 "returns 1-5% to the planted moment" is the README/G figure; D_fold.out cold-fold values are |ℓ=3| 9.9e-4 and |ℓ=4| 1.30e-2 (0.1%-1.3% of the planted amplitude, if that amplitude is 1). Quote D.out directly or define the normalisation.
N7. **Rim Proposition checks out.** Algebra (t ≥ 2√2/3, tanh r_w = 2√2/3 exactly), numerics (z=5: 0.6219, wall 0.7071, z=7: 0.7874; ψ0 = 48.19/45/41.41°) and Thomas turn (cos θ_T = 3/5, 53.13°; 53.01° measured) all verified. Two cosmetic points: l.58 says link rapidity ½ ln z while Prop. 3 uses step rapidity r = ln z; one clarifying clause needed. l.347 says "24 self-tests" but the bibliography says K1-K18: reconcile.
N8. **Abstract l.34** "A record carried across this wall is physical" still leads straight into engineered ℓ=3/4 plants; after Sec 6 the abstract's logic is "this is McCormick-setting sensitivity". Reword.
N9. **Sec 2 l.140 vs l.138**: figure caption says the neutrino step "sits on" the wall while text now says the data do not decide. Caption wording is softened at the end; fine, but the panel (a) title text still "where each step sits" with the neutrino dot drawn on the line.

## 3. Must change before delivery, ranked

1. Remove every "Draft 2/draft 2" narration from the abstract and body (l.36, 229, 246, 265); keep corrections in the ledger.
2. State that the ξ test and the hot-rebirth rate chain use standard-cosmology (BBN, CMB, sphaleron) inputs as McCormick-coordinate tools; extend l.304 to cover ξ and helium (N3).
3. Re-grade Prediction 1 honestly: equal flavours follow from oscillations for any source, so only a nonzero common ξ would support recurrence, and zero does not refute (N4).
4. Add "in a two-flavour toy model" to the abstract's cover sentence (N5); quote D.out numbers (N6).
5. Citations: JUNO first result, NuFIT 6.1, KATRIN, DESI/Planck Σm bound; fix the mixer eye-name quote at l.342 or confirm the v3 file exists.
6. Clarify step rapidity vs link rapidity at l.58/94 and the "24 self-tests" wording (N7).
7. Optional: make fig_wall.py compute z from inputs rather than hard-coding; README/LICENSE byline in the pocket repo.
