# Review of neutrino_submission_d6.pdf (19 Nov 2026)

Full read of all 24 pages. Every number that can be recomputed from the paper's own tables was recomputed
(`d6_check.py`, NU-D6-REVIEW-01; output in `d6_check.out`). McCormick's code was not rerun.

## Confirmed
G values for Tests A-D, H1, S1; the eleven link offsets; the line fit rms 0.014; every odd rate (fixed-step, stage-correct, three grid levels, shear-only);
the error budget 0.0091 / 0.015; the A.2 shifts 1.1051 / 1.0976; every door difference and shift, the 0.56 and 1.47 ratios, the 2-2.5% even parts;
Eq. (4) against the full chain; the 64% / 97.5% shear shares; the 200-moment onset 0.645; pi/sqrt3 = 1.81; M_H(1 MeV) = 1.50e5 Msun and the A.3 list;
e^-42 and the 10^1.9 factor; the +13.5% / -11.9% annihilation readings.
New: the non-orthogonality factor K = 4 phi^2 / sin^2(2 phi), which the paper takes from [16] and checks only at its limits,
equals the Petermann factor of the least-damped mode of the 200-moment chain to 5 digits at kappa/k = 1.0, 0.9, 0.8, 0.7.

## Must fix
1. Abstract: "A rule in which only eps_dec matters fails at eps_dec = 3." Section 4 and item 2 of Section 10 say it fails at B (eps_dec = 2) and D (eps_dec = 3); the miss at B is 0.110 > 0.08.
2. Section 7: the f = 0 restart 0.5107500 is 1.0e-5 ABOVE the fixed-step H1 threshold 0.51074, not below it (it is 2.85e-5 below S1, as stated).
3. Section 2: "The three values differ by less than the error bar of any G quoted for Tests A-D" is false: the spread 0.431 - 0.4253 = 0.0057 exceeds the +-0.004 bars of Tests A and B.
4. Section 13, ref [8]: the title is "Primordial black hole formation in bulk-viscous cosmology" (Yuwen, Joana, Wang, Cai, arXiv:2606.26532), and its runs are spherically symmetric BSSN with Eckart viscosity, not full 3+1; "in full numerical relativity" should read "in spherically symmetric numerical relativity". Its abstract: the threshold is "enhanced by an amount comparable to the bulk-viscosity strength", which supports the sentence otherwise.
5. Section 1 names IQGT but the reference list has no IQGT entry.

## Small
- r = 4 shift from S1 is -0.174 (0.25211 - 0.42656), printed -0.175 on pp. 3 and 8.
- "11-12% of McCormick's whole shift": the eps_s = 2, l = 3 pair gives 12.2% (11.5% with N_mu = 48).
- Observed order from the three printed central values is 6.3 (paper 6.2); both lie outside 0.5-4, so the conclusion stands.
- Annihilation: f = 1.135 needs c_s = 0.5203; with the printed 0.519, f = 1.138.
- At eps_s = 0.5 the +f thresholds for l = 3 and l = 4 are identical (0.5107685) and the -f l = 4 threshold equals the f = 0 restart exactly. Identical bisection decisions give identical endpoints, so this is possible; with the logs missing it cannot be checked. Say so.
- Figures 1 and 4: x-axis tick labels overlap.
- "one aeon" in Section 1 needs a sentence or should go; the paper's own rule keeps cyclic material out.
- The AI-assisted paragraph names "Grok Bot assistant (Cursor)"; make sure it names every assistant that did the work.

## Not checked this turn
Refs [7] (Hu, SciPost 2026), [10] (Escriva arXiv:2504.05814), [11] author list, [12] (arXiv:2607.03138); McCormick's Table II values.

## Addendum (19 Nov, evening): the items left unchecked are now checked
- McCormick's Table II, from his archived result files (quasilocal/PBH_neutrino_simulation, simulation/res_dec_*.json, res_fluid.json, res_nu32.json):
  G = 0.960, 0.868, 0.684, 0.431, 0.190, 0.063 at eps_dec = 0.25-8 against the paper's 0.959, 0.867, 0.683, 0.431, 0.190, 0.063 (rounding);
  res_dec_2.0 bracket (0.51074, 0.51109) matches the reproduction run; broad references 0.448047 / 0.477471 match.
- NEW MUST-FIX: the paper says "An uncertainty for his instantaneous reference is not given in the files we used". It is in his archive:
  res_nu32.json gives 0.5283203 +- 1.95e-4, and his finer pair res_nu409_fine.json 0.5283188 +- 3.1e-5 and res_pf_fine.json 0.4976719 +- 1.6e-5.
  With the res_nu32 half-width the level-3 odd rate moves +-0.0053 (1.0961 / 1.1067), not in the +-0.01 budget.
  With the fine pair: G_C, G_B, G_D, S1 = 0.6489, 0.3184, 0.1559, 0.4277; level-3 odd rate 1.0986 (corners 1.0970-1.1002, so the reference term shrinks from +-0.0038 to about +-0.0016);
  levels 1, 2, 3 = 1.1074, 1.0992, 1.0986. Rate one is still excluded and "1.10 +- 0.01" still covers it; the paper should either use the fine pair or carry the instantaneous width.
- Refs [7] (SciPost Phys. 20, 020; arXiv:2409.05131), [10] (arXiv:2504.05814) and [12] (arXiv:2607.03138) exist with the cited titles. Author lists of [11], [12] not checked.
