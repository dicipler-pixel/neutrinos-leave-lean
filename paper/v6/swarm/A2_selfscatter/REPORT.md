# A2: does the frozen flux-shear link law predict what neutrino self-scattering does to the threshold?

Yes. The law, applied with nothing refitted, predicts δc = 0.51956 with self-scattering. McCormick measured 0.51941 ± 0.00016. The opposite (timing) reading also survives its kill line, but it misses by about seven times as much. This does not settle it, because the law's number depends on a reference threshold that his archive does not have at this mass (section 3).

The tool refused to write `REPORT.md` (subagents may not create report files), so the report is below. Every other output is in `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A2_selfscatter/`. No GR collapse runs were made, and McCormick's files were only read and imported, never changed.

## 1. What was read
- **McCormick's paper:** Sec. II B, Sec. IV E, App. C (a–d), Tables VII–VIII.
- **His code:** `ms_mg.py`, `run_mg.py`, `multigroup/weak_rates.py` and `weak_rates.json`.
- **His archived runs at T_H = 1 MeV:**
  - with self-scattering: `res_mg_phys6_10.0.json`, δc = 0.519406 ± 0.000156
  - without: `res_mg_nonunu6_10.0.json`, δc = 0.526391 ± 0.000109
  - perfect fluid: `res_eos_pf_10.0.json`, δc = 0.497422
  - single-rate family: `res_eosc_<Tdec>_10.0.json`
- **v5.1:** the section "The shear sets the threshold", Appendices A.1, A.7–A.9 and A.12, and `SplitRate.lean`.

**How κ_e and κ_n enter (Eq. C2–C3, as the code runs it).** Each group's collision term is

A κ_e,s (ε_s/4π − I) + A κ_n,s (ε_s/4π + c_s μ − I), with c_s = q_s / (2π Σ μ_k² Δμ).

- κ_e,s = C_e G_F² T⁴ χ_e(T_b) x_s T_ν,b, scaled locally by (T/T_b)⁴. Only this term passes momentum to the plasma.
- κ_n,s = C_n G_F² T_ν,b⁵ x_s, scaled locally by ε_ν/ε_ν,b.
- Both background rates are capped at 100 H.
- Transport starts at T_b = 8.15 MeV with self-scattering and at 10 MeV without it.
- Both archived runs use the first-order target (nnmode 0).
- κ_e is identical in the two runs: switching self-scattering off only zeroes κ_n.

## 2. Exact algebra (`step2_algebra.py`, `step2_out.txt`)
**The statement.** For one frozen group with the C3 target, the collision operator on his 32 angle bins is

C = −κ_e (1 − P₀) − κ_n (1 − P₀ − P₁).

- P₀ and P₁ project onto 1 and μ. They are orthogonal because the bins are symmetric, so ⟨1, μ⟩ = 0.
- In the discrete orthonormal Legendre basis, C = −diag(0, κ_e, κ_e+κ_n, κ_e+κ_n, …).
- This is exactly the split link of v5.1, with k1 = κ_e, k2 = κ_e + κ_n and r = 1 + κ_n/κ_e.
- The connection energy is (1/8)‖[L, L*]‖² = k²(c₀² κ_e² + c₁² κ_n²). In the continuum this is k²(κ_e²/3 + 4κ_n²/15).

**Checks on the 32-bin grid**
| Check | Error |
|---|---|
| Operator against −diag(0, κ_e, κ_e+κ_n, …) | 3.6e−15 |
| Operator against the projector form (no basis) | 1.1e−16 |
| Eigenvalues | one 0, one −κ_e, 30 at −(κ_e+κ_n) |
| κ_n part taken from McCormick's own compiled `rhs()` (two calls differing only in κ_n) | 4.9e−15 |
| Connection energy at N_μ = 32, 64, 128, 1024 | relative 4e−16 |

**Discrete weights.** These were observed to machine precision at those four grid sizes; they are not proven.
- c₀² = 1/3 − Δμ²/12, which is v5.1's m₂/2.
- c₁² = (4/15)(1 − Δμ²).
- At 32 bins the continuum form is high by 0.37%.

**Lean-ready statement** (text only, not built; it instances `splitRateEnergy` with k1 = κ_e, k2 = κ_e + κ_n):
```lean
/-- McCormick's App. C collision term (plasma drag κe on the dipole, neutrino self-scattering κn on l ≥ 2):
the flux–shear link carries exactly the self-scattering rate. -/
theorem selfScatterEnergy (k κe κn : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 (k / Real.sqrt 3) (2 * k / Real.sqrt 15) κe (κe + κn)))
      = k ^ 2 * κe ^ 2 / 3 + (4 * k ^ 2 / 15) * κn ^ 2 := by
  rw [splitRateEnergy]; ring
```
The bin version would instance `splitRateEnergy_ab` with a² = (k²/3)(1 − Δμ²/4) and b² = (4k²/15)(1 − Δμ²).

## 3. The prediction (`PREREGISTERED.txt`, `step3_predict.py`, `step3_out.txt`, `step3_predictions.json`)
The method, weighting, references and kill lines were written at 14:04Z, before the rate script existed. The file records what was already visible: both thresholds are in the task, and the paper quotes rate ratios of 1.5 and 7.

**References for G**
- δ_fluid = 0.49742, from his Table VII.
- **His archive has no instantaneous free-streaming threshold at T_H = 1 MeV with the full equation of state.** The `res_eos_fs_*` runs stop at T_H = 0.506 MeV.
- I used δ_inst = 0.53379 as a stand-in. That is his pure-radiation run with R_ν = 0.488. The background R_ν at the epoch where the flux link lets go is 0.4877.
- His R_ν = 0.409 value (0.52832) cannot be the reference here: his own single-rate run with Tdec = 3 MeV at this mass already sits higher, at 0.53065.

**r_s(t) on the background, as `run_mg.rates` evaluates it**
- It is almost constant in time and energy: ν_e 2.43–2.45 and ν_μ,τ 7.69–7.77 for 0.3 < T_b < 5 MeV.
- The 100 H caps set r = 2 only for the top groups above about 5 MeV, where those groups carry no weight.

**Link rapidity**
- u = ½ ln r, weighted by when each group's flux link lets go, then energy-weighted over groups and flavours.
- **u_eff = 0.8313** (r_eff = 5.27). By flavour: ν_e 0.4468, ν_μ,τ 1.0235.
- Three other weightings agree to 0.2%: the total-rate release, a uniform window 0.1 < κ_e/H < 10, and v5.1's readout at ε* = 1.7 / 4.0.

**The frozen law**, applied from the threshold without self-scattering (G = 0.7965):

| Rate | G with | Shift in G | Predicted δc with |
|---|---|---|---|
| 1.11 (all ℓ ≥ 2) | 0.6087 | −0.1878 | **0.51956** |
| 1.19 (shear only) | 0.5928 | −0.2037 | 0.51898 |
| 1.20 (shear only) | 0.5908 | −0.2057 | 0.51891 |

**The opposite reading (timing).** Self-scattering only delays isotropy, so the threshold follows the decoupling temperature set by the total rate (mean rate = H).
- Tdec_eff is 1.552 MeV without self-scattering and 0.979 MeV with it.
- Through McCormick's single-rate family at T_H = 1 MeV this gives δc = 0.52613 without and 0.52040 with.
- Predicted shift in G: −0.1576.

## 4. Comparison (`step4_compare.py`, `step4_out.txt`)
Measured: G goes from 0.7966 to 0.6045, a shift of **−0.1920 ± 0.0052**. The kill tolerance is 0.096.

| Reading | Shift in G | Miss (% of shift) | δc with, predicted | Miss in δc | Verdict |
|---|---|---|---|---|---|
| Link law, rate 1.11 (deciding) | −0.1878 | 2.2% | 0.51956 | +0.00015 | **survives** |
| Link law, rate 1.19 / 1.20 | −0.2037 / −0.2057 | 6.1% / 7.1% | 0.51898 / 0.51891 | −0.00043 / −0.00050 | survives |
| Timing (opposite) | −0.1576 | 17.9% | 0.52040 (0.52066 anchored) | +0.00099 (+0.00125) | survives |

**What favours the link law**
- It lands within about one bracket half-width of the measured value.
- Using v5.1's eleven measured offsets directly, instead of the straight line, gives 0.51930, a miss of −0.00011.
- The timing reading gets the no-self-scattering point almost right (0.52613 against 0.52639). It misses the self-scattering point by about 0.001, in the direction the link law accounts for.

**What keeps it from being decisive**
- The link law's absolute number rests on the δ_inst stand-in. Moving δ_inst from 0.5315 to 0.5370 moves its δc miss from +0.0016 to −0.0014; the kill line holds over that whole range.
- The rate 1.11 was measured in pure radiation at ε_dec = 2 (G ≈ 0.43), with one group and constant r. Here G ≈ 0.80, and r = 7.7 for ν_μ,τ is outside the admissible window 3/4 ≤ r ≤ 3/2. That the rate carries over is the frozen assumption, tested only at this one point.

## 5. The simplest decisive simulation (not run)
In a copy of `ms_mg.py`, change the nnmode-0 self-scattering term to target isotropy in the plasma frame, κ_n(ε_s/4π − I), and add κ_n,s q_s to the momentum given to the plasma. This keeps the total isotropy history exactly as it is but sets r = 1, with flux rate κ_e + κ_n.

Run one bisection at T0 = 10 MeV (6 groups, 0.4–20, N = 300, 32 angle bins) to ±1e−4. The two readings then disagree:
- **Timing reading:** about 0.5194, unchanged, because the total-rate history is the same.
- **Link law:** about 0.5204 ± 0.0003. This is the r = 1 threshold at that flux rate; the ±0.0003 comes from the family mapping's 0.00026 miss on the no-self-scattering point.

Proposed kill lines for it: a result above 0.5194 by more than 0.0005 favours the link law; within ±0.0003 of 0.5194 favours timing.

One instantaneous free-streaming run at T_H = 1 MeV with the full equation of state (`run_eos` kind 'fs', T0 = 10) would replace the δ_inst stand-in.

## Files
All are in `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A2_selfscatter/`:
- `PREREGISTERED.txt`: method written at 14:04Z, then predictions, then comparison, appended in that order
- `step2_algebra.py`, `step2_out.txt`
- `step3_predict.py`, `step3_out.txt`, `step3_predictions.json`
- `step4_compare.py`, `step4_out.txt`
- `mcc.txt`, `mcc_raw.txt`: text extracted from McCormick's PDF