# Review ledger — v7 to v8 (13 November 2026)

This records the external review of v7 and what was done with each item. It is a working record, not part of the paper.

## Changed

| Item | v7 | v8 | Check |
|---|---|---|---|
| Attribution of the pole and the 2/π wall | presented as new ("v7 adds the exact wall") | credited to Romatschke 2016, Eq. (37), the BGK charge-diffusion channel; what this paper adds is the reading as the neutrino kept sector, the centre-of-cut statement, K = 4φ²/sin²2φ and the truncation approach | review read his Eq. (37): ω = −i/τ_D + ik/tan(kτ_D), kτ_D < π/2 |
| Convergence wording | "consistent with second-order convergence" | shift shrank to 0.42 (0.33–0.50); excludes first order in space; does not separate second order in space (0.44) from first order in the time step (0.33, predicts 0.50994197, at the bracket's lower edge 0.50994187) | recomputed: dt shrinks ×3 per level (Courant ×½, cells ×⅔) |
| Extrapolated rate | 1.099 / 1.096 (1.094–1.098) under the spatial reading | 1.099 and 1.094–1.098 under either reading | recomputed with oddrate.py: time-step reading gives R3 1.0992, R∞ 1.0979 |
| Isolated-mode share (§7) | k ≲ 1.4, 36% / 64% (60-moment chain) | exact: k < κπ/2 = 1.505 at κ = 0.958, 51% of the profile weight on the 36 nodes | recomputed on the nodes of diag_modes.py |
| §9 "most of the profile" | most | about half | follows from the line above |
| Shifts at r = 1/4, 4 | +0.183, −0.179 (McCormick's 0.431), "cancel to 0.004" | +0.188, −0.173 from the measured 0.425; reading (c) stated in the offset: −0.763, +0.786, equal and opposite to 3% | recomputed from the table's thresholds |
| Gramian suppression | 2.5×10⁻⁹ beside ε_dec = 2 eigenvalues | 3×10⁻⁷ for ε_dec = 2 (1.1×10⁻⁷/0.367), 2.5×10⁻⁹ named as the ε_dec = 0.5 value; both against e⁻⁴² (same exponent by scaling); snapshot statement scoped to ε_dec = 0.5 | A5_PREREGISTERED.txt lines 48–49, 104–106 |
| G at r = 1/16 | 0.776 | 0.777 | (0.521485 − 0.49773)/0.03059 = 0.7766 |
| Formal pairs | r = 1/2, 2 not listed | listed as formal | window ¾ ≤ r ≤ 3/2 |
| McCormick "exactly" | unscoped | scoped to his default per-group target (archived thresholds); boosted common-rest-frame option named as outside the identity, and as the target of the recorder runs | read ms_mg.py at eb7c4de: default eps_s/4π + c_s μ per group; nnmode = 1 common frame |
| Start time | not mentioned | his earlier-start runs move the references by about 4×10⁻⁴; all runs here at ε₀ = 0.1; dependence of the odd rate untested | earlier_start/summary.txt at eb7c4de: 0.49773 → 0.49727, 0.52832 → 0.52789 |
| Zenodo / README 0.646 | 0.646 | 0.645 (the computed value at 200 moments) | onset_exact_out.txt |
| Package | swarm/ working briefs inside; no top README | swarm/ removed from the public zip (the preregistrations and run logs the paper prints are kept in paper/code); top-level README added | — |

## Defended (kept as is)

- The 1.11 ± 0.01 headline: kept by the author's decision until the r = 0.8 third-level run lands; the body states the extrapolation 1.094–1.098 as untested.
- "The law lives in the link rapidity, not in the displacement of the kept state": the eigenprojector is still undefined over about half the profile, so it cannot serve as a profile-averaged ruler; the argument stands with "about half" in place of "most".
- K = 4φ²/sin²2φ, the centre-of-cut statement and the truncation approach: the review did not find them in Romatschke's paper; they stay as this paper's, without a novelty claim.

## Open

- The r = 0.8 third-level threshold (running).
- The Hu citation was not checked by the review.
- McCormick's paper text (section and equation numbers) could not be checked: not in his repository.
- Mixer: the package mixer is "The Standard Model in the Ball"; the author to confirm it is the intended explorer for this paper.
