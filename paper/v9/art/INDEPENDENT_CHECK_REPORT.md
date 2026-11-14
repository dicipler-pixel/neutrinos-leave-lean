# Independent check: v9 HTML vs art edition (r2)

**VERDICT: CHANGES FOUND** — but none to any word, number, equation, table, listing or figure geometry. Every character of
the paper's text is present once and identical; all 432 maths spans, 9 tables and 130 listings are byte-identical and in order;
all 11 figures are a pure per-colour recolour at the same pixel size. What did change is listed under Findings: one paragraph
sits in a different place, one caption's colour word no longer matches its recoloured figure, and seven contents-list entries
have faulty link markup. Everything else is presentation.

Files compared
- original: `out_v9/What_the_Neutrino_State_Must_Keep_v9_2026-11-13.html`
- art edition: `skin/What_the_Neutrino_State_Must_Keep_v9_art_r2_2026-11-13.html`

All scripts below are in this folder and were written for this check; the builder's `check_same_text.py` was not run or read.
Run as `python3 <script>` from this folder. Not tested: the page was not opened in a browser, so statements about how
something displays are read from the markup and stylesheet, not seen on screen. The embedded fonts' character coverage
could not be read (no Brotli module here), so that is untested too.

## Findings

1. **A paragraph moved (order change, wording identical).** The "AI-assisted. ..." paragraph came after the abstract in the
   v9 HTML; in the art edition it comes before the abstract, in the title panel. Its 336 characters are identical. (The .tex
   has it at line 19, straight after `\maketitle`.) This is the only difference in the reading order of the whole text.
2. **Fig. 4 caption is now wrong about colour.** It says "Black dots: McCormick's Gaussian runs" and "one weight fitted to
   the black dots". After the lightness flip those dots are cream-white (0,0,0 -> 237,237,237). No other caption is made wrong
   (table in check 6).
3. **Seven contents-list entries have a link inside a link** (B.19, B.20, B.21, B.22, B.23, B.24, B.27). Their headings
   contain a cross-reference link ("Section 7" etc.), and the heading markup was copied whole into the contents link. Nested
   links are invalid HTML: a browser ends the outer link where the inner one starts, so the entry is split, the section number
   becomes its own link to that other section, and (since contents links are styled `display:block`) it is likely to drop onto
   its own line. The words are all there; the fault is in the added contents list only. Not browser-tested.
4. **Figure recolour is not strictly reversible.** Forward it is a pure colour map (0 exceptions in 11 figures). In reverse,
   31 to 322 pairs of original colours per figure land on one new colour. Every merged pair was at most 2 levels (of 255)
   apart in the original, so nothing visibly distinct was merged. Cause: lightness is squeezed into 88% of its range.
5. **Things that look different with the same content** (for the author to know, not errors):
   - Byline is displayed in capitals (`text-transform:uppercase`); the text in the file is still "Jeromie Beasley". The
     painted title in the supplied cover had it in italic mixed case.
   - Body digits are set as old-style figures (`font-variant-numeric:oldstyle-nums`) outside tables and maths; same digits,
     different glyph shapes. v9 had no such rule.
   - "Abstract" is now a section heading (`<h1>`) in its own card; in v9 it was a label inside the title block.
   - Fig. 6: the bars use a dark-to-light colour scale (dark purple low, yellow high). Flipping lightness keeps each hue but
     makes the low bars pale (lilac, light blue) instead of dark, so the scale no longer runs dark to light. The caption does
     not rely on it.
   - Fig. 11: the two blues and the two red/oranges swap which is the lighter one (dark blue became light blue and the
     reverse). The in-figure legend was flipped with them, so it still matches.
   - Shaded bands sit close to the ground: Fig. 7 window (237,242,248)->(13,23,34) on (13,13,13); Fig. 5 band ->(16,38,56);
     Fig. 11 grey window (227,227,227)->(37,37,37). Still present and distinguishable in the files I viewed, but faint.
   - Leading/trailing blank lines differ at two joins (start of first section, end of body). No effect.
6. **Cover art: clean.** 13,602 pixels differ, all inside x 1243..1855, y 12..180; all 13,602 are the cream title/byline
   lettering and are now pure black; the other 1,586,398 pixels are identical. No art pixel is in or near the box (art starts
   at row 205).
7. **Scripts: clean.** MathJax tag byte-identical. One added script, which only sets `zoom`/`min-width` on equations too wide
   for their column; it writes no text.

---

## Check 1. Text

Why it would catch a change: visible text is extracted by an HTML parser (my own, not the builder's regexes), entities unescaped, whitespace collapsed; any added, dropped or altered character appears in the diff.

`python3 check1_text.py`

```python
import re,sys
B='<session>'
O=B+'/out_v9/What_the_Neutrino_State_Must_Keep_v9_2026-11-13.html'
A=B+'/skin/What_the_Neutrino_State_Must_Keep_v9_art_r2_2026-11-13.html'
def load(p): return open(p,encoding='utf-8',newline='').read()
def nodata(s): return re.sub(r'data:[a-z0-9/+\-]+;base64,[A-Za-z0-9+/=]+','DATA',s)
```
```python
# CHECK 1 (TEXT). Why it catches a change: the visible text of each page is pulled out by an HTML parser
# (not by the builder's regexes); any added, dropped or altered character shows up as a diff opcode.
import re, html, difflib, sys
from html.parser import HTMLParser
from strip import *
class T(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out=[]; s.skip=0; s.stack=[]; s.nav=[]; s.sub=[]; s.innav=0; s.insub=0
    def handle_starttag(s,tag,attrs):
        a=dict(attrs)
        if tag in('script','style'): s.skip+=1
        if tag in('br','img','hr','meta','link','input','col'):
            if tag=='img': s.out.append(' [IMG alt=%r] '%a.get('alt'))
            return
        s.stack.append(tag)
        if tag=='nav' and a.get('id')=='TOC': s.innav=len(s.stack)
        if tag=='p' and a.get('class')=='subtitle': s.insub=len(s.stack)
        s.out.append(' ' if tag in BLOCK else '')
    def handle_endtag(s,tag):
        if tag in('script','style'): s.skip-=1
        if tag in('br','img','hr','meta','link','input','col'): return
        assert s.stack and s.stack[-1]==tag,(tag,s.stack[-5:])
        if s.innav==len(s.stack): s.innav=0
        if s.insub==len(s.stack): s.insub=0
        s.stack.pop()
        if tag in BLOCK: s.out.append(' ')
    def handle_data(s,d):
        if s.skip: return
        if s.innav: s.nav.append(d)
        elif s.insub: s.sub.append(d)
        else: s.out.append(d)
BLOCK={'p','div','h1','h2','h3','h4','h5','li','ul','ol','table','tr','td','th','pre','figure','figcaption','section','header','nav','blockquote','caption','thead','tbody','dl','dt','dd','body','html','head','title'}
def col(x): return re.sub(r'\s+',' ',x).strip()
def body(s): return '<html>'+s[s.index('<body'):]
def ext(p):
    t=T(); t.feed(body(load(p))); t.close(); assert not t.stack,t.stack
    return col(''.join(t.out)), col(''.join(t.nav)), col(''.join(t.sub))
o,onav,osub=ext(O); a,anav,asub=ext(A)
print('orig visible chars',len(o),' art visible chars (nav+subtitle excluded)',len(a),' nav chars',len(anav),' subtitle:',repr(asub))
print('orig has nav/subtitle text:',repr(onav),repr(osub))
print('IDENTICAL as is:',o==a)
def fastdiff(x,y,label):
    # exact: trim common prefix/suffix, then diff the remaining middle word by word (character-exact inside words)
    n=min(len(x),len(y)); p=0
    while p<n and x[p]==y[p]: p+=1
    q=0
    while q<n-p and x[-1-q]==y[-1-q]: q+=1
    print(label,': common prefix',p,'chars, common suffix',q,'chars; differing middle: orig',len(x)-p-q,'art',len(y)-p-q)
    mx=x[p:len(x)-q].split(' '); my=y[p:len(y)-q].split(' ')
    if len(mx)*len(my)<4e8:
        for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,mx,my,autojunk=False).get_opcodes():
            if tag!='equal': print('   ',tag,'ORIG:',repr(' '.join(mx[i1:i2])[:400]),'| ART:',repr(' '.join(my[j1:j2])[:400]))
    print('    context before: %r'%x[max(0,p-80):p]); print('    context after: %r'%x[len(x)-q:len(x)-q+80])
fastdiff(o,a,'orig vs art (nav, subtitle excluded)')
# account for the rearrangement: split both into the same named pieces
ADVS='AI-assisted.'; 
io_=o.index(ADVS); ia=a.index(ADVS)
print('orig head (before advisory, first 200):',repr(o[:200]))
print('art  head (first 200):',repr(a[:200]))
# multiset / move check: remove advisory sentence from both and compare
m=re.search(r'AI-assisted\..*?not experiments\.',o); adv=m.group(0)
assert o.count(adv)==1 and a.count(adv)==1
o2=col(o.replace(adv,'')); a2=col(a.replace(adv,''))
print('advisory text identical in both, once each: True; len',len(adv))
print('after removing advisory from both: identical =',o2==a2, len(o2),len(a2))
if o2!=a2: fastdiff(o2,a2,'after removing advisory')
print('position of advisory: orig after', repr(o[max(0,io_-80):io_]),'| art after',repr(a[max(0,ia-80):ia]))
# subtitle vs tex
tex=open(B+'/nu6/paper_v9/neutrinos_v9.tex',encoding='utf-8').read()
tt=re.search(r'\\title\{(.*?)\}\n',tex,re.S).group(1); print('tex \\title:',repr(tt))
parts=[x.strip() for x in tt.split(r'\\')]; main=parts[0]; sub=' '.join(parts[1:]).replace('--','\u2013')
print('tex main title:',repr(main)); print('tex subtitle   :',repr(sub)); print('art subtitle   :',repr(asub)); print('SUBTITLE MATCH:',sub==asub, '| main title w/o colon == page h1:', main.rstrip(':')==a[:len(main)-1], repr(a[:len(main)-1]))
```
Output:
```
orig visible chars 429857  art visible chars (nav+subtitle excluded) 429857  nav chars 2457  subtitle: 'Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation'
orig has nav/subtitle text: '' ''
IDENTICAL as is: False
orig vs art (nav, subtitle excluded) : common prefix 108 chars, common suffix 423547 chars; differing middle: orig 6202 art 6202
    replace ORIG: 'bstract' | ART: 'I-assisted. The ideas and research direction are the author’s; AI tools (Claude, Anthropic) were used for literature search, computation, drafting and typesetting. The numbers come from the scripts, run logs and outputs printed in Appendix B. The simulations are runs of S. McCormick’s public code on a cloud computer, not experiments. Abstract'
    replace ORIG: 'rates. AI-assisted. The ideas and research direction are the author’s; AI tools (Claude, Anthropic) were used for literature search, computation, drafting and typesetting. The numbers come from the scripts, run logs and outputs printed in Appendix B. The simulations are runs of S. McCormick’s public code on a cloud computer, not experiment' | ART: 'rate'
    context before: ' Keep Jeromie Beasley 13 November 2026 (version 9 of When the Neutrinos Leave) A'
    context after: 's. The question Primordial black holes heavier than about \\(10^6\\,M_\\odot\\) form'
orig head (before advisory, first 200): 'What the Neutrino State Must Keep Jeromie Beasley 13 November 2026 (version 9 of When the Neutrinos Leave) Abstract McCormick has shown that neutrinos which stream freely out of a collapsing overdensi'
art  head (first 200): 'What the Neutrino State Must Keep Jeromie Beasley 13 November 2026 (version 9 of When the Neutrinos Leave) AI-assisted. The ideas and research direction are the author’s; AI tools (Claude, Anthropic) '
advisory text identical in both, once each: True; len 336
after removing advisory from both: identical = True 429520 429520
position of advisory: orig after ' are stated for the e\\(^\\pm\\) annihilation epoch and for the mean of the rates. ' | art after 't Keep Jeromie Beasley 13 November 2026 (version 9 of When the Neutrinos Leave) '
tex \title: 'What the Neutrino State Must Keep:\\\\ Hidden Angular Structure, the Flux--Shear Link\\\\ and the Threshold for Primordial Black Hole Formation'
tex main title: 'What the Neutrino State Must Keep:'
tex subtitle   : 'Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation'
art subtitle   : 'Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation'
SUBTITLE MATCH: True | main title w/o colon == page h1: True 'What the Neutrino State Must Keep'
```

Reading: 429,857 visible characters each (contents list and subtitle set aside). The only difference is the position of the
336-character advisory paragraph; with it removed from both, the two texts are identical character for character
(429,520 = 429,520). Subtitle equals the `\title` subtitle of the .tex with `--` as an en dash and the `\\` line breaks as
spaces. The page title is the .tex main title without its trailing colon — same as in v9.

### Check 1b. Contents list

Why: each entry's text is compared (with a parser) to the visible text of the heading its link points to, and the target id must exist exactly once.

`python3 check2b_toc.py`

```python
# CHECK 1b (CONTENTS LIST) with a real parser. Why: the regex check mis-split 7 entries whose headings contain a link;
# here each TOC <li>'s own text (excluding its sub-list) is compared with the visible text of the heading whose id it links to.
import re, collections
from html.parser import HTMLParser
from strip import *
o=load(O); a=load(A)
def nw(s): return re.sub(r'\s+',' ',s).strip()
class Heads(HTMLParser):
    def __init__(s): super().__init__(); s.h={}; s.cur=None; s.order=[]
    def handle_starttag(s,t,at):
        if re.fullmatch(r'h[1-6]',t) and s.cur is None:
            s.cur=[t,dict(at).get('id') or dict(at).get('class'),'']
    def handle_endtag(s,t):
        if s.cur and t==s.cur[0]: s.h[s.cur[1]]=(s.cur[0],nw(s.cur[2])); s.order.append(s.cur[1]); s.cur=None
    def handle_data(s,d):
        if s.cur: s.cur[2]+=d
ho=Heads(); ho.feed(re.sub(r'<pre\b.*?</pre>','',o[o.index('<body'):],flags=re.S))
navs=re.search(r'<nav id="TOC".*?</nav>',a,re.S).group(0)
class Toc(HTMLParser):
    def __init__(s): super().__init__(); s.items=[]; s.depth=0; s.stack=[]
    def handle_starttag(s,t,at):
        if t=='ul': s.depth+=1
        if t=='li': s.items.append([s.depth,None,'',[]]); s.stack.append(s.items[-1])
        if t=='a' and s.stack:
            h=dict(at).get('href'); s.stack[-1][3].append(h)
            if s.stack[-1][1] is None: s.stack[-1][1]=h
    def handle_endtag(s,t):
        if t=='ul': s.depth-=1
        if t=='li': s.stack.pop()
    def handle_data(s,d):
        if s.stack: s.stack[-1][2]+=d
tp=Toc(); tp.feed(navs)
ida=collections.Counter(re.findall(r'\bid="([^"]*)"',a))
bad=0; nested=[]
for d,h,x,hs in tp.items:
    i=h[1:]; x=nw(x)
    want='Abstract' if i=='abstract' else ho.h.get(i,(None,None))[1]
    ok=(x==want and ida[i]==1)
    if not ok: bad+=1; print('MISMATCH',d,i,repr(x),repr(want),ida[i])
    if len(hs)>1: nested.append((x,hs))
print('TOC entries',len(tp.items),'| depth1',sum(d==1 for d,*_ in tp.items),'depth2',sum(d==2 for d,*_ in tp.items),'| mismatches with heading text / id not unique:',bad)
lv=collections.Counter(v[0] for v in ho.h.values()); print('orig headings by level',dict(lv))
print('depth matches heading level:',all((d==1)==(i=='#abstract' or ho.h[i[1:]][0]=='h1') for d,i,*_ in tp.items))
print('TOC entries that contain a SECOND link inside the entry link (nested <a>, invalid HTML):',len(nested))
for x,hs in nested: print('   ',repr(x),hs)
```
Output:
```
TOC entries 61 | depth1 18 depth2 43 | mismatches with heading text / id not unique: 0
orig headings by level {'h1': 18, 'h4': 44, 'h2': 43}
depth matches heading level: True
TOC entries that contain a SECOND link inside the entry link (nested <a>, invalid HTML): 7
    'B.19 The stage-correct runner and the reconvergence of Section 7' ['#b.19-the-stage-correct-runner-and-the-reconvergence-of-section-seclink', '#sec:link']
    'B.20 Self-scattering as the flux–shear link: algebra and frozen prediction (Section 10)' ['#b.20-self-scattering-as-the-fluxshear-link-algebra-and-frozen-prediction-section-secmcc', '#sec:mcc']
    'B.21 The deciding run (Section 10)' ['#b.21-the-deciding-run-section-secmcc', '#sec:mcc']
    'B.22 The recorder in McCormick’s multigroup solver (Section 10)' ['#b.22-the-recorder-in-mccormicks-multigroup-solver-section-secmcc', '#sec:mcc']
    'B.23 The restart test (Section 9)' ['#b.23-the-restart-test-section-secdoor', '#sec:door']
    'B.24 The readout Gramian, the order swap and the closures (Section 8)' ['#b.24-the-readout-gramian-the-order-swap-and-the-closures-section-secgramian', '#sec:gramian']
    'B.27 The third resolution level (Section 7)' ['#b.27-the-third-resolution-level-section-seclink', '#sec:link']
```

## Check 2. Maths, tables, listings (and raw markup, ids, links: check 7)

Why: compared as raw bytes in document order, so one changed digit, sign or entity, or a dropped/duplicated/reordered block, breaks equality. Then the whole body is reduced by removing only the known wrapper strings and must equal the original markup byte for byte.

`python3 check2_blocks.py`

```python
# CHECK 2 (MATHS, TABLES, LISTINGS) and CHECK 7 (raw markup).
# Why it catches a change: maths/tables/listings are compared as raw bytes in document order, so a changed digit, sign,
# escaped entity or a swapped/dropped/duplicated block breaks equality. The raw-body comparison then removes ONLY the
# known wrapper strings and requires the remaining markup to be byte-identical to the original's.
import re, hashlib, collections
from strip import *
o=load(O); a=load(A)
ob=o[o.index('<body>'):]; ab=a[a.index('<body>'):]
def math(s): return re.findall(r'<span class="math [^"]*">.*?</span>',s,re.S)
for name,rx in [('math spans',None),('tables',r'<table\b.*?</table>'),('pre',r'<pre\b.*?</pre>'),('code',r'<code\b.*?</code>'),('figcaption',r'<figcaption\b.*?</figcaption>'),('blockquote',r'<blockquote\b.*?</blockquote>'),('ol/ul lists opening tags',r'<[ou]l\b[^>]*>'),('footnote refs',r'<a [^>]*footnote[^>]*>.*?</a>'),('citations',r'<span class="citation".*?</span>'),('h1-h6 (with ids)',r'<h[1-6]\b.*?</h[1-6]>')]:
    x=math(ob) if rx is None else re.findall(rx,ob,re.S); y=math(ab) if rx is None else re.findall(rx,ab,re.S)
    if name.startswith('ol/ul'):  # art adds the TOC lists
        nav=re.search(r'<nav id="TOC".*?</nav>',ab,re.S).group(0); y=re.findall(rx,ab.replace(nav,''),re.S)
    if name.startswith('h1'):
        print('  (headings: art header h1 and abstract h1 handled below)')
    print(f'{name:28s} orig {len(x):5d}  art {len(y):5d}  identical in order: {x==y}  sha1 orig {hashlib.sha1("".join(x).encode()).hexdigest()[:12]} art {hashlib.sha1("".join(y).encode()).hexdigest()[:12]}')
    if x!=y:
        sx=collections.Counter(x); sy=collections.Counter(y)
        print('    only orig:',[k[:200] for k in (sx-sy)]); print('    only art:',[k[:200] for k in (sy-sx)])
# any math span containing a nested span (would break the non-greedy regex)?
ms=math(ob); print('math spans containing "<span" inside:',sum('<span' in m[10:] for m in ms),'; inline',sum('math inline' in m[:30] for m in ms),'display',sum('math display' in m[:30] for m in ms))
print('count of "\\\\(" orig/art', ob.count('\\('),ab.count('\\('),' "\\\\[" ',ob.count('\\['),ab.count('\\['),' "$" ',ob.count('$'),ab.count('$'))

# ---- raw body reduction ----
IMG=r'(<img src=")data:image/png;base64,[^"]+(")'
on=re.sub(IMG,r'\1IMG\2',ob); an=re.sub(IMG,r'\1IMG\2',ab)
print('img tags orig',len(re.findall(r'<img\b[^>]*>',on)),'art',len(re.findall(r'<img\b[^>]*>',an)),' img tags (data stripped) identical:',re.findall(r'<img\b[^>]*>',on)==re.findall(r'<img\b[^>]*>',an))
# art: take apart using only literal wrappers
nav=re.search(r'<nav id="TOC" role="doc-toc">.*?</nav>\n',an,re.S); an2=an.replace(nav.group(0),'')
print('art section wrappers: open',an2.count('<section class="level1"'),'close',an2.count('</section>'),'; orig has <section>:',on.count('<section'))
print('ART body up to first section:\n'+an2[:an2.index('<section')])
print('ORIG body header (non-abstract part):\n'+on[:on.index('<div class="abstract">')])
# rebuild the original's order from the art pieces
m=re.search(r'<section class="level1" id="abstract">\n<h1>(.*?)</h1>(.*?)\n</section>\n',an2,re.S)
abs_title,abs_body=m.group(1),m.group(2)
adv=re.search(r'<p><em>AI-assisted\..*?</em></p>',an2[:m.start()],re.S).group(0)
rest=an2[m.end():]
assert rest.endswith('\n</body>\n</html>\n')
secs=rest[:-len('\n</body>\n</html>\n')]
n_open=secs.count('<section class="level1">\n'); n_close=secs.count('\n</section>')
secs=secs.replace('<section class="level1">\n','').replace('\n</section>','')
print('level-1 section wrappers removed:',n_open,n_close)
# original pieces
oh=re.search(r'<header id="title-block-header">(.*?)</header>',on,re.S)
oabs=re.search(r'<div class="abstract">\s*<div class="abstract-title">(.*?)</div>(.*)</div>\s*$',oh.group(1),re.S)
orest=on[oh.end():]; oadv=re.search(r'\s*(<p><em>AI-assisted\..*?</em></p>)',orest,re.S); orest2=orest[oadv.end():]
assert orest2.rstrip().endswith('</body>\n</html>')
orest2=orest2[:orest2.rindex('</body>')]
def nw(s): return re.sub(r'\s+',' ',s).strip()
print('abstract title  identical:',abs_title==oabs.group(1),repr(abs_title))
print('abstract body   byte-identical:',abs_body==oabs.group(2).rstrip(), len(abs_body))
print('advisory        byte-identical:',adv==oadv.group(1), len(adv))
print('rest of paper   byte-identical (exact):',secs==orest2,'| modulo whitespace:',nw(secs)==nw(orest2),len(secs),len(orest2))
if secs!=orest2:
    import difflib
    x=orest2.split('\n'); y=secs.split('\n'); k=0
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,x,y,autojunk=False).get_opcodes():
        if tag!='equal':
            k+=1
            if k<=30: print('   ',tag,i1,i2,j1,j2,repr('\n'.join(x[i1:i2])[:200]),'|',repr('\n'.join(y[j1:j2])[:200]))
    print('   differing line-groups:',k)
# title/author/date
for tag in ['<p class="author">(.*?)</p>','<p class="date">(.*?)</p>','<h1 class="title">(.*?)</h1>']:
    x=re.findall(tag,on,re.S); y=re.findall(tag,an2,re.S); print(tag,'| orig',x,'| art',y)
# ---- ids, links ----
def ids(s): return re.findall(r'\bid="([^"]*)"',s)
oi=ids(on); ai=ids(an)
ci=collections.Counter(ai); print('ids orig',len(oi),'art',len(ai),'| new in art:',sorted(set(ai)-set(oi)),'| lost:',sorted(set(oi)-set(ai)),'| duplicated ids in art:',[k for k,v in ci.items() if v>1],'| dup in orig:',[k for k,v in collections.Counter(oi).items() if v>1])
print('ids same order (ignoring added):',[i for i in ai if i in set(oi)]==oi)
oh_=re.findall(r'<a\b[^>]*>',on); ah_=re.findall(r'<a\b[^>]*>',an2)
print('<a> tags orig',len(oh_),'art (TOC excluded)',len(ah_),'identical in order:',oh_==ah_)
hre=re.findall(r'href="#([^"]*)"',an); print('internal links in art:',len(hre),'targets missing:',sorted({h for h in hre if ci[h]!=1}))
hro=re.findall(r'href="#([^"]*)"',on); print('internal links in orig:',len(hro),'targets missing in orig:',sorted({h for h in hro if collections.Counter(oi)[h]!=1}))
print('external hrefs identical:',re.findall(r'href="(?!#)([^"]*)"',on)==re.findall(r'href="(?!#)([^"]*)"',an2),len(re.findall(r'href="(?!#)([^"]*)"',on)))
# entities
ent=lambda s: collections.Counter(re.findall(r'&[#\w]+;',s))
print('entity counts identical outside nav:',ent(on)==ent(an2),'| diff:',(ent(an2)-ent(on)),(ent(on)-ent(an2)))
print('tag histogram difference (art minus orig, TOC excluded):',dict(collections.Counter(re.findall(r'<(/?\w+)',an2))-collections.Counter(re.findall(r'<(/?\w+)',on))),'| orig minus art:',dict(collections.Counter(re.findall(r'<(/?\w+)',on))-collections.Counter(re.findall(r'<(/?\w+)',an2))))
# ---- TOC ----
import html as H
print('--- TOC ---')
navs=nav.group(0); ents=re.findall(r'<li><a href="#([^"]+)">(.*?)</a>',navs,re.S)
heads=[(int(l),i,x) for l,i,x in re.findall(r'<h([1-6])[^>]*?\bid="([^"]+)"[^>]*>(.*?)</h\1>',on,re.S)]
hd={i:(l,x) for l,i,x in heads}
bad=0
for i,x in ents:
    if i=='abstract':
        ok=(x==oabs.group(1)) and ci[i]==1
    else: ok=(i in hd and hd[i][1]==x and ci[i]==1)
    if not ok: bad+=1; print('  BAD TOC ENTRY',i,repr(x),hd.get(i))
print('TOC entries',len(ents),'bad',bad,'| every entry text is byte-equal to the heading with that id, id unique in art')
h12=[i for l,i,x in heads if l<=2]
print('h1/h2 headings in orig:',len(h12),'| TOC order == document order of h1/h2:',[i for i,_ in ents][1:]==h12, '| h1/h2 missing from TOC:',[i for i in h12 if i not in dict(ents)])
print('heading level counts orig:',collections.Counter(l for l,_,_ in heads))
print('nav text other than entries:',repr(nw(re.sub(r'<li><a href="#[^"]+">.*?</a>','',navs,flags=re.S))))
print('headings without id in orig:',len(re.findall(r'<h[1-6]\b(?![^>]*\bid=)[^>]*>',on)))
```
Output (the 7 "BAD TOC ENTRY" lines are this script's regex stopping at the inner link; they are what exposed finding 3, and check 1b with a parser shows the entry texts are right):
```
math spans                   orig   432  art   432  identical in order: True  sha1 orig 280120b685a6 art 280120b685a6
tables                       orig     9  art     9  identical in order: True  sha1 orig 9c244da13e05 art 9c244da13e05
pre                          orig   130  art   130  identical in order: True  sha1 orig 0d0640d3be6f art 0d0640d3be6f
code                         orig   199  art   199  identical in order: True  sha1 orig f7d85b2ecf16 art f7d85b2ecf16
figcaption                   orig    11  art    11  identical in order: True  sha1 orig 0d5d71783e26 art 0d5d71783e26
blockquote                   orig     0  art     0  identical in order: True  sha1 orig da39a3ee5e6b art da39a3ee5e6b
ol/ul lists opening tags     orig     3  art     3  identical in order: True  sha1 orig c9139005b385 art c9139005b385
footnote refs                orig     0  art     0  identical in order: True  sha1 orig da39a3ee5e6b art da39a3ee5e6b
citations                    orig     0  art     0  identical in order: True  sha1 orig da39a3ee5e6b art da39a3ee5e6b
  (headings: art header h1 and abstract h1 handled below)
h1-h6 (with ids)             orig   105  art   106  identical in order: False  sha1 orig bd758edca19f art c44896e63c86
    only orig: ['<h1 class="title">What the Neutrino State Must Keep</h1>']
    only art: ['<h1 class="title"><span class="t-line">What the Neutrino State</span> <span class="t-line">Must Keep</span></h1>', '<h1>Abstract</h1>']
math spans containing "<span" inside: 0 ; inline 426 display 6
count of "\\(" orig/art 1528 1528  "\\["  27 27  "$"  157 157
img tags orig 11 art 11  img tags (data stripped) identical: True
art section wrappers: open 18 close 18 ; orig has <section>: 0
ART body up to first section:
<body>
<div id="bgart" aria-hidden="true"></div>
<header id="title-block-header" class="hero">
<div class="hero-art" aria-hidden="true"></div>
<div class="hero-text">
<h1 class="title"><span class="t-line">What the Neutrino State</span> <span class="t-line">Must Keep</span></h1>
<div class="rule" aria-hidden="true"></div>
<p class="author">Jeromie Beasley</p>
</div>
</header>
<div class="titlemeta">
<p class="subtitle">Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation</p>
<p class="date">13 November 2026 (version 9 of <em>When the Neutrinos
Leave</em>)</p>
<p><em>AI-assisted. The ideas and research direction are the author’s;
AI tools (Claude, Anthropic) were used for literature search,
computation, drafting and typesetting. The numbers come from the
scripts, run logs and outputs printed in Appendix B. The simulations are
runs of S. McCormick’s public code on a cloud computer, not
experiments.</em></p>
</div>

ORIG body header (non-abstract part):
<body>
<header id="title-block-header">
<h1 class="title">What the Neutrino State Must Keep</h1>
<p class="author">Jeromie Beasley</p>
<p class="date">13 November 2026 (version 9 of <em>When the Neutrinos
Leave</em>)</p>

level-1 section wrappers removed: 17 17
abstract title  identical: True 'Abstract'
abstract body   byte-identical: True 7883
advisory        byte-identical: True 352
rest of paper   byte-identical (exact): False | modulo whitespace: True 540144 540146
    delete 0 1 0 0 '' | ''
    delete 8485 8486 8484 8484 '' | ''
   differing line-groups: 2
<p class="author">(.*?)</p> | orig ['Jeromie Beasley'] | art ['Jeromie Beasley']
<p class="date">(.*?)</p> | orig ['13 November 2026 (version 9 of <em>When the Neutrinos\nLeave</em>)'] | art ['13 November 2026 (version 9 of <em>When the Neutrinos\nLeave</em>)']
<h1 class="title">(.*?)</h1> | orig ['What the Neutrino State Must Keep'] | art ['<span class="t-line">What the Neutrino State</span> <span class="t-line">Must Keep</span>']
ids orig 116 art 119 | new in art: ['TOC', 'abstract', 'bgart'] | lost: [] | duplicated ids in art: [] | dup in orig: []
ids same order (ignoring added): True
<a> tags orig 65 art (TOC excluded) 65 identical in order: True
internal links in art: 132 targets missing: []
internal links in orig: 64 targets missing in orig: []
external hrefs identical: True 1
entity counts identical outside nav: True | diff: Counter() Counter()
tag histogram difference (art minus orig, TOC excluded): {'div': 3, '/div': 3, 'h1': 1, 'span': 2, '/span': 2, '/h1': 1, 'p': 1, '/p': 1, 'section': 18, '/section': 18} | orig minus art: {}
--- TOC ---
  BAD TOC ENTRY b.19-the-stage-correct-runner-and-the-reconvergence-of-section-seclink 'B.19\nThe stage-correct runner and the reconvergence of Section\xa0<a\nhref="#sec:link" data-reference-type="ref"\ndata-reference="sec:link">7' (2, 'B.19\nThe stage-correct runner and the reconvergence of Section\xa0<a\nhref="#sec:link" data-reference-type="ref"\ndata-reference="sec:link">7</a>')
  BAD TOC ENTRY b.20-self-scattering-as-the-fluxshear-link-algebra-and-frozen-prediction-section-secmcc 'B.20\nSelf-scattering as the flux–shear link: algebra and frozen prediction\n(Section\xa0<a href="#sec:mcc" data-reference-type="ref"\ndata-reference="sec:mcc">10' (2, 'B.20\nSelf-scattering as the flux–shear link: algebra and frozen prediction\n(Section\xa0<a href="#sec:mcc" data-reference-type="ref"\ndata-reference="sec:mcc">10</a>)')
  BAD TOC ENTRY b.21-the-deciding-run-section-secmcc 'B.21\nThe deciding run (Section\xa0<a href="#sec:mcc" data-reference-type="ref"\ndata-reference="sec:mcc">10' (2, 'B.21\nThe deciding run (Section\xa0<a href="#sec:mcc" data-reference-type="ref"\ndata-reference="sec:mcc">10</a>)')
  BAD TOC ENTRY b.22-the-recorder-in-mccormicks-multigroup-solver-section-secmcc 'B.22\nThe recorder in McCormick’s multigroup solver (Section\xa0<a\nhref="#sec:mcc" data-reference-type="ref"\ndata-reference="sec:mcc">10' (2, 'B.22\nThe recorder in McCormick’s multigroup solver (Section\xa0<a\nhref="#sec:mcc" data-reference-type="ref"\ndata-reference="sec:mcc">10</a>)')
  BAD TOC ENTRY b.23-the-restart-test-section-secdoor 'B.23\nThe restart test (Section\xa0<a href="#sec:door" data-reference-type="ref"\ndata-reference="sec:door">9' (2, 'B.23\nThe restart test (Section\xa0<a href="#sec:door" data-reference-type="ref"\ndata-reference="sec:door">9</a>)')
  BAD TOC ENTRY b.24-the-readout-gramian-the-order-swap-and-the-closures-section-secgramian 'B.24\nThe readout Gramian, the order swap and the closures (Section\xa0<a\nhref="#sec:gramian" data-reference-type="ref"\ndata-reference="sec:gramian">8' (2, 'B.24\nThe readout Gramian, the order swap and the closures (Section\xa0<a\nhref="#sec:gramian" data-reference-type="ref"\ndata-reference="sec:gramian">8</a>)')
  BAD TOC ENTRY b.27-the-third-resolution-level-section-seclink 'B.27 The third\nresolution level (Section\xa0<a href="#sec:link" data-reference-type="ref"\ndata-reference="sec:link">7' (2, 'B.27 The third\nresolution level (Section\xa0<a href="#sec:link" data-reference-type="ref"\ndata-reference="sec:link">7</a>)')
TOC entries 61 bad 7 | every entry text is byte-equal to the heading with that id, id unique in art
h1/h2 headings in orig: 60 | TOC order == document order of h1/h2: True | h1/h2 missing from TOC: []
heading level counts orig: Counter({4: 44, 2: 43, 1: 17})
nav text other than entries: '<nav id="TOC" role="doc-toc"> <ul> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> <ul> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </ul></li> <ul> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </li> </a></li> )</a></li> )</a></li> )</a></li> )</a></li> )</a></li> </li> </li> )</a></li> </ul></li> </li> </ul> </nav>'
headings without id in orig: 1
```

Reading: 432 maths spans (426 inline, 6 display), 9 tables, 130 `<pre>`, 199 `<code>`, 11 figcaptions: identical, same order.
Abstract body, advisory and the whole rest of the paper are byte-identical apart from two blank lines at the joins.
116 original ids all present, same order, none duplicated; 3 added (`TOC`, `abstract`, `bgart`). 65 original links identical;
all 132 internal links in the art edition resolve to exactly one id. Entity counts identical. Added tags: 18 section wrappers,
3 divs, 2 spans (title line split), 1 h1 (Abstract), 1 p (subtitle). The paper has no footnotes; the reference list is inside
the byte-identical remainder.

## Check 3. Figures

Why: if anything were moved, redrawn, resized, blurred or relabelled, some original colour would land on two different new colours. A pure recolour gives one new colour per original colour. The reverse count shows merges. Lightness and hue are re-derived with Python's `colorsys`, not the builder's code.

`python3 check3_figs.py`

```python
# CHECK 3 (FIGURES). Why it catches a change: if anything was moved, redrawn, resized, blurred, relabelled or recompressed,
# then some original colour would land on two different new colours somewhere (the pixel->pixel map stops being a function of
# colour alone). A pure recolour gives exactly one new colour per original colour. The reverse count shows whether distinct
# colours were merged (information lost). Independently I also re-derive lightness/hue with python's colorsys (not darkfig.py).
import re, io, base64, colorsys, numpy as np
from PIL import Image
from strip import *
o=load(O); a=load(A)
RX=r'<img src="data:image/png;base64,([^"]+)"'
fo=re.findall(RX,o); fa=re.findall(RX,a); print('embedded PNGs: orig',len(fo),'art',len(fa))
def key(x): x=x.astype(np.uint32); return (x[...,0]<<16)|(x[...,1]<<8)|x[...,2]
tot_multi=0
for n,(bo,ba) in enumerate(zip(fo,fa),1):
    io_=Image.open(io.BytesIO(base64.b64decode(bo))); ia=Image.open(io.BytesIO(base64.b64decode(ba)))
    info=f'fig {n}: orig {io_.size} mode {io_.mode} | art {ia.size} mode {ia.mode}'
    alpha=''
    if io_.mode in('RGBA','LA','P'):
        al=np.array(io_.convert('RGBA'))[...,3]; alpha=f' | orig alpha min {al.min()} (pixels not opaque: {(al<255).sum()})'
    x=np.array(io_.convert('RGB')); y=np.array(ia.convert('RGB'))
    print(info+alpha, '| same size:',x.shape==y.shape)
    kx=key(x).ravel(); ky=key(y).ravel()
    pairs=np.unique(np.stack([kx,ky],1),axis=0)
    uo,co=np.unique(pairs[:,0],return_counts=True); ua,ca=np.unique(pairs[:,1],return_counts=True)
    multi=(co>1).sum(); tot_multi+=multi
    print(f'   distinct colours: orig {len(uo)}, art {len(ua)}; distinct (orig,new) pairs {len(pairs)}')
    print(f'   FORWARD single-valued: original colours sent to >1 new colour = {multi}')
    # reverse merges
    merged=ua[ca>1]; nm=0; worst=0; worstex=None; lost=len(uo)-len(ua)
    order=np.argsort(pairs[:,1],kind='stable'); ps=pairs[order]
    idx=np.flatnonzero(np.r_[True,ps[1:,1]!=ps[:-1,1],True])
    cnt=np.bincount(kx,minlength=1<<24) if False else None
    for s,e in zip(idx[:-1],idx[1:]):
        if e-s>1:
            g=ps[s:e,0]; rgb=np.stack([(g>>16)&255,(g>>8)&255,g&255],1).astype(int)
            d=(rgb.max(0)-rgb.min(0)).max(); nm+=1
            if d>worst: worst=d; worstex=(rgb.tolist()[:6],[(int(ps[s,1])>>16)&255,(int(ps[s,1])>>8)&255,int(ps[s,1])&255])
    print(f'   REVERSE: new colours that receive >1 original colour = {nm} (original colours lost by merging = {lost}); widest spread inside one merged group = {worst} levels (per channel){" e.g. "+str(worstex) if worstex else ""}')
    # pixel share affected by merges
    if nm:
        ma=np.isin(ky,merged); print(f'   pixels whose colour is in a merged group: {ma.mean()*100:.2f}%')
    # independent hue / lightness check via colorsys on the colour table
    def rgbk(k): return ((k>>16)&255,(k>>8)&255,k&255)
    mh=0; mhex=None; lerr=0; serr=0; nsat=0
    for ko,ka in pairs:
        r,g,b=rgbk(int(ko)); R,G,B_=rgbk(int(ka))
        h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255); H,L,S=colorsys.rgb_to_hls(R/255,G/255,B_/255)
        lerr=max(lerr,abs(L-(0.05+(1-l)*0.88)))
        if s>0.25 and 0.15<l<0.85 and (max(r,g,b)-min(r,g,b))>=40:
            nsat+=1; dh=abs(h-H); dh=min(dh,1-dh)*360
            if dh>mh: mh=dh; mhex=((r,g,b),(R,G,B_))
    print(f'   lightness: max |L_new - (0.05+0.88(1-L_old))| = {lerr:.4f} (i.e. {lerr*255:.2f} levels); hue shift over {nsat} saturated colours (chroma>=40/255): max {mh:.2f} deg {mhex}')
    # monotone lightness order preserved among greys?
    gr=[(rgbk(int(ko)),rgbk(int(ka))) for ko,ka in pairs if len(set(rgbk(int(ko))))==1]
    gr.sort(); mono=all(gr[i][1][0]>=gr[i+1][1][0] for i in range(len(gr)-1)); neutral=all(max(v)-min(v)<=0 for _,v in gr)
    print(f'   greys: {len(gr)} levels; stay neutral grey: {neutral}; order strictly reversed (monotone): {mono}; white {gr[-1][0]}->{gr[-1][1]}, darkest {gr[0][0]}->{gr[0][1]}')
    # geometry: edge maps coincide? compare binarised "ink" masks
    inko=(x.astype(int).sum(-1)<735); inka=(np.abs(y.astype(int)-np.array(gr[-1][1])).sum(-1)>0) if gr[-1][0]==(255,255,255) else None
    if inka is not None: print(f'   non-background mask (orig not white vs art not ground): identical = {np.array_equal((kx!=0xFFFFFF),(ky!=key(np.array(gr[-1][1],dtype=np.uint8)[None,None])[0,0]))}')
print('TOTAL original colours mapped to more than one new colour, all figures:',tot_multi)
```
Output:
```
embedded PNGs: orig 11 art 11
fig 1: orig (1584, 572) mode RGBA | art (1584, 572) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 1545, art 1476; distinct (orig,new) pairs 1545
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 69 (original colours lost by merging = 69); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 0.44%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 903 saturated colours (chroma>=40/255): max 1.01 deg ((236, 196, 191), (76, 28, 23))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 2: orig (2000, 760) mode RGBA | art (2000, 760) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 850, art 811; distinct (orig,new) pairs 850
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 39 (original colours lost by merging = 39); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 1.19%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 331 saturated colours (chroma>=40/255): max 0.87 deg ((211, 197, 169), (93, 77, 47))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 3: orig (1584, 792) mode RGBA | art (1584, 792) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 504, art 464; distinct (orig,new) pairs 504
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 40 (original colours lost by merging = 40); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 0.35%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 183 saturated colours (chroma>=40/255): max 1.01 deg ((236, 196, 191), (76, 28, 23))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 4: orig (2340, 1380) mode RGBA | art (2340, 1380) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 1244, art 1201; distinct (orig,new) pairs 1244
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 43 (original colours lost by merging = 43); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 0.49%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 690 saturated colours (chroma>=40/255): max 0.87 deg ((174, 205, 222), (36, 71, 89))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 5: orig (3150, 1140) mode RGBA | art (3150, 1140) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 314, art 283; distinct (orig,new) pairs 314
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 31 (original colours lost by merging = 31); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 0.30%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 10 saturated colours (chroma>=40/255): max 0.56 deg ((124, 96, 32), (220, 188, 118))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 6: orig (3600, 1560) mode RGBA | art (3600, 1560) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 10882, art 10560; distinct (orig,new) pairs 10882
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 322 (original colours lost by merging = 322); widest spread inside one merged group = 2 levels (per channel) e.g. ([[102, 160, 53], [104, 161, 54]], [139, 199, 87])
   pixels whose colour is in a merged group: 3.63%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 6430 saturated colours (chroma>=40/255): max 1.21 deg ((70, 94, 53), (169, 195, 149))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 7: orig (1760, 688) mode RGBA | art (1760, 688) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 919, art 878; distinct (orig,new) pairs 919
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 41 (original colours lost by merging = 41); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 3.72%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 384 saturated colours (chroma>=40/255): max 0.73 deg ((172, 195, 221), (37, 63, 91))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 8: orig (2100, 700) mode RGBA | art (2100, 700) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 306, art 273; distinct (orig,new) pairs 306
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 33 (original colours lost by merging = 33); widest spread inside one merged group = 1 levels (per channel) e.g. ([[252, 252, 252], [253, 253, 253]], [15, 15, 15])
   pixels whose colour is in a merged group: 0.84%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 27 saturated colours (chroma>=40/255): max 0.83 deg ((187, 218, 230), (29, 65, 78))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 9: orig (2100, 740) mode RGBA | art (2100, 740) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 579, art 541; distinct (orig,new) pairs 579
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 37 (original colours lost by merging = 38); widest spread inside one merged group = 2 levels (per channel) e.g. ([[210, 207, 203], [211, 209, 204]], [59, 56, 51])
   pixels whose colour is in a merged group: 0.80%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 57 saturated colours (chroma>=40/255): max 0.71 deg ((144, 190, 199), (58, 105, 115))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 10: orig (1920, 640) mode RGBA | art (1920, 640) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 821, art 779; distinct (orig,new) pairs 821
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 42 (original colours lost by merging = 42); widest spread inside one merged group = 2 levels (per channel) e.g. ([[198, 113, 82], [199, 115, 83]], [171, 87, 56])
   pixels whose colour is in a merged group: 0.88%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 394 saturated colours (chroma>=40/255): max 0.63 deg ((239, 223, 185), (82, 64, 19))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
fig 11: orig (1650, 935) mode RGBA | art (1650, 935) mode RGB | orig alpha min 255 (pixels not opaque: 0) | same size: True
   distinct colours: orig 12524, art 12303; distinct (orig,new) pairs 12524
   FORWARD single-valued: original colours sent to >1 new colour = 0
   REVERSE: new colours that receive >1 original colour = 221 (original colours lost by merging = 221); widest spread inside one merged group = 2 levels (per channel) e.g. ([[213, 184, 133], [214, 186, 134]], [126, 96, 43])
   pixels whose colour is in a merged group: 1.87%
   lightness: max |L_new - (0.05+0.88(1-L_old))| = 0.0019 (i.e. 0.49 levels); hue shift over 7565 saturated colours (chroma>=40/255): max 1.20 deg ((216, 215, 175), (88, 86, 43))
   greys: 256 levels; stay neutral grey: True; order strictly reversed (monotone): True; white (255, 255, 255)->(13, 13, 13), darkest (0, 0, 0)->(237, 237, 237)
   non-background mask (orig not white vs art not ground): identical = True
TOTAL original colours mapped to more than one new colour, all figures: 0
```

Reading: all 11 same size; originals are RGBA with every pixel opaque, so dropping alpha lost nothing. Forward map
single-valued in every figure (0 exceptions). Merges: 31-322 per figure, widest 2 levels, touching 0.3-3.7% of pixels.
Hue shift for saturated colours at most 1.21 degrees. Lightness follows L' = 0.05 + 0.88(1 - L) to within half a level.
Greys stay neutral and their order is reversed without crossing. White -> (13,13,13); black -> (237,237,237).
(The "order strictly reversed" label in the output is a non-strict test: equal neighbours, i.e. the merges, are allowed.)

## Check 4. Cover art

Why: the image actually embedded in the stylesheet is decoded and compared pixel by pixel with the supplied file; the bounding box of all differences is reported, so a crop, resize, recompression or colour shift anywhere would show.

`python3 check4_cover.py` then `python3 check4b_cover.py`

```python
# CHECK 4 (COVER ART). Why it catches a change: the image actually embedded in the stylesheet is decoded and compared pixel
# for pixel with the supplied file; the bounding box of ALL differing pixels is reported, so any touch outside the title
# area (crop, resize, recompression, colour shift) is visible. Inside the box, the supplied image is examined to see whether
# anything other than title lettering on pure black was there.
import re, io, base64, numpy as np
from PIL import Image
from strip import *
a=load(A)
css=re.search(r'<style>(.*?)</style>',a,re.S).group(1)
urls=re.findall(r'url\((data:image/(\w+);base64,([A-Za-z0-9+/=]+))\)',css)
print('data-URL images in stylesheet:',[(u[1],len(u[2])) for u in urls],'| --art uses:',re.search(r'--art:url\(data:image/(\w+)',css).group(1))
print('other data: URLs in stylesheet (fonts etc.):',collections.Counter(re.findall(r'url\(data:([\w/+\-]+)',css)) if (collections:=__import__('collections')) else 0)
raw=base64.b64decode(urls[0][2]); open('art_embedded.'+urls[0][1],'wb').write(raw)
e=Image.open(io.BytesIO(raw)); s=Image.open('<attachments>/ec8c2235-image.png')
print('embedded:',e.format,e.size,e.mode,'| supplied:',s.format,s.size,s.mode)
if s.mode in('RGBA','LA','P'): al=np.array(s.convert('RGBA'))[...,3]; print('supplied alpha min',al.min())
if e.mode in('RGBA','LA','P'): al=np.array(e.convert('RGBA'))[...,3]; print('embedded alpha min',al.min())
E_=np.array(e.convert('RGB')).astype(int); S=np.array(s.convert('RGB')).astype(int)
d=(E_!=S).any(-1); ys,xs=np.nonzero(d)
print('differing pixels:',d.sum(),'of',d.size)
x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
print(f'bounding box of differences: x {x0}..{x1}, y {y0}..{y1} (inclusive)  = {x1-x0+1} x {y1-y0+1} px')
out=d.copy(); out[y0:y1+1,x0:x1+1]=False; print('differing pixels outside that box:',out.sum(),'(by construction 0); pixels outside box identical:',np.array_equal(np.where(d[...,None],0,E_),np.where(d[...,None],0,S)))
box_e=E_[y0:y1+1,x0:x1+1]; box_s=S[y0:y1+1,x0:x1+1]
print('embedded image inside box: max channel value',box_e.max(),'-> pure black:',box_e.max()==0, '| distinct colours',len(np.unique(box_e.reshape(-1,3),axis=0)))
# was there a larger cleared rectangle? find maximal all-black rectangle region in embedded around the box
print('supplied image inside box: pixels pure black',(box_s.max(-1)==0).sum(),'| non-black',(box_s.max(-1)>0).sum(),'| max',box_s.max())
# characterise the non-black pixels in the supplied box: colour statistics (title glyphs should be near-neutral cream/white anti-aliased; art would be saturated/blue/gold structure)
nb=box_s[box_s.max(-1)>0]; sat=nb.max(-1)-nb.min(-1)
print('  non-black pixels: brightness percentiles',np.percentile(nb.max(-1),[1,25,50,75,99]).tolist(),'| chroma (max-min) percentiles',np.percentile(sat,[50,90,99,100]).tolist())
print('  mean colour of bright (>150) pixels',nb[nb.max(-1)>150].mean(0).round(1).tolist() if (nb.max(-1)>150).any() else None)
# margin: is there a pure-black moat around the box in the supplied image (art not touching)?
for m in (1,2,5,10,20,40):
    Y0,Y1,X0,X1=max(0,y0-m),min(S.shape[0],y1+1+m),max(0,x0-m),min(S.shape[1],x1+1+m)
    ring=S[Y0:Y1,X0:X1].max(-1).copy(); ring[y0-Y0:y1+1-Y0,x0-X0:x1+1-X0]=0
    print(f'  ring of {m}px around box in supplied image: max value {ring.max()}, non-black pixels {(ring>0).sum()}')
# row/column profile of non-black content in supplied box, to show it is lines of lettering
m_=box_s.max(-1)>24; rows=m_.any(1); cols=m_.any(0)
def runs(v):
    r=[];st=None
    for i,t in enumerate(v):
        if t and st is None: st=i
        if not t and st is not None: r.append((st,i-1)); st=None
    if st is not None: r.append((st,len(v)-1))
    return r
print('  rows containing lettering (y, absolute):',[(y0+p,y0+q) for p,q in runs(rows)])
cr=runs(cols); print('  column runs:',len(cr),'x from',x0+cr[0][0],'to',x0+cr[-1][1],'; widest gap between runs',max([b[0]-a_[1] for a_,b in zip(cr,cr[1:])] or [0]))
# connected components in the supplied box touching the box edge would mean art crossing into it
edge=np.r_[m_[0],m_[-1],m_[:,0],m_[:,-1]]; print('  non-black (>24) pixels on the box border:',edge.sum())
# save crops for viewing
Image.fromarray(S[max(0,y0-30):y1+31,max(0,x0-30):x1+31].astype(np.uint8)).save('crop_supplied.png')
Image.fromarray(E_[max(0,y0-30):y1+31,max(0,x0-30):x1+31].astype(np.uint8)).save('crop_embedded.png')
Image.fromarray((d*255).astype(np.uint8)).resize((1000,400)).save('diffmask.png')
Image.fromarray(E_.astype(np.uint8)).resize((1000,400)).save('embedded_small.png')
# does the hero-text CSS box cover the cleared area? .hero-text{left:55%;width:45%;top:0;height:25.6%}
print('CSS hero-text box in image px: x',0.55*2000,'..2000, y 0..',0.256*800)
```
Output:
```
data-URL images in stylesheet: [('webp', 1562124)] | --art uses: webp
other data: URLs in stylesheet (fonts etc.): Counter({'font/woff2': 6, 'image/webp': 1})
embedded: WEBP (2000, 800) RGB | supplied: PNG (2000, 800) RGB
differing pixels: 13602 of 1600000
bounding box of differences: x 1243..1855, y 12..180 (inclusive)  = 613 x 169 px
differing pixels outside that box: 0 (by construction 0); pixels outside box identical: True
embedded image inside box: max channel value 0 -> pure black: True | distinct colours 1
supplied image inside box: pixels pure black 89995 | non-black 13602 | max 243
  non-black pixels: brightness percentiles [2.0, 128.0, 243.0, 243.0, 243.0] | chroma (max-min) percentiles [27.0, 27.0, 27.0, 27.0]
  mean colour of bright (>150) pixels [231.5, 222.9, 205.8]
  ring of 1px around box in supplied image: max value 0, non-black pixels 0
  ring of 2px around box in supplied image: max value 0, non-black pixels 0
  ring of 5px around box in supplied image: max value 0, non-black pixels 0
  ring of 10px around box in supplied image: max value 0, non-black pixels 0
  ring of 20px around box in supplied image: max value 0, non-black pixels 0
  ring of 40px around box in supplied image: max value 201, non-black pixels 11088
  rows containing lettering (y, absolute): [(np.int64(12), np.int64(54)), (np.int64(78), np.int64(138)), (np.int64(151), np.int64(180))]
  column runs: 10 x from 1243 to 1855 ; widest gap between runs 17
  non-black (>24) pixels on the box border: 17
CSS hero-text box in image px: x 1100.0 ..2000, y 0.. 204.8
```
```python
# CHECK 4b. Why: title lettering is one flat cream colour anti-aliased onto black, so every removed pixel must lie on the
# straight line from black to that one colour; art (stars, gold, blue mesh) would not. Also shows what lies beyond the box.
import numpy as np
from PIL import Image
S=np.array(Image.open('<attachments>/ec8c2235-image.png').convert('RGB')).astype(float)
E=np.array(Image.open('art_embedded.webp').convert('RGB')).astype(float)
d=(S!=E).any(-1); px=S[d]
u,c=np.unique(px.astype(int),axis=0,return_counts=True); top=u[c.argmax()]
print('removed pixels:',len(px),'| distinct colours',len(u),'| most common',top.tolist(),'share %.1f%%'%(100*c.max()/len(px)))
print('every removed pixel is now pure black in the embedded image:',bool((E[d]==0).all()))
t=top/np.linalg.norm(top); proj=px@t; resid=np.linalg.norm(px-np.outer(proj,t),axis=1)
print('distance of removed pixels from the line black->%s: max %.2f levels'%(top.tolist(),resid.max()))
print('removed pixels brighter than that colour:',int((px.max(1)>top.max()).sum()))
x0,x1,y0,y1=1243,1855,12,180
print('non-black pixels of the supplied image inside the box that were NOT removed:',int(((S[y0:y1+1,x0:x1+1].max(-1)>0)&~d[y0:y1+1,x0:x1+1]).sum()))
for name,(Y0,Y1,X0,X1) in {'above the box (y<12)':(0,y0,x0-60,x1+61),'60 px below':(y1+1,y1+61,x0-60,x1+61),'60 px left':(0,y1+61,x0-60,x0),'60 px right':(0,y1+61,x1+1,x1+61)}.items():
    r=S[Y0:Y1,X0:X1].max(-1); ys,xs=np.nonzero(r>0)
    print(f'  supplied image, {name}: non-black pixels {len(ys)}', (f'(nearest at y {ys.min()+Y0}..{ys.max()+Y0})' if len(ys) else ''))
blk=(E.max(-1)==0)
print('first non-black row under the box, x 1243..1855 (embedded = supplied there):',int(np.nonzero((~blk[:,1243:1856]).any(1))[0].min()),'| box ends at row 180; CSS title box ends at 25.6% x 800 =',0.256*800)
```
Output:
```
removed pixels: 13602 | distinct colours 252 | most common [243, 234, 216] share 51.4%
every removed pixel is now pure black in the embedded image: True
distance of removed pixels from the line black->[243, 234, 216]: max 0.68 levels
removed pixels brighter than that colour: 0
non-black pixels of the supplied image inside the box that were NOT removed: 0
  supplied image, above the box (y<12): non-black pixels 0 
  supplied image, 60 px below: non-black pixels 26388 (nearest at y 205..240)
  supplied image, 60 px left: non-black pixels 2160 (nearest at y 205..240)
  supplied image, 60 px right: non-black pixels 2160 (nearest at y 205..240)
first non-black row under the box, x 1243..1855 (embedded = supplied there): 205 | box ends at row 180; CSS title box ends at 25.6% x 800 = 204.8
```
Reading: embedded image is a lossless WebP, 2000x800. Differences: 13,602 pixels, box x 1243..1855, y 12..180 (613 x 169).
Outside the box: identical. Inside the box in the supplied image: 89,995 pure-black pixels and 13,602 non-black, and those
13,602 are exactly the pixels that changed; each lies within 0.68 levels of the line from black to cream (243,234,216), i.e.
one flat colour anti-aliased on black = lettering. Viewed (`supplied_topright.png`): "What the Neutrino State / Must Keep /
Jeromie Beasley". 20 px all round the box is pure black; the art begins at row 205.

## Check 5. Head and scripts

Why: a script or stylesheet rule can change what is shown without touching the markup.

`python3 check5_head.py`

```python
# CHECK 5 (HEAD/SCRIPTS). Why: a script or CSS rule can change what is displayed without changing the markup
# (content:, display:none, text-transform, innerHTML writes). So every script is listed and searched for DOM-writing calls,
# and the stylesheet is searched for rules that hide, insert or transform text.
import re
from strip import *
o=nodata(load(O)); a=nodata(load(A))
oh=o[:o.index('<body')]; ah=a[:a.index('<body')]
so=re.findall(r'<script\b[^>]*>.*?</script>',o,re.S); sa=re.findall(r'<script\b[^>]*>.*?</script>',a,re.S)
print('scripts orig',len(so),'art',len(sa))
for i,s in enumerate(so): print(' ORIG script',i,'in head' if s in oh else 'in body',len(s),'bytes:',repr(s[:400]))
for i,s in enumerate(sa): print(' ART  script',i,'in head' if s in ah else 'in body',len(s),'bytes; identical to an original script:',s in so)
new=[s for s in sa if s not in so]; print('scripts only in art:',len(new),'| scripts lost:',len([s for s in so if s not in sa]))
for s in new:
    print('--- new script ---'); print(s)
    for kw in ['innerHTML','textContent','innerText','createElement','appendChild','insertBefore','remove(','replace','document.write','fetch','XMLHttp','src=','eval','setAttribute','insertAdjacent','style.']:
        if kw in s: print('   contains',kw,':',re.findall(r'[^;{]*'+re.escape(kw)+r'[^;}]*',s)[:4])
strip=lambda h: re.sub(r'<style>.*?</style>','<style/>',h,flags=re.S)
x=strip(oh); y=strip(ah)
for s in new: y=y.replace(s+'\n','').replace(s,'')
print('head identical once <style> contents and the new script are set aside:',x==y)
if x!=y:
    import difflib
    for l in difflib.unified_diff(x.split('\n'),y.split('\n'),lineterm='',n=0): print('   ',l[:300])
print('head (orig, style elided):'); print(x)
css=re.search(r'<style>(.*?)</style>',ah,re.S).group(1)
print('art <style> blocks:',len(re.findall(r'<style',a)),'orig:',len(re.findall(r'<style',o)),'| inline style= attributes in art body:',len(re.findall(r'\sstyle="',a[a.index('<body'):])),'orig:',len(re.findall(r'\sstyle="',o[o.index('<body'):])))
for kw in ['content:','display:none','visibility','text-transform','font-variant','opacity','text-indent','font-size:0','color:transparent','::before','::after','counter','clip','max-height','overflow:hidden','filter','mix-blend','@import','url(http']:
    hits=re.findall(r'[^{}]*\{[^{}]*'+re.escape(kw)+r'[^{}]*\}',css)
    print(f'  CSS "{kw}": {len(hits)}'); 
    for h in hits: print('      ',re.sub(r'\s+',' ',h).strip()[:330])
print('external resources in art (src/href http):',sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"',a))),'| orig:',sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"',o))))
print('@font-face families:',re.findall(r"@font-face\{font-family:'([^']+)'[^}]*?font-style:(\w+)[^}]*?font-weight:([\d ]+)",css))
print('unicode-range present:',len(re.findall('unicode-range',css)))
```
Output:
```
scripts orig 1 art 2
 ORIG script 0 in head 103 bytes: '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js" async></script>'
 ART  script 0 in head 103 bytes; identical to an original script: True
 ART  script 1 in head 973 bytes; identical to an original script: False
scripts only in art: 1 | scripts lost: 0
--- new script ---
<script>
(function(){
 function fit(){document.querySelectorAll('mjx-container').forEach(function(c){
   if(c.closest('table'))return; c.style.zoom=''; var m=c.firstElementChild; if(!m)return;
   var host=c.parentElement; while(host&&host.parentElement&&getComputedStyle(host).display.indexOf('inline')===0){host=host.parentElement;}
   var cs=getComputedStyle(host); var avail=host.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
   var w=m.getBoundingClientRect().width;
   if(avail>0&&w>avail+1){c.style.zoom=Math.max(0.5,Math.floor(100*avail/w-1)/100); if(c.getAttribute('display')==='true')c.style.minWidth='0';}
 });}
 function go(){if(window.MathJax&&MathJax.startup&&MathJax.startup.promise){MathJax.startup.promise.then(fit);}else{setTimeout(go,200);}}
 window.addEventListener('load',go);
 var t; window.addEventListener('resize',function(){clearTimeout(t);t=setTimeout(fit,150);});
 window.addEventListener('beforeprint',fit);
})();
</script>
   contains style. : [" c.style.zoom=''", 'c.style.zoom=Math.max(0.5,Math.floor(100*avail/w-1)/100)', " if(c.getAttribute('display')==='true')c.style.minWidth='0'"]
head identical once <style> contents and the new script are set aside: True
head (orig, style elided):
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <meta name="author" content="Jeromie Beasley" />
  <title>What the Neutrino State Must Keep</title>
  <style/>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js" async></script>
</head>

art <style> blocks: 1 orig: 1 | inline style= attributes in art body: 280 orig: 280
  CSS "content:": 3
       body::before{content:"";position:absolute;top:0;bottom:0;left:12px;right:12px;z-index:-1;background:linear-gradient(180deg,rgba(3,5,12,0) 0,rgba(4,7,17,.62) 900px);border-radius:24px;pointer-events:none}
       #bgart::after{content:"";position:absolute;inset:0;background: radial-gradient(ellipse 120% 90% at 50% 50%,rgba(3,5,12,.46),rgba(3,5,12,.86) 85%),rgba(3,5,12,.30)}
       .hero-text{position:absolute;left:55%;width:45%;top:0;height:25.6%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:.6cqw 1cqw 0}
  CSS "display:none": 1
       #bgart,nav#TOC,body::before{display:none!important}
  CSS "visibility": 0
  CSS "text-transform": 1
       .hero p.author{margin:0;color:var(--gold2);font:500 .9cqw/1 var(--display);letter-spacing:.34em;text-transform:uppercase;padding-left:.34em}
  CSS "font-variant": 3
       body{position:relative;margin:0 auto;max-width:1580px;padding:24px 30px 80px;color:var(--ink);background:transparent; font:19px/1.72 var(--serif);font-variant-numeric:oldstyle-nums proportional-nums;hyphens:auto;overflow-wrap:break-word;text-rendering:optimizeLegibility}
       table{border-collapse:collapse;display:block;width:max-content;max-width:100%;overflow:auto;margin:18px 0 24px;background:rgba(6,10,24,.70);border:1px solid var(--line);border-radius:10px;font-variant-numeric:lining-nums tabular-nums}
       span.smallcaps{font-variant:small-caps}
  CSS "opacity": 0
  CSS "text-indent": 0
  CSS "font-size:0": 0
  CSS "color:transparent": 0
  CSS "::before": 0
  CSS "::after": 0
  CSS "counter": 0
  CSS "clip": 0
  CSS "max-height": 2
       nav#TOC{position:sticky;top:14px;float:left;width:300px;max-height:calc(100vh - 28px);overflow:auto;margin:0 24px 30px 0;padding:18px; border:1px solid var(--line);border-radius:18px;background:rgba(4,7,17,.86);box-shadow:0 14px 34px rgba(0,0,0,.4);font:14px/1.38 var(--serif);hyphens:manual}
       nav#TOC{position:relative;float:none;width:auto;max-height:360px;margin:0 0 22px}
  CSS "overflow:hidden": 2
       /* the hero: the art whole, at its own shape, with the title set in its upper-right band */ header#title-block-header.hero{position:relative;overflow:hidden;margin:6px 0 0;padding:0;text-align:center;border:1px solid rgba(226,189,108,.30);border-radius:22px; background:#000;box-shadow:0 24px 60px rgba(0,0,0,.45);container-type:i
       html body mjx-container>mjx-assistive-mml{width:1px!important;max-width:1px!important;height:1px!important;overflow:hidden!important}
  CSS "filter": 0
  CSS "mix-blend": 0
  CSS "@import": 0
  CSS "url(http": 0
external resources in art (src/href http): ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js', 'https://github.com/dicipler-pixel/neutrinos-leave-lean'] | orig: ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js', 'https://github.com/dicipler-pixel/neutrinos-leave-lean']
@font-face families: [('Cormorant Garamond', 'normal', '500'), ('Cormorant Garamond', 'normal', '600'), ('EB Garamond', 'normal', '400'), ('EB Garamond', 'italic', '400'), ('EB Garamond', 'normal', '600'), ('EB Garamond', 'italic', '600')]
unicode-range present: 0
```

Reading: head identical apart from the stylesheet contents and one added script. MathJax tag identical. The added script
measures each rendered equation and sets `style.zoom` (never below 0.5) and `style.minWidth` when it is wider than its
column; equations in tables are skipped. It reads and writes no text. Stylesheet: the three `content:` hits are empty strings
or a false match (`justify-content`); `display:none` applies in print only, to the background art and the contents list;
`text-transform:uppercase` on the byline (finding 5). No external resources beyond MathJax and the one GitHub link, as in v9.

## Check 6. Captions against the recoloured figures

Why: the words are unchanged but lightness was flipped, so a sentence naming an element by a lightness word can now point at the wrong thing. Every sentence with a colour or lightness word is listed; the figures were then viewed (downscaled copies `view_a*.png`, `view_o*.png`).

`python3 check6_captions.py`, `python3 check6b_fills.py`

```python
# CHECK 6 (CAPTIONS vs RECOLOURED FIGURES). Why: the words did not change but the pictures' lightness did, so any
# sentence that identifies a figure element by a lightness word can now point at the wrong thing. Every sentence in the page
# (captions and body, listings excluded) containing a colour/lightness word is listed.
import re, html
from strip import *
a=nodata(load(A)); b=a[a.index('<body'):]
b=re.sub(r'<nav id="TOC".*?</nav>','',b,flags=re.S)
caps=re.findall(r'<figure[^>]*>(.*?)</figure>',b,re.S)
def txt(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
W=r'\b(black|white|dark\w*|light(?:er|est|ly)?|grey|gray|pale\w*|faint\w*|shad\w+|bright\w*|colou?r\w*|red|blue|green|orange|purple|violet|gold\w*|yellow|cyan|magenta|pink|brown|teal|navy|crimson|solid|dashed|dotted|open (?:circle|square|symbol|marker)s?|filled|hollow|thick|thin|bold|background|ground)\b'
print('=== FIGURE CAPTIONS (full) ===')
for n,c in enumerate(caps,1):
    t=txt(re.search(r'<figcaption>(.*?)</figcaption>',c,re.S).group(1)); hits=sorted(set(m.group(0).lower() for m in re.finditer(W,t,re.I)))
    print(f'[Fig {n}] words: {hits}\n   {t}\n')
print('=== OTHER SENTENCES (body text, tables; <pre> excluded) with a colour/lightness word ===')
nb=re.sub(r'<figure[^>]*>.*?</figure>','',b,flags=re.S); nb=re.sub(r'<pre\b.*?</pre>','',nb,flags=re.S)
t=txt(nb); k=0
W2=r'\b(black|white|dark\w*|grey|gray|pale\w*|faint\w*|shaded|shading|bright\w*|colou?r\w*|red|blue|green|orange|purple|violet|gold\w*|yellow|cyan|magenta|pink|brown|dashed|dotted|light (?:line|curve|band|grey|gray|blue|point|marker|symbol)s?)\b'
for s in re.split(r'(?<=[.!?])\s+(?=[A-Z(])',t):
    hs=sorted(set(m.group(0).lower() for m in re.finditer(W2,s,re.I)))
    if hs: k+=1; print(f'({k}) {hs}: {s[:420]}')
print('=== <pre> listings lines mentioning figure colours (plot code; informational) ===')
pre=' \n'.join(re.findall(r'<pre\b.*?</pre>',b,re.S)); 
print('lines with color=/facecolor in listings:',len(re.findall(r'color\s*=',pre)))
```
Output:
```
=== FIGURE CAPTIONS (full) ===
[Fig 1] words: []
   The neutrino moments form a chain. Streaming links each moment to its neighbours; collisions put a rate on each. Non-normality sits only where neighbouring rates differ: on the density–flux link (\(k^2\kappa_1^2/3\)) and, if shear relaxes at its own rate, on the flux–shear link. Every other link carries none.

[Fig 2] words: ['dashed']
   The wall of the full chain. Left: the kept-sector pole \(s=k\cot(k/\kappa)-\kappa\) (line) and the least-damped eigenvalue of a 400-moment chain (dots); the pole meets the branch cut at its centre \(s=-\kappa\) (dashed) at \(\kappa=2k/\pi\). Right: its non-orthogonality \(K=4\phi^2/\sin^22\phi\), with \(\phi=k/\kappa\), diverging at the onset. Inset numbers: the truncated chain’s onset at 50, 200 and 800 moments, closing on \(2/\pi\) from above.

[Fig 3] words: ['dotted']
   Test A. The broad profile collapses at \(\epsilon\approx7\)–\(9\), yet keeps the same share \(G\) of the free-streaming shift as the Gaussian. A clock tied to the collapse time would have given the dotted values.

[Fig 4] words: ['black', 'blue', 'dashed', 'grey', 'open squares', 'orange']
   The surviving share \(G\) of the free-streaming shift against decoupling time. Black dots: McCormick’s Gaussian runs with \(\kappa/H=(\epsilon_{\rm dec}/\epsilon)^3\); the grey dashed line through them is what a history-blind rule gives for any history. Blue: the kept-sector memory with one weight fitted to the black dots. Orange line: the same form for \(\kappa/H=(\epsilon_{\rm dec}/\epsilon)^6\), computed before any such run and not refitted. Orange diamonds: the new \(n=6\) runs C, B and D. Open squares: the broad profile (Test A).

[Fig 5] words: ['grey', 'orange', 'shaded']
   The three steep-history tests against their kill lines. The shaded band is \(\pm0.08\) around each measurement. Orange: the memory form’s prediction, made before the run. Grey circle: the history-blind rule. At \(\epsilon_{\rm dec}=3\) the history-blind rule falls outside the band.

[Fig 6] words: ['red']
   The door. Strength of the matched-pair witness, \(\log_{10}R_{\rm ret}\) at \(\tau=4\), against the time the hidden difference was planted (in units of \(\epsilon_{\rm dec}\)) and the moment that held it. Planted deep in the coupled era the difference is erased, down to \(10^{-30}\); planted at or after decoupling it returns at the \(10^{-1}\) level. The red plane is the witness threshold \(10^{-3}\). The steeper history (\(n=6\)) closes the door more sharply.

[Fig 7] words: ['dashed', 'shaded']
   The flux–shear link. Left: the surviving share \(G\) against the link’s reflection coefficient \(\Gamma_{12}\), eleven thresholds from McCormick’s code with the shear and higher moments relaxing at \(r\) times the flux rate. Right: the offset of \(G\) against the link rapidity \(\tfrac12\ln r\), with the shear-only pairs (squares); the shaded band is the admissible window \(\tfrac34\le r\le\tfrac32\). Lines: rate one (dashed) and the inner-pair rate \(1.11\).

[Fig 8] words: []
   Left: eigenvalues of the readout Gramian of the hidden moments \(\ell\ge3\), for structure planted in the coupled era, at decoupling and in free streaming (\(n=3\), \(\epsilon_{\rm dec}=2\), readout to \(\epsilon=4\)). Right: the memory form \(g_2\) for pairs of collision histories with equal optical depth and equal integrated connection energy, the rate reversed in time inside a window; R4 is the one pair whose window contains the readout.

[Fig 9] words: ['black']
   The door in the full collapse. Left: the difference in black-hole threshold between two neutrino states with identical density, flux, stress, energy, radial pressure, lapse and constraints, differing only in hidden angular structure, against the epoch at which the structure is planted; error bars are bracket half-widths plus twice the measured angular drift. Right: the threshold shifts from the unperturbed restart at decoupling.

[Fig 10] words: []
   Thresholds at \(T_H=1\) MeV in McCormick’s multigroup model. Removing the flux–shear split while keeping the isotropy history (\(r=1\)) moves the threshold by \(+0.0003\) from his self-scattering run; the timing reading predicted no move, the frozen link law \(+0.0010\).

[Fig 11] words: ['grey', 'shaded']
   Inside McCormick’s multigroup model at \(r=r_m\), his archived threshold edges at \(T_H=1\) and \(0.51\) MeV (positive common-frame target): energy-frame velocity of the neutrino gas, kept-share anisotropy \(1-A\), link rapidity of the dominant and of a \(\nu_e\) group against the admissible window (grey), moment ratios, the speed-limit ratio of the kept population, and the peak compaction. The readout epoch \(1.7\le\epsilon\le4\) is shaded.

=== OTHER SENTENCES (body text, tables; <pre> excluded) with a colour/lightness word ===
(1) ['black']: What the Neutrino State Must Keep Jeromie Beasley Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation 13 November 2026 (version 9 of When the Neutrinos Leave) AI-assisted.
(2) ['black']: Abstract McCormick has shown that neutrinos which stream freely out of a collapsing overdensity raise the threshold for primordial black hole formation, by about \(0.235\,R_\nu\) in the linear compaction, and that the effect fades when the neutrinos decouple gradually.
(3) ['black']: In McCormick’s full general-relativistic collapse, two neutrino states identical in density, flux, stress, lapse, constraints and every fluid and metric array, differing only in hidden angular structure planted at decoupling, have black-hole thresholds \(3.7\times10^{-3}\) apart for \(\ell=3\), \(2.1\times10^{-3}\) with the opposite sign for \(\ell=4\), and \(5.5\times10^{-3}\) along the Gramian’s leading direction, 
(4) ['black']: The question Primordial black holes heavier than about \(10^6\,M_\odot\) form while the neutrinos, which carry 41–49% of the radiation, stop scattering and stream freely.
(5) ['black']: A reproduction run at \(\delta=0.5109\) with \(n=3\), \(\epsilon_{\rm dec}=2\) forms a black hole, inside his published bracket \((0.51074,0.51109)\) [measured; Appendix B.4].
(6) ['black']: At \(r=1\) the changed code reproduces the unchanged one: \(\delta=0.5109\) forms a black hole at \(\epsilon=6.61\) in both [measured].
(7) ['black']: Evaluating it at each stage time is the only change of Appendix B.19; it moves black-hole formation at \(r=1\), \(\delta=0.5109\), from \(\epsilon=6.6147\) to \(6.6176\).
(8) ['black']: Here \(0.5132\) and \(0.5138\) bracket the first, and \(0.5165\) and \(0.5171\) the second, each dispersing below and forming a black hole above [measured].
(9) ['black']: The question it leaves is whether hidden angular structure that density, flux and stress do not carry can move the black-hole threshold itself, in the full general-relativistic collapse.
(10) ['black']: The black-hole threshold reads angular information that no closure on density, flux and stress holds.
(11) ['black']: The bisection (\(T_0=10\) MeV, six groups, \(N=300\), \(N_\mu=32\)) gives \[\delta_c(r=1)=0.51972\pm0.00009,\] above his self-scattering threshold by \(+0.00031\pm0.00018\), and strictly above it, since his \(0.5195625\) forms a black hole and here \(0.519625\) disperses [measured; Figure 10].
(12) ['black']: In the full collapse, hidden angular structure planted at decoupling, invisible to density, flux, stress and Einstein’s equations at the restart, moves the black-hole threshold by up to \(5.5\times10^{-3}\), with the sign set by its parity and the size ranked by the Gramian; planted in the coupled era it moves it by less than one per cent of that.
(13) ['black']: McCormick, Free-streaming neutrinos raise the threshold for primordial black hole formation, preprint (2026).
(14) ['black']: McCormick, Free-streaming neutrinos raise the threshold for primordial black hole formation, version 1.1, with multigroup decoupling (2026).
(15) ['colour']: Beasley, Colour Selects the Leader, v1.1 (2026). [12 ] J.
(16) ['black']: Papanikolaou, Toward the primordial black hole formation threshold in a time-dependent equation-of-state background, arXiv:2205.07748. [17 ] A.
(17) ['black']: Escrivà, arXiv:2504.05814. [18 ] Gonin, Froustey, Escrivà, Magaraggia, Kühnel and Hasinger, Primordial asymmetries, primordial equation of state and primordial black holes, arXiv:2608.22240 (2026). [19 ] Dave, Yan, Ilyas and Cai, Evading the CMB \(\mu\)-distortion bound on supermassive PBH seeds with non-Gaussian tails, arXiv:2607.03138 (2026). [20 ] C.-P.
=== <pre> listings lines mentioning figure colours (plot code; informational) ===
lines with color=/facecolor in listings: 73
```
```python
# CHECK 6b. Why: a shaded band or grey element named in a caption must still differ from the ground after the flip;
# lists the largest flat colours of each figure before -> after.
import re, io, base64, numpy as np
from PIL import Image
from strip import *
RX=r'<img src="data:image/png;base64,([^"]+)"'
for n,(bo,ba) in enumerate(zip(re.findall(RX,load(O)),re.findall(RX,load(A))),1):
    x=np.array(Image.open(io.BytesIO(base64.b64decode(bo))).convert('RGB')).reshape(-1,3); y=np.array(Image.open(io.BytesIO(base64.b64decode(ba))).convert('RGB')).reshape(-1,3)
    k=x.astype(np.uint32)@np.array([65536,256,1],dtype=np.uint32); u,idx,c=np.unique(k,return_index=True,return_counts=True)
    print(f'fig {n}:',[(tuple(int(v) for v in x[idx[i]]),'->',tuple(int(v) for v in y[idx[i]]),f'{100*c[i]/k.size:.1f}%') for i in np.argsort(-c)[:6]])
```
Output:
```
fig 1: [((255, 255, 255), '->', (13, 13, 13), '88.1%'), ((142, 68, 173), '->', (153, 77, 185), '4.4%'), ((192, 57, 43), '->', (211, 71, 57), '1.7%'), ((230, 126, 34), '->', (217, 115, 25), '1.7%'), ((244, 208, 63), '->', (193, 157, 11), '1.4%'), ((0, 0, 0), '->', (237, 237, 237), '0.6%')]
fig 2: [((255, 255, 255), '->', (13, 13, 13), '95.3%'), ((0, 0, 0), '->', (237, 237, 237), '1.3%'), ((227, 227, 227), '->', (37, 37, 37), '0.8%'), ((31, 78, 121), '->', (120, 172, 220), '0.5%'), ((224, 138, 0), '->', (255, 166, 22), '0.2%'), ((170, 51, 51), '->', (202, 78, 78), '0.1%')]
fig 3: [((255, 255, 255), '->', (13, 13, 13), '89.8%'), ((85, 85, 85), '->', (162, 162, 162), '3.4%'), ((46, 139, 87), '->', (106, 206, 150), '3.0%'), ((0, 0, 0), '->', (237, 237, 237), '1.3%'), ((198, 198, 198), '->', (63, 63, 63), '0.6%'), ((192, 57, 43), '->', (211, 71, 57), '0.2%')]
fig 4: [((255, 255, 255), '->', (13, 13, 13), '96.3%'), ((0, 0, 0), '->', (237, 237, 237), '1.3%'), ((0, 114, 178), '->', (63, 186, 255), '0.4%'), ((230, 159, 0), '->', (255, 181, 17), '0.4%'), ((212, 212, 212), '->', (51, 51, 51), '0.2%'), ((122, 122, 122), '->', (130, 130, 130), '0.1%')]
fig 5: [((255, 255, 255), '->', (13, 13, 13), '95.7%'), ((214, 230, 243), '->', (16, 38, 56), '2.1%'), ((0, 0, 0), '->', (237, 237, 237), '1.0%'), ((122, 122, 122), '->', (130, 130, 130), '0.1%'), ((230, 159, 0), '->', (255, 181, 17), '0.1%'), ((212, 212, 212), '->', (51, 51, 51), '0.1%')]
fig 6: [((255, 255, 255), '->', (13, 13, 13), '55.5%'), ((242, 242, 242), '->', (24, 24, 24), '6.3%'), ((248, 248, 248), '->', (19, 19, 19), '4.2%'), ((209, 202, 23), '->', (231, 224, 39), '3.6%'), ((245, 245, 245), '->', (22, 22, 22), '2.9%'), ((125, 189, 61), '->', (127, 192, 62), '1.8%')]
fig 7: [((255, 255, 255), '->', (13, 13, 13), '83.9%'), ((237, 242, 248), '->', (13, 23, 34), '8.3%'), ((237, 237, 237), '->', (29, 29, 29), '2.4%'), ((27, 27, 27), '->', (213, 213, 213), '0.8%'), ((0, 0, 0), '->', (237, 237, 237), '0.5%'), ((223, 227, 231), '->', (32, 37, 43), '0.4%')]
fig 8: [((255, 255, 255), '->', (13, 13, 13), '83.4%'), ((15, 127, 168), '->', (74, 195, 239), '6.8%'), ((200, 144, 10), '->', (244, 186, 45), '6.3%'), ((0, 0, 0), '->', (237, 237, 237), '1.1%'), ((227, 227, 227), '->', (37, 37, 37), '0.4%'), ((138, 132, 120), '->', (132, 127, 115), '0.0%')]
fig 9: [((255, 255, 255), '->', (13, 13, 13), '84.7%'), ((248, 241, 225), '->', (47, 36, 11), '5.6%'), ((91, 63, 168), '->', (110, 81, 190), '2.7%'), ((15, 127, 168), '->', (74, 195, 239), '1.9%'), ((181, 69, 27), '->', (227, 109, 65), '1.1%'), ((0, 0, 0), '->', (237, 237, 237), '1.1%')]
fig 10: [((255, 255, 255), '->', (13, 13, 13), '95.9%'), ((0, 0, 0), '->', (237, 237, 237), '1.1%'), ((227, 227, 227), '->', (37, 37, 37), '0.3%'), ((200, 144, 10), '->', (244, 186, 45), '0.1%'), ((181, 69, 27), '->', (227, 109, 65), '0.1%'), ((138, 132, 120), '->', (132, 127, 115), '0.0%')]
fig 11: [((255, 255, 255), '->', (13, 13, 13), '71.2%'), ((254, 252, 191), '->', (81, 79, 1), '17.8%'), ((227, 227, 227), '->', (37, 37, 37), '1.1%'), ((247, 247, 247), '->', (20, 20, 20), '1.0%'), ((254, 254, 242), '->', (35, 35, 3), '0.9%'), ((0, 0, 0), '->', (237, 237, 237), '0.8%')]
```

| Fig. | Words in the caption (or in the figure) | Now wrong? |
|---|---|---|
| 2 | "(dashed)" branch-cut centre | No. Line styles unchanged. |
| 3 | "the dotted values" | No. |
| 4 | "**Black dots**: McCormick's Gaussian runs"; "fitted to the **black dots**" | **Yes.** The dots are now cream-white. |
| 4 | "grey dashed line" | No. Mid-grey stays mid-grey (122 -> 130). |
| 4 | "Blue", "Orange line", "Orange diamonds" | No. Hues kept (lighter blue, brighter orange). |
| 4 | "Open squares" | No. Outline now cream, inside is the ground colour; still open. |
| 5 | "shaded band" | No, but faint: (214,230,243) -> (16,38,56) on (13,13,13). |
| 5 | "Orange", "Grey circle" | No. |
| 6 | "The red plane" (caption and in-figure label) | No. Still red, now a dark translucent red. |
| 7 | "shaded band is the admissible window"; "(dashed)" | No, but the band is faint: -> (13,23,34). |
| 9 | "black-hole threshold" | Not a colour word. |
| 11 | "admissible window (grey)"; "readout epoch ... is shaded" | No. Grey -> dark grey (37,37,37); yellow band -> dark olive (81,79,1). |
| 8 (in-figure title) | "blue odd ...; red even ..." | No. |
| 1, 10 | no colour words | - |

Body text outside captions: the only hits are "black hole" and the reference title "Colour Selects the Leader"; no sentence
in the running text names a figure element by colour.

## Check 7. Other things that could change silently

Why: the old stylesheet might have generated or hidden text (counters, `content:`) that the new one does differently; classes might have lost rules; encoding could have been damaged.

`python3 check7_misc.py` (ids, links, entities, tag counts, section order are in check 2)

```python
# CHECK 7 (ANYTHING ELSE). Why: (a) the original stylesheet may have generated or hidden text (counters, content:, display:none)
# that the new stylesheet no longer does or now does differently; (b) a class used in the body may have lost a rule that made
# its text readable/visible; (c) an embedded font subset lacking a character would show a fallback glyph (not a loss, but
# checked); (d) inline style attributes could hide content; (e) the file must be valid UTF-8 with no stray replacement chars.
import re, collections, base64, io, html
from strip import *
ro=load(O); ra=load(A); o=nodata(ro); a=nodata(ra)
co=re.search(r'<style>(.*?)</style>',o,re.S).group(1); ca=re.search(r'<style>(.*?)</style>',a,re.S).group(1)
print('ORIGINAL stylesheet,',len(co),'bytes; rules that generate/hide/transform text:')
for kw in ['content:','counter','display:none','display: none','visibility','text-transform','font-variant','::before','::after',':before',':after','quotes','hyphens','white-space']:
    hits=re.findall(r'[^{}]*\{[^{}]*'+re.escape(kw)+r'[^{}]*\}',co)
    for h in hits: print(f'   [{kw}]',re.sub(r'\s+',' ',h).strip()[:260])
bo=o[o.index('<body'):]; ba=a[a.index('<body'):]
clo=collections.Counter(c for m in re.findall(r'class="([^"]*)"',bo) for c in m.split()); cla=collections.Counter(c for m in re.findall(r'class="([^"]*)"',ba) for c in m.split())
print('classes in body orig:',dict(clo)); print('classes in body art :',dict(cla))
for c in clo:
    print(f'   .{c}: styled in orig css: {bool(re.search(r"\."+re.escape(c)+r"\b",co))}; styled in art css: {bool(re.search(r"\."+re.escape(c)+r"\b",ca))}')
st_o=collections.Counter(re.findall(r'\sstyle="([^"]*)"',bo)); st_a=collections.Counter(re.findall(r'\sstyle="([^"]*)"',ba))
print('inline style attributes identical multiset:',st_o==st_a,'| distinct values:',list(st_o.items())[:8])
print('white-space handling for <pre>/<code>: orig:',re.findall(r'(?:pre|code)[^{}]*\{[^{}]*\}',co)[:6])
print('lang attr:',re.search(r'<html[^>]*>',a).group(0),'| hyphens:auto in art css:', 'hyphens:auto' in ca,'(inactive without a lang; pre, code and nav set to manual)')
print('U+FFFD in art:',ra.count('�'),'orig:',ro.count('�'),'| NUL:',ra.count('\x00'),'| CR:',ra.count('\r'),ro.count('\r'),'| BOM:',ra.startswith('﻿'),ro.startswith('﻿'))
print('doctype/charset same:',ra[:120]==ro[:120])
print('file ends:',repr(ra[-40:]),'| orig:',repr(ro[-40:]))
print('counts of <body>,</body>,</html> art:',ra.count('<body>'),ra.count('</body>'),ra.count('</html>'))
# non-ASCII character inventory in visible body text (identical text already shown; this is for font coverage)
vis=html.unescape(re.sub(r'<[^>]+>','',re.sub(r'<(script|style)\b.*?</\1>','',ba,flags=re.S)))
chars=collections.Counter(ch for ch in vis if ord(ch)>126)
print('non-ASCII characters in art body text:',{f'U+{ord(k):04X} {k}':v for k,v in sorted(chars.items())})
try:
    from fontTools.ttLib import TTFont
    fonts=re.findall(r"@font-face\{font-family:'([^']+)'[^}]*?url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)[^}]*\}",re.search(r'<style>(.*?)</style>',ra,re.S).group(1))
    for name,b in fonts:
        f=TTFont(io.BytesIO(base64.b64decode(b))); cm=f.getBestCmap()
        miss=[f'U+{ord(k):04X} {k}' for k in sorted(chars) if ord(k) not in cm and not k.isspace()]
        ascii_miss=[chr(c) for c in range(33,127) if c not in cm]
        feats=sorted({fr.FeatureTag for fr in f['GSUB'].table.FeatureList.FeatureRecord}) if 'GSUB' in f else []
        print(f'   font {name}: {len(cm)} glyph codes; ASCII missing {ascii_miss}; body non-ASCII not covered (falls back to next font): {miss}; has onum:{"onum" in feats} lnum:{"lnum" in feats} liga:{"liga" in feats} dlig:{"dlig" in feats}')
except Exception as e: print('fontTools not usable:',repr(e))
```
Output:
```
ORIGINAL stylesheet, 3492 bytes; rules that generate/hide/transform text:
   [font-variant] table { margin: 1em 0; border-collapse: collapse; width: 100%; overflow-x: auto; display: block; font-variant-numeric: lining-nums tabular-nums; }
   [font-variant] span.smallcaps{font-variant: small-caps;}
   [hyphens] body { margin: 0 auto; max-width: 36em; padding-left: 50px; padding-right: 50px; padding-top: 50px; padding-bottom: 50px; hyphens: auto; overflow-wrap: break-word; text-rendering: optimizeLegibility; font-kerning: normal; }
   [hyphens] code { font-family: Menlo, Monaco, Consolas, 'Lucida Console', monospace; font-size: 85%; margin: 0; hyphens: manual; }
   [white-space] code{white-space: pre-wrap;}
classes in body orig: {'title': 1, 'author': 1, 'date': 1, 'abstract': 1, 'abstract-title': 1, 'math': 1555, 'inline': 1528, 'display': 27, 'center': 9, 'header': 9, 'odd': 26, 'even': 20, 'unnumbered': 44, 'uri': 1}
classes in body art : {'hero': 1, 'hero-art': 1, 'hero-text': 1, 'title': 1, 't-line': 2, 'rule': 1, 'author': 1, 'titlemeta': 1, 'subtitle': 1, 'date': 1, 'level1': 18, 'math': 1555, 'inline': 1528, 'display': 27, 'center': 9, 'header': 9, 'odd': 26, 'even': 20, 'unnumbered': 44, 'uri': 1}
   .title: styled in orig css: False; styled in art css: True
   .author: styled in orig css: False; styled in art css: True
   .date: styled in orig css: False; styled in art css: True
   .abstract: styled in orig css: True; styled in art css: False
   .abstract-title: styled in orig css: True; styled in art css: False
   .math: styled in orig css: False; styled in art css: True
   .inline: styled in orig css: False; styled in art css: False
   .display: styled in orig css: False; styled in art css: True
   .center: styled in orig css: False; styled in art css: False
   .header: styled in orig css: False; styled in art css: False
   .odd: styled in orig css: False; styled in art css: False
   .even: styled in orig css: False; styled in art css: False
   .unnumbered: styled in orig css: False; styled in art css: False
   .uri: styled in orig css: False; styled in art css: False
inline style attributes identical multiset: True | distinct values: [('width:95.0%', 3), ('text-align: left;', 52), ('text-align: center;', 200), ('width:90.0%', 1), ('text-align: right;', 24)]
white-space handling for <pre>/<code>: orig: ["code {\n      font-family: Menlo, Monaco, Consolas, 'Lucida Console', monospace;\n      font-size: 85%;\n      margin: 0;\n      hyphens: manual;\n    }", 'pre {\n      margin: 1em 0;\n      overflow: auto;\n    }', 'pre code {\n      padding: 0;\n      overflow: visible;\n      overflow-wrap: normal;\n    }', 'code{white-space: pre-wrap;}']
lang attr: <html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang=""> | hyphens:auto in art css: True (inactive without a lang; pre, code and nav set to manual)
U+FFFD in art: 0 orig: 0 | NUL: 0 | CR: 0 0 | BOM: False False
doctype/charset same: True
file ends: 'exactly.</p>\n</section>\n</body>\n</html>\n' | orig: 'inequality\nexactly.</p>\n</body>\n</html>\n'
counts of <body>,</body>,</html> art: 1 1 1
non-ASCII characters in art body text: {'U+00A0 \xa0': 146, 'U+00B1 ±': 1, 'U+00B7 ·': 3, 'U+00E0 à': 3, 'U+00FC ü': 1, 'U+2006 \u2006': 16, 'U+2013 –': 71, 'U+2014 —': 5, 'U+2019 ’': 96, 'U+201C “': 1, 'U+201D ”': 1, 'U+2212 −': 3}
The WOFF2 decoder requires the Brotli Python extension, available at: https://github.com/google/brotli
fontTools not usable: ImportError('No module named brotli')
```
Reading: the v9 stylesheet generated no text (no `content:`, no counters), so nothing that was drawn by CSS has gone missing.
Inline `style=` attributes: same 280. No replacement characters, no CR, same doctype and charset. `hyphens:auto` is present in
both stylesheets and the page has `lang=""` in both. New: old-style figures in body text (finding 5).
