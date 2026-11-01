import time,numpy as np, wb_lin
eg=np.linspace(0.02,6,1200)
for kk,ed in [(3.0,8.0),(0.0415,4.0),(0.0079,8.0),(6.0,2.0)]:
    t=time.time(); D,Y=wb_lin.run_mode(kk,0.02,eg,0.409,ed); t1=time.time()-t
    D2,_=wb_lin.run_mode(kk,0.02,eg,0.409,ed,rtol=1e-12)
    print(kk,ed,'%.2fs'%t1,'rel diff to rtol1e-12: %.1e'%(np.max(np.abs(D-D2))/np.max(np.abs(D))),flush=True)
