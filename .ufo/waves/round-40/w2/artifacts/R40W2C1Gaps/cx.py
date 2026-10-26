#!/usr/bin/env python3
"""Counterexample battery: probe the frozen gap rule for looseness/tightness."""
import importlib.util, json, copy, collections

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('c1c', LANE + '/tools/round-40/c1-counter.py')
c1c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1c)

model, _ = c1c.gap_rule_model(open(LANE + '/.ufo/waves/round-40/c1/gap-rule.json', 'rb').read())

def env_of(p):
    d = json.load(open(p))
    return d['data'] if isinstance(d, dict) and isinstance(d.get('data'), dict) else d

L1 = env_of(LANE + '/corpus/evidence/round-40/c1/L1/after.json')
L2 = env_of(LANE + '/corpus/evidence/round-40/c1/L2/after.json')
V1 = env_of(LANE + '/corpus/evidence/round-40/c1/V1/after.json')
nonregL1, _ = c1c.parse_nonregular(open(LANE + '/corpus/evidence/round-40/c1/L1/nonregular.tsv', 'rb').read())
nonregL2, _ = c1c.parse_nonregular(open(LANE + '/corpus/evidence/round-40/c1/L2/nonregular.tsv', 'rb').read())
nonregV1, _ = c1c.parse_nonregular(open(LANE + '/corpus/evidence/round-40/c1/V1/nonregular.tsv', 'rb').read())

def gaps_of(e):
    return [g for g in c1c.gaps(e) if isinstance(g, dict)]

baseL1 = gaps_of(L1)
print('L1 base gaps:', [(g['kind'], g['relative_path']) for g in baseL1])

def probe(name, gaps_list, nonreg, expect, note=''):
    ok, why = c1c.gap_check(gaps_list, nonreg, model)
    verdict = 'AS-EXPECTED' if ok == expect else '*** UNEXPECTED ***'
    print(f'  {name:52s} gap_check={ok!s:5s} {verdict}  | {why}')
    if note:
        print(f'    -> {note}')

def g(kind, rp):
    return {'kind': kind, 'relative_path': rp, 'dependencies': [], 'handler': None,
            'input_path': ('$output/firmware.bin_extract' if rp is None else '$output/firmware.bin_extract/' + rp),
            'provider_id': None, 'range': None, 'root_file_range': None,
            'continuation_id': 'f' * 64}

print()
print('== LOOSENESS probes (wrong receipts the rule alone accepts) ==')
probe('CX-A duplicate unpublished-entry on one symlink',
      baseL1 + [g('unpublished-entry', 'firmware.bin_extract/bin/sh')], nonregL1, True,
      'rule has no per-entry cap; claim text says ONE per symlink')
probe('CX-B fabricated deep-prefix path satisfies required gap',
      [baseL1[0], g('unpublished-entry', 'deep/nested/bin/sh'), baseL1[2]], nonregL1, True,
      'gap attributed to bin/sh via suffix; path is no real entry')
probe("CX-C './'-prefixed gap path",
      [baseL1[0], g('unpublished-entry', './bin/sh'), baseL1[2]], nonregL1, True,
      'same_rel endswith accepts ./bin/sh')
probe('CX-D symlink materialised as regular file, gap kept',
      baseL1, nonregL1, True, 'gap_check alone passes; see sibling binding below')
d = copy.deepcopy(L1)
d['normalized_result']['files'] = d['normalized_result']['files'] + [
    {'relative_path': 'firmware.bin_extract/bin/sh', 'sha256': 'a' * 64, 'size': 10}]
esc = c1c.nonregular_published(c1c.published(d), nonregL1)
print(f'  CX-D sibling nonregular_published -> {esc} (caught by nonregular_unpublished_ok)')
probe('CX-E zero structural gaps (drop depth-limited)',
      baseL1[1:], nonregL1, True, '"at most one" allows zero; fresh run has 1 -> projection catches')
probe('CX-F exact duplicate depth-limited gap',
      baseL1 + [copy.deepcopy(baseL1[0])], nonregL1, False, 'structural cap 1 enforced')
probe('CX-R swapped symlink gap paths',
      [baseL1[0], baseL1[2], baseL1[1]], nonregL1, True, 'harmless: both entries still covered')
probe('CX-S dependencies unchecked on structural gap',
      [dict(baseL1[0], dependencies=['whatever']), baseL1[1], baseL1[2]], nonregL1, True,
      'gap_check never reads dependencies')
nr2 = copy.deepcopy(L1)
nr2['normalized_result']['unpublished_entries'] = []
probe('CX-T unpublished_entries field emptied, gaps kept', baseL1, nonregL1, True,
      'gap_check reads only extraction_gaps; projection compares the field')

print()
print('== TIGHTNESS probes (honest shapes the rule rejects) ==')
probe('CX-O honest gap on usr/lib multi-matches lib+usr/lib (L1 dirs)',
      [baseL1[0], g('unpublished-entry', 'firmware.bin_extract/usr/lib'), baseL1[2]], nonregL1, False,
      'suffix collision: len(hits)=2 -> honest symlink gap at usr/lib would be rejected')
esc_table = [('bin/escape', 'symlink'), ('etc', 'dir')]
probe('CX-U escaping symlink removed with MSR, no gap (recon t1/t2/t2b shape)',
      [], esc_table, False,
      'required[symlink]=true demands a gap unblob never records for removed links')
probe('CX-V same but with MSR diagnostic recorded in receipt',
      [], esc_table, False, 'gap_check has no diagnostics input at all')

print()
print('== NEGATIVE controls (must fail; rule not loose here) ==')
probe('N1 depth-limited WITH a path', baseL1 + [g('depth-limited', 'x')], nonregL1, False)
probe('N2 unknown-chunk-handler null path', baseL1 + [g('unknown-chunk-handler', None)], nonregL1, False)
probe('N3 unpublished-entry null path', baseL1 + [g('unpublished-entry', None)], nonregL1, False)
probe('N4 gap on a dir entry', baseL1 + [g('unpublished-entry', 'firmware.bin_extract/lib')], nonregL1, False)
probe('N5 gap on the char device (V1 table)', gaps_of(V1) + [g('unpublished-entry', 'firmware.bin_extract/dev/led')], nonregV1, False)
probe('N6 gap path matching nothing', baseL1 + [g('unpublished-entry', 'no/such/path')], nonregL1, False)
probe('N7 required gap dropped (etc/mtab)', [baseL1[0], baseL1[1]], nonregL1, False)
probe('N8 unknown gap kind on symlink', baseL1 + [g('weird-gap', 'firmware.bin_extract/bin/sh')], nonregL1, False)
probe('N9 structural kind outside the rule', baseL1 + [g('residual-chunk', None)], nonregL1, False)
probe('N10 empty-string path', baseL1 + [g('unpublished-entry', '')], nonregL1, False)
probe('N11 two depth-limited + one unknown-chunk-handler',
      baseL1 + [copy.deepcopy(baseL1[0]), g('unknown-chunk-handler', None)], nonregL1, False)

print()
print('== composite closure demo (projection vs mutated receipts, plus-extractor) ==')
for name, mut in (('CX-A dup gap', lambda e: e['normalized_result']['extraction_gaps'].append(g('unpublished-entry', 'firmware.bin_extract/bin/sh'))),
                  ('CX-B deep prefix', lambda e: e['normalized_result']['extraction_gaps'].__setitem__(1, g('unpublished-entry', 'deep/nested/bin/sh'))),
                  ('CX-E no depth-limited', lambda e: e['normalized_result']['extraction_gaps'].pop(0)),
                  ('CX-T empty unpub field', lambda e: e['normalized_result'].__setitem__('unpublished_entries', []))):
    m = copy.deepcopy(L1)
    mut(m)
    eq, keys, _ = c1c.projection_diff(c1c.projection(L1, 'plus-extractor'), c1c.projection(m, 'plus-extractor'), 'plus-extractor')
    print(f'  {name:24s} projection_equal={eq} differing={keys}')
