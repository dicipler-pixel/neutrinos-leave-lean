# SCRIPT: NU-ART-B1-DATA  data for card B1: the twin collapse of the restart test, from McCormick's GR code
# Reads twin_minus_0.5107000.json and twin_plus_0.5107000.json (twin_run.py), writes data_B1.js. Nothing is smoothed or fitted.
import json, numpy as np, restart

def load(sign):
    d = json.load(open(f'twin_{sign}_0.5107000.json'))
    ks = sorted(d['snaps'], key=float)
    r = np.array(d['r']); rc = 0.5 * (r[1:] + r[:-1])
    sel = np.where(rc <= 2.6)[0][::2]                                   # every second cell out to r = 2.6
    eps = [d['snaps'][k]['eps'] for k in ks]
    C = [np.array(d['snaps'][k]['C'])[sel].round(5).tolist() for k in ks]
    sh = [(np.array(d['snaps'][k]['nu']) / (np.array(d['snaps'][k]['nu']) + np.array(d['snaps'][k]['e'])))[sel].round(4).tolist() for k in ks]
    Cmax = [d['snaps'][k]['Cmax'] for k in ks]
    # angular moments of the restart state, at every cell, on the 32 bins (discrete Legendre, McCormick's grid)
    mue = np.array(d['mue']); mu, P = restart.discrete_legendre(mue); dmu = mue[1] - mue[0]
    I = np.array(d['I_restart']); comp = np.array([I @ (P[l] * dmu) for l in range(5)])     # (5, ncell)
    return d, rc[sel].round(4).tolist(), eps, C, sh, Cmax, comp, I

dm, rs, em, Cm, Sm, Mm, compm, Im = load('minus')
dp, _, ep, Cp, Sp, Mp, compp, Ip = load('plus')
diff = np.abs(compm - compp)                                          # per moment, per cell
scale = np.abs(compm[0]).max()
icell = int(np.argmax(diff[3]))                                       # the cell where the planted l = 3 difference is largest
mom = dict(cell=icell, r=float(0.5 * (np.array(dm['r'])[icell] + np.array(dm['r'])[icell + 1])),
           minus=(compm[:, icell] / compm[0, icell]).round(6).tolist(), plus=(compp[:, icell] / compp[0, icell]).round(6).tolist(),
           maxdiff_rel=[float(diff[l].max() / scale) for l in range(5)])
# angular profile of both restart states at that cell, for the direction spheres
mu = 0.5 * (np.array(dm['mue'])[1:] + np.array(dm['mue'])[:-1])
ang = dict(mu=mu.round(5).tolist(), minus=(Im[icell] / Im[icell].mean()).round(6).tolist(), plus=(Ip[icell] / Ip[icell].mean()).round(6).tolist())
out = dict(delta=0.5107, r=rs, minus=dict(status=dm['status'], eps_end=dm['eps_end'], eps=em, C=Cm, share=Sm, Cmax=Mm),
           plus=dict(status=dp['status'], eps_end=dp['eps_end'], eps=ep, C=Cp, share=Sp, Cmax=Mp),
           mom=mom, ang=ang, thresholds=dict(plus=0.5125833, minus=0.5088395, none=0.5107500, plus_w=1.85e-5))
open('data_B1.js', 'w').write('window.DATA_B1 = ' + json.dumps(out) + ';\n')
print('minus', dm['status'], round(dm['eps_end'], 4), 'plus', dp['status'], round(dp['eps_end'], 4))
print('restart moments at cell', icell, 'r =', round(mom['r'], 3))
print('  minus l0..4 / l0', mom['minus']); print('  plus  l0..4 / l0', mom['plus'])
print('  max |diff| over cells / max c0, l = 0..4:', ['%.1e' % x for x in mom['maxdiff_rel']])
print('rows', len(em), len(ep), 'cols', len(rs))
