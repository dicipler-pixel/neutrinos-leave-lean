# d3 check against the cut list (watcher: Fable, 15 Nov 2026)

Line numbers are in `naw_d3/neutrinos_at_the_wall_d3.tex`, read in full (405 lines).
`wall_checks.py` (NAW-CHECKS-03) rerun with `python3 -I`: output byte-identical to `wall_checks.out`. Script diff against d2: tau mass, mass scaling, new sections 10-14 and 2c only.
PDF: 18 pages, byline "Jeromie Beasley" (title page and metadata), all 32 fonts Type 1, no boxed text, no overfull lines, no "??", every cite defined and every bibitem cited. Page images not viewed.

## 1. Cut-list items

| # | Item | Status | Where |
|---|---|---|---|
| 1 | Carried angular record | Fixed | 36, 246-262, 281-289, 310 |
| 2 | Parity prediction | Fixed (withdrawn, G reported) | 36, 265 |
| 3 | Mass inverted | Fixed: M_H/eps², 4e4, range 1e4-1e6; script too | 34, 229 |
| 4 | Fold overclaim | Partly. Degeneracy and diverging density now stated (234, 313). Still "the setting of Theorem 2" and still calls da/dt "the coefficient blow-up of the fold" (234). Abstract still says the theorem "applies to the radiation era itself" (36) | 234, 36 |
| 5 | Turn or run undecided | Fixed (range, 34% run side). "held, at the edge" survives two sentences before "the data do not decide" | 138, 140 |
| 6 | New pocket results | Fixed, with limits and Dolgov/Castorina caveat | 255-278 |
| 7 | Tests table | Fixed (60.6, 4.8, "at 2σ"). Ratio row still 3σ | 163, 299-301 |
| 8 | Koide | Fixed; script and paper agree | 124 |
| 9 | "Every number from scripts" | Mostly fixed (header reworded, label 03). Quark step ratios still hard-coded in fig_wall.py with no source | 17, 124, 351 |
| 10 | Mixed data sets in table | Partly: grade line now says which row uses which | 157, 161 |
| 11 | Data provenance | Partly. NuFIT 6.0 table named, JHEP reference added. JUNO still not cited (only through Alikhanov). NuFIT 6.1 still not in the bibliography | 127-131 |
| 12 | Gaussian caveat | Fixed | 226 |
| 13 | Big-bang wording | Fixed (53, 185, 234, 304, 312, 334) | |
| 14 | Lean claim | Fixed: says what each statement covers, and not re-run | 75 |
| 15 | Mixer v2 material | Fixed (rim proposition, Thomas turn, unequal steps, R = T = ½, lineage) | 90-101, 142, 347 |
| 16 | Small items | Mostly fixed (ball radius, "below 1e-14", "damped", hyperbolic, PDF metadata, Dave title). Not fixed: BFT2 volume, McCormick arXiv number | 140, 206, 390 |

## 2. New errors in d3

**N1. Wrong table quoted for the paper's own prediction (line 285).**
Prediction 1 is a common ξ, equal in three flavours. d3 quotes 0.052 (+0.045/-0.040) and 0.009 (+0.015/-0.013). I fetched Ghedini et al. (arXiv:2606.28135): those are its split-case ξ_νe values (Table IV, one flavour differing from the other two). For the common ξ (Table III) it gives 0.041 (+0.036/-0.035) with EMPRESS and 0.006 ± 0.011 with LBT, both 95%. Also the first number is cited to EMPRESS, but it is Ghedini's combination (Planck + ACT + SPT + DESI DR2 + EMPRESS); EMPRESS predates DESI.

**N2. "Cool passage" contradicts the fold of §6.1 (lines 234 vs 253, 287, 292, 325).**
§6.1 says the radiation density diverges at η = 0. That fold is infinitely hot at its centre. Prediction 2, the Tests row and Summary bullet 6 keep "a passage that stayed below about 2 MeV" as a live case, and §6.4 uses experiment D's "cold fold", whose collision rate vanishes at η = 0. As written the two cannot both hold.

**N3. The lepton asymmetry against the paper's own survival principle (lines 117, 239 vs 274).**
"Readings odd under the mirror cancel across it; even readings survive." Line 274 then says the asymmetry changes sign under the CPT mirror, which makes it an odd reading. The paper needs one sentence on why the record it now relies on is not one that "cancels".

**N4. Lepton number "conserved" needs two qualifications (line 274).**
- Graded "cited physics" with no citation.
- If the neutrinos are Majorana (the table's m_ββ row, and Boyle-Finn-Turok's prediction) total lepton number is not exactly conserved. The rate is tiny, but the sentence says "nothing".
- From my memory, not checked here: a rebirth hotter than the electroweak scale lets sphalerons turn a large B-L into a large baryon number, far above the observed one. A ξ near 1e-2 would then need the last hot phase to stay below that scale. Line 283 mentions leptogenesis but not this limit.

**N5. Correction narration in the paper (lines 13, 36, 229, 246, 265).**
"(draft 3)" in the date; "the parity prediction of draft 2 is withdrawn" in the abstract; "(Draft 2 wrote ... that inverted the scaling.)"; "Draft 2 of this paper took..."; "Draft 2's parity prediction". The author's standing rule is that a paper does not read as a correction log.

**N6. "1-5%" understates the spread (line 265).** D and G give the returned share as 0.1% (ℓ=3, k=1.5) to 4.8% (ℓ=2, k=1.5). The conclusion (no rule) holds.

**N7. NuFIT 6.0 with-SK value stated as fact (line 131).** 2.513e-3 and its error came from my memory in phase 1, flagged unverified. I still have not seen the NuFIT table. Verify at nu-fit.org or drop the sentence.

**N8. Smaller.**
- Line 124 still says the charged steps are "loxodromic"; Theorem 1 now says hyperbolic.
- Line 258: "This is the quantum Zeno effect in transport". The chain is a classical damped system; "Zeno-like sealing" is what is shown.
- Line 345: the author's statement is tidied inside quotation marks (his words: "not sure there is a first moment my point is i see a way beyond big bang").
- Line 300: "refuted if Σ outside 59.0-60.6 meV" is sharper than any cosmological measurement, and line 304 then says cosmology is "a check rather than a verdict". Soften the row.

**Checked and correct in the new material.**
- Proposition (wall on the rim): algebra verified by hand; t ≥ 2√2/3 and tanh r_w = 2√2/3. Matches the mixer's K11/K12 tests and script section 10.
- Thomas turn, run-side shares, erasure table, Σ and m_ββ ranges, and every pocket number quoted, against the outputs I reran.
- Ghedini: authors, title and arXiv number confirmed by fetch.
- Dolgov2, Castorina, Stodolsky, EMPRESS, NuFIT JHEP and PDG entries look right from memory; not fetched.
- No big-bang framing in the author's voice found.

## 3. Must change before delivery, ranked

1. **N1**: quote the common-ξ numbers (0.041, 0.006 ± 0.011) for Prediction 1, or both tables labelled; cite Ghedini for both.
2. **N2**: reconcile the hot radiation-era fold with the "cool passage" branch, or drop that branch from Prediction 2, Tests and Summary.
3. **N3**: one sentence squaring the sign-changing asymmetry with "odd readings cancel".
4. **N5**: remove the five draft-2 / draft-3 mentions.
5. **Item 11**: add JUNO (arXiv:2511.14593) and a NuFIT 6.1 entry; **N7**: verify 2.513 or cut it.
6. **N4**: cite the lepton-number statement; add the Majorana and electroweak-scale qualifications.
7. **Item 4**: line 234 "the coefficient blow-up of the fold" and abstract "applies to the radiation era itself" to match the body's own caveat.
8. **N6, N8**, quark-mass source, BFT2 volume.

Sources fetched: [arXiv:2606.28135](https://arxiv.org/pdf/2606.28135).
