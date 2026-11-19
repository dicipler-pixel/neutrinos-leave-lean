# Coverage of v11b

Built 19 Nov 2026 (CT). In this folder the tex/pdf file names keep `_v11` (neutrinos_v11.tex / neutrinos_v11.pdf are the v11b build). The "v11" label on the title page is provisional: the author has not chosen between v13 and v11.

## A. Mechanical coverage (coverage_v11b.py → coverage_v11b_auto.md)
In the auto file, the column headed "v11" is this v11b build. The rows headed "Items of v11" are the v11 build at /workspace/ink/D17/v11.

| | v10 | v12 | v11 | v11b |
|---|---|---|---|---|
| pages (PDF) | 131 | 135 | 142 | 144 |
| structural items extracted | 279 | 294 | 317 | — |
| missing from v11b | 0 | 0 | 0 | |

- Missing items: **NONE** (v10, v12 and v11 items all present in v11b).
- PDF title word-set cross-check: PASS. Figure captions: 11/11.
- dr eggbot inventory: 71/71 present.
- Build: tectonic, 144 pp, 0 undefined references, no "??" in the pdftotext output, and the phrase "draft for the author's review" no longer appears.

## B. Neutrinos at the Wall d4 vs draft 3 (aa8d6ec)
Rule, as for d3: v11 is v12 in full plus corrections and the four requested additions. Wall-paper material is cited, not copied, unless it bears on the author's frame (item 1).
The d3 items are carried over unchanged from the v11 hand map (coverage_v11.md, section C). Source of the d4-only items: /workspace/ink/D19/changes_vs_d3_d4.md, E1–E20.

| d4 edit | item | status in v11b | reason |
|---|---|---|---|
| E1 | date "Draft d4" | excluded | Wall-paper header |
| E2 | grade key extended (EXACT/DERIVED/MODEL/ANALOGY/author's interpretation) | excluded | v11 has its own grade key. The two grades used here (author's interpretation, reading) are spelled out in place |
| E3, E5, E7 (6.1), E16 | author's stance: no Big Bang, maybe no first moment, aeon passage, memory prior | **added** in §frame, paragraph "The author's position, and the conformal boundary" | this is the frame (item 1). Quotes were checked against DIRAC_TIME_v3_0_1.txt l.393 and what_jeromie_asked_v1.md l.12 |
| E4, E11 | "folds" → "crossings" wording | not applicable | v11 has no such sentence (grep: no "through a fold" / "far side is the mirror") |
| E6, E8 | FLRW = inside one aeon; mirror not in his voice | present in substance | v11's frame makes no mirror claim; BFT is already cited as others' work |
| E9 (6.3) | CCC conformal boundary: $a^2\eta_{\rm Mink}=\check\Omega^2 g$ | **added** (one sentence; identity is immediate) | needed for the stance |
| E9 (6.4) | memory through the boundary; DT "failure of one metric description ⇏ failure of every spectral record" as ANALOGY | **added**, labelled reading/analogy | frame. DT quote checked at l.2484 |
| E9 mass caveat | neutrino mass scale at Σ is open | **added** | honesty about scope |
| E10, E13, E15 | removal of overreaches about the fold | not applicable | v11 does not contain those overreaches |
| E12 | toy runs D/G use the mirror continuation | excluded | the pocket toy runs are Wall-paper experiments, not in v12 |
| E14 | physical vs rescaled density | excluded | Wall-paper "not claimed" item |
| E17, E18 | A.2 de Sitter toy, R=0, checked symbolically | **cited** (stated as d4's result, "not rechecked here") | derivation belongs to the Wall paper |
| E19, E20 | lineage and bib (PenroseFP, Tod, DT) | DT and CCC already in v11, WallD4 added | PenroseFP and Tod are not cited because v11 does not use their content directly |

## C. Inventory CORE items (sources_inventory_v1.md, 60 rows)
| group | rows | status |
|---|---|---|
| What the Neutrino State Must Keep v10 pdf (×2 paths), v10 Zenodo record | 3 | present: v10 is covered mechanically (A) |
| v12 / v11 builds | — | present (A) |
| neutrino_submission d1–d7 | 7 | present: the d1–d7 corrections were applied in v11 (changes_v12_to_v11.md) and are kept |
| neutrinos_at_the_wall (13 pp, npr) and d4 (21 pp) | 2 | cited. d4 is mapped in B. The 13 pp draft 1 is superseded by d3/d4 |
| npr (1/2/3).zip, npr2.zip, npr2 (1).zip | 5 | npr2.zip was downloaded and diffed (D). npr2 (1) has the same size as npr2 and was not downloaded separately |
| November_NPR_and_Black_Hole_Research_Archive 1.zip | 1 | **not read**: outside this request's step 1 |
| When the Neutrinos Leave v1, v3, v3.1, v4, v4.1, v5.1, v6 (pdf/html/code zips), WNL Zenodo 23858157 | 21 | present by succession: v12 is the current form of this lineage. Not re-diffed item by item (not verified) |
| What the Neutrino State Must Keep v6 (pdf/html ×3) | 3 | present by succession (v10 ⊃ v6). Not re-diffed |
| Beyond the Event Horizon (Zenodo 21147367, 21860392, 23391175, 23493466; bh_paper_v10 html) | 5 | cited as [BH] edition 10 (concept DOI). Readings are in §bhreadings |
| IQGT Zenodo 23351266 | 1 | cited |
| Dirac Time Zenodo 22979186 | 1 | cited [DT] |
| Ledger Outlives the Metric (2 records) | 2 | **cited, new in v11b** [Ledger] (DOI 22023237 as given in the repo README) |
| Square Case 21855591 | 1 | **cited, new in v11b** [SquareCase] (DOI 21855590 as given in the repo README) |
| Operator-First Relational Atlas 21978567 | 1 | not cited: the repo branch adds nothing new, and the atlas quote d4 uses was not found in relational-atlas-lean, so it was not used |
| GitHub repos: neutrinos-leave-lean, event-horizon-lean, what-the-neutrino-state-must-keep, iqgt-grassmannian-lean, iqgt-core-lean | 5 | read in v11 and cited |
| GitHub repos: relational-atlas-lean, three-body-lean, dirac-time-lean, gravity-ledger-lean, square-case-lean | 5 | read for v11b (E). Three-body, gravity-ledger and square-case are cited in the new §19 |

Missing: none, beyond the one archive zip marked not read.

## D. npr2.zip (Drive id 1En2nRRy-7wvjy08RpzU3f5iWoEIgufTg) vs /workspace/npr/x3/neutrino-pocket-record
- 68,451,327 bytes, 270 zip entries, 174 files. The box copy has 190 files. See src/npr2_diff.md.
- npr2 is a single squashed commit (ac28179), while the box copy has the 5-commit history. All files that are only in one copy are .git objects.
- Content changes:
  - LOG.md: experiment B's second part was rerun after an np.trapz crash, giving survival 0.967, 0.948, 0.942 and 0.936 from 2, 5, 10 and 100 MeV. The log also records an independent review.
  - README.md: explains the missing experiment C, and that the commit times are packaging times.
  - experiments/pockets/B_rebirth.out: the rerun output.
  - acc_side/*.py: environment-variable paths. ACC tools, not relevant here.
  - cards/source/cap.js.
- Bearing on the paper: none added. The B numbers belong to the Wall paper's pocket experiments, and they bear on Test R (posed, not run). They are excluded under the same rule as the d3 pocket experiments.

## E. Repos read for v11b (read-only clones in gh/)
| repo@commit | read | used |
|---|---|---|
| event-horizon-lean claude/bh-recovery-20261116 @7c3d5f6 vs main@7dd6164 | MANIFEST_v1, ledger E (neutrino entries) | §19: no new Lean. BH ed. 11 "orientation records" not recovered. 2 Nov E1 FAIL and E3 values, quoted |
| votkp-lean claude/votkp-research-20261110 @3565281 (BallJoins.lean from 629f3bf) | J1–J8 header, J3, J4, lakefile | §19: **Γ²=½ wall found** as `line_ratio` (value) and `trace_reflect_transmit`. Outside the build targets and not compiled |
| gravity-ledger-lean @885932f | README, 30 theorem names | §19 reading |
| square-case-lean @6769949 | README | §19 reading |
| three-body-lean @1f3ddcd | README, 369 report (pdftotext, 0 "neutrino") | §19 reading. Report not used |
| dirac-time-lean test-* (5 branches) | READMEs and diff stats | §19 one line (UPG) |
| relational-atlas-lean atlas-207-coverage-2026-10-23 @4032bd4 | merge-base check | ancestor of main@060c904: nothing new |

gravity-ledger and square-case have no pdf/tex in the repo, so only the READMEs and Lean names were read. The relational-atlas main branch was read in v11.
