# A5: controlled kinetic tests on the linear chain (v5.1 objects)

The house rules ask for `REPORT.md` in the folder, but the tool here blocked writing report files, so this message is the report. Every prediction and kill line was written to `PREREGISTERED.txt` at 2026-11-11T14:10Z, before any computation. The verdicts are appended under it; nothing above was edited.

Main findings:
1. **Order is visible.** Pairs with the same total opacity but different order give l≤2 readouts that differ by 33–72%, and memory-form values g2 that differ by 0.06–0.16. That is at or above v5.1's kill line of 0.08, so the memory form predicts that the threshold separates the two orders. That is untested in GR.
2. **Nothing hidden is fully invisible.** In this truncated chain the predictive quotient V/N_∞ is the whole hidden space. What carries information is the spectrum of the readout Gramian G. Its top direction is odd, l=3-dominated (0.92–0.99), with an l=5 admixture.
3. **Only the exact elimination is exact.** Every instantaneous closure misses badly for early decoupling. The exact elimination of l≥3 is exact to 4.6e-6. M1 and M2 entropy closures reduce exactly to P1 and P2 at linear order.
4. **Prior art not read.** All four allowed web requests were used but none returned paper text; what I say about the two papers is from memory.

**Setup.** This is v5.1's chain:
- dv/dτ = −(ikM + D(τ))v, with D = σ·diag(0,1,1,…), or σ·diag(0,1,r,r,…) for the split case.
- σ = ed^n/τ^(n+1).
- Start v = |0⟩ at τ0 = 0.02, LM = 60.
- Profile weights k²e^(−k²/2) on 36 k-points.

The chain reproduces v5.1's `memory_curve.py`:

| case | g(1.7) here | g2 here | v5.1 |
|---|---|---|---|
| n=3, ed=2 | 0.3432 | 0.4110 | 0.344 / 0.411 |
| n=3, ed=0.25 | 0.9404 | 0.9467 | 0.941 / 0.947 |
| n=6, ed=3 | 0.0256 | 0.1175 | 0.026 / 0.118 |

The 0.001 offset at 1.7 is v5.1's grid index landing just past 1.7.

## 1. Rate-order swap
There are two families of pairs:
- **Family R:** σ is reversed in time inside a window W and left unchanged outside it.
- **Family S:** v5.1's n=6 histories against an n=3 history whose ed3 is rescaled to give the same ∫_W σ.

**The scalar summaries are blind, as predicted (P1a–c confirmed):**
- Optical depth is equal by construction.
- Time-integrated connection energy ∫(k²/3)σ² (split case: k²[σ1²/3 + 4(σ2−σ1)²/15]) is identical under reversal.
- The operator at readout (σ(ε\*), connection energy, E_B) is identical whenever W closes before ε\*.
- In family S these are not blind but simply different: the n=6 member's ∫σ² is 2.09–2.15× the n=3 member's at equal optical depth.

**The exact readout is not blind: P1d holds for every pair.** The kill line was R_diff < 1e-3.

| pair | W | dg(1.7) | dg(4) | R_diff at 1.7 / 4 | g2 forward → reversed |
|---|---|---|---|---|---|
| R1: n3, ed1 | [0.5, 1.5] | −0.070 | −0.014 | 0.45 / 0.43 | 0.705 → 0.641 |
| R2: n3, ed1 | [0.25, 1.5] | −0.118 | −0.023 | 0.56 / 0.56 | 0.705 → 0.598 |
| R3: n6, ed1 | [0.5, 1.5] | −0.130 | −0.021 | 0.56 / 0.57 | 0.662 → 0.544 |
| R4: n3, ed2 (1.7 is inside W) | [1, 3.5] | +0.184 | −0.022 | 0.33 / 0.72 | 0.411 → 0.572 |
| R5: split, r=4 | [0.5, 1.5] | −0.070 | −0.009 | 0.45 / 0.43 | 0.712 → 0.649 |
| R6: split, r=1/4 | [0.5, 1.5] | −0.074 | −0.016 | 0.43 / 0.47 | 0.700 → 0.633 |

- The l≤2 powers move a lot. In R1 at ε\*=1.7, |v1|² is 0.292 forward and 0.042 reversed.
- **My lean failed.** I expected the reversed (rising-rate) member to lose more of the kept population. It keeps more: g is smaller in every pair where W closes before the readout.

**Family S:**
- Matching optical depth over the whole run [0.02, 4] gives ed3 = 40, 159 and 357. The earliest times dominate the integral, so this matching is meaningless.
- Matching on [0.5, 4] gives ed3 = 1.588, 6.354 and 14.296. Matching on [1, 4] gives ed3 = 0.798, 3.191 and 7.180.
- At equal optical depth, g still differs by up to 0.74. For W=[0.5, 4] and ed6=3, g(4) is 0.124 for the n=3 member and 0.861 for the n=6 member.
- My lean that n=6 keeps more when W starts late failed in 5 of 6 cases.

## 2. Readout Gramian of the hidden sector
G = ∫_s^4 Qᵀ Φᵀ Rᵀ R Φ Q dt, with R the projection onto l≤2 and Q the embedding of l≥3. G is averaged over ±k (which makes its eigenvectors pure-parity) and summed over the profile.

**Convergence:** LM=90 changes nothing at double precision. Halving dt changes the top five eigenvalues by at most 3e-6. The top-eigenvector overlap is 1.0000000000.

**Connection to the predictive quotient (P2a confirmed):**
- N_∞ is the kernel of G as the horizon goes to infinity.
- Here N_∞ = {0}. The entry (R B^j)_{2,2+j} = k^j c_2⋯c_{j+1} is nonzero for every j, so the observability matrix built from R and the time-frozen operator B has full rank. G is positive definite for every T > s.
- So for this chain the predictive quotient V/N_∞ is the whole hidden space. The part that carries information is set by a tolerance on G's eigenvalues.
- V/N_∞ is the same as the Kalman observable quotient, and G is the standard observability Gramian (control-theory prior art).

| history, planting time s | top eigenvalues | effective rank (>1e-3 of top) | top vector, l-weights |
|---|---|---|---|
| ed0.5 n3, s=0.125 (coupled) | 1.7e-9, 9e-15, 2.5e-19 | 1 | odd; l3 1.000 |
| ed0.5 n3, s=0.5 (transition) | 0.685, 0.430, 0.232 | 9 | odd; l3 0.919, l5 0.080 |
| ed0.5 n3, s=1.0 (free) | 1.000, 0.578, 0.269 | 8 | odd; l3 0.923, l5 0.077 |
| ed0.5 n6, s=0.125 | 4.7e-27 | 1 | odd; l3 1.000 |
| ed0.5 n6, s=0.5 / 1.0 | 0.942 / 1.074 | 9 / 8 | odd; l3 0.918 / 0.922 |
| ed2 n3, s=0.5 (coupled) | 1.1e-7, 9e-12, 1e-15 | 1 | odd; l3 1.000 |
| ed2 n3, s=2 (transition) | 0.367, 0.148, 0.040 | 5 | odd; l3 0.953, l5 0.047 |
| ed2 n3, s=3 (free) | 0.147, 0.024, 0.0016 | 3 | odd; l3 0.990 |

The second eigenvector is always even and l=4-dominated (0.87–1.00). The snapshot version of G at the end of the horizon, which is the witness's R_ret object, has the same structure.

**Verdicts:**
- **P2c holds:** the top vector is odd with l=3 weight above 0.5 in every case.
- **P2b is killed for the time-integrated G.** The coupled/transition ratio is 2.5e-9, against a predicted e^(−42) ≈ 6e-19.
  - My prediction left out the (k/σ)^l leakage through the damped rungs into the conserved l=0. v5.1's own witness predictions included it.
  - For the snapshot G at the horizon end, the ratio is 4.8e-17, within a factor of about 10 of the survival factor.
- **P2d is killed:** the free planting has lower effective rank than the transition planting. This is confounded with its shorter remaining horizon.
- **The direction is stable with horizon:** at ed2, s=2, extending to T=6 gives l3 0.923, l5 0.076.

**Direction for the restart agent:** written to `restart_direction.json`.
- It uses A4's discrete p_l on the 32 bin midpoints, extended to l=12. These match A4's for l≤4 to 1.7e-16.
- The discrete l≤2 components are exactly zero, and d is normalised so max|d_k| = 1.

Readout signal at the positivity edge, relative to pure p_3, on the A4 surface (ε_s=2, ed=2, n=3, T=4):

| direction | signal vs pure p_3 |
|---|---|
| L∞-optimal | 2.47× (2.63× at T=6) |
| unconstrained top eigenvector | 0.74× (its l=5 part raises max\|d\|) |
| pure p_4 | 0.40× |

- **Recommended: the L∞-optimal direction.** It is odd, with weights l3 0.851, l5 0.117, l7 0.010. Its shape is a clipped P3-like profile, with b_l = (2.04, 0, −0.95, 0, −0.32, 0, −0.17, 0, 0.58, 0) for l = 3..12.
- It comes out as the same direction for every planting epoch. The positivity limit sets its shape; the Gramian sets odd parity and l=3 dominance.
- On a coupled surface (ε_s=0.5) only l=3 is seen at all, at about 2e-8.
- **Caveat:** the chain is a single-Fourier-mode (plane-wave) model. Mapping its hidden vector onto an angular perturbation applied uniformly in radius is not exact. Whether this direction moves the GR collapse bracket more than p_3 does is untested.

## 3. Closures at linear level
The error E_traj is the profile-weighted relative L2 error of the l≤2 trajectories over [0.02, 4], with step h = 2e-3.

| history | P1 = M1 | P2 = M2 | P3 | P5 | CE2 | OP2 | MFe | MFf |
|---|---|---|---|---|---|---|---|---|
| n3 ed0.25 | 0.790 | 0.496 | 0.284 | 0.0705 | 1.390 | 0.247 | 4.6e-6 | 0.134 |
| n3 ed0.5 | 0.712 | 0.433 | 0.235 | 0.0519 | 1.214 | 0.214 | 3.5e-6 | 0.089 |
| n3 ed1 | 0.576 | 0.322 | 0.157 | 0.0272 | 0.949 | 0.157 | 2.6e-6 | 0.038 |
| n3 ed2 | 0.373 | 0.167 | 0.064 | 0.0067 | 0.596 | 0.081 | 1.9e-6 | same as MFe |
| n3 ed4 | 0.150 | 0.037 | 0.0083 | 3.1e-4 | 0.195 | 0.018 | 1.5e-6 | 0.0082 |
| n3 ed8 | 0.023 | 0.0014 | 9e-5 | 4e-7 | 0.012 | 4.6e-4 | 1.1e-6 | 0.0015 |
| n6 ed1 | 0.609 | 0.343 | 0.169 | 0.0284 | 1.113 | 0.178 | 2.4e-6 | 0.039 |
| n6 ed2 | 0.388 | 0.169 | 0.061 | 0.0051 | 0.768 | 0.095 | 1.5e-6 | 0.0038 |
| n6 ed3 | 0.213 | 0.061 | 0.014 | 5e-4 | 0.479 | 0.038 | 1.1e-6 | 0.0045 |

**The comparators:**
- **P1 = M1 and P2 = M2.** Linearised M1 is identical to P1, and linearised M2 to P2. The maximum-entropy closed moment is quadratic in the perturbation ε: 0.333ε² for M1 and 0.300ε² for M2. An entropy closure adds nothing at linear order.
- **CE2:** the quasi-static (Chapman–Enskog, viscous) closure for l=2.
- **OP2:** P2 plus a short-memory "crescendo" kernel for the hidden block.
- **MFe:** the exact elimination of l≥3 using his closed-form hidden propagator, with the A.5 cut moved to l=2|3.
- **MFf:** the same kernel, frozen to the n=3, ed=2 history and reused for all histories.

**Worst cases:**
- Overall: CE2 at n3 ed0.25, with E_traj 1.39, error in g(4) 0.80, error in g2 0.73.
- Among truncations, for g2: P1 at n3 ed0.25, 0.100.
- For P2: error in g(1.7) at most 1.2e-3, but error in g(4) up to 0.26 (both at n3 ed0.25).

**Verdicts:**
- **P3a–P3e all hold.**
  - P5 < P3 < P2 < P1 in all 9 histories.
  - The worst case is ed=0.25 for every truncation.
  - MFe's largest error is 4.6e-6.
  - No instantaneous closure gets below 0.43 for the early histories.
- **My OP2 lean failed:** it beats P2 in all 9 histories.

**Reading:**
- At ε\*=1.7, every truncation from P2 up gives the memory form's g to within about 1e-3. By ε\*=4 they miss it by up to 0.26.
- The exact elimination is his memory form with the hidden block written in closed form. It is the only comparator that is exact at linear level. Freezing its kernel to one history costs up to 0.13.

## 4. Prior art: Frank & Seibold (arXiv:0806.4707) and Seibold & Frank (arXiv:0902.0076)
**I could not read either paper.** All four allowed web requests were spent:
- Two downloads were refused by the proxy (403).
- One WebFetch was refused because the URL is not on the allowlist.
- One web search confirmed the titles only: "Optimal prediction for radiative transfer: A new perspective on moment closure" and "Optimal prediction for moment models: Crescendo diffusion and reordered equations".

Nothing was saved, so `prior_art/` is empty.

The following is from memory and unverified. They apply optimal prediction (a conditional-expectation memory method with a Gaussian prior on the unresolved moments) to the P_N hierarchy of radiative transfer with constant coefficients. The conditional expectation alone gives back P_N. A first-order memory approximation adds a diffusion-like correction whose coefficient grows in time, the "crescendo" term.

If that is right:
- **Item 3:** they contain OP2's form (here extended to a time-dependent σ) and the point that a truncation needs a memory term.
- **Item 1 (rate-order swap):** not in those papers, as far as I recall.
- **Item 2 (Gramian and predictive quotient):** not in those papers; the Gramian itself is standard Kalman observability theory.

This needs checking against the actual texts.

## Files
All in `/tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/nu6/A5_kinetic/`:
- `PREREGISTERED.txt` (predictions, with results appended)
- `chain_lib.py` (shared solver)
- `t0_reproduce.py`, `t0_reproduce_out.txt` (setup check)
- `t1_order.py`, `t1_order_out.txt`, `t1_order.json` (Test 1)
- `t2_gramian.py`, `t2b_checks.py`, `t2c_direction.py`, with their `*_out.txt` and `*.json` files and the `G_*.npy` matrices (Test 2)
- `restart_direction.json` (direction for the restart agent)
- `t3_closures.py`, `t3b_entropy_linear.py`, with `t3_closures_out.txt`, `t3_probe_out.txt`, `t3b_entropy_linear_out.txt` and `t3_closures_h0.002_*.json` (Test 3)

Sources (titles only; these are the search result links):
- [Optimal prediction for radiative transfer: A new perspective on moment closure](https://arxiv.org/pdf/0806.4707)
- [Optimal prediction for moment models: Crescendo diffusion and reordered equations](https://arxiv.org/pdf/0902.0076)