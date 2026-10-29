# Locate a quote in a committed snapshot after tag strip + whitespace collapse (same normalisation as round-49 html_norm) and report the nearest preceding heading-like text.
import re, sys, html
path, quote = sys.argv[1], sys.argv[2]
raw = open(path, encoding='utf-8', errors='replace').read()
# headings: h1-h6 tags, and <a name>/id text in man pages
heads = [(m.start(), re.sub(r'<[^>]+>', '', m.group(0))) for m in re.finditer(r'<h[1-6][^>]*>.*?</h[1-6]>', raw, re.S|re.I)]
txt_chars = []
pos_map = []
in_tag = False
for i, ch in enumerate(raw):
    if ch == '<': in_tag = True; continue
    if ch == '>' and in_tag: in_tag = False; continue
    if not in_tag: txt_chars.append(ch); pos_map.append(i)
text = html.unescape(''.join(txt_chars))
norm = re.sub(r'\s+', ' ', text)
q = re.sub(r'\s+', ' ', quote)
idx = norm.find(q)
print('located', idx >= 0, 'count', norm.count(q))
if idx >= 0:
    # nearest preceding h-tag by raw offset
    off = pos_map[min(idx, len(pos_map)-1)]
    prev = [h for h in heads if h[0] < off]
    print('raw_offset', off, 'nearest_heading', re.sub(r'\s+',' ', (prev[-1][1] if prev else 'NONE')).strip()[:120])
    # all headings text in order (first 40)
    print('headings_in_order', [re.sub(r'\s+',' ',h[1]).strip()[:40] for h in heads][:40])
