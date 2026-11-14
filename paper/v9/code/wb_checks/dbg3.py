import time,numpy as np
import importlib.util,sys
src=open('wb_steve_03_paper_objects.py').read()
src=src[:src.index('res = {}')]
exec(src)
for meth in ['LSODA','BDF']:
    import scipy.integrate as si
    for keep in [1,2]:
        t=time.time()
        import types
        def surv(k,ed,keep,meth=meth):
            n=LM+1; P=np.zeros(n); P[:keep]=1
            def rhs(t,v):
                K=0.0 if ed is None else ed**3/t**4
                x,y=v[:n],v[n:]
                return np.concatenate([-K*(1-P)*x+k*(M@y),-K*(1-P)*y-k*(M@x)])
            v0=np.zeros(2*n); v0[0]=1
            sol=si.solve_ivp(rhs,(tau0,6.0),v0,method=meth,t_eval=eg,rtol=1e-9,atol=1e-12)
            return sol.nfev
        print(meth,keep,surv(2.0,2.0,keep),time.time()-t,flush=True)
