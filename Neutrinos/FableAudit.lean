import Mathlib

/-!
# Independent audit arithmetic for Tests J and K (flux–shear link, v4 runs)

Written as an independent check, not compiled locally (no Mathlib build here).

WHAT LEAN CHECKS HERE
 (a) the link coordinate (r-1)/(r+1) is odd under r -> 1/r for r > 0;
 (b) the Legendre streaming weights c_l^2 = (l+1)^2/((2l+1)(2l+3)) give
     c0^2/c1^2 = 5/4, c1^2/c2^2 = 28/27 (and c0^2/c2^2 = 35/27) exactly;
 (c) the verdict arithmetic of Tests J and K as exact rational comparisons,
     with no logarithms: for r > 1 the odd rate [tau(r) - tau(1/r)]/ln r lies
     in [p/q, p'/q'] iff r^p <= Q^q and Q^q' <= r^p', where
         Q = O(r)/O(1/r),  O(dc) = (1-G)/G = (ins - dc)/(dc - fl),
         fl = 0.49773, ins = 0.52832  (McCormick's reference thresholds).
     The bracket endpoints dc +- w/2 are taken from the res_*.json files
     (exact decimals, rounded OUTWARD to 10 places so every bracket here
     contains the driver's bracket).  O is decreasing in dc on (fl, ins), so
         Q is LARGEST at (dc_r = lower end, dc_{1/r} = upper end)  -> Qmax,
         Q is SMALLEST at (dc_r = upper end, dc_{1/r} = lower end) -> Qmin.
     These two corners bound the odd rate from above and below over the
     whole bracket rectangle (Q is monotone in each coordinate separately).
 (d) a bridge lemma from the rational comparisons to the logarithmic form.

WHAT LEAN DOES NOT CHECK
 - McCormick's code, the modified solver ms_nuc_split.py, the collapse runs,
   the BH/dispersed/crash classification, or the bracket values themselves:
   the dc, w numbers below are INPUT DATA copied from res_K_r125.json,
   res_K_r08.json, res_J_r2.json, res_J_r05.json.
 - That the reference thresholds 0.49773 and 0.52832 are correct or exact.
 - Anything about physics: that the odd rate "is" c0/c1 is not a theorem
   anywhere in this file; the file only shows which pre-registered windows
   the measured corners fall in, under two treatments of the two runs in
   res_K_r08.json whose status was "crash" (the driver trisect_split.py
   silently counted them as "dispersed"; the "honest" variant below keeps
   the last genuinely dispersed point as the lower end of that bracket).
-/

namespace Neutrinos.FableAudit

/-! ## (a) The link coordinate is odd under inversion -/

/-- Gamma(r) = (r-1)/(r+1).  For r > 0, Gamma(1/r) = -Gamma(r). -/
theorem link_coord_odd (r : ℝ) (hr : 0 < r) :
    (1 / r - 1) / (1 / r + 1) = -((r - 1) / (r + 1)) := by
  have hr0 : r ≠ 0 := hr.ne'
  have h1 : r + 1 ≠ 0 := by positivity
  have h2 : 1 / r + 1 ≠ 0 := by positivity
  field_simp
  ring

/-- Same statement as a sum: Gamma(1/r) + Gamma(r) = 0. -/
theorem link_coord_sum_zero (r : ℝ) (hr : 0 < r) :
    (1 / r - 1) / (1 / r + 1) + (r - 1) / (r + 1) = 0 := by
  rw [link_coord_odd r hr]; ring

/-! ## (b) Streaming weights of the Legendre chain -/

/-- c_l^2 = (l+1)^2 / ((2l+1)(2l+3)). -/
def cSq (l : ℕ) : ℚ := ((l : ℚ) + 1) ^ 2 / ((2 * (l : ℚ) + 1) * (2 * (l : ℚ) + 3))

theorem cSq_zero : cSq 0 = 1 / 3 := by norm_num [cSq]
theorem cSq_one : cSq 1 = 4 / 15 := by norm_num [cSq]
theorem cSq_two : cSq 2 = 9 / 35 := by norm_num [cSq]

theorem ratio_c0_c1 : cSq 0 / cSq 1 = 5 / 4 := by norm_num [cSq]
theorem ratio_c1_c2 : cSq 1 / cSq 2 = 28 / 27 := by norm_num [cSq]
/-- The next weight ratio, relevant to the proposed "jump at l = 3" test and
to the far point 1.139 = sqrt(35/27) to three digits. -/
theorem ratio_c0_c2 : cSq 0 / cSq 2 = 35 / 27 := by norm_num [cSq]

/-! ## (c) Verdict arithmetic, exact rationals, no logarithms

Reference thresholds (McCormick, Gaussian profile, R_nu = 0.409). -/

def fl : ℚ := 0.49773
def ins : ℚ := 0.52832

/-- O(dc) = (1-G)/G with G = (dc - fl)/(ins - fl). -/
def O (dc : ℚ) : ℚ := (ins - dc) / (dc - fl)

/-- (1-G)/G is exactly (ins - dc)/(dc - fl): the G normalisation cancels. -/
theorem O_eq_G (dc : ℚ) (h1 : dc - fl ≠ 0) (h2 : ins - fl ≠ 0) :
    (1 - (dc - fl) / (ins - fl)) / ((dc - fl) / (ins - fl)) = O dc := by
  unfold O
  field_simp
  ring

/-! ### Bracket endpoints (INPUT DATA from the json files, rounded outward)

Test K (tolerance 1e-5, initial bracket width 0.003, six trisection rounds,
reported w = 0.003/729 = 4.115e-6).
  res_K_r125.json : dc = 0.5098411522633745, w = 4.115226337475519e-6
  res_K_r08.json  : dc = 0.5117123456790122, w = 4.115226337364497e-6
Honest r = 0.8 bracket: the two runs at delta = 0.51170617 and 0.51171029
returned "crash"; the last run that actually dispersed is 0.51169383 and the
first that actually formed a black hole is 0.51171440.
Test J (tolerance 5e-5, initial width 0.005, five rounds, w = 0.005/243).
  res_J_r2.json  : dc = 0.5079732510288066, w = 2.0576131687266574e-5
  res_J_r05.json : dc = 0.513656378600823,  w = 2.0576131687266574e-5 -/

def K125_lo : ℚ := 0.5098390946   -- r = 1.25, lower end of bracket
def K125_hi : ℚ := 0.5098432099   -- r = 1.25, upper end
def K08_lo  : ℚ := 0.5117102880   -- r = 0.8, lower end as the driver reported it
def K08_hi  : ℚ := 0.5117144033   -- r = 0.8, upper end
def K08_lo_honest : ℚ := 0.5116938271   -- r = 0.8, last run that really dispersed

def J2_lo  : ℚ := 0.5079629629   -- r = 2
def J2_hi  : ℚ := 0.5079835391
def J05_lo : ℚ := 0.5136460905   -- r = 1/2
def J05_hi : ℚ := 0.5136666667

/-- Q is smallest at (dc_r upper end, dc_{1/r} lower end): O decreases in dc,
so O(r) is smallest and O(1/r) largest there. -/
def QK_min : ℚ := O K125_hi / O K08_lo
/-- Q is largest at (dc_r lower end, dc_{1/r} upper end). -/
def QK_max : ℚ := O K125_lo / O K08_hi
/-- Same corner with the honest r = 0.8 bracket (crash runs not counted). -/
def QK_min_honest : ℚ := O K125_hi / O K08_lo_honest

def QJ_min : ℚ := O J2_hi / O J05_lo
def QJ_max : ℚ := O J2_lo / O J05_hi

/-! ### Test K, windows as pre-registered
  sqrt(5/4) window [1.108, 1.128] = [277/250, 141/125]
  trend window     [1.093, 1.113] = [1093/1000, 1113/1000]
  r = 5/4.
Reported result 1.1223; corners here give the odd rate in [1.1198, 1.1248]. -/

/-- Lower edge of the sqrt(5/4) window, reported bracket: rate >= 1.108. -/
theorem K_reported_above_1108 : (5 / 4 : ℚ) ^ 277 ≤ QK_min ^ 250 := by
  unfold QK_min O K125_hi K08_lo ins fl; norm_num

/-- Upper edge of the sqrt(5/4) window, reported bracket: rate <= 1.128. -/
theorem K_reported_below_1128 : QK_max ^ 125 ≤ (5 / 4 : ℚ) ^ 141 := by
  unfold QK_max O K125_lo K08_hi ins fl; norm_num

/-- The paper's kill of the trend reading: the smallest corner already
exceeds 1.113, so the whole reported bracket lies above the trend window. -/
theorem K_reported_kills_trend : (5 / 4 : ℚ) ^ 1113 < QK_min ^ 1000 := by
  unfold QK_min O K125_hi K08_lo ins fl; norm_num

/-- With the honest r = 0.8 bracket the sqrt(5/4) window still holds at the
lower edge (rate >= 1.108; the corner is 1.1101). -/
theorem K_honest_above_1108 : (5 / 4 : ℚ) ^ 277 ≤ QK_min_honest ^ 250 := by
  unfold QK_min_honest O K125_hi K08_lo_honest ins fl; norm_num

/-- ...but the trend reading is NOT killed: the honest lower corner lies
below 1.113, inside the trend window.  The K verdict on the trend reading
depends entirely on counting two crashed runs as "dispersed". -/
theorem K_honest_trend_not_killed : QK_min_honest ^ 1000 < (5 / 4 : ℚ) ^ 1113 := by
  unfold QK_min_honest O K125_hi K08_lo_honest ins fl; norm_num

/-- The two pre-registered windows of Test K overlap on [1.108, 1.113]:
a value there would have killed neither reading. -/
theorem K_windows_overlap : (277 / 250 : ℚ) < 1113 / 1000 := by norm_num

/-! ### Test J, window [1.108, 1.128], r = 2
Reported 1.1093 +- 0.0031 "survives at the edge".  Corners: [1.1052, 1.1134]. -/

/-- The lower corner of J lies BELOW the window (rate < 1.108). -/
theorem J_lower_corner_below_window : QJ_min ^ 250 < (2 : ℚ) ^ 277 := by
  unfold QJ_min O J2_hi J05_lo ins fl; norm_num

/-- The upper corner of J lies inside the window. -/
theorem J_upper_corner_above_1108 : (2 : ℚ) ^ 277 ≤ QJ_max ^ 250 := by
  unfold QJ_max O J2_lo J05_hi ins fl; norm_num

theorem J_upper_corner_below_1128 : QJ_max ^ 125 ≤ (2 : ℚ) ^ 141 := by
  unfold QJ_max O J2_lo J05_hi ins fl; norm_num

/-! ### J against K: are the bracket intervals disjoint?
Under the reported brackets: J <= 1.114 < 1.119 <= K, so the two hard
intervals do not touch (this is the "2.5 sigma" of the log, which under
hard bounds is not a fluctuation at all but a certain non-monotonicity or
an unmodelled systematic).  Under the honest K bracket they overlap. -/

theorem J_rate_le_1114 : QJ_max ^ 500 ≤ (2 : ℚ) ^ 557 := by
  unfold QJ_max O J2_lo J05_hi ins fl; norm_num

theorem K_reported_rate_ge_1119 : (5 / 4 : ℚ) ^ 1119 ≤ QK_min ^ 1000 := by
  unfold QK_min O K125_hi K08_lo ins fl; norm_num

theorem K_honest_rate_le_1114 : QK_min_honest ^ 500 ≤ (5 / 4 : ℚ) ^ 557 := by
  unfold QK_min_honest O K125_hi K08_lo_honest ins fl; norm_num

/-! ### Specificity of the window [1.108, 1.128]
Each statement says that an n-th root of a small number lies in the window:
x in [1.108, 1.128] iff 1.108^n <= x^n <= 1.128^n.  None of these is a
physics claim; they show how many "natural" constants the window admits. -/

theorem sqrt54_in_window : (1.108 : ℚ) ^ 2 < 5 / 4 ∧ (5 / 4 : ℚ) < 1.128 ^ 2 := by
  constructor <;> norm_num
theorem root6_2_in_window : (1.108 : ℚ) ^ 6 < 2 ∧ (2 : ℚ) < 1.128 ^ 6 := by
  constructor <;> norm_num
theorem root10_3_in_window : (1.108 : ℚ) ^ 10 < 3 ∧ (3 : ℚ) < 1.128 ^ 10 := by
  constructor <;> norm_num
theorem root14_5_in_window : (1.108 : ℚ) ^ 14 < 5 ∧ (5 : ℚ) < 1.128 ^ 14 := by
  constructor <;> norm_num
theorem root20_10_in_window : (1.108 : ℚ) ^ 20 < 10 ∧ (10 : ℚ) < 1.128 ^ 20 := by
  constructor <;> norm_num
theorem ten_ninths_in_window : (1.108 : ℚ) < 10 / 9 ∧ (10 / 9 : ℚ) < 1.128 := by
  constructor <;> norm_num
theorem nine_eighths_in_window : (1.108 : ℚ) < 9 / 8 ∧ (9 / 8 : ℚ) < 1.128 := by
  constructor <;> norm_num
/-- The next link-weight ratio c0/c2 = sqrt(35/27) = 1.1386 is OUTSIDE the
window, but matches the far point (|x| = 1.386, rate 1.139) to three digits. -/
theorem c0_c2_outside_window : (1.128 : ℚ) ^ 2 < 35 / 27 := by norm_num

/-! ## (d) Bridge to the logarithmic form (reals)

For Q > 0 and r > 1:  log Q / log r <= b  iff  Q <= r ^ b,  and
for 0 <= Q, 0 <= r, q > 0:  Q <= r ^ (p/q)  iff  Q ^ q <= r ^ p.
Together they turn each rational theorem above into a statement about the
odd rate [tau(r) - tau(1/r)] / ln r = log Q / log r. -/

theorem rate_le_iff {Q r b : ℝ} (hQ : 0 < Q) (hr : 1 < r) :
    Real.log Q / Real.log r ≤ b ↔ Q ≤ r ^ b := by
  have hr0 : 0 < r := by linarith
  have hlr : 0 < Real.log r := Real.log_pos hr
  rw [div_le_iff₀ hlr, ← Real.log_rpow hr0 b]
  exact Real.log_le_log_iff hQ (Real.rpow_pos_of_pos hr0 b)

theorem le_rate_iff {Q r a : ℝ} (hQ : 0 < Q) (hr : 1 < r) :
    a ≤ Real.log Q / Real.log r ↔ r ^ a ≤ Q := by
  have hr0 : 0 < r := by linarith
  have hlr : 0 < Real.log r := Real.log_pos hr
  rw [le_div_iff₀ hlr, ← Real.log_rpow hr0 a]
  exact Real.log_le_log_iff (Real.rpow_pos_of_pos hr0 a) hQ

theorem le_rpow_div_iff {Q r : ℝ} (hQ : 0 ≤ Q) (hr : 0 ≤ r) (p q : ℕ) (hq : 0 < q) :
    Q ≤ r ^ ((p : ℝ) / q) ↔ Q ^ q ≤ r ^ p := by
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq
  have hq0 : (q : ℝ) ≠ 0 := hqR.ne'
  have hmul : ((p : ℝ) / q) * q = p := by field_simp
  have key : (r ^ ((p : ℝ) / q)) ^ (q : ℝ) = r ^ p := by
    rw [← Real.rpow_mul hr, hmul, Real.rpow_natCast]
  rw [← Real.rpow_le_rpow_iff hQ (Real.rpow_nonneg hr _) hqR, key, Real.rpow_natCast]

theorem rpow_div_le_iff {Q r : ℝ} (hQ : 0 ≤ Q) (hr : 0 ≤ r) (p q : ℕ) (hq : 0 < q) :
    r ^ ((p : ℝ) / q) ≤ Q ↔ r ^ p ≤ Q ^ q := by
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq
  have hq0 : (q : ℝ) ≠ 0 := hqR.ne'
  have hmul : ((p : ℝ) / q) * q = p := by field_simp
  have key : (r ^ ((p : ℝ) / q)) ^ (q : ℝ) = r ^ p := by
    rw [← Real.rpow_mul hr, hmul, Real.rpow_natCast]
  rw [← Real.rpow_le_rpow_iff (Real.rpow_nonneg hr _) hQ hqR, key, Real.rpow_natCast]

end Neutrinos.FableAudit
