# SCRIPT: NU-V9-ART-HTML  put the cover art and the VOTKP page design on the v9 HTML, changing no word of the paper
# Usage: python3 build_art_html.py <v9.html> <art_clean.webp> <votkp.html (for the embedded Garamond fonts)> <out.html>
# The paper's text, maths, tables, listings and figures are taken byte for byte from the v9 HTML. What is added:
# section wrappers, a contents list built from the paper's own headings, the hero, and the paper's own subtitle (from \title).
import sys, re, base64, html

SRC, ART, VOTKP, OUT = sys.argv[1:5]
t = open(SRC, encoding='utf-8').read()

# ---------- take the v9 page apart ----------
head_end = t.index('<body>')
body = t[head_end + len('<body>'): t.rindex('</body>')]
hdr = re.search(r'<header id="title-block-header">(.*?)</header>', body, re.S)
hb = hdr.group(1)
title = re.search(r'<h1 class="title">(.*?)</h1>', hb, re.S).group(1)
author = re.search(r'<p class="author">(.*?)</p>', hb, re.S).group(1)
date = re.search(r'<p class="date">(.*?)</p>', hb, re.S).group(1)
ab = re.search(r'<div class="abstract">\s*<div class="abstract-title">(.*?)</div>(.*)</div>\s*$', hb, re.S)
abstract_title, abstract_body = ab.group(1), ab.group(2)
rest = body[hdr.end():]
adv = re.match(r'\s*(<p><em>AI-assisted\..*?</em></p>)', rest, re.S)
advisory = adv.group(1); rest = rest[adv.end():]
assert title.strip() == 'What the Neutrino State Must Keep'

# ---------- sections: one card per top-level heading ----------
cuts = [m.start() for m in re.finditer(r'<h1[ >]', rest)]
assert rest[:cuts[0]].strip() == '', 'unexpected content before the first heading'
chunks = [rest[a:b] for a, b in zip(cuts, cuts[1:] + [len(rest)])]
sections = ['<section class="level1">\n' + c.rstrip() + '\n</section>' for c in chunks]

# ---------- contents list from the paper's own headings ----------
def heads(chunk):
    return [(int(m.group(1)), m.group(2), m.group(3)) for m in re.finditer(r'<h([12])[^>]*?\bid="([^"]+)"[^>]*>(.*?)</h\1>', chunk, re.S)]
toc = ['<li><a href="#abstract">' + abstract_title + '</a></li>']
for c in chunks:
    hs = heads(c); assert hs and hs[0][0] == 1, c[:80]
    item = f'<li><a href="#{hs[0][1]}">{hs[0][2]}</a>'
    subs = [h for h in hs[1:] if h[0] == 2]
    if subs: item += '\n<ul>\n' + '\n'.join(f'<li><a href="#{i}">{x}</a></li>' for _, i, x in subs) + '\n</ul>'
    toc.append(item + '</li>')
nav = '<nav id="TOC" role="doc-toc">\n<ul>\n' + '\n'.join(toc) + '\n</ul>\n</nav>'

# ---------- fonts (from the VOTKP page) and art ----------
v = open(VOTKP, encoding='utf-8').read()
fonts = re.findall(r"@font-face\{font-family:'(?:Cormorant Garamond|EB Garamond)'[^}]*\}", v)
assert len(fonts) == 6
art = 'data:image/' + ART.rsplit('.', 1)[1] + ';base64,' + base64.b64encode(open(ART, 'rb').read()).decode()   # lossless WebP: every pixel of the art, under the browser's size limit for an image inside a stylesheet

CSS = r'''
:root{
  --night:#03050c; --panel:rgba(5,8,20,.78); --cream:#f3ead8; --ink:#e6dfcd; --muted:#b9b3a4;
  --gold:#e2bd6c; --gold2:#f0d495; --mesh:#7fa6e8; --line:rgba(140,168,240,.17); --gline:rgba(226,189,108,.34);
  --serif:'EB Garamond',Georgia,'Times New Roman','Liberation Serif','DejaVu Serif',serif;
  --display:'Cormorant Garamond','EB Garamond',Georgia,'Liberation Serif','DejaVu Serif',serif;
  --art:url(ARTDATA);
}
*{box-sizing:border-box}
html{background:var(--night);scroll-behavior:smooth;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{position:relative;margin:0 auto;max-width:1580px;padding:24px 30px 80px;color:var(--ink);background:transparent;
  font:19px/1.72 var(--serif);font-variant-numeric:oldstyle-nums proportional-nums;hyphens:auto;overflow-wrap:break-word;text-rendering:optimizeLegibility}
body::before{content:"";position:absolute;top:0;bottom:0;left:12px;right:12px;z-index:-1;background:linear-gradient(180deg,rgba(3,5,12,0) 0,rgba(4,7,17,.62) 900px);border-radius:24px;pointer-events:none}

/* the art, fixed behind the page, muted and faded */
#bgart{position:fixed;inset:0;z-index:-2;pointer-events:none;background:
  linear-gradient(180deg,rgba(3,5,12,.35),rgba(3,5,12,.15) 30%,rgba(3,5,12,.55)),
  var(--art) 50% 50%/cover no-repeat,var(--night)}
#bgart::after{content:"";position:absolute;inset:0;background:
  radial-gradient(ellipse 120% 90% at 50% 50%,rgba(3,5,12,.46),rgba(3,5,12,.86) 85%),rgba(3,5,12,.30)}

/* the hero: the art whole, at its own shape, with the title set in its upper-right band */
header#title-block-header.hero{position:relative;overflow:hidden;margin:6px 0 0;padding:0;text-align:center;border:1px solid rgba(226,189,108,.30);border-radius:22px;
  background:#000;box-shadow:0 24px 60px rgba(0,0,0,.45);container-type:inline-size}
.hero-art{width:100%;aspect-ratio:2000/800;background:var(--art) center/100% 100% no-repeat}
.hero-text{position:absolute;left:55%;width:45%;top:0;height:25.6%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:.6cqw 1cqw 0}
.hero h1.title{margin:0;padding:0;border:0;color:var(--cream);font:500 3.05cqw/1.04 var(--display);letter-spacing:.012em;text-shadow:0 2px 18px rgba(0,0,0,.6)}
.hero h1.title .t-line{display:block}
.hero .rule{width:5.2cqw;height:1px;background:var(--gline);margin:.85cqw 0 .8cqw}
.hero p.author{margin:0;color:var(--gold2);font:500 .9cqw/1 var(--display);letter-spacing:.34em;text-transform:uppercase;padding-left:.34em}
@media (max-width:760px){
  .hero-text{position:static;width:auto;height:auto;padding:20px 12px 16px}
  .hero h1.title{font-size:clamp(1.55rem,7.2vw,2.3rem)} .hero .rule{width:54px;margin:12px 0 11px} .hero p.author{font-size:.72rem}
}

.titlemeta{margin:18px 0 26px;padding:20px 28px;border:1px solid var(--line);border-radius:18px;background:var(--panel)}
.titlemeta p.subtitle{font:italic 500 1.45rem/1.35 var(--display);color:var(--gold2);margin:.1em 0 .35em}
.titlemeta p.date{font:500 .98rem var(--serif);letter-spacing:.05em;color:var(--muted);margin:0 0 .6em}
.titlemeta p{margin:.5em 0 .1em}

nav#TOC{position:sticky;top:14px;float:left;width:300px;max-height:calc(100vh - 28px);overflow:auto;margin:0 24px 30px 0;padding:18px;
  border:1px solid var(--line);border-radius:18px;background:rgba(4,7,17,.86);box-shadow:0 14px 34px rgba(0,0,0,.4);font:14px/1.38 var(--serif);hyphens:manual}
nav#TOC ul{list-style:none;padding-left:11px;margin:0} nav#TOC>ul{padding-left:0} nav#TOC li{margin:5px 0}
nav#TOC a{color:var(--ink);text-decoration:none;display:block;padding:4px 6px;border-radius:6px}
nav#TOC a:hover{color:var(--gold2);background:rgba(226,189,108,.08)}
nav#TOC ul ul a{color:var(--muted);font-size:13px}

section.level1{margin:24px 0 24px 324px;padding:20px 28px 28px;border:1px solid var(--line);border-radius:18px;background:var(--panel);box-shadow:0 14px 40px rgba(0,0,0,.30)}
h1,h2,h3,h4,h5{font-family:var(--display);font-weight:600;letter-spacing:.005em;scroll-margin-top:18px}
section.level1>h1{color:var(--cream);font-size:2.35rem;line-height:1.15;border-bottom:1px solid var(--gline);padding-bottom:.25em;margin:.35em 0 .6em}
h2{color:var(--gold2);font-size:1.8rem;line-height:1.2;border-bottom:1px solid var(--line);padding-bottom:.18em;margin-top:1.8em}
h3{color:var(--cream);font-size:1.42rem;margin-top:1.6em} h4,h5{color:var(--gold2)}
p{margin:1em 0} p,li{color:var(--ink)} strong{color:var(--cream)}
a{color:var(--mesh);text-underline-offset:2px} a:hover{color:#cfe0ff}
ol,ul{padding-left:1.7em} li>ol,li>ul{margin-top:0}
blockquote{margin:1em 0;border-left:3px solid var(--gold);background:rgba(93,127,208,.10);padding:14px 18px;border-radius:0 12px 12px 0;color:var(--cream)}
hr{border:0;border-top:1px solid var(--line);margin:34px 0}
pre,code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace;hyphens:manual}
code{font-size:85%;color:var(--gold2);background:rgba(127,166,232,.10);padding:.08em .26em;border-radius:4px;white-space:pre-wrap}
pre{margin:1em 0;overflow:auto;background:rgba(3,5,12,.82);border:1px solid var(--line);border-radius:12px;padding:16px;color:var(--cream);font-size:13.5px;line-height:1.5}
pre code{background:transparent;padding:0;color:inherit;font-size:inherit;white-space:pre}
table{border-collapse:collapse;display:block;width:max-content;max-width:100%;overflow:auto;margin:18px 0 24px;background:rgba(6,10,24,.70);border:1px solid var(--line);border-radius:10px;font-variant-numeric:lining-nums tabular-nums}
th,td{padding:9px 11px;border-bottom:1px solid rgba(140,168,240,.12);vertical-align:top;text-align:left}
th{color:var(--gold2);background:rgba(30,44,96,.92);font-family:var(--serif);white-space:nowrap}
tr:nth-child(even) td{background:rgba(127,166,232,.035)}
table caption{color:var(--muted);padding:8px 11px;text-align:left}
figure{margin:1.6em 0;padding:16px 18px 14px;background:rgba(3,5,13,.58);border:1px solid var(--line);border-radius:16px}
figure img{display:block;width:100%;max-width:1150px;height:auto;margin:0 auto;background:#fff;border-radius:8px}
figcaption{color:var(--muted);font-size:.93em;margin-top:.6em;line-height:1.45}
img{max-width:100%}
.math.display{display:block;overflow:visible;border:none;background:none;padding:0;margin:1.1em 0}
mjx-container{color:var(--cream)} mjx-container[display="true"]{overflow:visible!important;margin:1em 0}
html body mjx-container>mjx-assistive-mml{width:1px!important;max-width:1px!important;height:1px!important;overflow:hidden!important}
span.smallcaps{font-variant:small-caps}

@media (max-width:1050px){
  body{padding:16px 18px 60px}
  nav#TOC{position:relative;float:none;width:auto;max-height:360px;margin:0 0 22px}
  section.level1{margin-left:0;padding:18px} .titlemeta{padding:16px 18px}
}
@media (max-width:640px){
  body{font-size:17px;padding:12px 14px 48px} figure{padding:10px} section.level1>h1{font-size:1.9rem} h2{font-size:1.5rem}
  mjx-container:not([display="true"]){display:inline-block!important} p,li,figcaption,blockquote{overflow-wrap:anywhere} code{word-break:break-all}
}
@page{size:letter;margin:0}
@media print{
  html,body{background:transparent} #bgart,nav#TOC,body::before{display:none!important}
  body{padding:0 16mm;font-size:11.5pt}
  header#title-block-header.hero{break-inside:avoid}
  section.level1{margin-left:0;padding:14px 20px;box-shadow:none}
  figure{break-inside:avoid} h1,h2,h3{break-after:avoid}
  table{display:table;width:100%;table-layout:auto;font-size:8.6pt} th{white-space:normal} th,td{padding:4px 6px;overflow-wrap:anywhere}
  pre,code{white-space:pre-wrap!important;overflow-wrap:anywhere}
}
'''.replace('ARTDATA', art)

FIT = r'''
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
'''

head = t[:head_end]
head = re.sub(r'<style>.*?</style>', lambda m: '<style>\n' + '\n'.join(fonts) + CSS + '</style>', head, count=1, flags=re.S)
head = head.replace('</head>', '<script>' + FIT + '</script>\n</head>')

subtitle = 'Hidden Angular Structure, the Flux–Shear Link and the Threshold for Primordial Black Hole Formation'   # from \title, as in the PDF
hero = f'''<div id="bgart" aria-hidden="true"></div>
<header id="title-block-header" class="hero">
<div class="hero-art" aria-hidden="true"></div>
<div class="hero-text">
<h1 class="title"><span class="t-line">What the Neutrino State</span> <span class="t-line">Must Keep</span></h1>
<div class="rule" aria-hidden="true"></div>
<p class="author">{author}</p>
</div>
</header>
<div class="titlemeta">
<p class="subtitle">{subtitle}</p>
<p class="date">{date}</p>
{advisory}
</div>'''
abstract = f'<section class="level1" id="abstract">\n<h1>{abstract_title}</h1>{abstract_body.rstrip()}\n</section>'
out = head + '<body>\n' + hero + '\n' + nav + '\n' + abstract + '\n' + '\n'.join(sections) + '\n</body>\n</html>\n'
open(OUT, 'w', encoding='utf-8').write(out)
print('sections', len(sections), 'toc entries', out.count('<li><a href="#'), 'bytes', len(out))
