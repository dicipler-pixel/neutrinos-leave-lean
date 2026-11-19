# SCRIPT: STEVE-TABLES-01  consistency checks on McCormick's published tables (no new physics)
import numpy as np
from scipy.special import erfc
# Table II
Rnu=np.array([.10,.20,.30,.409,.488]); dpf=0.49773
dnu=np.array([.50547,.51297,.52027,.52832,.53379])
def Cl(d): return 4/3*(1-np.sqrt(1-1.5*d))
print("Eq15 inverse: Cl,c pf=%.4f"%Cl(dpf))
sh_d=dnu/dpf-1; sh_C=Cl(dnu)/Cl(dpf)-1
print("R_nu  dd/d(tab)  dd/d(calc)  dC/C(tab) dC/C(calc)  dd/(R d)  dC/(R C)")
tabd=[1.56,3.06,4.53,6.15,7.24]; tabC=[2.3,4.7,7.0,9.6,11.5]
for r,a,b,c,d in zip(Rnu,tabd,sh_d,tabC,sh_C): print("%.3f %7.2f %9.2f %9.1f %9.2f %9.4f %9.4f"%(r,a,100*b,c,100*d,b/r,d/r))
print("linear fit through origin: slope dd=%.4f dC=%.4f"%((sh_d@Rnu)/(Rnu@Rnu),(sh_C@Rnu)/(Rnu@Rnu)))
# rapidity additivity test: ln(1+shift)/R
print("ln(1+dd)/R:",np.round(np.log1p(sh_d)/Rnu,4)," ln(1+dC)/R:",np.round(np.log1p(sh_C)/Rnu,4))
# gradual decoupling
edec=np.array([.25,.5,1,2,4,8]); dg=np.array([.52709,.52428,.51865,.51092,.50354,.49967])
shd=dg/dpf-1; shC=Cl(dg)/Cl(dpf)-1
print("edec  dd/d(calc) tab   dC/C(calc) tab")
for e,a,t1,b,t2 in zip(edec,shd,[5.90,5.33,4.20,2.65,1.17,.39],shC,[9.2,8.3,6.5,4.0,1.8,.6]): print("%5.2f %7.2f %5.2f %8.2f %5.2f"%(e,100*a,t1,100*b,t2))
inst=0.52832/dpf-1
G=shd/inst; print("G=S/S_inst:",np.round(G,4))
print("-ln G:",np.round(-np.log(G),4)); 
print("log-log slope of -lnG vs edec:",np.round(np.diff(np.log(-np.log(G)))/np.diff(np.log(edec)),3))
y=1/G-1; print("1/G-1:",np.round(y,4)," slope:",np.round(np.diff(np.log(y))/np.diff(np.log(edec)),3))
# optical depth remaining after eps for kappa=H (edec/eps)^3 :  tau(eps)=(edec/eps)^3/3  (dt/(2t)=d eps/eps)
# Table III
dm=np.array([1e-1,3e-2,1e-2,3e-3,1e-3,3e-4,1e-4])
pf=np.array([.679,.497,.390,.288,.215,.151,.105]); fs=np.array([.799,.590,.470,.343,.255,.178,.123])
print("ratios:",np.round(fs/pf,3),"mean(1e-3..1e-1)=%.3f"%np.mean((fs/pf)[:5]))
a=np.polyfit(np.log(dm),np.log(pf),1)[0]; b=np.polyfit(np.log(dm),np.log(fs),1)[0]; print("fit slopes pf %.3f fs %.3f"%(a,b))
r=1.19
print("candidate: (1+dd)^n=1.19 -> n=%.3f ; (1+dC)^n -> n=%.3f"%(np.log(r)/np.log(1+inst),np.log(r)/np.log(Cl(.52832)/Cl(dpf))))
print("equal-mass distance rescale s=r^(1/slope)=%.3f"%(r**(1/0.267)))
# Table IV
for lab,D in [("Gaussian C_l (D=9.7%)",.097),("Gaussian delta_m (D=6.2%)",.062)]:
    out=[]
    for beta in [1e-9,1e-12,1e-15]:
        # find sigma: erfc(x)=beta, x=Clc/(sqrt2 sigma)
        from scipy.optimize import brentq
        x=brentq(lambda x:erfc(x)-beta,0.1,10)
        out.append(erfc(x*(1+D))/beta)
    print(lab,np.round(out,4))
for eta in [1,0.6]:
    print("eta",eta,[round(b**((1.097)**eta-1),3) for b in [1e-9,1e-12,1e-15]])
print("power-law n=3,5:",1.097**-3,1.097**-5)
print("beta^1.18 -> exponent from (1+D)^2-1 =",1.097**2-1)
