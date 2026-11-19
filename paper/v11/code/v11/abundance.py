# SCRIPT: NU-V11-ABUNDANCE  Gaussian abundance beta=erfc(dc/(sqrt2 sigma)); sigma tuned so beta(dc0)=beta0. Threshold shifts from v10.
from scipy.special import erfc; from scipy.optimize import brentq; import math
dc0=0.51075
shifts={'l3 +f':0.5125833-dc0,'l3 -f':0.5088395-dc0,'l4 +f':0.5096749-dc0,'l4 -f':0.5117726-dc0,'Gram +f':0.5134352-dc0,'Gram -f':0.5079300-dc0,'split (McC r=1 vs his)':0.00031}
for b0 in [1e-6,1e-10,1e-16]:
    s=brentq(lambda s: erfc(dc0/(math.sqrt(2)*s))-b0,0.01,1); f=lambda d: erfc((dc0+d)/(math.sqrt(2)*s))/b0
    print(f'beta0={b0:g} sigma={s:.4f}')
    for k,d in shifts.items(): print(f'   {k:24s} d={d:+.5f}  beta/beta0={f(d):.3f}')
    for k in ['l3','l4','Gram']: print(f'   {k} random sign (mean of +/-): {(f(shifts[k+" +f"])+f(shifts[k+" -f"]))/2:.3f}')
