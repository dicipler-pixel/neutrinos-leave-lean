# SCRIPT: K0-STEVE-ARITHMETIC
# Purpose: check which Steve numbers follow from his own Eq.(15) alone, so that nothing below is credited with them.
# KILL (written first): if Eq.(15) with C_l,c = 0.662 -> 0.726 does NOT give delta_c = 0.4977 -> 0.5284 within 3e-3,
# or the Table II G column is not reproduced from shifts/inst-shift within 2e-3, the inputs are mis-transcribed and all below is void.
import numpy as np
d = lambda C: C - 3/8*C**2
print('Eq15: delta(0.662)=%.4f  delta(0.726)=%.4f  ratio-1=%.4f' % (d(.662), d(.726), d(.726)/d(.662)-1))
C=0.662; print('local conversion dln(delta)/dln(C) at C=0.662: %.3f  -> 0.235*that = %.4f (Steve quotes 0.15)' % ((1-.75*C)/(1-.375*C), .235*(1-.75*C)/(1-.375*C)))
# Table II gradual decoupling, shifts in delta_c (percent) and C_l,c
edec=np.array([.25,.5,1,2,4,8]); sd=np.array([5.90,5.33,4.20,2.65,1.17,0.39]); sc=np.array([9.2,8.3,6.5,4.0,1.8,0.6])
G_pub=np.array([.959,.867,.683,.431,.190,.063])
print('G from delta_c shifts /6.15:', np.round(sd/6.15,3)); print('G from C_l shifts /9.6    :', np.round(sc/9.6,3)); print('published G              :', G_pub)
ok = np.max(np.abs(sd/6.15-G_pub))<2e-3
print('KILL K0:', 'did not fire' if (abs(d(.726)/d(.662)-1-0.0615)<3e-3 and ok) else 'FIRED')
# Table II shift vs R_nu (instantaneous), C_l column
R=np.array([.1,.2,.3,.409,.488]); sC=np.array([2.3,4.7,7.0,9.6,11.5]); sD=np.array([1.56,3.06,4.53,6.15,7.24])
print('shift_C / R :', np.round(sC/R,2)); print('shift_d / R :', np.round(sD/R,2))
