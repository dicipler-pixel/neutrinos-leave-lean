# SCRIPT: NU-V12-HTML  flatten, number citations, plain grade labels, pandoc, inline images, MathJax 3 from cdnjs
import re, base64, subprocess, sys
def flat(f):
    t = open(f).read()
    t = re.sub(r'\\input\{([^}]+)\}', lambda m: flat(m.group(1) + ('' if m.group(1).endswith('.tex') else '.tex')), t)
    def lst(m):
        try: body = open(m.group(1), errors='replace').read()
        except Exception: return ''
        return '\\begin{verbatim}\n' + body.replace('\\end{verbatim}', '\\end{verb atim}') + '\n\\end{verbatim}\n'
    return re.sub(r'\\lstinputlisting(?:\[[^\]]*\])?\{([^}]+)\}', lst, t)
t = flat('neutrinos_v12.tex')
keys = re.findall(r'\\bibitem\{([^}]+)\}', t); num = {k: i+1 for i, k in enumerate(keys)}
def cite(m):
    opt, ks = m.group(1), m.group(2).split(',')
    s = ','.join(str(num.get(k.strip(), '?')) for k in ks)
    return '[' + s + (', ' + opt if opt else '') + ']'
t = re.sub(r'~?\\cite(?:\[([^\]]*)\])?\{([^}]+)\}', lambda m: ' ' + cite(m), t)
t = re.sub(r'\\bibitem\{([^}]+)\}', lambda m: '\\item[[' + str(num[m.group(1)]) + ']] ', t)
t = t.replace('\\begin{thebibliography}{99}', '\\section*{References}\\begin{description}').replace('\\end{thebibliography}', '\\end{description}')
def grade(t):
    out, i = [], 0
    while True:
        j = t.find('\\grade{', i)
        if j < 0: out.append(t[i:]); return ''.join(out)
        k, d = j + 7, 1
        while d:
            d += {'{': 1, '}': -1}.get(t[k], 0); k += 1
        out.append(t[i:j] + '[' + t[j+7:k-1] + ']'); i = k
t = grade(t)
t = re.sub(r'\\text\{\[([^\]]*)\]\}', lambda m: '\\text{[' + re.sub(r'\$([^$]*)\$', lambda n: '$' + n.group(1) + '$', m.group(1)) + ']}', t)
open('flat_v12.tex', 'w').write(t)
subprocess.run(['pandoc', 'flat_v12.tex', '-s', '--mathjax', '--metadata', 'title=What the Neutrino State Must Keep', '-o', 'raw_v12.html'], check=True)
v6 = open('../paper_v6/neutrinos_v6.html').read(); v = open('raw_v12.html').read()
v = re.sub(r'<style>.*?</style>', lambda m: re.search(r'<style>.*?</style>', v6, re.S).group(0), v, count=1, flags=re.S)
v = re.sub(r'<script src="https://polyfill.io[^>]*>\s*</script>\s*', '', v)
v = re.sub(r'<script src="[^"]*MathJax.js"\s*type="text/javascript">.*?</script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js" async></script>', v, flags=re.S)
v = re.sub(r'src="([^"]+\.png)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode(open(m.group(1), 'rb').read()).decode() + '"', v)
open('neutrinos_v12.html', 'w').write(v)
print('cites', len(keys), 'unknown', t.count('[?'), 'imgs', v.count('<img'))
