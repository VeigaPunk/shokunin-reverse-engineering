import sys, importlib.util, json, re
D = '/fast/scratch/hyaku/kaidoku-r49/W2C2Rescore/clone.m6J4'
R = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('c2', D + '/tools/round-49/c2-mismatch.py')
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
g = c2.Git(D)
sx = c2.text(g.show(R, 'corpus/SOURCES.md'))
s147 = [l for l in sx.split('\n') if l.startswith('| S147 |')][0]
pop = g.show(R, 'corpus/evidence/round-49/c2/popper.html')
norm = c2.html_norm(pop)
for q, n in c2.quotes(s147.split('|')[6] if False else [c for c in c2.cells(s147)][5]):
    i = norm.find(re.sub(r'\s+',' ',q).strip())
    print('quote:', q[:70], '| stated', n, '| found at', i, '| section:', c2.section_of(norm, i))
# find section-3 sentences: text between the marker of '3. The Problem of Demarcation' and next marker
heads = [(m.start(), m.group(1)) for m in re.finditer('\x01(.*?)\x02', norm)]
for hpos, h in heads[:12]:
    print('HEAD', hpos, h[:80])

sec3 = norm[12990:16713]
sec3 = sec3[sec3.find('\x02')+1:]
# pick a sentence of 12-20 words with no quotes/markers
sents = re.split(r'(?<=[.])\s+', sec3)
pick = None
for s in sents:
    s2 = s.strip()
    w = len(s2.split())
    if 12 <= w <= 20 and '"' not in s2 and '\x01' not in s2 and '\x02' not in s2 and s2 in norm:
        pick = s2; break
print('PICK', len(pick.split()), repr(pick))
new_quote_cell = '"%s" (%d words)' % (pick, len(pick.split()))
old_cell = [c for c in c2.cells(s147)][5]
q1 = '"falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific" (21 words)'
print('q1 in cell:', q1 in s147)
variants = {
 'V1 quote moved to section 3, anchor keeps parenthetical naming section 3': s147.replace(q1, new_quote_cell, 1),
 'V2 same but parenthetical about section 3 removed': s147.replace(q1, new_quote_cell, 1).replace(' (they precede `3. The Problem of Demarcation`)', '', 1),
}
out = {}
for name, row in variants.items():
    over = {'corpus/SOURCES.md': sx.replace(s147, row, 1).encode()}
    o = c2.Overlay(g, R, over)
    got = c2.score(o, R)
    print(name, '-> red', sorted(k for k,v in got.items() if v), {k:v for k,v in got.items() if v})
