# SCRIPT: NU-V6-ODDRATE  odd rate [tau(r)-tau(1/r)]/ln r with hard four-corner bracket ranges (v5.1 App. A.9, A.11)
import math, json, sys
DF, DI = 0.49773, 0.52832
def tau(d, df=DF, di=DI): return math.log((di-d)/(d-df))
def G(d, df=DF, di=DI): return (d-df)/(di-df)
def rate(dr, dir_, r, df=DF, di=DI): return (tau(dr,df,di)-tau(dir_,df,di))/math.log(r)
def corners(br, bir, r, df=DF, di=DI):
    # br, bir = (lo, hi) brackets for r and 1/r; tau decreases in delta
    vals = [rate(a, b, r, df, di) for a in br for b in bir]
    return min(vals), max(vals)
def even(dr, dir_, d1, df=DF, di=DI): return 0.5*(tau(dr,df,di)+tau(dir_,df,di))-tau(d1,df,di)
def summary(name, br, bir, r, d1=None):
    mr = 0.5*sum(br); mi = 0.5*sum(bir); out = dict(pair=name, r=r, dc_r=mr, dc_inv=mi, G_r=G(mr), G_inv=G(mi))
    out['rate'] = rate(mr, mi, r); out['range'] = corners(br, bir, r)
    for s, lab in ((+7.8e-5, 'df+7.8e-5'), (-7.8e-5, 'df-7.8e-5')):
        out['rate_'+lab] = rate(mr, mi, r, DF+s); out['range_'+lab] = corners(br, bir, r, DF+s)
    if d1 is not None: out['even'] = even(mr, mi, d1)
    return out
if __name__ == '__main__':
    # reproduce v5.1's inner rates from its stored brackets
    for nm, br, bir, r in (('v5.1 all r=1.2', (0.51001440, 0.51001532), (0.51151422, 0.51151483), 1.2),
                           ('v5.1 all r=1.25', (0.50984047, 0.50984092), (0.51169535, 0.51169611), 1.25),
                           ('v5.1 shear r=1.2', (0.50995397, 0.50995435), (0.51157461, 0.51157499), 1.2)):
        s = summary(nm, br, bir, r, d1=0.510741)
        print(f"{nm}: rate {s['rate']:.4f} range [{s['range'][0]:.4f}, {s['range'][1]:.4f}] even {s['even']:+.4f}  "
              f"df+: {s['rate_df+7.8e-5']:.4f}  df-: {s['rate_df-7.8e-5']:.4f}")
