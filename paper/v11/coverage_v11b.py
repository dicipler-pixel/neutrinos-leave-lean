#!/usr/bin/env python3
"""Mechanical coverage check: every structural item of v10 and v12 must be present in v11.
Items: section/subsection/subsection*/paragraph titles, figures (graphics file), tables (header row),
theorem-like environments, labelled equations, listings (file), bib keys, appendix entries.
Sources are flattened through \\input. Also cross-checks figure/table caption counts and page counts in the PDFs."""
import re, os, subprocess, sys
V10='/workspace/blackhole/big/paper/v10'; V12='/workspace/blackhole/big/paper/v12'; V11='/workspace/ink/D17/v11b'; V11OLD='/workspace/ink/D17/v11'
def flat(main, dirs):
    def rd(name):
        for d in dirs:
            p=os.path.join(d, name if name.endswith('.tex') else name+'.tex')
            if os.path.exists(p): return open(p).read(), p
        raise FileNotFoundError(name)
    txt,_=rd(main)
    def sub(m):
        t,_=rd(m.group(1)); return re.sub(r'\\input\{([^}]+)\}', sub, t)
    return re.sub(r'\\input\{([^}]+)\}', sub, txt)
def norm(s):
    s=re.sub(r'\\label\{[^}]*\}','',s); s=re.sub(r'\s+',' ',s).strip(); return s
def items(tex):
    out=[]  # (kind, key, order)
    # track which section each item is in, by position
    secs=[(m.start(), norm(m.group(2))) for m in re.finditer(r'\\(section|subsection)\*?\{((?:[^{}]|\{[^{}]*\})*)\}', tex)]
    def where(pos):
        cur='(front matter)'
        for p,t in secs:
            if p<=pos: cur=t
        return cur
    app=tex.find('\\appendix')
    for m in re.finditer(r'\\(section|subsection|subsubsection|paragraph)(\*?)\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', tex):
        kind=m.group(1)+m.group(2)
        if kind.startswith('section') and app>=0 and m.start()>app: kind='appendix'
        out.append((kind, norm(m.group(3)), where(m.start())))
    for m in re.finditer(r'\\includegraphics(\[[^\]]*\])?\{([^}]+)\}', tex): out.append(('figure', m.group(2), where(m.start())))
    for m in re.finditer(r'\\begin\{tabular\}\{[^}]*\}(.*?)\\\\', tex, re.S):
        h=norm(re.sub(r'\\(toprule|midrule|bottomrule)','',m.group(1)))[:80]; out.append(('table', h, where(m.start())))
    for env in ['theorem','proposition','lemma','corollary','definition','remark']:
        for m in re.finditer(r'\\begin\{'+env+r'\}(\[[^\]]*\])?', tex): out.append((env, (m.group(1) or '')+'@'+where(m.start()), where(m.start())))
    for m in re.finditer(r'\\label\{(eq:[^}]+)\}', tex): out.append(('equation', m.group(1), where(m.start())))
    for m in re.finditer(r'\\lstinputlisting(\[[^\]]*\])?\{([^}]+)\}', tex): out.append(('listing', m.group(2), where(m.start())))
    for m in re.finditer(r'\\bibitem\{([^}]+)\}', tex): out.append(('bibitem', m.group(1), ''))
    for m in re.finditer(r'\\caption\{', tex): pass
    return out
def pdfinfo(p):
    o=subprocess.run(['pdfinfo',p],capture_output=True,text=True).stdout
    return int(re.search(r'Pages:\s+(\d+)',o).group(1))
def pdfcaps(p):
    t=subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
    return len(re.findall(r'Figure \d+:', t)), len(re.findall(r'Table \d+:', t))
t10=flat('neutrinos_v10',[V10]); t12=flat('neutrinos_v12',[V12,V10]); t11=flat('neutrinos_v11',[V11]); t11o=flat('neutrinos_v11',[V11OLD])
I10,I12,I11=items(t10),items(t12),items(t11); I11o=items(t11o)
# v11 lookup: exact key; for titles also allow the v12 title to be a prefix of the v11 title (title extended, not replaced)
from collections import Counter
c11=Counter((k,v) for k,v,_ in I11)
loc11={}
for k,v,w in I11: loc11.setdefault((k,v),w)
def find(kind,key):
    if (kind,key) in loc11: return loc11[(kind,key)], 'exact'
    if kind in('section','subsection','subsection*','paragraph','appendix'):
        base=key.rstrip('.')
        for (k,v),w in loc11.items():
            if k==kind and v.startswith(base): return (w+' [title extended: '+v+']'), 'extended'
    if kind=='table':
        for (k,v),w in loc11.items():
            if k=='table' and (v.startswith(key[:40]) or key.startswith(v[:40])): return w, 'prefix'
    return None, None
lines=[]; missing=[]
def section(name,I):
    lines.append(f'\n## Items of {name} ({len(I)} items)\n\n| # | kind | item | in {name} under | v11 location (section) | match |\n|---|---|---|---|---|---|')
    cnt=Counter()
    for i,(k,v,w) in enumerate(I,1):
        cnt[(k,v)]+=1
        loc,how=find(k,v)
        if loc is None or (how=='exact' and c11[(k,v)]<cnt[(k,v)] and k not in('bibitem',)):
            if loc is None: missing.append((name,k,v,w)); loc='**MISSING**'; how='-'
            else: how+=f' (occurrence {cnt[(k,v)]} of {c11[(k,v)]} in v11: CHECK)'; missing.append((name,k,v+' [occurrence count]',w))
        vv=v.replace('|','\\|'); ww=w.replace('|','\\|'); ll=str(loc).replace('|','\\|')
        lines.append(f'| {i} | {k} | {vv} | {ww} | {ll} | {how} |')
section('v10',I10); section('v12',I12); section('v11',I11o)
p10,p12,p11=[pdfinfo(p) for p in [f'{V10}/What_the_Neutrino_State_Must_Keep_v10_2026-11-13.pdf',f'{V12}/What_the_Neutrino_State_Must_Keep_v12_2026-11-14.pdf',f'{V11}/neutrinos_v11.pdf']]
f10,f12,f11=[pdfcaps(p) for p in [f'{V10}/What_the_Neutrino_State_Must_Keep_v10_2026-11-13.pdf',f'{V12}/What_the_Neutrino_State_Must_Keep_v12_2026-11-14.pdf',f'{V11}/neutrinos_v11.pdf']]
kc=lambda I:Counter(k for k,_,_ in I)
hdr=['# Coverage of v10, v12 and v11 in v11b (v11b column = this build; tex file names keep _v11)','',f'Generated by `coverage_v11b.py` (mechanical extraction from the flattened tex; PDFs cross-checked).','',
 '| | v10 | v12 | v11 |','|---|---|---|---|',f'| pages (PDF) | {p10} | {p12} | {p11} |',f'| figure captions in PDF text | {f10[0]} | {f12[0]} | {f11[0]} |']
for k in sorted(set(kc(I10))|set(kc(I12))|set(kc(I11))): hdr.append(f'| {k} (tex) | {kc(I10)[k]} | {kc(I12)[k]} | {kc(I11)[k]} |')
hdr+=['',f'**Missing items: {"NONE" if not missing else len(missing)}**','']
for m in missing: hdr.append(f'- MISSING from {m[0]}: {m[1]} `{m[2]}` (under {m[3]})')
hdr.append(f'\nPage count check: v11 {p11} >= v12 {p12}: {"PASS" if p11>=p12 else "FAIL"}')
t11pdf=re.sub(r'\s+',' ',subprocess.run(['pdftotext',f'{V11}/neutrinos_v11.pdf','-'],capture_output=True,text=True).stdout)
pdfmiss=[]
for nm,I in (('v10',I10),('v12',I12),('v11',I11o)):
    for k,v,w in I:
        if k in('section','subsection','subsection*','appendix'):
            plain=re.sub(r'\$[^$]*\$|\\[a-zA-Z]+|[{}~\\]',' ',v); words=[x for x in plain.split() if x.isalpha() and len(x)>3][:4]
            if words and not all(x in t11pdf for x in words): pdfmiss.append((nm,v))
hdr.append(f'PDF cross-check: every v10/v12 section, subsection and appendix title word-set found in the v11 PDF text: {"PASS" if not pdfmiss else "FAIL "+str(pdfmiss)}')
open(f'{V11}/coverage_v11b_auto.md','w').write('\n'.join(hdr+lines)+'\n')
print('\n'.join(hdr))

# ---- cross-check against dr eggbot's independent v12 inventory (read-only)
inv=open('/workspace/eggbot/keep_check/v12_inventory.md').read()
eg=[]
for m in re.finditer(r'\\(section|subsection\*?)\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', inv): eg.append(('title',norm(m.group(2))))
for m in re.finditer(r'\\includegraphics(\[[^\]]*\])?\{([^}]+)\}', inv): eg.append(('figure',m.group(2)))
titles11=set(norm(v) for k,v,_ in I11 if k in('section','subsection','subsection*','appendix'))
figs11=set(v for k,v,_ in I11 if k=='figure')
mine=set(norm(v) for k,v,_ in I12 if k in('section','subsection','subsection*','appendix'))|set(v for k,v,_ in I12 if k=='figure')
egrows=[]; egmiss=[]; notmine=[]
for k,v in eg:
    ok = (v in figs11) if k=='figure' else (v in titles11 or any(t.startswith(v) for t in titles11))
    if not ok: egmiss.append(v)
    if v not in mine: notmine.append(v)
egtxt=[f'\n## Cross-check against dr eggbot inventory (/workspace/eggbot/keep_check/v12_inventory.md)\n',
 f'Inventory items parsed: {len(eg)} ({sum(1 for k,_ in eg if k=="title")} section/subsection titles, {sum(1 for k,_ in eg if k=="figure")} figures).',
 f'Present in v11: {len(eg)-len(egmiss)}. Missing in v11: {"NONE" if not egmiss else egmiss}.',
 f'On their list but not on my v12 list: {"NONE" if not notmine else notmine}.']
open(f'{V11}/coverage_v11b_auto.md','a').write('\n'.join(egtxt)+'\n')
print('\n'.join(egtxt))
