# Locate quotes in the committed SEP snapshot after tag stripping; report nearest preceding heading.
import html, re, sys
from html.parser import HTMLParser

SNAP = sys.argv[1]
raw = open(SNAP, 'rb').read().decode('utf-8')

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []; self.heads = []; self.skip = 0; self.hdepth = None; self.hbuf = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5'):
            self.hdepth = tag; self.hbuf = []
        if tag in ('p', 'div', 'li', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'tr', 'td', 'th', 'section'):
            self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip -= 1
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5') and self.hdepth == tag:
            t = ''.join(self.hbuf).strip()
            self.heads.append((len(''.join(self.out)), tag, re.sub(r'\s+', ' ', t)))
            self.hdepth = None
        if tag in ('p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5'):
            self.out.append('\n')
    def handle_data(self, d):
        if self.skip: return
        self.out.append(d)
        if self.hdepth: self.hbuf.append(d)

p = P(); p.feed(raw)
text = ''.join(p.out)
def norm(s):
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    return re.sub(r'\s+', ' ', s).strip()
body = norm(text)
print('snapshot bytes', len(raw.encode('utf-8')), 'normalised body chars', len(body))
# headings with offsets in normalised body
heads = []
for off, tag, t in p.heads:
    if t: heads.append((len(norm(text[:off])), tag, t))
quotes = [
 "falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific",
 "it is consistent with all possible observations, is unscientific",
]
for q in quotes:
    n = len(q.split())
    hits = [m.start() for m in re.finditer(re.escape(norm(q)), body)]
    print(f'\nQUOTE ({n} words) hits={len(hits)} offsets={hits}')
    for h in hits:
        prev = [x for x in heads if x[0] <= h]
        nxt = [x for x in heads if x[0] > h]
        print('  nearest preceding heading:', prev[-1] if prev else None)
        print('  next heading:', nxt[0] if nxt else None)
print('\nHEADINGS (h1-h5, normalised offsets):')
for h in heads: print(' ', h)
