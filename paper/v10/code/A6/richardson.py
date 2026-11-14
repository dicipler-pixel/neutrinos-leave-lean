# SCRIPT: NU-V6-RICHARDSON-A6  three-level odd rate (r = 1.25 / 0.8), kill line and Richardson extrapolation as preregistered
import json, math, itertools, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import oddrate as o
q = 1.5
L1 = ((0.5098412859375, 0.509841871875), (0.5116919799999999, 0.5116926831249999))
L2 = ((0.5099165789062501, 0.50991716484375), (0.5117560815625, 0.5117567846875))
def br(tag):
    d = json.load(open(os.path.join(HERE, f'res_{tag}.json'))); return (d['lo'], d['hi'])
L3 = (br('L3_r125'), br('L3_r08'))
def rich(R1, R2, R3):
    s12, s23 = R2-R1, R3-R2
    if s23 == 0 or s12/s23 <= 1: return float('nan'), float('nan')
    p = math.log(s12/s23)/math.log(q); return p, R3 + s23/(q**p - 1)
out = {}
for df_lab, df in (('central', o.DF), ('df+7.8e-5', o.DF+7.8e-5), ('df-7.8e-5', o.DF-7.8e-5)):
    S = [o.summary('', *L, 1.25) for L in (L1, L2, L3)]
    R = [o.rate(0.5*sum(L[0]), 0.5*sum(L[1]), 1.25, df) for L in (L1, L2, L3)]
    rng = [o.corners(L[0], L[1], 1.25, df) for L in (L1, L2, L3)]
    p, Rinf = rich(*R)
    corner = [rich(*c)[1] for c in itertools.product(*rng)]
    corner = [c for c in corner if c == c]
    part_i = 0.5*(max(corner)-min(corner)) if corner else float('nan')
    s23 = R[2]-R[1]
    two = {pp: R[2] + s23/(q**pp - 1) for pp in (1, 2)}
    part_ii = max(abs(Rinf-two[1]), abs(Rinf-two[2]))
    out[df_lab] = dict(R=R, ranges=rng, s12=R[1]-R[0], s23=s23, ratio=(s23/(R[1]-R[0])), p_obs=p, R_inf=Rinf,
                       err_bracket=part_i, err_order=part_ii, err=part_i+part_ii, two_level=two,
                       kill=abs(s23) > abs(R[1]-R[0]), corner_n=len(corner))
dc3 = (0.5*sum(L3[0]), 0.5*sum(L3[1]))
out['thresholds_L3'] = dict(r125=dc3[0], r08=dc3[1], shift23_r125=dc3[0]-0.509916871875, shift23_r08=dc3[1]-0.511756433125,
                            brackets=L3)
print(json.dumps(out, indent=1))
