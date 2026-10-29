# Locator check for a SOURCES row: normalise a committed snapshot (tags stripped, entities unescaped, whitespace collapsed),
# find the quote, and name the nearest preceding section word among the candidates. Exit 0 = nearest equals the row's anchor
# heading; 1 = differs (named); 2 = quote absent.
import re, html, sys
snap, quote, expected, cands = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split('|')
raw = open(snap, encoding='utf-8', errors='replace').read()
out = []; intag = False
for ch in raw:
    if ch == '<': intag = True; continue
    if ch == '>' and intag: intag = False; continue
    if not intag: out.append(ch)
txt = re.sub(r'\s+', ' ', html.unescape(''.join(out)))
q = re.sub(r'\s+', ' ', html.unescape(quote))
i = txt.find(q)
if i < 0: print(f'quote_absent snap={snap}'); sys.exit(2)
best = None
for c in cands:
    j = txt.rfind(c, 0, i)
    if j >= 0 and (best is None or j > best[0]): best = (j, c)
nearest = best[1] if best else 'NONE'
ok = nearest == expected
print(f'quote_at={i} nearest_heading={nearest!r} anchor={expected!r} match={ok}')
sys.exit(0 if ok else 1)
