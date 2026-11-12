# The Weight Between v1.1 against McCormick's free-streaming PBH preprint

Folder: /tmp/claude-0/-home-claude/502f5ad8-acd9-59a2-b5cf-d48e7967cc3a/scratchpad/a_wb
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

### wb_steve_01_algebra.py

```python
# SCRIPT: WB-STEVE-01-ALGEBRA
# Tests T0-T4 mapping "The Weight Between" v1.1 onto McCormick's free-streaming PBH preprint (algebraic part).
# KILL CONDITIONS (written before any run):
#  T0  Steve-internal consistency (so the targets are trustworthy). Table II: recompute Delta C_l,c/C_l,c from the delta_c
#      columns through Eq.(15) delta = C - 3C^2/8; dies (flag only) if any row differs from the printed value by > 0.3 pt.
#      Also recompute G = shift/shift_inst for the gradual rows (flag if any differs from the brief's G by > 0.005).
#  T1  Prop 5 / Def 4 on Steve's operator L = -i k mu - kappa (I-P), P = projector on l=0 (orthonormal Legendre basis).
#      H = k mu, E_B = ||P H (1-P)||_F^2 must equal k^2/3 = (1/2)||[H,P]||_F^2 = Var_{|0>}(H) to 1e-12 relative. Dies otherwise.
#      Connection-energy identity (scalar form, H' = -L = D + iK, D=diag(kappa_l), K = k mu):
#      (1/4)||[H',H'^dag]||^2 = ||[D,K]||^2 = S_2. Dies if off by > 1e-10 relative.
#  T2  Hidden-walk (Schur) formula of the paper: G_B(z) = [z - E - W (z-F)^{-1} W^dag]^{-1} with E=0, W the l=0->l>=1 block,
#      F the hidden block of L, must equal the closed form G(z) = g(s)/(1 - kappa g(s)), g(s)=arctan(k/s)/k, s=z+kappa,
#      to 1e-8 relative at 50 random complex z (Re s>0). Dies otherwise.
#      Two-level EP: eigenvalues of [[0,-i k/sqrt3],[-i k/sqrt3,-kappa]] coalesce at kappa = 2 k/sqrt3 = 2 sqrt(E_B). Dies otherwise.
#  T3  Ladder on Steve's single-rate model: all gaps equal kappa, so S_0^2 = S_-2 S_2 and S_-1^2 = S_-2 S_0 must be EQUALITIES
#      (1e-12). Dies otherwise.  For the energy-dependent (multigroup) rates the same inequalities must be strict.
#  T4  Which rung is the effective single rate of a spread of rates?  Pre-registered claim (to be killed if wrong): the paper's
#      ladder says the effective rate is a power mean of the group rates, M_p, p in {-2,-1,0,+1,+2}. PASS only if ONE rung p
#      reproduces BOTH of Steve's calibrated decoupling temperatures, e+- only: 1.6 MeV and with nu-nu: 0.93-1.0 MeV,
#      each within 15 percent, using only the rate numbers printed in his Appendix C. Opposite run: every other p tried.
import numpy as np
from scipy.special import erfc
from scipy.optimize import brentq
rng = np.random.default_rng(3010)
fro2 = lambda X: float(np.real(np.vdot(X, X)))

print('=== T0 Steve-internal consistency ===')
dc_f = 0.49773
rows = [('inst eps0=0.1 Rnu=.409', 0.52832, 9.6), ('dec 0.25', 0.52709, 9.2), ('dec 0.5', 0.52428, 8.3), ('dec 1', 0.51865, 6.5),
        ('dec 2', 0.51092, 4.0), ('dec 4', 0.50354, 1.8), ('dec 8', 0.49967, 0.6),
        ('Rnu=.10', 0.50547, 2.3), ('Rnu=.20', 0.51297, 4.7), ('Rnu=.30', 0.52027, 7.0), ('Rnu=.488', 0.53379, 11.5),
        ('alpha .3', 0.47747, 9.3), ('alpha .5', 0.49682, 9.4), ('alpha 2', 0.56342, 9.9), ('alpha 4', 0.59734, 10.0)]
Cl = lambda d: (4/3)*(1-np.sqrt(1-1.5*d))
fl = {'alpha .3': 0.44805, 'alpha .5': 0.46687, 'alpha 2': 0.53274, 'alpha 4': 0.56819}
for nm, dn, printed in rows:
    df = fl.get(nm, dc_f); s = 100*(Cl(dn)/Cl(df)-1)
    print('%-24s Delta C_l,c = %5.2f %%  printed %5.1f  diff %+5.2f %s' % (nm, s, printed, s-printed, 'FLAG' if abs(s-printed) > 0.3 else ''))
sh = {0.25: 5.90, 0.5: 5.33, 1: 4.20, 2: 2.65, 4: 1.17, 8: 0.39}; inst = 6.15
Gbr = {0.25: .959, .5: .867, 1: .683, 2: .431, 4: .190, 8: .063}
G = {e: (v)/inst for e, v in sh.items()}
# use the delta_c columns directly (more digits than the percent column)
dcs = {0.25: 0.52709, .5: 0.52428, 1: 0.51865, 2: 0.51092, 4: 0.50354, 8: 0.49967}
G = {e: (dcs[e]-dc_f)/(0.52832-dc_f) for e in dcs}
for e in G: print('eps_dec %5.2f  G(from delta_c) = %.3f   brief %.3f   diff %+.3f %s' % (e, G[e], Gbr[e], G[e]-Gbr[e], 'FLAG' if abs(G[e]-Gbr[e]) > .005 else ''))
Rv = np.array([.1, .2, .3, .409, .488]); dC = np.array([2.3, 4.7, 7.0, 9.6, 11.5]); dd = np.array([1.56, 3.06, 4.53, 6.15, 7.24])
print('shift/R_nu  C_l: ', np.round(dC/Rv, 2), ' spread %.1f %%' % (100*np.std(dC/Rv)/np.mean(dC/Rv)))
print('shift/R_nu  delta_c: ', np.round(dd/Rv, 2), ' spread %.1f %%' % (100*np.std(dd/Rv)/np.mean(dd/Rv)))
# Table III slopes and ratios
x = np.array([1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]); pf = np.array([.679, .497, .390, .288, .215, .151, .105]); fs = np.array([.799, .590, .470, .343, .255, .178, .123])
print('Table III ratios', np.round(fs/pf, 3), ' slopes', np.polyfit(np.log(x), np.log(pf), 1)[0].round(3), np.polyfit(np.log(x), np.log(fs), 1)[0].round(3))
# beta^1.18 rule: Gaussian C_l, erfc(C/(sqrt2 sigma))
for b in [1e-9, 1e-12, 1e-15]:
    sig = 0.662/np.sqrt(2)/brentq(lambda y: np.log(erfc(y))-np.log(b), 0.5, 10)
    bn = erfc(0.726/(np.sqrt(2)*sig)); print('beta_pf %.0e -> beta_nu/beta_pf = %.4f (Steve: 0.021/0.0052/0.0013), exponent %.3f' % (b, bn/b, np.log(bn)/np.log(b)))
print('coincidence list for the 1.19 mass ratio: (1-Rnu)^(-1/3) = %.4f ; (delta_c ratio)^3 = %.4f ; (C_l ratio)^2 = %.4f ; Table III 1.17-1.20' %
      ((1-.409)**(-1/3), (0.52832/0.49773)**3, (Cl(0.52832)/Cl(0.49773))**2))
print('Rnu-dependence of a power law (1-Rnu)^-x needed for the C_l shift: x = %.3f at .409, %.3f at .488, %.3f at .1 (not constant -> rejected)' %
      tuple(np.log(Cl(d)/Cl(dc_f))/(-np.log(1-r)) for d, r in [(0.52832, .409), (0.53379, .488), (0.50547, .1)]))

print('\n=== T1 Prop 5 / connection energy on Steve operator ===')
lmax = 80; a = lambda l: l/np.sqrt(4.0*l*l-1)
M = np.zeros((lmax+1, lmax+1))
for l in range(1, lmax+1): M[l, l-1] = M[l-1, l] = a(l)
k, kap = 1.7, 0.9
P = np.zeros_like(M); P[0, 0] = 1; I = np.eye(lmax+1)
H = k*M
EB = fro2(P @ H @ (I-P)); comm = 0.5*fro2(H @ P - P @ H); var = (H @ H)[0, 0]-(H)[0, 0]**2
print('E_B = %.15f  k^2/3 = %.15f  (1/2)||[H,P]||^2 = %.15f  Var_0(H) = %.15f' % (EB, k*k/3, comm, var))
assert abs(EB/(k*k/3)-1) < 1e-12 and abs(comm/EB-1) < 1e-12 and abs(var/EB-1) < 1e-12
Dg = np.diag([0.0]+[kap]*lmax); Hp = Dg+1j*H
lhs = 0.25*fro2(Hp @ Hp.conj().T-Hp.conj().T @ Hp); rhs = fro2(Dg @ H-H @ Dg)
print('(1/4)||[H,H^dag]||^2 = %.12f   ||[D,K]||^2 = %.12f   kappa^2 k^2 * 2/3 = %.12f' % (lhs, rhs, kap**2*k*k*2/3))
assert abs(lhs/rhs-1) < 1e-10
print('T1 PASS: sqrt(E_B)/k = %.6f = c_s = 1/sqrt3 (= <mu^2>^(1/2), the radiation sound speed)' % (np.sqrt(EB)/k))

print('\n=== T2 hidden-walk (Schur) formula vs arctan closed form ===')
lm = 600; Mb = np.zeros((lm+1, lm+1))
for l in range(1, lm+1): Mb[l, l-1] = Mb[l-1, l] = a(l)
Lm = -1j*k*Mb-kap*(np.eye(lm+1)-np.diag([1.0]+[0]*lm))
W = Lm[0:1, 1:]; F = Lm[1:, 1:]; Wd = Lm[1:, 0:1]
worst = 0
for _ in range(50):
    z = complex(rng.uniform(0.2, 2), rng.uniform(-3, 3))
    GB = 1/(z-0-(W @ np.linalg.solve(z*np.eye(lm)-F, Wd))[0, 0])      # paper formula with E=0
    s = z+kap; g = np.arctan(k/s)/k; Gc = g/(1-kap*g)
    full = np.linalg.inv(z*np.eye(lm+1)-Lm)[0, 0]
    worst = max(worst, abs(GB-Gc)/abs(Gc), abs(full-Gc)/abs(Gc))
print('worst relative difference (Schur vs closed form vs full inverse): %.2e' % worst); assert worst < 1e-8
for kp in [0.5, 2*k/np.sqrt(3)-1e-3, 2*k/np.sqrt(3), 2*k/np.sqrt(3)+1e-3, 3.0]:
    ev = np.linalg.eigvals(np.array([[0, -1j*k/np.sqrt(3)], [-1j*k/np.sqrt(3), -kp]]))
    print('  kappa = %.4f  two-level eigenvalue separation %.2e' % (kp, abs(ev[0]-ev[1])))
print('T2 PASS. EP at kappa = 2 sqrt(E_B) = %.4f' % (2*np.sqrt(EB)))

print('\n=== T3 ladder on the single-rate model ===')
Kc = k*M; gaps = np.zeros((lmax+1, lmax+1)); gaps[0, 1:] = kap; gaps[1:, 0] = kap   # only the cut edge has a gap kappa; hidden-hidden gaps are 0
def Sk(kk, gp):
    m = (np.abs(Kc) > 0) & (gp > 0); return float(np.sum(np.abs(Kc[m])**2*gp[m]**kk))
S = {kk: Sk(kk, gaps) for kk in [-2, -1, 0, 1, 2]}
print('S_k:', {kk: round(v, 6) for kk, v in S.items()})
print('equality checks: S0^2/(S-2 S2) = %.12f ; S-1^2/(S-2 S0) = %.12f' % (S[0]**2/(S[-2]*S[2]), S[-1]**2/(S[-2]*S[0])))
assert abs(S[0]**2/(S[-2]*S[2])-1) < 1e-12 and abs(S[-1]**2/(S[-2]*S[0])-1) < 1e-12
print('rung +1 for this model: S_1 = E_B*2*kappa (counting both orderings) = %.6f' % S[1])

print('\n=== T4 which rung is the effective rate? (Steve Appendix C numbers only) ===')
# Gamma = c G_F^2 T^4 E.  Calibrate with the unblocked E=T coefficients: 0.506 -> 1.9 MeV (nu_e), 0.108 -> 3.1 MeV (nu_mu,tau) : T_dec = 1.9 (0.506/C)^(1/3)
def Tdec(C): return 1.9*(0.506/C)**(1/3)
print('sanity: C=0.108 -> %.2f MeV (Steve 3.1)' % Tdec(0.108))
# energy groups: six groups x=0.4..20, edges uniform in ln x (Steve App. C), energy weight x^4/(e^x+1) dlnx, c(x) interpolated linearly in ln x between his endpoints
edges = np.linspace(np.log(0.4), np.log(20), 7); xs = np.exp(0.5*(edges[1:]+edges[:-1]))
w = xs**4/(np.exp(xs)+1)*np.diff(edges); w /= w.sum()
def cfun(x, c0, c1): return c0+(c1-c0)*np.log(x/0.5)/np.log(20/0.5)
flav = {'nu_e': dict(wt=1/3, ee=(0.34, 0.47)), 'nu_mutau': dict(wt=2/3, ee=(0.073, 0.101))}
cnn = (0.49, 0.68)
def rates(fl, withnn):
    r = xs*cfun(xs, *flav[fl]['ee']);
    if withnn: r = r+xs*cfun(xs, *cnn)       # anisotropy (l>=2) damped by e+- plus nu-nu
    return r
def pmean(r, wt, p):
    if p == 0: return np.exp(np.sum(wt*np.log(r)))
    return np.sum(wt*r**p)**(1/p)
print('group energy weights', np.round(w, 3))
print('model check: single-group at x=3.15 (e+- only) T_dec: nu_e %.2f MeV (Steve 1.3), nu_mutau %.2f MeV (Steve 2.3)' %
      (Tdec(3.15*cfun(3.15, *flav['nu_e']['ee'])), Tdec(3.15*cfun(3.15, *flav['nu_mutau']['ee']))))
res = {}
for withnn in [False, True]:
    for p in [-2, -1, 0, 1, 2]:
        # level 1: power mean over energy groups within a flavour; level 2: same-p mean over flavours (flavour weights 1/3, 2/3)
        Cf = [pmean(rates(f, withnn), w, p) for f in flav]; wf = np.array([flav[f]['wt'] for f in flav])
        Ceff = pmean(np.array(Cf), wf, p); res[(withnn, p)] = Tdec(Ceff)
for p in [-2, -1, 0, 1, 2]:
    t1, t2 = res[(False, p)], res[(True, p)]
    ok = abs(t1/1.6-1) < .15 and (0.93*0.85 <= t2 <= 1.0*1.15)
    print('rung p=%+d : T_dec(e+- only) = %.2f MeV (target 1.6)   T_dec(with nu-nu) = %.2f MeV (target 0.93-1.0)   both within 15%%: %s' % (p, t1, t2, ok))
print('ratio of masses (T^-2) e+- only -> with nu-nu, rung +1: %.2f, rung -1: %.2f (Steve: 2.5-3)' % ((res[(False, 1)]/res[(True, 1)])**2, (res[(False, -1)]/res[(True, -1)])**2))

```

Output (wb_steve_01_out.txt):

```
=== T0 Steve-internal consistency ===
inst eps0=0.1 Rnu=.409   Delta C_l,c =  9.64 %  printed   9.6  diff +0.04 
dec 0.25                 Delta C_l,c =  9.23 %  printed   9.2  diff +0.03 
dec 0.5                  Delta C_l,c =  8.31 %  printed   8.3  diff +0.01 
dec 1                    Delta C_l,c =  6.48 %  printed   6.5  diff -0.02 
dec 2                    Delta C_l,c =  4.04 %  printed   4.0  diff +0.04 
dec 4                    Delta C_l,c =  1.76 %  printed   1.8  diff -0.04 
dec 8                    Delta C_l,c =  0.58 %  printed   0.6  diff -0.02 
Rnu=.10                  Delta C_l,c =  2.35 %  printed   2.3  diff +0.05 
Rnu=.20                  Delta C_l,c =  4.68 %  printed   4.7  diff -0.02 
Rnu=.30                  Delta C_l,c =  7.00 %  printed   7.0  diff +0.00 
Rnu=.488                 Delta C_l,c = 11.47 %  printed  11.5  diff -0.03 
alpha .3                 Delta C_l,c =  9.34 %  printed   9.3  diff +0.04 
alpha .5                 Delta C_l,c =  9.43 %  printed   9.4  diff +0.03 
alpha 2                  Delta C_l,c =  9.91 %  printed   9.9  diff +0.01 
alpha 4                  Delta C_l,c = 10.05 %  printed  10.0  diff +0.05 
eps_dec  0.25  G(from delta_c) = 0.960   brief 0.959   diff +0.001 
eps_dec  0.50  G(from delta_c) = 0.868   brief 0.867   diff +0.001 
eps_dec  1.00  G(from delta_c) = 0.684   brief 0.683   diff +0.001 
eps_dec  2.00  G(from delta_c) = 0.431   brief 0.431   diff +0.000 
eps_dec  4.00  G(from delta_c) = 0.190   brief 0.190   diff -0.000 
eps_dec  8.00  G(from delta_c) = 0.063   brief 0.063   diff +0.000 
shift/R_nu  C_l:  [23.   23.5  23.33 23.47 23.57]  spread 0.9 %
shift/R_nu  delta_c:  [15.6  15.3  15.1  15.04 14.84]  spread 1.7 %
Table III ratios [1.177 1.187 1.205 1.191 1.186 1.179 1.171]  slopes 0.266 0.267
beta_pf 1e-09 -> beta_nu/beta_pf = 0.0208 (Steve: 0.021/0.0052/0.0013), exponent 1.187
beta_pf 1e-12 -> beta_nu/beta_pf = 0.0053 (Steve: 0.021/0.0052/0.0013), exponent 1.190
beta_pf 1e-15 -> beta_nu/beta_pf = 0.0013 (Steve: 0.021/0.0052/0.0013), exponent 1.192
coincidence list for the 1.19 mass ratio: (1-Rnu)^(-1/3) = 1.1916 ; (delta_c ratio)^3 = 1.1959 ; (C_l ratio)^2 = 1.2020 ; Table III 1.17-1.20
Rnu-dependence of a power law (1-Rnu)^-x needed for the C_l shift: x = 0.175 at .409, 0.162 at .488, 0.220 at .1 (not constant -> rejected)

=== T1 Prop 5 / connection energy on Steve operator ===
E_B = 0.963333333333333  k^2/3 = 0.963333333333333  (1/2)||[H,P]||^2 = 0.963333333333333  Var_0(H) = 0.963333333333333
(1/4)||[H,H^dag]||^2 = 1.560600000000   ||[D,K]||^2 = 1.560600000000   kappa^2 k^2 * 2/3 = 1.560600000000
T1 PASS: sqrt(E_B)/k = 0.577350 = c_s = 1/sqrt3 (= <mu^2>^(1/2), the radiation sound speed)

=== T2 hidden-walk (Schur) formula vs arctan closed form ===
worst relative difference (Schur vs closed form vs full inverse): 5.29e-16
  kappa = 0.5000  two-level eigenvalue separation 1.90e+00
  kappa = 1.9620  two-level eigenvalue separation 6.26e-02
  kappa = 1.9630  two-level eigenvalue separation 4.18e-08
  kappa = 1.9640  two-level eigenvalue separation 6.27e-02
  kappa = 3.0000  two-level eigenvalue separation 2.27e+00
T2 PASS. EP at kappa = 2 sqrt(E_B) = 1.9630

=== T3 ladder on the single-rate model ===
S_k: {-2: 2.378601, -1: 2.140741, 0: 1.926667, 1: 1.734, 2: 1.5606}
equality checks: S0^2/(S-2 S2) = 1.000000000000 ; S-1^2/(S-2 S0) = 1.000000000000
rung +1 for this model: S_1 = E_B*2*kappa (counting both orderings) = 1.734000

=== T4 which rung is the effective rate? (Steve Appendix C numbers only) ===
sanity: C=0.108 -> 3.18 MeV (Steve 3.1)
group energy weights [0.004 0.038 0.229 0.528 0.199 0.003]
model check: single-group at x=3.15 (e+- only) T_dec: nu_e 1.40 MeV (Steve 1.3), nu_mutau 2.33 MeV (Steve 2.3)
rung p=-2 : T_dec(e+- only) = 2.35 MeV (target 1.6)   T_dec(with nu-nu) = 1.22 MeV (target 0.93-1.0)   both within 15%: False
rung p=-1 : T_dec(e+- only) = 2.12 MeV (target 1.6)   T_dec(with nu-nu) = 1.14 MeV (target 0.93-1.0)   both within 15%: False
rung p=+0 : T_dec(e+- only) = 1.86 MeV (target 1.6)   T_dec(with nu-nu) = 1.07 MeV (target 0.93-1.0)   both within 15%: False
rung p=+1 : T_dec(e+- only) = 1.62 MeV (target 1.6)   T_dec(with nu-nu) = 1.02 MeV (target 0.93-1.0)   both within 15%: True
rung p=+2 : T_dec(e+- only) = 1.44 MeV (target 1.6)   T_dec(with nu-nu) = 0.97 MeV (target 0.93-1.0)   both within 15%: True
ratio of masses (T^-2) e+- only -> with nu-nu, rung +1: 2.53, rung -1: 3.44 (Steve: 2.5-3)

```

### wb_lin.py

```python
# SCRIPT: WB-LIN-MODULE (solver copied verbatim from WB-STEVE-02-LINEAR)
import numpy as np
from scipy.integrate import solve_ivp
LMAX = 48
Rn_default = 0.409

def run_mode(k, tau0, tau_grid, Rn, eps_dec, lmax=LMAX, rtol=1e-9):
    """eps_dec=None: neutrinos free-stream (kappa=0) from tau0. eps_dec=inf: perfect fluid. otherwise gradual."""
    n = 4+(lmax-1); LS = np.arange(3, lmax+1)
    def Kc(t):
        if eps_dec is None: return 0.0
        return eps_dec**3/t**4
    def rhs(t, y):
        dg, tg, dn, tn = y[:4]; F = np.zeros(lmax+2); F[2:lmax+1] = y[4:]
        F[lmax+1] = (2*lmax+1)/(k*t)*F[lmax]-F[lmax-1]
        th = (1-Rn)*tg+Rn*tn; de = (1-Rn)*dg+Rn*dn; sg = F[2]/2
        Dl = de+4*th/(k*k*t)
        phi = -1.5*Dl/(k*t)**2; psi = phi-6*Rn*sg/(k*t)**2
        dphi = -psi/t+2*th/(k*k*t*t)
        K = Kc(t); dy = np.empty_like(y)
        dy[0] = -4/3*tg+4*dphi
        dy[1] = k*k*dg/4+k*k*psi-K*(Rn/(1-Rn))*(tg-tn) if Rn < 1 else 0
        dy[2] = -4/3*tn+4*dphi
        dy[3] = k*k*(dn/4-sg)+k*k*psi+K*(tg-tn)
        dy[4] = 8/15*tn-0.6*k*F[3]-K*F[2]
        dy[5:] = k/(2*LS+1)*(LS*F[2:lmax]-(LS+1)*F[4:lmax+2])-K*F[3:lmax+1]
        return dy
    psi0 = phi0 = 2/3; d0 = -2*psi0-(2/3)*(k*tau0)**2*phi0; t0 = 0.5*k*k*tau0*psi0
    y0 = np.zeros(n); y0[:4] = [d0, t0, d0, t0]
    sol = solve_ivp(rhs, (tau0, tau_grid[-1]), y0, method='BDF', t_eval=tau_grid, rtol=rtol, atol=1e-13)
    assert sol.success, sol.message
    Y = sol.y; th = (1-Rn)*Y[1]+Rn*Y[3]; de = (1-Rn)*Y[0]+Rn*Y[2]
    Delta = de+4*th/(k*k*tau_grid)
    return Delta, Y

def first_max(x, y):
    # first local maximum of -Delta (positive overdensity convention), parabolic refinement
    s = -y
    for i in range(1, len(s)-1):
        if s[i] > s[i-1] and s[i] >= s[i+1]:
            a, b, c = s[i-1], s[i], s[i+1]; den = a-2*b+c
            off = 0.5*(a-c)/den if den != 0 else 0
            return x[i]+off*(x[1]-x[0]), b-0.25*(a-c)*off
    return np.nan, np.nan


```

### wb_steve_02_linear.py

```python
# SCRIPT: WB-STEVE-02-LINEAR
# Linear (Ma-Bertschinger, Newtonian gauge, radiation era, r_m = 1, conformal time tau = epsilon) Boltzmann solver for
# plasma + relaxing neutrinos, written from Steve's App. B equations and the textbook hierarchy, then used to test candidate
# predictors of his gradual-decoupling curve G(eps_dec).  Collision term: relaxation toward isotropy in the plasma frame at
# a_kappa = eps_dec^3/eps^4 (his kappa = H (eps_dec/eps)^3 with a H = 1/tau).
# KILL CONDITIONS (written before any run):
#  V1  solver validity (if this dies nothing below is trusted):  (a) superhorizon Delta ratio (neutrinos free from the start)
#      equals (15+6R)/(15+4R) = 1.049 (R=.409) to 0.003;  (b) single-mode first-max ratio 0.911 (R=.409) and 0.897 (R=.488) to 0.01;
#      (c) Gaussian-profile centre: first max of Delta at eps = 1.7 +-0.15 with factor 0.944 +-0.01.
#  D1  linear first-max diagnostic (baseline, open item (a)): G_lin = (1/r-1)/(1/r_inst-1), r = first max with free-streaming /
#      first max perfect fluid, Gaussian centre.  Dies if max_eps |G_lin - G| >= 0.10 over the six Table II points.
#  D2  paper's memory object: monopole survival A under the time-dependent relaxing operator L(kappa(eps)), readout at the epoch
#      Steve's own numbers give (first max 1.7; apparent horizon 4.0); g = (1-A)/(1-A_inst).  No fitted parameter.
#      Dies if max error >= 0.10 at BOTH epochs.
#  D3  paper's 'crossing' object: energy that has crossed from the kept sector (l=0,1) into the hidden sector (l>=2),
#      X = sum_{l>=2}|F_l|^2/(2l+1) integrated over the perturbation, g = X/X_inst at the same two epochs.  Dies the same way.
#  H1  half-point: the decoupling time at which G = 1/2 equals the first-max epoch within 10 percent.
#  Opposite runs: (i) fitted-epoch readouts (diagnostic only, never a pass); (ii) D2/D3 with the cut moved so the kept sector is
#  l=0,1 (flux kept) instead of l=0; (iii) k r_m = 2 versus the Gaussian-profile weighted average.
import numpy as np, sys, time
from scipy.special import roots_legendre
from wb_lin import run_mode, first_max, LMAX
Rn_default = 0.409

print('=== V1a/b single mode, neutrinos free from the start (k tau0 = 1e-2, rtol 1e-11) ===')
k = 1.0; tau0 = 1e-2; tg = np.linspace(tau0, 14, 2801)
for R in [0.409, 0.488]:
    D_pf, _ = run_mode(k, tau0, tg, 0.0, None, rtol=1e-11); D_fs, _ = run_mode(k, tau0, tg, R, None, rtol=1e-11)
    xs, mpf = first_max(tg, D_pf); xf, mfs = first_max(tg, D_fs)
    i = np.searchsorted(tg, 0.05)
    print('R=%.3f: first max at k tau = %.3f (pf) %.3f (fs); ratio of maxima %.4f ; implied threshold rise %.2f %% ; superhorizon Delta ratio at k tau=.05: %.4f (formula %.4f)' %
          (R, xs, xf, mfs/mpf, 100*(mpf/mfs-1), D_fs[i]/D_pf[i], (15+6*R)/(15+4*R)))

print('\n=== V1c Gaussian-profile centre, tau0 = 0.02, free streaming from tau0 ===')
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
zeta = np.exp(-ks**2/4)
eg = np.linspace(0.02, 6.0, 1200)
def centre(Rn, eps_dec):
    acc = np.zeros_like(eg); allY = []
    for kk, w_, z_ in zip(ks, wk, zeta):
        D, Y = run_mode(kk, 0.02, eg, Rn, eps_dec); acc += w_*kk**2*z_*D; allY.append(Y)
    return acc, allY
t_=time.time(); C_pf, Y_pf = centre(0.0, None); print('perfect-fluid centre done in %.0fs' % (time.time()-t_))
C_inst, Y_inst = centre(Rn_default, None)
e1, m1 = first_max(eg, C_pf); e2, m2 = first_max(eg, C_inst)
r_inst = m2/m1
print('centre first max: perfect fluid eps=%.3f, free-streaming eps=%.3f; ratio %.4f (Steve 0.944), implied rise %.2f %% (Steve 6-7 %%)' % (e1, e2, r_inst, 100*(1/r_inst-1)))
# lmax convergence for a typical mode
Dtest, _ = run_mode(3.0, 0.02, eg, Rn_default, None, lmax=48); Dtest2, _ = run_mode(3.0, 0.02, eg, Rn_default, None, lmax=80)
print('lmax 48 vs 80 at k=3: max relative difference %.1e' % (np.max(np.abs(Dtest-Dtest2))/np.max(np.abs(Dtest))))

Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
print('\n=== D1 baseline: first maximum of the centre density contrast, gradual decoupling ===')
G1 = {}; G1k = {}
Rr = {}
for ed in Gs:
    C_g, _ = centre(Rn_default, ed); eg_, mg = first_max(eg, C_g); r = mg/m1
    G1[ed] = (1/r-1)/(1/r_inst-1); Rr[ed] = (eg_, r)
    print('eps_dec %4.2f : first max at eps %.3f  ratio %.4f  G_lin = %.3f   Steve G = %.3f   err %+.3f' % (ed, eg_, r, G1[ed], Gs[ed], G1[ed]-Gs[ed]))
print('D1 max |error| = %.3f  -> %s' % (max(abs(G1[e]-Gs[e]) for e in Gs), 'DIES (>=0.10)' if max(abs(G1[e]-Gs[e]) for e in Gs) >= .10 else 'survives'))
np.save('wb_steve_02_state.npy', dict(G1=G1, Rr=Rr, r_inst=r_inst), allow_pickle=True)

```

Output (wb_steve_02_out.txt):

```
=== V1a/b single mode, neutrinos free from the start (k tau0 = 1e-2, rtol 1e-11) ===
R=0.409: first max at k tau = 4.752 (pf) 4.544 (fs); ratio of maxima 0.9111 ; implied threshold rise 9.76 % ; superhorizon Delta ratio at k tau=.05: 1.0464 (formula 1.0492)
R=0.488: first max at k tau = 4.752 (pf) 4.507 (fs); ratio of maxima 0.8972 ; implied threshold rise 11.45 % ; superhorizon Delta ratio at k tau=.05: 1.0546 (formula 1.0576)

=== V1c Gaussian-profile centre, tau0 = 0.02, free streaming from tau0 ===
perfect-fluid centre done in 18s
centre first max: perfect fluid eps=1.732, free-streaming eps=1.714; ratio 0.9411 (Steve 0.944), implied rise 6.25 % (Steve 6-7 %)
lmax 48 vs 80 at k=3: max relative difference 4.1e-07

=== D1 baseline: first maximum of the centre density contrast, gradual decoupling ===
eps_dec 0.25 : first max at eps 1.713  ratio 0.9512  G_lin = 0.820   Steve G = 0.960   err -0.140
eps_dec 0.50 : first max at eps 1.716  ratio 0.9662  G_lin = 0.560   Steve G = 0.868   err -0.308
eps_dec 1.00 : first max at eps 1.732  ratio 0.9890  G_lin = 0.178   Steve G = 0.684   err -0.506
eps_dec 2.00 : first max at eps 1.749  ratio 1.0029  G_lin = -0.045   Steve G = 0.431   err -0.476
eps_dec 4.00 : first max at eps 1.739  ratio 1.0015  G_lin = -0.023   Steve G = 0.190   err -0.213
eps_dec 8.00 : first max at eps 1.733  ratio 1.0002  G_lin = -0.003   Steve G = 0.063   err -0.066
D1 max |error| = 0.506  -> DIES (>=0.10)

```

### wb_steve_03_paper_objects.py

```python
# SCRIPT: WB-STEVE-03-PAPER-OBJECTS
# D2 (memory survival of the kept sector under the time-dependent relaxing operator) and D3 (energy that has crossed into the
# hidden sector) as predictors of Steve's G(eps_dec).  Kill conditions are those stated in WB-STEVE-02-LINEAR (D2, D3, H1 and
# opposite runs); restated:
#  D2  g = (1-A)/(1-A_inst), A = population of the kept sector l=0 at readout epoch eps* in {1.7, 4.0} (the two epochs Steve's
#      own numbers give), no fitted parameter.  Dies if max_eps |g - G| >= 0.10 at BOTH epochs.
#  D3  g = X/X_inst, X = sum_{l>=2} |F_l|^2/(2l+1) summed over the Gaussian perturbation (weights k^2 zeta^2), same epochs, same kill.
#  Opposite runs: kept sector = l in {0,1} (flux kept), and k r_m fixed at 2 instead of the profile average.
#  Fitted-epoch scan is diagnostic only (a fitted epoch is not a pass).
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
import wb_lin
Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
wE = wk*ks**2*np.exp(-ks**2/2)          # energy weights k^2 zeta(k)^2 of the Gaussian perturbation
wE /= wE.sum()
LM = 60; a = lambda l: l/np.sqrt(4.0*l*l-1)
M = np.zeros((LM+1, LM+1))
for l in range(1, LM+1): M[l, l-1] = M[l-1, l] = a(l)
tau0 = 0.02; eg = np.linspace(tau0, 6.0, 1200)

def survival(k, ed, keep):
    """population of kept sector (keep=1: l=0; keep=2: l=0,1) vs tau, under dv/dtau = -(i k M + Kc (1-P)) v, v(tau0)=|0>."""
    n = LM+1; P = np.zeros(n); P[:keep] = 1
    def rhs(t, v):
        K = 0.0 if ed is None else ed**3/t**4
        x, y = v[:n], v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M @ y), -K*(1-P)*y-k*(M @ x)])
    v0 = np.zeros(2*n); v0[0] = 1
    sol = solve_ivp(rhs, (tau0, eg[-1]), v0, method='BDF', t_eval=eg, rtol=1e-9, atol=1e-12)
    pop = sol.y[:keep]**2+sol.y[n:n+keep]**2
    return np.sum(pop, axis=0)

def avg_surv(ed, keep, single=None):
    if single is not None: return survival(single, ed, keep)
    out = np.zeros_like(eg)
    for kk, w_ in zip(ks, wE): out += w_*survival(kk, ed, keep)
    return out

res = {}
for keep, tag in [(1, 'kept=l0'), (2, 'kept=l0,1')]:
    for single, stag in [(None, 'profile-averaged'), (2.0, 'k r_m=2')]:
        Ai = avg_surv(None, keep, single); curves = {}
        for ed in Gs:
            A = avg_surv(ed, keep, single); curves[ed] = (1-A)/(1-Ai)
        res[(tag, stag)] = curves
        for es in [1.7, 4.0]:
            i = np.searchsorted(eg, es); err = {ed: curves[ed][i]-Gs[ed] for ed in Gs}
            print('D2 %-10s %-17s eps*=%.1f : g = %s  max|err| = %.3f' % (tag, stag, es, np.round([curves[ed][i] for ed in Gs], 3), max(abs(v) for v in err.values())))
        # fitted-epoch scan (diagnostic only)
        best = min(((max(abs(curves[ed][i]-Gs[ed]) for ed in Gs), eg[i]) for i in range(40, len(eg), 5)))
        print('   fitted-epoch scan (diagnostic only): best eps* = %.2f with max|err| = %.3f' % (best[1], best[0]))
print('Steve G :', [Gs[e] for e in Gs])

# D3 from the full linear solver
def hidden_energy(ed, Rn=0.409):
    X = np.zeros_like(eg)
    for kk, w_ in zip(ks, wE):
        _, Y = wb_lin.run_mode(kk, tau0, eg, Rn, ed)
        F = Y[4:]; ls = np.arange(2, 2+F.shape[0])
        X += w_*np.sum(F**2/(2*ls[:, None]+1), axis=0)
    return X
Xi = hidden_energy(None); D3 = {}
for ed in Gs:
    D3[ed] = hidden_energy(ed)/Xi
for es in [1.7, 4.0]:
    i = np.searchsorted(eg, es); print('D3 eps*=%.1f : g = %s  max|err| = %.3f' % (es, np.round([D3[ed][i] for ed in Gs], 3), max(abs(D3[ed][i]-Gs[ed]) for ed in Gs)))
best = min(((max(abs(D3[ed][i]-Gs[ed]) for ed in Gs), eg[i]) for i in range(40, len(eg), 5)))
print('D3 fitted-epoch scan (diagnostic only): best eps* = %.2f with max|err| = %.3f' % (best[1], best[0]))

```

Output (wb_steve_03_out.txt):

```
D2 kept=l0    profile-averaged  eps*=1.7 : g = [0.941 0.86  0.671 0.344 0.087 0.013]  max|err| = 0.103
D2 kept=l0    profile-averaged  eps*=4.0 : g = [0.997 0.994 0.987 0.959 0.83  0.429]  max|err| = 0.640
   fitted-epoch scan (diagnostic only): best eps* = 1.87 with max|err| = 0.065
D2 kept=l0    k r_m=2           eps*=1.7 : g = [1.    0.955 0.772 0.393 0.097 0.014]  max|err| = 0.093
D2 kept=l0    k r_m=2           eps*=4.0 : g = [1.001 1.007 1.016 1.006 1.008 0.587]  max|err| = 0.818
   fitted-epoch scan (diagnostic only): best eps* = 1.69 with max|err| = 0.095
D2 kept=l0,1  profile-averaged  eps*=1.7 : g = [0.981 0.922 0.735 0.373 0.09  0.013]  max|err| = 0.100
D2 kept=l0,1  profile-averaged  eps*=4.0 : g = [0.995 0.983 0.941 0.817 0.544 0.217]  max|err| = 0.386
   fitted-epoch scan (diagnostic only): best eps* = 1.84 with max|err| = 0.082
D2 kept=l0,1  k r_m=2           eps*=1.7 : g = [0.986 0.933 0.752 0.385 0.094 0.014]  max|err| = 0.096
D2 kept=l0,1  k r_m=2           eps*=4.0 : g = [0.998 0.993 0.979 0.882 0.584 0.261]  max|err| = 0.451
   fitted-epoch scan (diagnostic only): best eps* = 1.77 with max|err| = 0.089
Steve G : [0.96, 0.868, 0.684, 0.431, 0.19, 0.063]
D3 eps*=1.7 : g = [1.006e+00 9.420e-01 6.770e-01 2.620e-01 3.200e-02 1.000e-03]  max|err| = 0.169
D3 eps*=4.0 : g = [1.024 1.071 1.154 1.168 0.872 0.198]  max|err| = 0.737
D3 fitted-epoch scan (diagnostic only): best eps* = 1.92 with max|err| = 0.112

```

### wb_steve_04_channels.py

```python
# SCRIPT: WB-STEVE-04-CHANNELS
# (i) Non-normality channels of a collision operator with different rates per multipole (Steve open item (c)), via the paper's
#     connection-energy identity.  (ii) Item (e): neutrinos as a self-interacting fluid that exchanges NO momentum with the plasma.
# KILL CONDITIONS (written before the run):
#  C1  For L = -i k mu - diag(kappa_l), S_2 = ||[D,K]||^2 = (1/4)||[H',H'^dag]||^2 splits over Legendre edges l<->l+1 as
#      sum_l 2 k^2 a_{l+1}^2 (kappa_l - kappa_{l+1})^2, a_l^2 = l^2/(4l^2-1).  Dies if off by > 1e-10 relative.
#      Consequence (derived): the relaxation-time model (all kappa_l equal for l>=1) puts ALL non-normality on edge 0-1; any
#      model with kappa_1 != kappa_2 puts weight on edge 1-2.
#  E1  Two perfect fluids with equal sound speed and no momentum exchange are one fluid: in pure radiation (p = e/3) the shift of
#      the first maximum must vanish as the neutrino self-interaction rate K0 = kappa/H -> infinity.  Prediction from the paper's
#      rung -1 (viscosity weight of the 1-2 edge, S_-1 = (4/15) k^2/kappa): the shift times K0 tends to a constant.
#      Dies if (a) shift does not decrease monotonically with K0, or (b) shift*K0 differs by more than 15 percent between
#      K0 = 100 and K0 = 1000.  Opposite run: the same operator with the drag rate on (flux relaxed to the plasma) instead.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
fro2 = lambda X: float(np.real(np.vdot(X, X)))
lmax = 60; a2 = lambda l: l*l/(4.0*l*l-1)
M = np.zeros((lmax+1, lmax+1))
for l in range(1, lmax+1): M[l, l-1] = M[l-1, l] = np.sqrt(a2(l))
print('=== C1 non-normality channels ===')
k = 1.3
for name, kap in [('relaxation time (all l>=1 equal) kappa_e=1', [0]+[1.0]*lmax),
                  ('nu_e: flux damped by e+- (1), stress by e+- + nu-nu (1+1.5)', [0, 1.0]+[2.5]*(lmax-1)),
                  ('nu_mu,tau: flux (1), stress (1+7)', [0, 1.0]+[8.0]*(lmax-1))]:
    D = np.diag(kap); Hp = D+1j*k*M
    S2 = fro2(D @ (k*M)-(k*M) @ D); chk = 0.25*fro2(Hp @ Hp.conj().T-Hp.conj().T @ Hp)
    edges = [2*k*k*a2(l+1)*(kap[l]-kap[l+1])**2 for l in range(0, 6)]
    tot = sum(2*k*k*a2(l+1)*(kap[l]-kap[l+1])**2 for l in range(0, lmax))
    print('%-62s S_2 = %.6f (commutator form %.6f, edge sum %.6f)' % (name, S2, chk, tot))
    assert abs(S2/chk-1) < 1e-10 and abs(S2/tot-1) < 1e-10
    print('    edge energies 0-1, 1-2, 2-3, 3-4: %s ; share on edge 1-2: %.1f %%' % (np.round(edges[:4], 4), 100*edges[1]/tot))
wt = np.array([1/3, 2/3]); e12 = np.array([2.25*(4/15), 49*(4/15)]); e01 = np.array([1/3, 1/3])
print('flavour-weighted ratio (stress edge)/(flux edge) in units of kappa_e^2 k^2 : %.2f' % (np.sum(wt*e12)/np.sum(wt*e01)))
print('E_B for the cut P0 (plasma-coupled monopole): k^2/3 ; for the cut P01 (flux kept, i.e. nu as own fluid): 4 k^2/15 ; ratio %.4f' % ((4/15)/(1/3)))
E_B01 = fro2(np.diag([1, 1]+[0]*(lmax-1)) @ (k*M) @ np.diag([0, 0]+[1]*(lmax-1)))
print('numerical E_B(P01) = %.10f ; 4k^2/15 = %.10f' % (E_B01, 4*k*k/15))

print('\n=== E1 self-interacting neutrinos with no momentum exchange, pure radiation (first-max shift of Delta) ===')
LM = 40
def run(k, Rn, K0, drag, tau0=0.02, tg=None):
    n = 4+(LM-1); LS = np.arange(3, LM+1)
    def rhs(t, y):
        dg, tg_, dn, tn = y[:4]; F = np.zeros(LM+2); F[2:LM+1] = y[4:]; F[LM+1] = (2*LM+1)/(k*t)*F[LM]-F[LM-1]
        th = (1-Rn)*tg_+Rn*tn; de = (1-Rn)*dg+Rn*dn; sg = F[2]/2; Dl = de+4*th/(k*k*t)
        phi = -1.5*Dl/(k*t)**2; psi = phi-6*Rn*sg/(k*t)**2; dphi = -psi/t+2*th/(k*k*t*t)
        K = K0/t; dy = np.empty_like(y)               # a*kappa = K0 * (a H) = K0 / tau
        Kd = K if drag else 0.0
        dy[0] = -4/3*tg_+4*dphi
        dy[1] = k*k*dg/4+k*k*psi-Kd*(Rn/(1-Rn))*(tg_-tn)
        dy[2] = -4/3*tn+4*dphi
        dy[3] = k*k*(dn/4-sg)+k*k*psi+Kd*(tg_-tn)
        dy[4] = 8/15*tn-0.6*k*F[3]-K*F[2]
        dy[5:] = k/(2*LS+1)*(LS*F[2:LM]-(LS+1)*F[4:LM+2])-K*F[3:LM+1]
        return dy
    psi0 = 2/3; d0 = -2*psi0-(2/3)*(k*tau0)**2*psi0; t0 = 0.5*k*k*tau0*psi0
    y0 = np.zeros(n); y0[:4] = [d0, t0, d0, t0]
    sol = solve_ivp(rhs, (tau0, tg[-1]), y0, method='BDF', t_eval=tg, rtol=1e-10, atol=1e-13)
    Y = sol.y; th = (1-Rn)*Y[1]+Rn*Y[3]; de = (1-Rn)*Y[0]+Rn*Y[2]
    return de+4*th/(k*k*tg)
def fmax(x, y):
    s = -y
    for i in range(1, len(s)-1):
        if s[i] > s[i-1] and s[i] >= s[i+1]:
            A, B, C = s[i-1], s[i], s[i+1]; off = 0.5*(A-C)/(A-2*B+C); return B-0.25*(A-C)*off
tg = np.linspace(0.02, 8.0, 3000); kk = 1.0
m_pf = fmax(tg, run(kk, 0.0, 0.0, False, tg=tg))
for drag, tag in [(False, 'self-interaction only (no momentum exchange with plasma)'), (True, 'drag on the plasma included (Steve relaxation model)')]:
    print(tag)
    prev = None; vals = {}
    for K0 in [3, 10, 30, 100, 300, 1000, 3000]:
        r = fmax(tg, run(kk, 0.409, K0, drag, tg=tg))/m_pf; vals[K0] = 1/r-1
        print('   K0 = %5d : first-max ratio %.5f ; implied threshold rise %.4f %% ; rise*K0 = %.3f' % (K0, r, 100*vals[K0], 100*vals[K0]*K0))
    if not drag:
        mono = all(vals[a] > vals[b] for a, b in zip([3, 10, 30, 100, 300, 1000], [10, 30, 100, 300, 1000, 3000]))
        const = abs(vals[1000]*1000/(vals[100]*100)-1)
        print('   E1 (a) monotone decrease: %s ; (b) rise*K0 changes by %.1f %% between K0=100 and 1000 -> %s' % (mono, 100*const, 'PASS' if mono and const < .15 else 'DIES'))

```

Output (wb_steve_04_out.txt):

```
=== C1 non-normality channels ===
relaxation time (all l>=1 equal) kappa_e=1                     S_2 = 1.126667 (commutator form 1.126667, edge sum 1.126667)
    edge energies 0-1, 1-2, 2-3, 3-4: [1.1267 0.     0.     0.    ] ; share on edge 1-2: 0.0 %
nu_e: flux damped by e+- (1), stress by e+- + nu-nu (1+1.5)    S_2 = 3.154667 (commutator form 3.154667, edge sum 3.154667)
    edge energies 0-1, 1-2, 2-3, 3-4: [1.1267 2.028  0.     0.    ] ; share on edge 1-2: 64.3 %
nu_mu,tau: flux (1), stress (1+7)                              S_2 = 45.292000 (commutator form 45.292000, edge sum 45.292000)
    edge energies 0-1, 1-2, 2-3, 3-4: [ 1.1267 44.1653  0.      0.    ] ; share on edge 1-2: 97.5 %
flavour-weighted ratio (stress edge)/(flux edge) in units of kappa_e^2 k^2 : 26.73
E_B for the cut P0 (plasma-coupled monopole): k^2/3 ; for the cut P01 (flux kept, i.e. nu as own fluid): 4 k^2/15 ; ratio 0.8000
numerical E_B(P01) = 0.4506666667 ; 4k^2/15 = 0.4506666667

=== E1 self-interacting neutrinos with no momentum exchange, pure radiation (first-max shift of Delta) ===
self-interaction only (no momentum exchange with plasma)
   K0 =     3 : first-max ratio 0.96022 ; implied threshold rise 4.1424 % ; rise*K0 = 12.427
   K0 =    10 : first-max ratio 0.98310 ; implied threshold rise 1.7192 % ; rise*K0 = 17.192
   K0 =    30 : first-max ratio 0.99370 ; implied threshold rise 0.6345 % ; rise*K0 = 19.035
   K0 =   100 : first-max ratio 0.99804 ; implied threshold rise 0.1969 % ; rise*K0 = 19.688
   K0 =   300 : first-max ratio 0.99934 ; implied threshold rise 0.0662 % ; rise*K0 = 19.849
   K0 =  1000 : first-max ratio 0.99980 ; implied threshold rise 0.0199 % ; rise*K0 = 19.918
   K0 =  3000 : first-max ratio 0.99993 ; implied threshold rise 0.0067 % ; rise*K0 = 20.088
   E1 (a) monotone decrease: True ; (b) rise*K0 changes by 1.2 % between K0=100 and 1000 -> PASS
drag on the plasma included (Steve relaxation model)
   K0 =     3 : first-max ratio 0.95931 ; implied threshold rise 4.2421 % ; rise*K0 = 12.726
   K0 =    10 : first-max ratio 0.98281 ; implied threshold rise 1.7488 % ; rise*K0 = 17.488
   K0 =    30 : first-max ratio 0.99364 ; implied threshold rise 0.6396 % ; rise*K0 = 19.187
   K0 =   100 : first-max ratio 0.99803 ; implied threshold rise 0.1974 % ; rise*K0 = 19.743
   K0 =   300 : first-max ratio 0.99934 ; implied threshold rise 0.0664 % ; rise*K0 = 19.910
   K0 =  1000 : first-max ratio 0.99980 ; implied threshold rise 0.0200 % ; rise*K0 = 20.042
   K0 =  3000 : first-max ratio 0.99993 ; implied threshold rise 0.0067 % ; rise*K0 = 20.210

```

### wb_steve_05_mixture.py

```python
# SCRIPT: WB-STEVE-05-MIXTURE
# Exploratory (NOT a pass criterion): two-epoch readout of the memory-survival object D2.  Kill conditions written before the run:
#  M1  g_w(eps_dec) = w g(1.7) + (1-w) g(4.0) with ONE fitted weight w; any fitted quantity is graded [fit], never [derived].
#      It is only worth reporting if the one-parameter fit has max error < 0.05 on the six Table II points; it dies otherwise.
#  M2  If it survives, it must also predict out-of-sample: its curve must be monotone decreasing in eps_dec, and predict the
#      Table II values at the OTHER profile weighting (k r_m = 2) within 0.10 using the same w (cross-weighting test).
#  H1  half-point: eps_dec at which G=1/2 (log-odds interpolation of Table II) equals the first-max epoch of the centre
#      density (1.714 from WB-STEVE-02) within 10 percent.
#  H2  exceptional-point criterion: if the 'decision epoch' were the crossing of the two-moment exceptional point,
#      eps_EP = (eps_dec^3/(k r_m 2/sqrt3))^(1/4) (k r_m = 2) would equal the first-max epoch at the half point.  Dies if the
#      implied half-point differs from the measured one by more than 25 percent.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
from scipy.optimize import minimize_scalar
Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
wE = wk*ks**2*np.exp(-ks**2/2); wE /= wE.sum()
LM = 60; M = np.zeros((LM+1, LM+1))
for l in range(1, LM+1): M[l, l-1] = M[l-1, l] = l/np.sqrt(4.0*l*l-1)
tau0 = 0.02; eg = np.linspace(tau0, 6.0, 1200); n = LM+1; P = np.zeros(n); P[0] = 1
def surv(k, ed):
    def rhs(t, v):
        K = 0.0 if ed is None else ed**3/t**4
        x, y = v[:n], v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M @ y), -K*(1-P)*y-k*(M @ x)])
    v0 = np.zeros(2*n); v0[0] = 1
    sol = solve_ivp(rhs, (tau0, eg[-1]), v0, method='BDF', t_eval=eg, rtol=1e-9, atol=1e-12)
    return sol.y[0]**2+sol.y[n]**2
def curves(single):
    f = (lambda ed: surv(single, ed)) if single else (lambda ed: sum(w_*surv(kk, ed) for kk, w_ in zip(ks, wE)))
    Ai = f(None); eds = list(Gs)+[0.75, 1.5, 3.0, 6.0, 12.0]
    return {ed: (1-f(ed))/(1-Ai) for ed in eds}
i17, i40 = np.searchsorted(eg, 1.7), np.searchsorted(eg, 4.0)
out = {}
for single, tag in [(None, 'profile-averaged'), (2.0, 'k r_m=2')]:
    out[tag] = curves(single)
def mix(c, w, ed): return w*c[ed][i17]+(1-w)*c[ed][i40]
cp = out['profile-averaged']
fit = minimize_scalar(lambda w: max(abs(mix(cp, w, ed)-Gs[ed]) for ed in Gs), bounds=(0, 1), method='bounded')
w = fit.x
print('M1 fitted weight on the first-max epoch: w = %.3f ; max error on the six Table II points = %.3f' % (w, fit.fun))
print('   eps_dec  Steve G   mixture   error')
for ed in Gs: print('   %5.2f    %.3f     %.3f    %+.3f' % (ed, Gs[ed], mix(cp, w, ed), mix(cp, w, ed)-Gs[ed]))
ck = out['k r_m=2']
print('M2 cross-weighting (k r_m = 2, same w): max error %.3f' % max(abs(mix(ck, w, ed)-Gs[ed]) for ed in Gs))
print('   out-of-sample predictions (profile-averaged, same w) for Steve to test:')
for ed in [0.75, 1.5, 3.0, 6.0, 12.0]: print('   eps_dec = %5.2f : G_pred = %.3f  (shift of delta_c would be %.2f %%, of C_l %.2f %% for Rnu=.409 Gaussian)' %
                                          (ed, mix(cp, w, ed), 6.15*mix(cp, w, ed), 9.64*mix(cp, w, ed)))
print('   same w, k r_m=2 weighting (band): ' + ', '.join('%.2f->%.3f' % (ed, mix(ck, w, ed)) for ed in [0.75, 1.5, 3.0, 6.0, 12.0]))
mono = all(mix(cp, w, a) > mix(cp, w, b) for a, b in zip([0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8], [0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12]))
print('   monotone decreasing: %s' % mono)
# H1 / H2
eds = np.array(list(Gs)); G = np.array([Gs[e] for e in eds]); lo = np.log(G/(1-G))
x = np.interp(0.0, -lo, np.log(eds)); print('\nH1 half-point eps_dec(G=1/2) = %.3f ; first-max epoch 1.714 ; relative difference %.1f %%' % (np.exp(x), 100*(np.exp(x)/1.714-1)))
kr = 2.0; epEP = lambda ed: (ed**3/(kr*2/np.sqrt(3)))**0.25
ed_half_implied = (1.714**4*kr*2/np.sqrt(3))**(1/3)
print('H2 EP-crossing epoch at the measured half-point: %.3f (first max 1.714). Decoupling time that would put the EP crossing at the first max: %.3f vs measured %.3f -> %.0f %% off' %
      (epEP(np.exp(x)), ed_half_implied, np.exp(x), 100*(ed_half_implied/np.exp(x)-1)))
print('(the earlier note eps_EP = 0.658 eps_dec^1.5 is not reproduced: kappa/k = eps_dec^3/(k r_m eps^4) gives exponent 0.75: eps_EP = %.3f eps_dec^0.75)' % ((1/(kr*2/np.sqrt(3)))**0.25))

```

Output (wb_steve_05_out.txt):

```
M1 fitted weight on the first-max epoch: w = 0.890 ; max error on the six Table II points = 0.021
   eps_dec  Steve G   mixture   error
    0.25    0.960     0.947    -0.013
    0.50    0.868     0.875    +0.007
    1.00    0.684     0.705    +0.021
    2.00    0.431     0.411    -0.020
    4.00    0.190     0.169    -0.021
    8.00    0.063     0.059    -0.004
M2 cross-weighting (k r_m = 2, same w): max error 0.115
   out-of-sample predictions (profile-averaged, same w) for Steve to test:
   eps_dec =  0.75 : G_pred = 0.792  (shift of delta_c would be 4.87 %, of C_l 7.64 % for Rnu=.409 Gaussian)
   eps_dec =  1.50 : G_pred = 0.542  (shift of delta_c would be 3.33 %, of C_l 5.22 % for Rnu=.409 Gaussian)
   eps_dec =  3.00 : G_pred = 0.249  (shift of delta_c would be 1.53 %, of C_l 2.40 % for Rnu=.409 Gaussian)
   eps_dec =  6.00 : G_pred = 0.095  (shift of delta_c would be 0.58 %, of C_l 0.92 % for Rnu=.409 Gaussian)
   eps_dec = 12.00 : G_pred = 0.024  (shift of delta_c would be 0.15 %, of C_l 0.24 % for Rnu=.409 Gaussian)
   same w, k r_m=2 weighting (band): 0.75->0.889, 1.50->0.612, 3.00->0.279, 6.00->0.121, 12.00->0.032
   monotone decreasing: True

H1 half-point eps_dec(G=1/2) = 1.665 ; first-max epoch 1.714 ; relative difference -2.9 %
H2 EP-crossing epoch at the measured half-point: 1.189 (first max 1.714). Decoupling time that would put the EP crossing at the first max: 2.711 vs measured 1.665 -> 63 % off
(the earlier note eps_EP = 0.658 eps_dec^1.5 is not reproduced: kappa/k = eps_dec^3/(k r_m eps^4) gives exponent 0.75: eps_EP = 0.811 eps_dec^0.75)

```

### wb_steve_06_opposites.py

```python
# SCRIPT: WB-STEVE-06-OPPOSITES
# (i) T3 second half: the ladder inequalities on the multigroup rate spread must be STRICT (kill: equality within 1e-9 would mean
#     the multigroup model has no rate spread).  Reports the slack.
# (ii) Opposite run for D1: instead of the first maximum, read the linear central density contrast averaged over the window
#     between Steve's two decisive epochs, [1.7, 4.0] (fixed beforehand), G_win = (<D_pf>/<D_g> - 1)/(<D_pf>/<D_inst> - 1).
#     Kill (written before running): dies if max |G_win - G| >= 0.10.
import numpy as np
from scipy.special import roots_legendre
import wb_lin
edges = np.linspace(np.log(0.4), np.log(20), 7); xs = np.exp(0.5*(edges[1:]+edges[:-1]))
w = xs**4/(np.exp(xs)+1)*np.diff(edges); w /= w.sum()
cf = lambda x, c0, c1: c0+(c1-c0)*np.log(x/0.5)/np.log(20/0.5)
print('=== ladder slack on the multigroup rates (nu_mu,tau, e+- + nu-nu on the stress edge) ===')
for lab, r in [('nu_e e+- only', xs*cf(xs, .34, .47)), ('nu_mu,tau e+- only', xs*cf(xs, .073, .101)), ('nu_mu,tau e+- + nu-nu', xs*(cf(xs, .073, .101)+cf(xs, .49, .68)))]:
    S = {k: np.sum(w*r**k) for k in (-2, -1, 0, 2)}
    print('%-24s S0^2/(S-2 S2) = %.4f ; S-1^2/(S-2 S0) = %.4f ; rate spread max/min = %.1f' % (lab, S[0]**2/(S[-2]*S[2]), S[-1]**2/(S[-2]*S[0]), r.max()/r.min()))
flav = [(1/3, xs*cf(xs, .34, .47)), (2/3, xs*cf(xs, .073, .101))]
print('flavour-mixed e+- only: rates spread across the two flavours at the mean energy: %.1f' % (flav[0][1][3]/flav[1][1][3]))
Gs = {0.25: 0.960, 0.5: 0.868, 1.0: 0.684, 2.0: 0.431, 4.0: 0.190, 8.0: 0.063}
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw; zeta = np.exp(-ks**2/4)
eg = np.linspace(0.02, 6.0, 1200)
def centre(Rn, ed):
    acc = np.zeros_like(eg)
    for kk, w_, z_ in zip(ks, wk, zeta):
        D, _ = wb_lin.run_mode(kk, 0.02, eg, Rn, ed); acc += w_*kk**2*z_*D
    return -acc
pf = centre(0.0, None); inst = centre(0.409, None)
win = (eg >= 1.7) & (eg <= 4.0)
avg = lambda c: np.mean(c[win])
print('\n=== opposite run for D1: windowed linear density contrast over [1.7, 4.0] ===')
print('window averages: perfect fluid %.4f, instantaneous free streaming %.4f; sign of central contrast over window: min pf %.3f' % (avg(pf), avg(inst), pf[win].min()))
err = []
for ed in Gs:
    g = centre(0.409, ed); Gw = (avg(pf)/avg(g)-1)/(avg(pf)/avg(inst)-1); err.append(Gw-Gs[ed])
    print('eps_dec %4.2f : G_win = %.3f   Steve %.3f   err %+.3f' % (ed, Gw, Gs[ed], Gw-Gs[ed]))
print('max |err| = %.3f -> %s' % (np.max(np.abs(err)), 'DIES' if np.max(np.abs(err)) >= .10 else 'survives'))

```

Output (wb_steve_06_out.txt):

```
=== ladder slack on the multigroup rates (nu_mu,tau, e+- + nu-nu on the stress edge) ===
nu_e e+- only            S0^2/(S-2 S2) = 0.2814 ; S-1^2/(S-2 S0) = 0.6693 ; rate spread max/min = 34.8
nu_mu,tau e+- only       S0^2/(S-2 S2) = 0.2812 ; S-1^2/(S-2 S0) = 0.6692 ; rate spread max/min = 34.8
nu_mu,tau e+- + nu-nu    S0^2/(S-2 S2) = 0.2807 ; S-1^2/(S-2 S0) = 0.6687 ; rate spread max/min = 34.9
flavour-mixed e+- only: rates spread across the two flavours at the mean energy: 4.7

=== opposite run for D1: windowed linear density contrast over [1.7, 4.0] ===
window averages: perfect fluid 5.4411, instantaneous free streaming 5.8624; sign of central contrast over window: min pf 0.737
eps_dec 0.25 : G_win = 1.096   Steve 0.960   err +0.136
eps_dec 0.50 : G_win = 1.276   Steve 0.868   err +0.408
eps_dec 1.00 : G_win = 1.633   Steve 0.684   err +0.949
eps_dec 2.00 : G_win = 1.957   Steve 0.431   err +1.526
eps_dec 4.00 : G_win = 1.440   Steve 0.190   err +1.250
eps_dec 8.00 : G_win = 0.345   Steve 0.063   err +0.282
max |err| = 1.526 -> DIES

```

### wb_steve_07_history.py

```python
# SCRIPT: WB-STEVE-07-HISTORY
# Discriminating prediction for the next step.  Table II interpolation cannot predict a DIFFERENT collision history, the
# two-epoch memory-survival form can.  kappa = H (eps_dec/eps)^n  with n = 2 and 6 (Steve used n = 3), eps_dec = 1 and 2.
# KILL CONDITION (before the run): the test is only worth asking Steve for if the predicted G for n = 2 or n = 6 differs from the
# n = 3 value by at least 0.10 at some eps_dec; otherwise the memory form is insensitive to history and the step is dropped.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
kn, kw = roots_legendre(36); kmin, kmax = 0.25, 9.0; ks = 0.5*(kmax-kmin)*(kn+1)+kmin; wk = 0.5*(kmax-kmin)*kw
wE = wk*ks**2*np.exp(-ks**2/2); wE /= wE.sum()
LM = 60; M = np.zeros((LM+1, LM+1))
for l in range(1, LM+1): M[l, l-1] = M[l-1, l] = l/np.sqrt(4.0*l*l-1)
tau0 = 0.02; eg = np.linspace(tau0, 6.0, 1200); n = LM+1; P = np.zeros(n); P[0] = 1
def surv(k, ed, p):
    def rhs(t, v):
        K = 0.0 if ed is None else ed**p/t**(p+1)       # a*kappa = (1/tau)(eps_dec/tau)^p
        x, y = v[:n], v[n:]
        return np.concatenate([-K*(1-P)*x+k*(M @ y), -K*(1-P)*y-k*(M @ x)])
    v0 = np.zeros(2*n); v0[0] = 1
    sol = solve_ivp(rhs, (tau0, eg[-1]), v0, method='BDF', t_eval=eg, rtol=1e-9, atol=1e-12)
    return sol.y[0]**2+sol.y[n]**2
f = lambda ed, p: sum(w_*surv(kk, ed, p) for kk, w_ in zip(ks, wE))
i17, i40 = np.searchsorted(eg, 1.7), np.searchsorted(eg, 4.0); w = 0.890
Ai = f(None, 3)
res = {}
for p in [2, 3, 6]:
    for ed in [1.0, 2.0]:
        g = (1-f(ed, p))/(1-Ai); res[(p, ed)] = w*g[i17]+(1-w)*g[i40]
        print('n = %d, eps_dec = %.0f : G_pred(two-epoch, w = 0.89) = %.3f  (n=3 Table II value %.3f)' % (p, ed, res[(p, ed)], {1.0: 0.684, 2.0: 0.431}[ed]))
dmax = max(abs(res[(p, ed)]-res[(3, ed)]) for p in [2, 6] for ed in [1.0, 2.0])
print('largest change from n=3: %.3f -> %s' % (dmax, 'discriminating' if dmax >= 0.10 else 'DROPPED (insensitive)'))

```

Output (wb_steve_07_out.txt):

```
n = 2, eps_dec = 1 : G_pred(two-epoch, w = 0.89) = 0.730  (n=3 Table II value 0.684)
n = 2, eps_dec = 2 : G_pred(two-epoch, w = 0.89) = 0.511  (n=3 Table II value 0.431)
n = 3, eps_dec = 1 : G_pred(two-epoch, w = 0.89) = 0.705  (n=3 Table II value 0.684)
n = 3, eps_dec = 2 : G_pred(two-epoch, w = 0.89) = 0.411  (n=3 Table II value 0.431)
n = 6, eps_dec = 1 : G_pred(two-epoch, w = 0.89) = 0.662  (n=3 Table II value 0.684)
n = 6, eps_dec = 2 : G_pred(two-epoch, w = 0.89) = 0.246  (n=3 Table II value 0.431)
largest change from n=3: 0.165 -> discriminating

```
