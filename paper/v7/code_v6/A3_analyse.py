# SCRIPT: analyse_A3
"""Derived two-cut quantities from raw_<label>.json (recorder output), the preregistered separation readings, the compact
JSON and the plots. usage: python3 analyse.py <label> [<label> ...]"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = ('centre', 'rm')

def derive(raw):
    G, NF = raw['G'], raw['NF']; rec = raw['rec']
    out = dict(eps=np.array([x['eps'] for x in rec]), t=np.array([x['t'] for x in rec]), Tb=np.array([x['Tb'] for x in rec]),
               Rm=np.array([x['Rm'] for x in rec]), Cmax=np.array([x['Cmax'] for x in rec]))
    for c, name in enumerate(CELLS):
        g = lambda k: np.array([x['cells'][c][k] for x in rec])
        mom = g('mom'); n2 = g('norm2'); es = g('es'); qs = g('qs'); ps = g('ps'); ke = g('ke'); kn = g('kn')
        momT = g('momT'); nT = g('normT'); momF = g('momF'); nF = g('normF'); lapse = g('A')
        e, q, P = es.sum(1), qs.sum(1), ps.sum(1)
        d = {}
        d['vL'] = 2*q/(e + P + np.sqrt(np.maximum((e+P)**2 - 4*q*q, 0.0)))
        d['q_e'] = q/e; d['P_e'] = P/e
        d['A'] = momT[:, 0]**2/nT                                  # whole-gas kept share, full discrete norm
        d['one_minus_A'] = 1.0 - d['A']
        d['A4'] = momT[:, 0]**2/np.sum(momT**2, axis=1)
        d['ratio_l'] = np.abs(momT[:, 1:])/momT[:, :1]            # |I_l|/I_0, l=1..4, whole gas
        d['AF'] = momF[:, :, 0]**2/nF                              # per flavour
        d['As'] = mom[:, :, 0]**2/n2                               # per (flavour, group)
        d['qs_es'] = qs/es; d['ps_es'] = ps/es
        d['r_s'] = 1.0 + kn/ke; d['rho_s'] = 0.5*np.log(d['r_s'])
        d['ke_H'] = ke/np.array([x['Hb'] for x in rec])[:, None]; d['kn_H'] = kn/np.array([x['Hb'] for x in rec])[:, None]
        d['dom'] = np.argmax(es, axis=1)
        d['rho_dom'] = d['rho_s'][np.arange(len(rec)), d['dom']]; d['r_dom'] = d['r_s'][np.arange(len(rec)), d['dom']]
        d['es_share'] = es/e[:, None]
        # speed-limit ratio for the whole-gas kept share, proper time of the cell, E_B = 1/R(r_m)^2
        tau = np.concatenate([[0.0], np.cumsum(0.5*(lapse[1:]+lapse[:-1])*np.diff(out['t']))])
        A = d['A']; dA = np.gradient(A, tau)
        EB = 1.0/out['Rm']**2
        d['R_SL'] = np.where(1-A > 1e-10, dA**2/(4*EB*A*np.maximum(1-A, 1e-300)), np.nan)   # undefined where 1-A is at roundoff
        d['lapse'] = lapse
        out[name] = d
    return out

def first_sep(a, b, key, cell='rm', thr=0.01, rel_to_self=False, skip=0):
    """first eps (on a's records, within the common range) where |X_b - X_a| > thr * running max |X_a|"""
    ea, eb = a['eps'], b['eps']; m = ea <= min(ea.max(), eb.max())
    get = lambda z: z[cell][key] if key in z[cell] else z[key]
    Xa = get(a)[m]; Xb = np.interp(ea[m], eb, get(b))
    scale = np.abs(Xa) if rel_to_self else np.maximum.accumulate(np.abs(Xa))
    idx = np.nonzero(np.abs(Xb - Xa) > thr*scale)[0]
    idx = idx[idx >= skip]
    return (float(ea[m][idx[0]]) if len(idx) else None), float(ea[m].max())

if __name__ == '__main__':
    labels = sys.argv[1:]
    raws = {L: json.load(open(os.path.join(HERE, f'raw_{L}.json'))) for L in labels}
    D = {L: derive(raws[L]) for L in labels}
    for L in labels:
        r = raws[L]; d = D[L]; m = (d['eps'] >= 1.7) & (d['eps'] <= 4.0)
        print(f"{L}: delta={r['delta']} {r['status']} eps_end={r['eps_end']:.3f} TH={r['TH']:.4f} records={len(r['rec'])} wall={r['seconds']/60:.1f} min")
        for cell in CELLS:
            c = d[cell]
            doms = sorted(set(int(x) for x in c['dom'][m]))
            print(f"   {cell}: readout 1.7-4: dominant slots {doms} (s=f*G+g); r_dom range [{c['r_dom'][m].min():.3f}, {c['r_dom'][m].max():.3f}] "
                  f"rho_dom [{c['rho_dom'][m].min():.3f}, {c['rho_dom'][m].max():.3f}]; nu_e r range [{c['r_s'][m][:, :6].min():.3f},{c['r_s'][m][:, :6].max():.3f}] "
                  f"nu_mutau r range [{c['r_s'][m][:, 6:].min():.3f},{c['r_s'][m][:, 6:].max():.3f}]")
            print(f"      max|v_L| {np.abs(c['vL']).max():.4f} at eps {d['eps'][np.argmax(np.abs(c['vL']))]:.3f}; 1-A max {c['one_minus_A'].max():.3e}; "
                  f"min A {c['A'].min():.6f}; max R_SL (eps 0.2-end) {np.nanmax(c['R_SL'][d['eps'] > 0.2]):.3e}; "
                  f"max R_SL in 1.7-4 {np.nanmax(c['R_SL'][m]):.3e}; max |q_s|/e_s {np.abs(c['qs_es']).max():.3f}")
    pairs = [(a, b) for a, b in (('T10_lo', 'T10_hi'), ('T5_lo', 'T5_hi'), ('T10b_lo', 'T10b_hi'), ('T5b_lo', 'T5b_hi')) if a in D and b in D]
    for a, b in pairs:
        for cell in CELLS:
            s = {k: first_sep(D[a], D[b], k, cell) for k in ('vL', 'one_minus_A', 'A', 'Cmax')}
            print(f"   separation {a} vs {b} [{cell}]: " + '; '.join(f"{k} first >1% at eps {v[0]} (common range to {v[1]:.3f})" for k, v in s.items()))
            s2 = {k: first_sep(D[a], D[b], k, cell, skip=1) for k in ('vL', 'one_minus_A', 'A', 'Cmax')}
            print(f"      same, first record (X = 0 to roundoff, metric undefined) excluded: " + '; '.join(f"{k} {v[0]}" for k, v in s2.items()))
