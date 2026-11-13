# SCRIPT: A2_STEP3_LINK_PREDICTION
"""Prediction of McCormick's T_H = 1 MeV multigroup threshold WITH nu-nu scattering, from the one WITHOUT it,
by the frozen v5.1 flux-shear link law (Reading 1) and by the opposite timing reading (Reading 2).
Rates exactly as run_mg.rates(Tb) evaluates them on the background (G=6, 0.4..20, FD, chi_e at T_b, cap 100 H).
Weighting fixed in PREREGISTERED.txt before this script was written. Does NOT use the with-nu-nu threshold."""
import os, sys, json
import numpy as np
SIM = os.path.join(os.environ.get('NU_UPSTREAM', '.'), 'simulation')  # McCormick checkout at eb7c4de (set NU_UPSTREAM)
sys.path.insert(0, SIM)
import run_mg as M

G, XLO, XHI, CAP, SWITCH = 6, 0.4, 20.0, 100.0, 100.0
edges, xg, dl = M.groups(G, XLO, XHI)
NF = 2
wE = M.spectral_weights(edges, 1.0)[:, 0]
W = np.concatenate([M.FR[0]*wE, M.FR[1]*wE])               # energy weight of each (flavour, group), sums to 1
ce_e = M.coef('e_FD', xg)('nu_e'); ce_m = M.coef('mu_FD', xg)('nu_e'); cn = M.coef('e_FD', xg)('nu_nu')
c1 = M.coef('mu_FD', np.array([1.0])); c_sw = (c1('nu_e')[0], c1('nu_nu')[0])

def rates_uncapped(Tb, nunu=True):
    H, Tnu, chi = M.background(Tb)
    re = np.concatenate([ce_e, ce_m])*M.GF2*np.tile(xg, NF)*Tnu*Tb**4*chi/H
    rn = np.tile(cn, NF)*M.GF2*np.tile(xg, NF)*Tnu**5/H*(1.0 if nunu else 0.0)
    return re, rn
def rates(Tb, nunu=True):                                     # == run_mg.rates (mode 'phys', scale 1)
    re, rn = rates_uncapped(Tb, nunu)
    return np.minimum(re, CAP), np.minimum(rn, CAP)
def tight_at(Tb, nunu=True):
    H, Tnu, chi = M.background(Tb)
    tot = (c_sw[0]*Tb**4*chi + c_sw[1]*Tnu**4*(1.0 if nunu else 0.0))*M.GF2*Tnu/H
    return tot > SWITCH

# background clock: ln a = -ln T_nu ; eps = (T_nu/H)/(T_nu/H)|_{T_H}
TH = 1.00296                                                   # T_b at eps = 1 in res_mg_*_10.0.json
Tb = np.exp(np.linspace(np.log(10.0), np.log(0.02), 40001))
H, Tnu, chi = M.background(Tb)
lna = -np.log(Tnu)
HH, TnuH, _ = M.background(TH)
eps = (Tnu/H)/(TnuH/HH)
RE = np.zeros((len(Tb), 2*G)); RN = np.zeros((len(Tb), 2*G)); RE0 = np.zeros_like(RE); RN0 = np.zeros_like(RE)
for j, T in enumerate(Tb):
    RE[j], RN[j] = rates(T); RE0[j], RN0[j] = rates_uncapped(T)
tight_nn = np.array([tight_at(T, True) for T in Tb]); tight_no = np.array([tight_at(T, False) for T in Tb])
jsw_nn = np.argmax(~tight_nn); jsw_no = np.argmax(~tight_no)
print(f'switch to transport: with nu-nu at T_b = {Tb[jsw_nn]:.3f} MeV (eps {eps[jsw_nn]:.3f}); without at {Tb[jsw_no]:.3f} MeV (eps {eps[jsw_no]:.3f})')
print(f'eps at T_b = 1.6, 1.0, 0.5, 0.2 MeV: ' + ', '.join(f'{np.interp(-np.log(T), -np.log(Tb), eps):.3f}' for T in (1.6, 1.0, 0.5, 0.2)))

r = (RE + RN)/RE
u = 0.5*np.log(r)
print('\nr_s on the background (rates as the code evaluates them, capped):')
print('  T_b   eps   ' + ' '.join(f'e{g}:{xg[g]:.2f}' for g in range(G)) + ' | ' + ' '.join(f'm{g}' for g in range(G)))
for T in (8.0, 5.0, 3.0, 2.0, 1.6, 1.3, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.15):
    j = np.argmin(np.abs(Tb - T))
    print(f'  {Tb[j]:5.2f} {eps[j]:5.2f}  ' + ' '.join(f'{v:7.3f}' for v in r[j]))
print('\nk_e/H and k_n/H at x_s (uncapped) at T_b = 2, 1, 0.5 MeV:')
for T in (2.0, 1.0, 0.5):
    j = np.argmin(np.abs(Tb - T))
    print(f'  T={Tb[j]:.2f}: k_e/H ' + ' '.join(f'{v:8.3f}' for v in RE0[j]) + '\n          k_n/H ' + ' '.join(f'{v:8.3f}' for v in RN0[j]))

def visibility(rate, j0):
    """g = (k/H) exp(-tau) per d ln a, tau = integral of k/H d ln a to the future; zero before the switch j0."""
    d = np.diff(lna)
    mid = 0.5*(rate[1:] + rate[:-1])
    tau = np.zeros(len(rate)); tau[:-1] = np.cumsum((mid*d)[::-1])[::-1]
    g = rate*np.exp(-tau); g[:j0] = 0.0
    return g, tau
def wavg(f, g):
    num = np.trapezoid(f*g, lna); den = np.trapezoid(g, lna)
    return num/den, den

U = {}
# (a) primary: visibility of the flux link k_e,s
ueff_s = np.zeros(2*G); norm_s = np.zeros(2*G); Teps = np.zeros(2*G)
for s in range(2*G):
    g, tau = visibility(RE[:, s], jsw_nn)
    ueff_s[s], norm_s[s] = wavg(u[:, s], g)
    Teps[s] = np.exp(-wavg(-np.log(Tb), g)[0])
U['primary: visibility of k_e'] = float(np.sum(W*ueff_s))
print('\nper (flavour, group): energy weight, <u>_vis(k_e), r_eff = exp(2<u>), visibility norm, last-scattering T_b')
for s in range(2*G):
    print(f'  {"nu_e " if s < G else "nu_mt"} x={xg[s % G]:5.2f}  w={W[s]:.4f}  <u>={ueff_s[s]:.4f}  r_eff={np.exp(2*ueff_s[s]):.3f}  norm={norm_s[s]:.4f}  T_ls={Teps[s]:.3f}')
for f, nm in ((0, 'nu_e'), (1, 'nu_mt')):
    sl = slice(f*G, (f+1)*G)
    print(f'  flavour {nm}: <u> = {np.sum(W[sl]*ueff_s[sl])/np.sum(W[sl]):.4f}')
# sensitivity weightings
ueff_t = np.zeros(2*G)
for s in range(2*G):
    g, _ = visibility(RE[:, s] + RN[:, s], jsw_nn); ueff_t[s] = wavg(u[:, s], g)[0]
U['sens: visibility of k_e+k_n'] = float(np.sum(W*ueff_t))
ueff_w = np.zeros(2*G)
for s in range(2*G):
    g = ((RE0[:, s] > 0.1) & (RE0[:, s] < 10.0)).astype(float); g[:jsw_nn] = 0.0; ueff_w[s] = wavg(u[:, s], g)[0]
U['sens: uniform in ln a, 0.1<k_e/H<10'] = float(np.sum(W*ueff_w))
uu17 = np.array([np.interp(1.7, eps, u[:, s]) for s in range(2*G)]); uu40 = np.array([np.interp(4.0, eps, u[:, s]) for s in range(2*G)])
U['sens: v5.1 readout eps*=1.7/4.0 (0.89/0.11)'] = float(np.sum(W*(0.89*uu17 + 0.11*uu40)))

# R_nu at the flux-link last-scattering epoch (for the sensitivity reference)
rpl = np.interp(Tb, M._T, M._rpl); rnu = np.interp(Tb, M._T, M._rnu); Rnu = rnu/(rnu + rpl)
T_ls = float(np.exp(np.sum(W*np.log(Teps))))
Rnu_ls = float(np.interp(-np.log(T_ls), -np.log(Tb), Rnu))
print(f'\nenergy-weighted flux-link last-scattering T_b = {T_ls:.3f} MeV, R_nu there = {Rnu_ls:.4f}; R_nu(T_H) = {np.interp(-np.log(TH), -np.log(Tb), Rnu):.4f}')

d_fluid = 0.49742; d_without = 0.52639
d_inst_P = 0.53379
d_inst_S = 0.52832 + (0.53379 - 0.52832)*(Rnu_ls - 0.409)/(0.488 - 0.409)
def Gof(d, di): return (d - d_fluid)/(di - d_fluid)
def tau(Gv): return np.log((1 - Gv)/Gv)
def inv(t, di):
    Gv = 1/(1 + np.exp(t)); return d_fluid + Gv*(di - d_fluid), Gv
out = dict(U=U, d_inst_primary=d_inst_P, d_inst_sens=d_inst_S, Rnu_ls=Rnu_ls, T_ls=T_ls, reading1={}, reading2={})
print('\nREADING 1 (frozen link law) predictions for delta_c WITH nu-nu, from delta_c without = 0.52639:')
for refname, di in (('primary d_inst=0.53379', d_inst_P), (f'sens d_inst={d_inst_S:.5f}', d_inst_S)):
    G0 = Gof(d_without, di); t0 = tau(G0)
    for wname, ue in U.items():
        for rate in (1.11, 1.19, 1.20):
            dpred, Gp = inv(t0 + rate*ue, di)
            key = f'{refname} | {wname} | rate {rate}'
            out['reading1'][key] = dict(u_eff=ue, r_eff=float(np.exp(2*ue)), G_without=G0, G_with_pred=Gp, dG_pred=Gp - G0, delta_with_pred=dpred)
            print(f'  {key}: u_eff={ue:.4f} (r_eff {np.exp(2*ue):.3f})  G_without={G0:.4f} -> G_with={Gp:.4f}  dG={Gp-G0:+.4f}  delta_c(with)={dpred:.5f}')

# READING 2: timing. Energy-weighted mean rate = H.
def Tdec_eff(nunu):
    m = np.array([np.sum(W*(RE0[j] + (RN0[j] if nunu else 0.0))) for j in range(len(Tb))])
    j = np.argmax(m < 1.0)
    # log interpolation between j-1 and j
    x0, x1 = np.log(m[j-1]), np.log(m[j]); t0_, t1_ = np.log(Tb[j-1]), np.log(Tb[j])
    return float(np.exp(t0_ + (0 - x0)*(t1_ - t0_)/(x1 - x0)))
Td_with = Tdec_eff(True); Td_without = Tdec_eff(False)
fam_T = np.array([0.75, 1.0, 1.5, 2.0, 3.0]); fam_d = np.array([0.51586, 0.52076, 0.52583, 0.52837, 0.53065])
def fam(T): return float(np.interp(np.log(T), np.log(fam_T), fam_d))
dw, dwo = fam(Td_with), fam(Td_without)
print(f'\nREADING 2 (timing): Tdec_eff with nu-nu = {Td_with:.3f} MeV, without = {Td_without:.3f} MeV')
print(f'  single-rate family at T_H = 1 MeV -> delta_c(with) = {dw:.5f}, delta_c(without) = {dwo:.5f}, shift {dw-dwo:+.5f}')
for refname, di in (('primary', d_inst_P), ('sens', d_inst_S)):
    print(f'  [{refname} d_inst={di:.5f}] G(with) = {Gof(dw, di):.4f}, G(without) = {Gof(dwo, di):.4f}, dG = {Gof(dw, di)-Gof(dwo, di):+.4f}')
    out['reading2'][refname] = dict(Tdec_with=Td_with, Tdec_without=Td_without, d_with=dw, d_without=dwo,
                                    dG_pred=Gof(dw, di) - Gof(dwo, di), G_with=Gof(dw, di), G_without=Gof(dwo, di))
# Reading 2, variant: anchored on the measured no-nu-nu threshold (shift only, from the family's slope)
print(f'  anchored on measured 0.52639: delta_c(with) = {0.52639 + dw - dwo:.5f}')
json.dump(out, open('step3_predictions.json', 'w'), indent=1)
