# SCRIPT: NU-V9-GUARD  diff guard: every sentence changed between v8 and v9 must be registered to a ledger item
# Usage: NU_OLD=<v8 paper dir> NU_NEW=<v9 paper dir> python3 guard.py   (writes DIFF_REPORT.md; exit 1 if any change is unregistered)
import os, re, sys, glob, difflib
H = os.path.dirname(os.path.abspath(__file__))
OLD = os.environ.get('NU_OLD', os.path.join(H, '..', 'paper_v8'))   # v8 source (from the v8 zip)
NEW = os.environ.get('NU_NEW', os.path.join(H, '..', 'paper_v9'))
def load(d, main):
    parts = [(main, open(os.path.join(d, main)).read())]
    for f in sorted(glob.glob(d + '/sec_new_*.tex') + glob.glob(d + '/app_new_*.tex')):
        parts.append((os.path.basename(f), open(f).read()))
    return parts
def sentences(parts):
    out = []
    for name, t in parts:
        for line in t.split('\n'):
            for s in re.split(r'(?<=[.;:])\s+(?=[A-Z\\$(])', line):
                s = s.strip()
                if s: out.append((name, s))
    return out
a = sentences(load(OLD, 'neutrinos_v8.tex'))
b = sentences(load(NEW, 'neutrinos_v9.tex'))
A = [s for _, s in a]; B = [s for _, s in b]
reg = []
for line in open(H + '/CHANGES.tsv'):
    if line.strip() and not line.startswith('#'):
        item, snip = line.rstrip('\n').split('\t', 1); reg.append((item, snip))
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
rep = ['# v8 -> v9 changed sentences\n']; bad = 0; used = set()
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal': continue
    old = A[i1:i2]; new = B[j1:j2]
    tags = set()
    for s in new + old:
        hit = [it for it, sn in reg if sn in s]
        tags.update(hit); used.update(hit)
    if not tags: bad += 1
    rep.append(f'## {op} [{", ".join(sorted(tags)) or "UNREGISTERED"}] ({b[j1][0] if j1 < len(b) else a[i1][0]})')
    for s in old: rep.append('- OLD: ' + s)
    for s in new: rep.append('+ NEW: ' + s)
    rep.append('')
unused = [it for it, _ in reg if it not in used]
rep.append(f'\nUnregistered change blocks: {bad}\nRegistered snippets never matched: {unused}')
open(H + '/DIFF_REPORT.md', 'w').write('\n'.join(rep))
print(f'change blocks: {sum(1 for o in sm.get_opcodes() if o[0] != "equal")}, unregistered: {bad}, unused registrations: {unused}')
sys.exit(1 if bad or unused else 0)
