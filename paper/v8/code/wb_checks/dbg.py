import time,numpy as np, wb_lin, scipy.integrate as si
orig=si.solve_ivp
eg=np.linspace(0.02,6,1200)
kk=0.0415
for meth in ['BDF','Radau']:
    def f(*a,**kw):
        kw['method']=meth; kw['rtol']=1e-8; r=orig(*a,**kw); print(meth,'nfev',r.nfev,flush=True); return r
    wb_lin.solve_ivp=f
    t=time.time(); D,Y=wb_lin.run_mode(kk,0.02,eg,0.409,4.0); print(meth,time.time()-t,flush=True)
