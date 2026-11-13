# SCRIPT: PBH-NU-WITNESS-CONV  compare production vs LM=120 and tight-tolerance runs (K2)
import json
P={(d['n'],d['ratio'],d['L']):d for d in json.load(open('witness_prod.json'))}
worst=0
for mode in ('convLM','convTol'):
    for d in json.load(open('witness_%s.json'%mode)):
        p=P[(d['n'],d['ratio'],d['L'])]; ch=[]
        for tt in ('1.7','4.0','6.0'):
            for q in ('R_ret','R_A','R_F'):
                ch.append(abs(d['res'][tt][q]-p['res'][tt][q])/abs(p['res'][tt][q]))
        worst=max(worst,max(ch)); print(mode,d['n'],d['ratio'],d['L'],'max rel change %.2e'%max(ch),'bound %.6f'%d['bound_worst'])
print('WORST',worst)
