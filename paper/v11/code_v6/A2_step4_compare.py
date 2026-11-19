# SCRIPT: A2_STEP4_COMPARE
"""Compare the step-3 predictions with McCormick's measured T_H = 1 MeV multigroup thresholds; kill lines from
PREREGISTERED.txt. Plus sensitivity: bracket errors, d_inst scan, and v5.1's measured eleven-point table used directly
in place of the linear law."""
import json
import numpy as np
P = json.load(open('step3_predictions.json'))
d_fluid = 0.49742
d_with, e_with = 0.51940625, 0.00031249999999993783/2        # res_mg_phys6_10.0.json (midpoint, half-width)
d_wo, e_wo = 0.526390625, 0.00021874999999993427/2            # res_mg_nonunu6_10.0.json
def Gof(d, di): return (d - d_fluid)/(di - d_fluid)
def tau(G): return np.log((1 - G)/G)
di = 0.53379
dG_meas = Gof(d_with, di) - Gof(d_wo, di)
dG_err = np.hypot(e_with, e_wo)/(di - d_fluid)
dtau_meas = tau(Gof(d_with, di)) - tau(Gof(d_wo, di))
print(f'measured: G(without) = {Gof(d_wo, di):.4f}, G(with) = {Gof(d_with, di):.4f}, shift in G = {dG_meas:+.4f} +- {dG_err:.4f} (brackets);'
      f' shift in tau_G = {dtau_meas:+.4f}; implied rapidity at rate 1.11: {dtau_meas/1.11:.4f}')
print(f'kill tolerance = 0.5*|shift| = {0.5*abs(dG_meas):.4f}\n')
k1 = 'primary d_inst=0.53379 | primary: visibility of k_e | rate 1.11'
for name, pr in (('READING 1, rate 1.11 (decides)', P['reading1'][k1]),
                 ('READING 1, rate 1.19', P['reading1'][k1.replace('1.11', '1.19')]),
                 ('READING 1, rate 1.20', P['reading1'][k1.replace('1.11', '1.2')])):
    miss = pr['dG_pred'] - dG_meas
    verdict = 'KILLED' if (np.sign(pr['dG_pred']) != np.sign(dG_meas) or abs(miss) > 0.5*abs(dG_meas)) else 'SURVIVES'
    print(f'{name}: predicted shift {pr["dG_pred"]:+.4f}, miss {miss:+.4f} ({100*abs(miss)/abs(dG_meas):.1f}% of shift); '
          f'delta_c(with) predicted {pr["delta_with_pred"]:.5f} vs {d_with:.5f} +- {e_with:.5f}: miss {pr["delta_with_pred"]-d_with:+.5f} -> {verdict}')
r2 = P['reading2']['primary']
miss2 = r2['dG_pred'] - dG_meas
v2 = 'KILLED' if (np.sign(r2['dG_pred']) != np.sign(dG_meas) or abs(miss2) > 0.5*abs(dG_meas)) else 'SURVIVES'
print(f'READING 2 (timing): predicted shift {r2["dG_pred"]:+.4f}, miss {miss2:+.4f} ({100*abs(miss2)/abs(dG_meas):.1f}% of shift) -> {v2}')
print(f'   absolute: without {r2["d_without"]:.5f} vs {d_wo:.5f} (miss {r2["d_without"]-d_wo:+.5f}); '
      f'with {r2["d_with"]:.5f} vs {d_with:.5f} (miss {r2["d_with"]-d_with:+.5f}); anchored with {d_wo + r2["d_with"] - r2["d_without"]:.5f} (miss {d_wo + r2["d_with"] - r2["d_without"] - d_with:+.5f})')
# equivalent single-rate Tdec of the measured thresholds (McCormick's family at T_H = 1 MeV)
fam_T = np.array([0.75, 1.0, 1.5, 2.0, 3.0]); fam_d = np.array([0.51586, 0.52076, 0.52583, 0.52837, 0.53065])
def Teq(d): return float(np.exp(np.interp(d, fam_d, np.log(fam_T))))
print(f'   measured thresholds as single-rate Tdec: without {Teq(d_wo):.3f} MeV, with {Teq(d_with):.3f} MeV '
      f'(Reading 2 rate-based: {r2["Tdec_without"]:.3f}, {r2["Tdec_with"]:.3f})')

# d_inst scan
print('\nd_inst scan (Reading 1, rate 1.11, u_eff = %.4f):' % P['U']['primary: visibility of k_e'])
u = P['U']['primary: visibility of k_e']
for dI in (0.5315, 0.5325, 0.53379, 0.5345, 0.5355, 0.5370):
    G0 = Gof(d_wo, dI); t = tau(G0) + 1.11*u; Gp = 1/(1 + np.exp(t)); dp = d_fluid + Gp*(dI - d_fluid)
    dGm = Gof(d_with, dI) - G0
    print(f'  d_inst={dI:.5f}: delta_c(with) pred {dp:.5f} (miss {dp-d_with:+.5f}); shift pred {Gp-G0:+.4f} vs meas {dGm:+.4f}')

# v5.1's eleven measured offsets used directly (per flavour, then energy-averaged in tau_G), instead of the linear law
uu = np.array([-1.386, -0.693, -0.347, -0.112, -0.091, 0.0, 0.091, 0.112, 0.347, 0.693, 1.386])
tt = np.array([-1.547, -0.763, -0.384, -0.127, -0.103, 0.0, 0.098, 0.122, 0.385, 0.786, 1.610])
o = np.argsort(uu); uu, tt = uu[o], tt[o]
ue, um = 0.4468, 1.0235
dt = (1/3)*np.interp(ue, uu, tt) + (2/3)*np.interp(um, uu, tt)
G0 = Gof(d_wo, di); Gp = 1/(1 + np.exp(tau(G0) + dt)); dp = d_fluid + Gp*(di - d_fluid)
print(f'\nv5.1 table used directly: d tau_G = {dt:.4f} (linear law: {1.11*u:.4f}); delta_c(with) = {dp:.5f} (miss {dp-d_with:+.5f}); shift {Gp-G0:+.4f}')
# v5.1 shear-only family has no table beyond two pairs; rate 1.19-1.20 above is its stand-in.
