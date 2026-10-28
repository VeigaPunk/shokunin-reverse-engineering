# C1PlanMatch probe: exercises the frozen counter's own functions (imported read-only from the
# dev-freeze clone of the draft) on predicate edges the plan sentences name. Writes nothing.
import importlib.util, json, hashlib
CL = '/fast/scratch/hyaku/kaidoku-r49/C1PlanMatch/clone/tools/round-49/'
FIX = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-42/c2/fixtures/'
spec = importlib.util.spec_from_file_location('c1c', CL + 'c1-counter.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
car = json.load(open(CL + 'carriers.json'))
print('## layout_probe: pristine carriers vs the three CTL-C1-5 mutations (probe is never reached by the control)')
for c in car['carriers']:
    raw = open(FIX + c['path'].split('/')[-1], 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == c['sha256']
    e = c.get('endian') or 'le'; bo = 'big' if e == 'be' else 'little'
    base = m.layout_probe(raw, c)
    res = []
    for name, off, val in [('bad-magic', 0, b'XXXX'), ('swapped-s_major', 28, (3).to_bytes(2, bo)), ('swapped-s_minor', 30, (9).to_bytes(2, bo))]:
        mm = bytearray(raw); mm[off:off + len(val)] = val
        r = m.layout_probe(bytes(mm), c)
        res.append('%s ok=%s' % (name, r.get('ok')))
    print(c['id'], 'pristine ok=%s' % base.get('ok'), '|', '; '.join(res))
print('## provenance_ok (run_provenance_ok clause)')
for p in ['/fast/scratch/hyaku/kaidoku-r49/x/corpus/evidence/round-49/c1/v1le',
          '/fast/scratch/hyaku/kaidoku-r42/x/kaidoku-r49/y',
          '/tmp/kaidoku-r49/x',
          '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-49/c1/v1le',
          'relative/kaidoku-r49/x']:
    print(repr(p), '->', m.provenance_ok(p))
print('## frontier_note token: STEM alone satisfies the SquashFS v1/v2 token')
print('SQFS12 match on STEM:', m.SQFS12_TEXT_RE.search(m.STEM).group(0))
line = 'Round-49 frontier note, 2026-10-28: see `' + m.STEM + '`.'
print('frontier_note predicate on a line with no SquashFS text but the stem ->',
      m.FRONTIER_MARK in line and m.STEM in line and bool(m.SQFS12_TEXT_RE.search(line)))
print('## gap rule constant vs docstring')
print('GAP_RULE structural =', m.GAP_RULE['structural'], '| counter docstring line 17-18 says "at most one structural depth-limited"')
print('## carriers.json top-level target key present =', 'target' in car, '(counter docstring: "`target` frozen in carriers.json")')
