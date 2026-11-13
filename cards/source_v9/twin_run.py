# SCRIPT: NU-ART-BH-TWIN  record the twin collapse of the restart test (eps_s = 2, l = 3, +f and -f) at one delta
# between the two thresholds (+f: 0.5125833, -f: 0.5088395), so one member forms a black hole and the other disperses.
import sys, json, numpy as np, restart
delta = float(sys.argv[1]); sign = sys.argv[2]; f = 0.5 if sign == 'plus' else -0.5
snaps = [round(2.0 + 0.05*i, 4) for i in range(0, 260)]
o = restart.run_member(delta, 2.0, 3, f, 'cache', mode='bump', snap_eps=snaps)
st = restart.surface_state(delta, 2.0, 'cache')
pert = restart.perturb_bump(st, 3, f)
out = dict(delta=delta, sign=sign, f=f, status=o['status'], eps_end=float(o['eps']), max2MR=float(o['max2MR']),
           r=np.asarray(o['r']).tolist(), mue=np.asarray(o['mue']).tolist(),
           snaps={str(k): dict(eps=v['eps'], C=v['C'].tolist(), e=v['e'].tolist(), nu=v['nu'].tolist(), rC=v['rC'], Cmax=v['Cmax'])
                  for k, v in o['snaps'].items()},
           I_restart=np.asarray(pert['I']).tolist(), I_restart_base=np.asarray(st['I']).tolist())
json.dump(out, open(f'twin_{sign}_{delta:.7f}.json', 'w'))
print(sign, delta, o['status'], round(float(o['eps']), 3), 'snaps', len(o['snaps']), 'max2M/R', round(float(o['max2MR']), 4))
