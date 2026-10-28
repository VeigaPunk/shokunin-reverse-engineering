import sys, os
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import rd, wr, rep, line_rep, edit_s147, SRC, L, SC
def n23():  # LOG.md (append-only pointer) edited in the middle at REV
    t = rd("LOG.md"); i = len(t)//3; 
    wr('LOG.md', t[:i] + 'x' + t[i:])
def n24():  # S145 row edited (append-only)
    line_rep(SRC, r'^\| S145 \|', lambda l: l.replace('Karl Popper', 'Karl Popper (ed.)', 1))
def n25():  # S146 row edited
    line_rep(SRC, r'^\| S146 \|', lambda l: l.replace('HTTP 404', 'HTTP 410', 1))
def n26():  # S147 quote fabricated (same word count), pin unchanged
    line_rep(SRC, r'^\| S147 \|', lambda l: l.replace('if a theory is incompatible with possible empirical observations it is scientific', 'if a theory is compatible with every possible empirical observation it is scientific', 1))
def n27():  # duplicate S147 row appended
    t = rd(SRC).split('\n'); i = [k for k, l in enumerate(t) if l.startswith('| S147 |')][0]
    t.insert(i + 1, t[i]); wr(SRC, '\n'.join(t))
def n28():  # lesson A6 names a different row
    rep(L, '- A6 row=S147', '- A6 row=S999')
EXTRA = [('N23', 'LOG.md edited mid-file at REV (not append-only)', 'red A3', n23),
         ('N24', 'S145 row edited at REV (append-only)', 'red A6', n24),
         ('N25', 'S146 row edited at REV (append-only)', 'red A7', n25),
         ('N26', 'S147 quote fabricated with the same word count; pin unchanged', 'red A6 (quote not in snapshot)', n26),
         ('N27', 'duplicate S147 row appended', 'red A6 (duplicate id)', n27),
         ('N28', 'lesson A6 line names S999', 'red A6', n28)]
if __name__ == '__main__':
    import json, datetime
    res = []
    for label, desc, expect, fn in EXTRA:
        f.reset()
        try:
            fn(); msg = f.commit('forgery ' + label)
        except AssertionError as e:
            print(label, 'EDIT-ERROR', e); continue
        p = f.ctr('HEAD', f.F, False, tag=label)
        b = f.ctr('HEAD', f.F, True, tag=label) if p['exit'] == 0 else None
        print(label, 'plain exit', p['exit'], 'mism', p['mismatches'], 'red', p['red'], '| bat', (b or {}).get('exit'), (b or {}).get('battery_failing'), '|', expect)
        res.append(dict(label=label, desc=desc, expect=expect, commit=msg, plain=p, battery=b))
    json.dump(res, open(os.path.join(f.OUT, 'results-extra.json'), 'w'), indent=1, default=str)
