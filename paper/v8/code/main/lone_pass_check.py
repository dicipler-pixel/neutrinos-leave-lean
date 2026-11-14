# SCRIPT: PBH-NU-LONE-PASS  the one rate-ratio form that passed (1 of 32) tested on Test B, which it never saw
# Kill condition (written first): dies if |G_pred - 0.317| > 0.08 at n=6, eps_dec=2.
import numpy as np
eps=np.linspace(0.1,4,6001); kr=1.0
f=lambda kap,k:np.exp(-kap/k)
for n,ed,meas in [(3,2.0,0.431),(6,2.0,0.317)]:
    pred=np.mean(f((ed/eps)**n,kr*eps)); print('n=%d eps_dec=%.0f  pred %.3f  measured %.3f  diff %.3f  %s'%(n,ed,pred,meas,pred-meas,'dies' if abs(pred-meas)>0.08 else 'survives'))
