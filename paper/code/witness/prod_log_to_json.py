# SCRIPT: PBH-NU-WITNESS-LOG2JSON  rebuild witness_prod.json (the machine-readable production output) from prod.log, the shipped run log
import re, json, os
here=os.path.dirname(os.path.abspath(__file__)); out=[]
for line in open(os.path.join(here,'prod.log')):
    m=re.match(r'\((\d+), ([\d.]+), (\d+)\) [\d.]+s (.*) pos ([\d.]+) ([\d.]+) bound ([\d.]+) ([\d.]+)',line.strip())
    if not m: continue
    n,ratio,L=int(m.group(1)),float(m.group(2)),int(m.group(3)); res={}
    for tt,a,b,c in re.findall(r'([\d.]+):([\d.e+-]+)/([\d.e+-]+)/([\d.e+-]+)',m.group(4)):
        res[tt]=dict(R_ret=float(a),R_A=float(b),R_F=float(c))
    out.append(dict(n=n,ratio=ratio,L=L,pos_min=[float(m.group(5)),float(m.group(6))],bound_worst=float(m.group(7)),bound_worst_N=float(m.group(8)),res=res))
json.dump(out,open(os.path.join(here,'witness_prod.json'),'w'),indent=1); print(len(out),'records ->',os.path.join(here,'witness_prod.json'))
