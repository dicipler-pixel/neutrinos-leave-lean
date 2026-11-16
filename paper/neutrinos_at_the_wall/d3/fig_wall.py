# SCRIPT: NAW-FIG-WALL-01  The neutrino step against the wall, drawn from the boost matrices (no fitted curve).
# Panel a: g = sinh^2(ln z / 2) = (z-1)^2/(4z) for the neutrino step and the charged generation steps; g = 1 is the wall.
# Panel b: the square (step a, step b, back a, back b) of two equal perpendicular steps, repeated, in the Poincare disc.
#          Below the wall it is a turn about a fixed point; past it, a run to the rim.
import numpy as np, math, matplotlib
matplotlib.use('pgf'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':8,'pgf.texsystem':'pdflatex','pgf.rcfonts':False,'font.family':'serif','axes.spines.top':False,'axes.spines.right':False})
def boost(ux,uy,r):
    c,s=math.cosh(r),math.sinh(r); u=np.array([ux,uy]); B=np.eye(3); B[0,0]=c; B[0,1:]=s*u; B[1:,0]=s*u; B[1:,1:]=np.eye(2)+(c-1)*np.outer(u,u); return B
def square(r): return boost(1,0,r)@boost(0,1,r)@boost(-1,0,r)@boost(0,-1,r)
disc=lambda p: (p[1]/(1+p[0]), p[2]/(1+p[0]))
g=lambda z:(z-1)**2/(4*z)
nu={'neutrino step, current data':5.80689,'neutrino step, NuFIT 6.0':5.8165}
ch={'$\\mu\\to\\tau$':16.82,'$d\\to s$':19.89,'$s\\to b$':44.74,'$c\\to t$':135.6,'$e\\to\\mu$':206.8,'$u\\to c$':589.4}
zw=3+2*math.sqrt(2)
fig,ax=plt.subplots(1,2,figsize=(6.5,3.0),gridspec_kw={'width_ratios':[1.25,1]})
a=ax[0]; Z=np.geomspace(1.2,800,400); a.plot(np.log(Z),g(Z),color='0.35',lw=1.2)
a.axhline(1,color='#c0392b',lw=1); a.axvline(math.log(zw),color='#c0392b',lw=0.6,ls=':')
a.text(2.0,0.62,'wall $g=1$: $z=3+2\\sqrt{2}$, $\\Gamma^2=1/2$',color='#c0392b')
for k,z in ch.items(): a.plot(math.log(z),g(z),'s',color='#2a78d6',ms=5); a.annotate(k,(math.log(z),g(z)),xytext=((4,-12) if k!='$d\\to s$' else (-30,6)),textcoords='offset points',color='#2a78d6',fontsize=7)
a.plot([math.log(z) for z in nu.values()],[g(z) for z in nu.values()],'o',color='#e67e22',ms=6)
a.annotate('neutrino step\n$m_3/m_2$',(math.log(5.81),g(5.81)),xytext=(-30,34),textcoords='offset points',color='#e67e22',arrowprops=dict(arrowstyle='-',color='#e67e22',lw=0.7))
a.set_yscale('log'); a.set_xlabel('$\\ln z$ (step between neighbouring masses)'); a.set_ylabel('$g=\\sinh^2(\\ln z/2)$'); a.set_title('a. where each step sits',fontsize=7)
a.text(0.3,0.012,'turn (held)',color='0.3'); a.text(5.0,1.6,'run (leaves)',color='0.3')
b=ax[1]; t=np.linspace(0,2*np.pi,300); b.plot(np.cos(t),np.sin(t),color='0.3',lw=1); b.set_aspect('equal'); b.axis('off')
def walk(r,reps):
    dirs=[(1,0),(0,1),(-1,0),(0,-1)]; M=np.eye(3); pts=[disc(M@np.array([1.,0,0]))]; ends=[]
    for k in range(reps):
        for (ux,uy) in dirs:
            for f in np.linspace(0,1,25)[1:]: pts.append(disc(M@boost(ux,uy,r*f)@np.array([1.,0,0])))
            M=M@boost(ux,uy,r)
        ends.append(disc(M@np.array([1.,0,0])))
    return np.array(pts),np.array(ends),M
out=[]
for z,col,reps,lab in [(5.80689,'#e67e22',1,'neutrino step, current data'),(16.82,'#2a78d6',1,'$\\mu\\to\\tau$ step')]:
    r=math.log(z); P,E,M=walk(r,reps); b.plot(P[:,0],P[:,1],color=col,lw=1.2,label=lab+': one square')
    out.append((lab,np.hypot(*E[-1])))
r=math.log(5.80689); C=square(r); p=np.array([1.,0,0]); orb=[disc(p)]
for k in range(15): p=C@p; orb.append(disc(p))
orb=np.array(orb); b.plot(orb[:,0],orb[:,1],'o',color='#e67e22',ms=3,mfc='white',label='neutrino step: the square repeated')
w,v=np.linalg.eig(C); i=np.argmin(abs(w-1)); fp=np.real(v[:,i]); fp=fp/np.sqrt(fp[0]**2-fp[1]**2-fp[2]**2); fp=fp*np.sign(fp[0])
b.plot(*disc(fp),'*',color='k',ms=9,label='fixed point of the turn'); out.append(('fixed point radius',np.hypot(*disc(fp))))
b.plot(0,0,'k.',ms=4); b.legend(frameon=False,fontsize=6.5,loc='upper center',bbox_to_anchor=(0.5,0.0)); b.set_title('b. one square of two equal steps, from the centre',fontsize=7)
plt.tight_layout(); plt.savefig('fig_wall.pdf'); plt.savefig('fig_wall.pgf')
for k,z in {**nu,'mu->tau':16.82}.items():
    gg=g(z); print(f'{k}: z={z} g={gg:.5f}', f'turn {math.degrees(4*math.acos(gg)):.2f} deg' if gg<1 else f'run {4*math.acosh(gg):.3f}')
for lab,R in out: print(lab,'last disc radius',round(R,4))
