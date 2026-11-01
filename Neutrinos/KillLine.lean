/-
Neutrinos: arithmetic of the pre-registered kill-line verdicts
(Jeromie Beasley, 31 October 2026).
G = (dc - 49773/100000) / (52832/100000 - 49773/100000) is the fraction of the way from the
reference threshold to the free-streaming threshold. Each test is compared with two predictions
and a tolerance of 0.08.
Developed with AI assistance.
-/
import Mathlib

namespace Neutrinos.KillLine

/-- The interpolation fraction `G`. -/
def G (dc : ℚ) : ℚ := (dc - 49773 / 100000) / (52832 / 100000 - 49773 / 100000)

theorem G_D : G (50245 / 100000) = 472 / 3059 := by norm_num [G]
theorem G_C : G (51756 / 100000) = 1983 / 3059 := by norm_num [G]
theorem G_B : G (50743 / 100000) = 970 / 3059 := by norm_num [G]

/-- Test D: `G` lies in `[0.15, 0.16]`, within `0.08` of `0.1176`, and not within `0.08` of `0.30`. -/
theorem testD_verdict :
    (15 / 100 : ℚ) ≤ G (50245 / 100000) ∧ G (50245 / 100000) ≤ 16 / 100
      ∧ |G (50245 / 100000) - 1176 / 10000| < 8 / 100
      ∧ 8 / 100 < |G (50245 / 100000) - 30 / 100| := by
  rw [G_D]
  refine ⟨by norm_num, by norm_num, ?_, ?_⟩
  · rw [abs_lt]; constructor <;> norm_num
  · rw [lt_abs]; right; norm_num

/-- Test C: `G` lies within `0.08` of both `0.6625` and `0.683`. -/
theorem testC_verdict :
    |G (51756 / 100000) - 6625 / 10000| < 8 / 100
      ∧ |G (51756 / 100000) - 683 / 1000| < 8 / 100 := by
  rw [G_C]
  refine ⟨?_, ?_⟩
  · rw [abs_lt]; constructor <;> norm_num
  · rw [abs_lt]; constructor <;> norm_num

/-- Test B: `G` lies within `0.08` of `0.246` and not within `0.08` of `0.431`. -/
theorem testB_verdict :
    |G (50743 / 100000) - 246 / 1000| < 8 / 100
      ∧ 8 / 100 < |G (50743 / 100000) - 431 / 1000| := by
  rw [G_B]
  refine ⟨?_, ?_⟩
  · rw [abs_lt]; constructor <;> norm_num
  · rw [lt_abs]; right; norm_num

end Neutrinos.KillLine
