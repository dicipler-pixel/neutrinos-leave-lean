/-
The flux-shear link: exact algebra and the verdict arithmetic of Tests J and K
(*When the Neutrinos Leave*, version 4 and its audit, 4 November 2026).

Lean checks:
* the link coordinate `(r - 1)/(r + 1)` is odd under `r ↦ 1/r`;
* the reference point cancels from the odd part of the offset;
* the streaming weights `c_ℓ² = (ℓ+1)²/((2ℓ+1)(2ℓ+3))` and the ratios `c₀²/c₁² = 5/4`, `c₁²/c₂² = 28/27`;
* the verdicts, as exact rational comparisons with no logarithm: with `O(δ) = (δ_inst - δ)/(δ - δ_fluid)`
  (the odds `(1 - G)/G`) and `Q = O(δ_r)/O(δ_{1/r})`, the odd rate `ln Q / ln r` lies in `[p/q, p'/q]`
  exactly when `r^p ≤ Q^q ≤ r^p'`.  `O` decreases in `δ`, so `Q` is smallest at (upper edge of the `r` bracket,
  lower edge of the `1/r` bracket) and largest at the opposite corner; both corners are checked.

Lean does NOT check: the simulation, the bracket edges themselves (they are inputs, copied to ten decimals from the
run logs), McCormick's reference thresholds `0.49773` and `0.52832`, or whether a run that crashed was correctly excluded.
-/
import Mathlib

namespace Neutrinos.LinkVerdict

/-- The Smith coordinate of a link whose two rates have ratio `r`. -/
noncomputable def gam (r : ℝ) : ℝ := (r - 1) / (r + 1)

/-- Exchanging the ends of a link negates its coordinate. -/
theorem gam_inv (r : ℝ) (hr : 0 < r) : gam (1 / r) = - gam r := by
  have h1 : r ≠ 0 := hr.ne'
  have h2 : r + 1 ≠ 0 := by linarith
  have h3 : 1 + r ≠ 0 := by linarith
  unfold gam
  field_simp
  ring

/-- The reference value cancels from the odd part of the offset. -/
theorem odd_part_free_of_anchor (a b t₁ : ℝ) : (a - t₁) - (b - t₁) = a - b := by ring

/-- Squared streaming weight of the link `ℓ → ℓ + 1` of the Legendre chain. -/
def cSq (ℓ : ℕ) : ℚ := ((ℓ : ℚ) + 1) ^ 2 / ((2 * ℓ + 1) * (2 * ℓ + 3))

theorem cSq_zero : cSq 0 = 1 / 3 := by norm_num [cSq]
theorem cSq_one : cSq 1 = 4 / 15 := by norm_num [cSq]
theorem cSq_two : cSq 2 = 9 / 35 := by norm_num [cSq]
theorem weight_ratio_01 : cSq 0 / cSq 1 = 5 / 4 := by norm_num [cSq]
theorem weight_ratio_12 : cSq 1 / cSq 2 = 28 / 27 := by norm_num [cSq]

/-! ### The verdicts, in whole numbers

All thresholds are written as integers on a common scale (`10¹⁰` for Test K, `10⁹` for Test J); McCormick's reference
thresholds `δ_fluid = 0.49773` and `δ_inst = 0.52832` are inputs.  With `O(δ) = (δ_inst - δ)/(δ - δ_fluid)` and
`Q = O(δ_r)/O(δ_{1/r}) = qNum/qDen`, where `qNum = (I - Dr)(D1r - F)` and `qDen = (Dr - F)(I - D1r)`, the odd rate
`ln Q / ln r` with `r = u/v` is at least `p/q` exactly when `u^p qDen^q ≤ v^p qNum^q`, and at most `p/q` exactly when
`v^p qNum^q ≤ u^p qDen^q`.  `O` decreases in `δ`, so `Q` is smallest at (upper edge of the `r` bracket, lower edge of the
`1/r` bracket) and largest at the opposite corner; both corners are checked.  Each comparison is decided by the kernel. -/

abbrev qNum (I F Dr D1r : ℕ) : ℕ := (I - Dr) * (D1r - F)
abbrev qDen (I F Dr D1r : ℕ) : ℕ := (Dr - F) * (I - D1r)

/-- The odd rate is at least `p/q` (ratio `r = u/v`). -/
abbrev rateAtLeast (u v p q : ℕ) (I F Dr D1r : ℕ) : Prop :=
  u ^ p * qDen I F Dr D1r ^ q ≤ v ^ p * qNum I F Dr D1r ^ q
/-- The odd rate is at most `p/q` (ratio `r = u/v`). -/
abbrev rateAtMost (u v p q : ℕ) (I F Dr D1r : ℕ) : Prop :=
  v ^ p * qNum I F Dr D1r ^ q ≤ u ^ p * qDen I F Dr D1r ^ q

/-! ### Test K, `r = 5/4`, scale `10¹⁰` -/

/-- First search, clean edges only: `r = 1.25` bracket `[0.5098390947, 0.5098432099]`, `r = 0.8` bracket
`[0.5116938272, 0.5117144033]`.  The whole odd-rate range lies inside the `√(5/4)` window `[1.108, 1.128]`. -/
theorem testK_first_sqrt_window :
    rateAtLeast 5 4 277 250 5283200000 4977300000 5098432099 5116938272 ∧
    rateAtMost 5 4 282 250 5283200000 4977300000 5098390947 5117144033 := by
  constructor <;> decide +kernel

/-- First search, clean edges: the range reaches below `1.113`, the top of the trend window: not killed. -/
theorem testK_first_trend_not_killed :
    ¬ rateAtLeast 5 4 1113 1000 5283200000 4977300000 5098432099 5116938272 := by decide +kernel

/-- First search with the crashed run `0.5117102881` as the lower `r = 0.8` edge: the whole range sat above `1.113`.
That was the false kill. -/
theorem testK_crash_edge_false_kill :
    rateAtLeast 5 4 1113 1000 5283200000 4977300000 5098432099 5117102881 := by decide +kernel

/-- Clean reruns at tolerance `10⁻⁶`: `r = 1.25` bracket `[0.5098404700, 0.5098409200]`, `r = 0.8` bracket
`[0.5116953500, 0.5116961100]`.  The odd rate lies in `[1.112, 1.114]`. -/
theorem testK_clean_range :
    rateAtLeast 5 4 1112 1000 5283200000 4977300000 5098409200 5116953500 ∧
    rateAtMost 5 4 1114 1000 5283200000 4977300000 5098404700 5116961100 := by
  constructor <;> decide +kernel

/-- After the clean reruns, `√(5/4) = 1.1180…` lies above the measured range: the odd rate is below `1.117`. -/
theorem testK_clean_below_sqrt :
    rateAtMost 5 4 1117 1000 5283200000 4977300000 5098404700 5116961100 := by decide +kernel

/-- After the clean reruns, the trend value `1.103` lies below the measured range: the odd rate is above `1.11`. -/
theorem testK_clean_above_trend :
    rateAtLeast 5 4 111 100 5283200000 4977300000 5098409200 5116953500 := by decide +kernel

/-! ### Test J, `r = 2`, scale `10⁹` -/

/-- Over its full bracket (`r = 2`: `[0.507962963, 0.507983539]`; `r = 1/2`: `[0.513646090, 0.513666667]`) the odd rate of
Test J straddles `1.108`, the lower edge of the `√(5/4)` window, and stays at most `1.128`. -/
theorem testJ_straddles :
    ¬ rateAtLeast 2 1 277 250 528320000 497730000 507983539 513646090 ∧
    ¬ rateAtMost 2 1 277 250 528320000 497730000 507962963 513666667 ∧
    rateAtMost 2 1 282 250 528320000 497730000 507962963 513666667 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide +kernel

end Neutrinos.LinkVerdict
