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

/-- McCormick's reference thresholds (inputs). -/
def dFluid : ℚ := 49773 / 100000
def dInst : ℚ := 52832 / 100000

/-- The odds `(1 - G)/G` of a threshold `δ`. -/
def odds (d : ℚ) : ℚ := (dInst - d) / (d - dFluid)

/-! ### Test K, `r = 5/4`.  Bracket edges from the clean runs (crashed runs excluded). -/

def kAlo : ℚ := 5098390947 / 10000000000   -- r = 1.25, dispersed
def kAhi : ℚ := 5098432099 / 10000000000   -- r = 1.25, BH
def kBlo : ℚ := 5116938272 / 10000000000   -- r = 0.8, dispersed (last clean)
def kBhi : ℚ := 5117144033 / 10000000000   -- r = 0.8, BH
/-- The lower edge the first search used, which was a crashed run. -/
def kBcrash : ℚ := 5117102881 / 10000000000

def kQmin : ℚ := odds kAhi / odds kBlo
def kQmax : ℚ := odds kAlo / odds kBhi

/-- With clean edges the whole odd-rate range of Test K lies inside the `√(5/4)` window `[1.108, 1.128]`. -/
theorem testK_sqrt_window : (5 / 4 : ℚ) ^ 277 ≤ kQmin ^ 250 ∧ kQmax ^ 250 ≤ (5 / 4 : ℚ) ^ 282 := by
  constructor <;> norm_num [kQmin, kQmax, odds, kAlo, kAhi, kBlo, kBhi, dFluid, dInst]

/-- With clean edges the range reaches below `1.113`, the top of the trend window `[1.093, 1.113]`:
the trend reading is not killed by Test K. -/
theorem testK_trend_not_killed : kQmin ^ 1000 < (5 / 4 : ℚ) ^ 1113 := by
  norm_num [kQmin, odds, kAhi, kBlo, dFluid, dInst]

/-- With the crashed run used as an edge, the range sat wholly above `1.113`: that is the false kill. -/
theorem testK_crash_edge_false_kill : (5 / 4 : ℚ) ^ 1113 < (odds kAhi / odds kBcrash) ^ 1000 := by
  norm_num [odds, kAhi, kBcrash, dFluid, dInst]

/-! ### Test J, `r = 2`. -/

def jAlo : ℚ := 507962963 / 1000000000    -- r = 2, dispersed
def jAhi : ℚ := 507983539 / 1000000000    -- r = 2, BH
def jBlo : ℚ := 513646090 / 1000000000    -- r = 1/2, dispersed
def jBhi : ℚ := 513666667 / 1000000000    -- r = 1/2, BH

def jQmin : ℚ := odds jAhi / odds jBlo
def jQmax : ℚ := odds jAlo / odds jBhi

/-- The odd-rate range of Test J straddles the lower edge `1.108` of the `√(5/4)` window and stays below `1.128`:
over its full bracket Test J neither passes nor kills that reading. -/
theorem testJ_straddles : jQmin ^ 250 < (2 : ℚ) ^ 277 ∧ (2 : ℚ) ^ 277 < jQmax ^ 250 ∧
    jQmax ^ 250 ≤ (2 : ℚ) ^ 282 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num [jQmin, jQmax, odds, jAlo, jAhi, jBlo, jBhi, dFluid, dInst]

end Neutrinos.LinkVerdict
