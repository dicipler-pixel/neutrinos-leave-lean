# The Weight Between v1.1 against McCormick's free-streaming PBH preprint

Folder: $NU_WORK/a_wb
Grades: [derived] proved/identity checked on Steve's operator; [measured] number from a computation run here or printed by Steve; [proposed] reading, untested or fitted. Every comparison is structural unless a number is computed from Steve's equations or tables. Jeromie's intrinsic (projector) metric is never used as a spacetime metric: it is used only on the multipole Hilbert space of the neutrino transport operator (Legendre basis), which is the projector bundle the paper's identities are about.

Verdict in one paragraph: the paper's identities hold exactly on Steve's collision operator and say what his single-rate model is (equality case of the ladder, all non-normality on the 0-1 edge, exceptional point at 2 sqrt(E_B)). No pre-registered kill on the G curve was passed without a fitted parameter, but the paper's own object (survival of the kept l=0 sector under Steve's kappa(eps)) read at the epoch Steve's numbers give (first maximum, eps = 1.7) lands within 0.10 of all six G values (0.103 profile-averaged, 0.093 at k r_m = 2), against 0.30 for the sharp-wall model, 0.51 for the linear first-maximum diagnostic and 0.17 for the hidden-sector energy. The open rung +1 of the ladder gets an empirical identification (momentum-drag rate) that reproduces Steve's calibrated decoupling temperatures from his Appendix C numbers.

## 1. The paper's main results (all read in full: body, 7 scripts' kill conditions, outputs, figure script)

1. [derived; Lean cited] Predictive quotient: the first dim V readings decide; N_inf = intersection of ker R L^n is L-invariant and is the least memory; the present closes iff RL = AR (Thm 1-3).
2. [derived; Lean cited] Reduction gives a memory kernel K(tau) = B e^{D tau} C; for a Hermitian split the zero-lag trace is Tr BB^dagger, the coupling energy (eq. kernel); frequency form is the Schur complement.
3. [derived; Lean cited] A tangent to the set of projectors is purely off-diagonal (PVP = 0): every motion of the kept sector is a crossing of the cut.
4. [derived; computed C1, 4e-15] Prop 5: E_B = ||P H (1-P)||_F^2 = (1/2)||[H,P]||_F^2 = Var_psi H for rank one: speed of the kept sector, energy variance and zero-lag memory are one number.
5. [derived; known, Mera-Ozawa] 4 det g >= Omega^2 from Cauchy-Schwarz for the Hermitian form Q.
6. [derived; Lean cited; computed C7, 4e-16 with a failing control at 5e-2] Non-normality is connection energy: (1/8)||[H,H^dagger]||^2 = sum over edges ||D_i - A_ij D_j A_ij^dagger||^2; the scalar form is ||[H,H^dagger]||^2 = 4||[D,K]||^2.
7. [derived; computed B4, 7e-15] Two books on a plane pair: E_- = 2k(1-p), E_+ = 2k(1+p), E_- + E_+ = 4k; p = Tr(PR)/k is the transition probability only for three or more outcomes (cited).
8. [derived: classical log-convexity; the reading of rungs is explicitly [open]] Gap-power ladder S_k = sum |K_ij|^2 |Delta_ij|^k: rungs -2 memory geometry, -1 static response / friction weight, 0 coupling energy, +2 connection energy; rung +1 "not yet identified". Light: alpha_0^2 <= 4 g Var (derived), phase-record witness and the oplus film law (Lean cited).
9. [derived] Survival of the kept sector: overlap = k - E_B t^2 + o(t^2).
10. [derived; computed B5, 2e-15] Ordered hidden walks: G_12 - G_21 = -2i bc sin(phi)/p(z) while the single return G_11 is blind to phi. The figure-eight fold-versus-EP remark is [cited, not re-run].

Reading notes (not errors in results): the HTML body does not state the offset speed limit (tau_dot^2 <= 4 g S) although scripts C2-C5 and Fig. 7 test it and the ladder table cites "Offset Speed Limit"; the equation after "the memory vanishes at every lag exactly when the coupling vanishes" lost its left-hand side in the HTML (display reads "=0 iff B=0 iff BB^dagger=0"). Neither affects what follows.

## 2. Mappings to Steve's items and tables, with grade

Setup used throughout (derived from Steve's Eq. 7-10 and App. B): conformal time tau = epsilon (r_m = 1, radiation era), kappa -> a*kappa = eps_dec^3/eps^4, k_phys/H = (k r_m) eps. Kept sector P = Legendre l = 0 (the isotropic part the collisions relax toward), hidden sector l >= 1, H = k mu, L = -i k mu - kappa (1-P).

| # | Steve item | Mapping | Grade | Result |
|---|---|---|---|---|
| M1 | Eq. 7 relaxation operator | Def. 4 / Prop. 5 on L | [derived] T1 | E_B = k^2/3 exactly; sqrt(E_B) = k/sqrt3 = c_s k (radiation sound speed: E_B/k^2 = <mu^2> = p/e). Non-normality S_2 = 2 kappa^2 E_B, all on the 0-1 edge, identity checked to 1e-10. |
| M2 | "ν as a hidden interior" | Hidden-walk/Schur formula (paper Sec. 4) | [derived] T2 | Monopole propagator G(z) = g(s)/(1 - kappa g(s)), g = arctan(k/s)/k, s = z + kappa: Schur form, full inverse and closed form agree to 5e-16. Two-level exceptional point at kappa = 2 sqrt(E_B) (= 2k/sqrt3). |
| M3 | Single-rate model | Ladder equality case | [derived] T3 | All gaps equal kappa, so S_0^2 = S_-2 S_2 and S_-1^2 = S_-2 S_0 hold with equality (1e-12). The multigroup model (rates spread 35x across x = 0.4-20) is strict: S_0^2/(S_-2 S_2) = 0.28, S_-1^2/(S_-2 S_0) = 0.67. |
| M4 | App. C effective single rate; Tdec = 1.6 MeV (e+- only) and 0.93-1.0 MeV (with nu-nu); step 2.5-3x in mass | Power mean of group rates = rung p of the ladder | [proposed], measured against Steve's calibration | Rung p = +1 (arithmetic mean = S_1/S_0 = E_B<kappa>/E_B): 1.62 MeV and 1.02 MeV, mass step 2.53. p = +2: 1.44 / 0.97. p = 0, -1, -2 fail (1.86, 2.12, 2.35 MeV). Harmonic mean (rung -1) gives step 3.44. Class p >= +1 passes; +1 is closest. |
| M5 | Table II G curve | Survival of kept sector under kappa(eps) (paper Sec. 2 "survival of what is kept", memory kernel) | [measured] D2 | At eps* = 1.7 (Steve's linear first max): g = 0.941, 0.860, 0.671, 0.344, 0.087, 0.013 vs G = 0.960, 0.868, 0.684, 0.431, 0.190, 0.063. Max error 0.103 (profile-averaged), 0.093 (k r_m = 2), 0.100 / 0.096 with the flux kept (cut l = 0,1). By the pre-registered rule the primary variant misses by 0.003: NOT a pass. |
| M6 | Table II G curve, two-epoch form | Same object read at first max (1.7) and apparent horizon (4.0) | [proposed], one fitted weight | g = w g(1.7) + (1-w) g(4.0), w = 0.89: max error 0.021 on the six points. Cross-weighting (same w at k r_m = 2) 0.115: dies. Not a pass; a candidate shape with a stated sensitivity. |
| M7 | Open item (a): which diagnostic predicts delta_c | Linear first max of Delta vs paper objects | [measured] D1, D3, H1 | Linear first-max G_lin = 0.82, 0.56, 0.18, -0.05, -0.02, -0.00 (max error 0.51). Windowed linear contrast over [1.7, 4.0] (opposite run): max error 1.5. Hidden-sector energy X/X_inst: max error 0.169 at 1.7, best fitted epoch 0.112. So no linear density diagnostic and no hidden-energy diagnostic works; kept-sector survival is the best; decisive epoch is a window from first max to apparent horizon. Half-point eps_dec(G=1/2) = 1.665 vs first-max epoch 1.714 (-2.9%): the neutrinos must be decoupled by first max. |
| M8 | Open item (c): collisions beyond relaxation time | Connection energy per edge | [derived] C1 | If l=1 is damped only by e+- (kappa_e) and l >= 2 also by nu-nu: non-normality moves to the 1-2 edge. Share of S_2 on edge 1-2: 64% (nu_e, kappa_nu-nu = 1.5 kappa_e), 97.5% (nu_mu,tau, 7 kappa_e); flavour-weighted stress/flux edge ratio 26.7. Prediction [proposed, threshold response untested]: the multigroup threshold is far more sensitive to the l >= 2 (stress) rate than to the l = 1 (momentum) rate. |
| M9 | Open item (e): second fluid, no momentum exchange | Cut at l = 0,1 (nu own fluid) | [derived] C1, [measured] E1 | E_B(P01) = 4k^2/15 = 0.8 E_B(P0). In pure radiation (p = e/3 both) two non-interacting fluids with the same equation of state are one fluid: the linear shift of the first max vanishes as 0.20/K0 (K0 = kappa/H; rise*K0 = 19.7 at 100, 19.9 at 300, 19.9 at 1000, 20.1 at 3000, i.e. constant within 1.2%), same with drag on. Any effect appears only through the equation-of-state difference at annihilation, as Steve says. This is ordinary viscous damping (rung -1 of the 1-2 edge); the coefficient 0.20 is for my single-mode linear diagnostic, not the nonlinear threshold. |
| M10 | Open item (b): critical exponent; (d) non-Gaussian compaction | none | blocker | The paper is linear/finite-dimensional; it has no nonlinear collapse content. Untested conjecture only: the free-streaming limit is the exceptional-point crossing, so the critical solution may change class there (Steve cites type I for collisionless matter); no kill test exists for it here. |
| M11 | 0.235 R_nu, 0.15 R_nu | none | no mapping | The paper gives no coefficient. Steve-internal check: shift/R_nu is flat to 0.9% in C_l (23.0-23.6) and to 1.7% in delta_c (15.6-14.8), so weights enter linearly; my linear solver gives 23.9 and 23.5 per unit R_nu at R_nu = 0.409, 0.488 (single-mode first max). Not explained, only consistent. |
| M12 | AH mass ratio ~1.19; "plasma carries 59%" | weight as sector share | no mapping (numerology rejected) | (1-R_nu)^(-1/3) = 1.192, (delta_c ratio)^3 = 1.196, (C_l ratio)^2 = 1.202 all land on 1.19: three unrelated forms, so the match is not evidence. A power law (1-R_nu)^(-x) fitted to the C_l shift needs x = 0.220, 0.175, 0.162 at R_nu = 0.1, 0.409, 0.488 (not constant). The paper's weight E_B is a coupling energy, not a Misner-Sharp mass; no bridge to the 59% is derived. |
| M13 | Steve's own numbers re-derived | Table II, III, beta rule | [measured] T0 | Delta C_l,c recomputed from the delta_c columns through Eq. 15 agrees with every printed row (max 0.05 pt); G recomputed matches the brief to 0.001; Table III log slopes 0.266 / 0.267; beta rule exponent 1.187-1.192 and ratios 0.0208 / 0.0053 / 0.0013 vs his 0.021 / 0.0052 / 0.0013. |

Solver validation (V1, needed before D1-D3, E1 are trusted): my Ma-Bertschinger solver with Steve's initial conditions reproduces his App. B numbers: single-mode first-max factor 0.9111 (his 0.911) and 0.8972 (0.897); superhorizon Delta ratio 1.0464 at k tau = 0.05 versus (15+6R)/(15+4R) = 1.0492 (0.003 off, not fully superhorizon); Gaussian centre first max at eps = 1.714 (his 1.7) with factor 0.9411 (his 0.944), a rise of 6.25% (his 6-7%).

## 3. Kill conditions and outcomes (each written in its script header before the run)

| id | kill condition (short) | outcome |
|---|---|---|
| T0 | Steve tables self-consistent to 0.3 pt | PASS |
| T1 | E_B = k^2/3 = (1/2)||[H,P]||^2 = Var; S_2 identity to 1e-10 | PASS |
| T2 | Schur formula = arctan closed form to 1e-8; EP at 2 sqrt(E_B) | PASS (5e-16) |
| T3 | single rate gives ladder equalities; multigroup strict | PASS (equal to 1e-12; slack 0.28 / 0.67) |
| T4 | one rung reproduces both Tdec within 15% | PASS for p >= +1 (not unique: +1 and +2); FAIL for p <= 0. Opposite (harmonic mean) tried: fails both |
| V1 | solver reproduces 0.911, 0.897, 1.049, 1.7 / 0.944 | PASS (first run at k tau0 = 1e-3, rtol 1e-9 failed with 0.9485 from a spurious growing mode; rerun at k tau0 = 1e-2, rtol 1e-11 passes, and 1e-3 with rtol 1e-11 also gives 0.9109) |
| D1 | linear first max within 0.10 of G | DIES (0.51). Opposite (windowed linear contrast [1.7, 4.0]): DIES (1.5) |
| D2 | kept-sector survival at 1.7 or 4.0 within 0.10, no fit | primary variant DIES by 0.003 (0.103); k r_m = 2: 0.093; flux-kept cut: 0.100 / 0.096. At eps* = 4.0: 0.64 (dies). Reported as FAIL, near miss |
| D3 | hidden-sector energy within 0.10 | DIES (0.169 at 1.7; 0.74 at 4.0; best fitted epoch 0.112) |
| M1 (script 05) | one-parameter two-epoch fit under 0.05 | survives (0.021), graded [fit] |
| M2 (script 05) | same w predicts the k r_m = 2 weighting within 0.10 | DIES (0.115) |
| H1 | half-point = first-max epoch within 10% | PASS (-2.9%) |
| H2 | EP crossing epoch = first max at the half point | DIES (implied half-point 2.71 vs measured 1.665, 63% off). Note: the earlier eps_EP = 0.658 eps_dec^1.5 is not reproduced here; kappa/k = eps_dec^3/(k r_m eps^4) gives eps_EP = 0.811 eps_dec^0.75 |
| C1 | edge decomposition of S_2 to 1e-10 | PASS |
| S07 | memory form discriminates a different collision history by >= 0.10 | PASS (0.165) |
| E1 | shift falls monotonically with K0 and shift*K0 is constant within 15% | PASS (1.2%) |

Opposite-direction runs performed before declaring a mapping dead: D1 opposite (windowed, later epoch) dies; D2 opposite cut (flux kept) and opposite weighting (single k) are within 0.01 of the primary, so the near miss is not an artefact of the cut; T4 opposite rungs (-2, -1, 0) fail; the "decision epoch" opposite (EP crossing instead of first max) dies.

## 4. What Steve's numbers give this paper (opposite direction)

- First external, nonlinear-simulation-anchored case where the paper's cut is physical: the kept sector is the plasma-coupled isotropic mode, E_B/k^2 = c_s^2, and Steve's single-rate decoupling is the exact equality case of the ladder [derived].
- Candidate identification of the open rung +1: S_1 = sum |K|^2 |Delta| = E_B <kappa>, the momentum-drag rate (flux relaxed to the plasma at the energy-weighted arithmetic mean rate). Support: Steve's Appendix C calibrations (Tdec 1.6 MeV e+- only, ~1.0 MeV with nu-nu, step 2.5-3x) are matched by p = +1 from his printed rate numbers (1.62, 1.02, 2.53) and not by rung -1. Caveats: interpolation of c(x) between his endpoints, flavour weights 1/3 and 2/3, the sum-of-rates rule for nu-nu on l >= 2, and the 15% tolerance on T (a 52% tolerance on C since Tdec scales as C^(-1/3)). [proposed]. The paper's table already puts a "friction weight" at -1; this is a different object (drag rate vs viscosity weight) and the paper's wording should keep them apart.
- The paper's survival/memory object has measurable content: with no free parameter it follows a nonlinear apparent-horizon-threshold curve to 0.02 for eps_dec <= 1 and to about 0.10 overall. Where it fails (late decoupling, eps_dec >= 2, under-predicted by 0.09-0.13) it fails in the direction Steve states: decoupling after first maximum still changes the outcome because collapse is decided up to apparent-horizon formation.
- Steve's shift is linear in R_nu in C_l to 0.9%: weights enter additively there, as the paper's sector populations do; the paper does not predict the slope.
- Nothing in Steve's tables contradicts a claim of the paper.

## 5. Best single next step

One extra point of Steve's gradual-decoupling scan with a different collision history: kappa = H (eps_dec/eps)^6 at eps_dec = 2 (Gaussian, R_nu = 0.409, same code, one bisection, normalised to the same instantaneous shift). More points on his own n = 3 curve would not test anything: interpolating Table II already gives 0.54 and 0.28 at eps_dec = 1.5 and 3, and the memory-survival form gives 0.54 and 0.25, so those points cannot separate the two (checked). A different history can: the two-epoch memory form (w = 0.89, fitted on n = 3) predicts G = 0.25 at (n = 6, eps_dec = 2), i.e. shifts of about 1.5% in delta_c and 2.4% in C_l, whereas "only eps_dec matters" (no memory of the history) predicts the n = 3 value 0.43 (2.65% and 4.0%). Companion point: n = 2 at eps_dec = 2 gives 0.51 against 0.43 (script 07: n = 2: 0.730 / 0.511, n = 6: 0.662 / 0.246 at eps_dec = 1 / 2; largest change from n = 3 is 0.165, so the kill condition of script 07 passes). Kill condition to state before asking: |G_measured - 0.25| > 0.10 at (n = 6, eps_dec = 2) kills the memory-survival form; a value near 0.43 kills it too and says the history does not matter. If it survives, the next object to build is the survival integral with the readout window set by the neutrino flux and enclosed mass between first maximum and apparent horizon (Steve's own suggestion in Sec. IV C), instead of the fitted weight.

## 6. For the main session (facts learned, nothing saved)

- From this task: the paper's zip holds Offset Speed Limit checks (C2-C5) and a Fig. 7/8 that the HTML body does not state; and the earlier eps_EP exponent 1.5 in the brief is not reproduced (0.75 here).
- From memory (used silently): the intrinsic-metric rule, no subagents, no lab, show kill conditions first, do the mapping before the verdict.

## Appendix A. Outputs and code (exactly as run)
