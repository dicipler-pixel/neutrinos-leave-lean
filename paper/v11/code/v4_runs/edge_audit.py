# SCRIPT: NU-V4-EDGE-AUDIT  rerun the decisive bracket edges of every reported threshold with the v2 runners:
# records how each run ended (horizon, breakdown, dispersed, crash), min I over the run, max 2M/R.
import sys, json, os, importlib
from multiprocessing import Pool
sys.path.insert(0, os.environ['SIMDIR']); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
base=dict(fnu=0.409,N=400,K=32,eps0=0.1,eps_dec=2.0,eps_max=15.0,nexp=3)
# (label, runner, kwargs, result file)
T=[('E fnu=0.2','run_nuc_n_v2',dict(base,fnu=0.2),'E_fnu020_ed2_n3'),
   ('F r=1/4','run_split_v2',dict(base,rr=0.25),'F_r025'),('F r=4','run_split_v2',dict(base,rr=4.0),'F_r4'),
   ('F2 r=1/16','run_split_v2',dict(base,rr=0.0625),'F2_r1o16'),('F2 r=16','run_split_v2',dict(base,rr=16.0),'F2_r16'),
   ('H1 r=1','run_split_v2',dict(base,rr=1.0),'H1_r1'),('I r=1/4 dt/4','run_split_dt_v2',dict(base,rr=0.25,dtk=4.0),'I_r025_dt4'),
   ('J r=2','run_split_v2',dict(base,rr=2.0),'J_r2'),('J r=1/2','run_split_v2',dict(base,rr=0.5),'J_r05'),
   ('K r=1.25','run_split_v2',dict(base,rr=1.25),'K_r125_clean'),('K r=0.8','run_split_v2',dict(base,rr=0.8),'K_r08_clean'),
   ('L r=4 shear','run_shear_v2',dict(base,rr=4.0),'L_r4'),('L r=1/4 shear','run_shear_v2',dict(base,rr=0.25),'L_r025'),
   ('M r=4 K48','run_split_v2',dict(base,rr=4.0,K=48),'M_r4_K48'),('M r=1/4 K48','run_split_v2',dict(base,rr=0.25,K=48),'M_r025_K48')]
def edges(f):
    j=json.load(open(f'res_{f}.json')); lg=j['log']
    if 'lo' in j: lo,hi=j['lo'],j['hi']
    else: lo,hi=j['dc']-j['w']/2,j['dc']+j['w']/2
    # snap to the logged run nearest each edge
    dl=min((x for x in lg if x[1]=='dispersed'),key=lambda x:abs(x[0]-lo))[0]; dh=min((x for x in lg if x[1]=='BH'),key=lambda x:abs(x[0]-hi))[0]
    return dl,dh
def go(a):
    lab,runner,kw,d,which=a; o=importlib.import_module(runner).run(d,**kw)
    return lab,which,d,o['status'],float(o['eps']),float(o['Imin']),float(o['max2MR'])
jobs=[]
for lab,runner,kw,f in T:
    dl,dh=edges(f); jobs+= [(lab,runner,kw,dl,'lower'),(lab,runner,kw,dh,'upper')]
with Pool(2) as p:
    for lab,which,d,s,e,im,m2 in p.imap(go,jobs):
        print(f'{lab:16s} {which} edge delta={d:.8f}: {s:12s} eps={e:.2f} minI={im:.3e} max2M/R={m2:.4f}',flush=True)
