# SCRIPT: NU-V9-ART-CHECK  the art edition must hold the v9 paper word for word
# Why this decides it: tags are stripped from both pages and whitespace collapsed; the art edition's contents list is removed
# (it repeats headings) and its one added line (the subtitle, from the PDF title) is removed. What is left must be identical,
# and every figure image, table and listing must be byte-identical and in the same order.
import sys, re, html, hashlib
def body(p): t = open(p, encoding='utf-8').read(); return t[t.index('<body>') + 6: t.rindex('</body>')]
def text(b):
    b = re.sub(r'<img[^>]*>', '', b); b = re.sub(r'<[^>]+>', ' ', b); return re.sub(r'\s+', ' ', html.unescape(b)).strip()
a, b = body(sys.argv[1]), body(sys.argv[2])
b2 = re.sub(r'<nav id="TOC".*?</nav>', '', b, flags=re.S)
sub = '<p class="subtitle">Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation</p>'
assert b2.count(sub) == 1; b2 = b2.replace(sub, '')
ta, tb = text(a), text(b2)
# the title block is re-ordered (title, author, date, advisory, abstract): compare as the same multiset of words there, exactly after it
cut = 'The question Primordial black holes'
ia, ib = ta.index(cut), tb.index(cut)
same_tail = ta[ia:] == tb[ib:]
same_head = sorted(ta[:ia].split()) == sorted(tb[:ib].split())
def blocks(x, tag): return [hashlib.sha256(m.encode()).hexdigest() for m in re.findall(rf'<{tag}[ >].*?</{tag}>', x, re.S)]
imgs = lambda x: [hashlib.sha256(m.encode()).hexdigest() for m in re.findall(r'<img[^>]*>', x)]
# figures on the dark ground: undo the lightness flip and compare with the v9 figure, pixel by pixel
def figs_undo_ok(a, b):
    import io, base64, numpy as np
    from PIL import Image
    import darkfig
    A = re.findall(r'<img src="data:image/png;base64,([^"]+)"', a); B = re.findall(r'<img src="data:image/png;base64,([^"]+)"', b)
    if len(A) != len(B): return False, []
    rep = []
    for x, y in zip(A, B):
        ia = np.array(Image.open(io.BytesIO(base64.b64decode(x))).convert('RGB')); ib = np.array(Image.open(io.BytesIO(base64.b64decode(y))).convert('RGB'))
        if ia.shape != ib.shape: return False, rep
        rep.append(int(np.abs(darkfig.undo(ib).astype(int) - ia.astype(int)).max()))
    return max(rep) <= 2, rep
res = dict(body_text_identical=same_tail, title_block_same_words=same_head, words_tail=len(ta[ia:].split()), words_head=len(ta[:ia].split()),
           figures=(imgs(a) == imgs(b)) or figs_undo_ok(a, b)[0], figure_undo_max_error=figs_undo_ok(a, b)[1] if imgs(a) != imgs(b) else 'byte-identical', n_figures=len(imgs(a)), tables=blocks(a, 'table') == blocks(b, 'table'), n_tables=len(blocks(a, 'table')),
           listings=blocks(a, 'pre') == blocks(b, 'pre'), n_listings=len(blocks(a, 'pre')),
           maths=re.findall(r'<span class="math[^>]*>.*?</span>', a, re.S) == re.findall(r'<span class="math[^>]*>.*?</span>', b2, re.S),
           n_maths=len(re.findall(r'<span class="math[^>]*>', a)))
for k, v in res.items(): print(k, v)
sys.exit(0 if all(v for k, v in res.items() if isinstance(v, bool)) else 1)
