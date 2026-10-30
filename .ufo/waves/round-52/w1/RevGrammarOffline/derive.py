import collections
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
spec = importlib.util.spec_from_file_location('counter', ROOT / 'tools/round-50/c1-counter.py')
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)
old = json.loads((ROOT / 'tools/round-50/gap-rule.json').read_text())
new = copy.deepcopy(old)
new['claim'] = 'R52-C1'
for kind in ('char-device', 'block-device', 'fifo', 'socket'):
    new['allowed'][kind] = []
    new['required'][kind] = False
    new['removed']['silent'].pop(kind, None)

def relative(path, root):
    if path.startswith('$output/'):
        path = path[len('$output/'):]
    prefix = root + '/'
    return path[len(prefix):] if path.startswith(prefix) else None

def derive(env, rows, rule, root):
    by_path = {p.removeprefix('./'): (kind, detail) for p, kind, detail in rows}
    structural = collections.Counter()
    gapped = collections.Counter()
    removed = collections.Counter()
    errors = []
    for gap in env['normalized_result']['extraction_gaps']:
        kind, path = gap['kind'], gap['relative_path']
        if path is None:
            structural[kind] += 1
            if kind not in rule['structural']:
                errors.append('unallowed structural kind: ' + kind)
            continue
        rel = relative(path, root)
        if kind in rule['structural'] or rel not in by_path:
            errors.append('unresolved/structural path: ' + str(path))
        elif kind not in rule['allowed'].get(by_path[rel][0], []):
            errors.append('unallowed gap: ' + str(rel))
        else:
            gapped[rel] += 1
    for kind, n in structural.items():
        if n > rule['structural'].get(kind, -1):
            errors.append('structural over allowance: ' + kind)
    output = env['parameters']['output_directory']
    trusted = str(Path(output).parent) + '/'
    for diagnostic in env['normalized_result']['diagnostics']:
        report = diagnostic.get('report', {})
        if report.get('__typename__') != rule['removed']['diagnostic']:
            continue
        link = report.get('link', '')
        marker = '/' + root + '/'
        rel = link.rsplit(marker, 1)[1] if link.startswith(trusted) and marker in link else None
        if rel not in by_path or by_path[rel][0] not in rule['removed']['kinds'] or gapped[rel]:
            errors.append('invalid/exclusive removal: ' + str(rel))
        else:
            removed[rel] += 1
    missing, silent = [], []
    for rel, (kind, detail) in by_path.items():
        if not rule['required'].get(kind, bool(rule['allowed'].get(kind))):
            continue
        if gapped[rel] or removed[rel]:
            continue
        allowance = rule['removed']['silent'].get(kind, [])
        if detail in allowance or (detail == '' and 'empty-target' in allowance):
            silent.append(rel)
        else:
            missing.append(rel)
    errors.extend('missing: ' + p for p in sorted(missing))
    return {'pass': not errors, 'errors': errors, 'missing': sorted(missing),
            'structural': dict(structural), 'path_gaps': sum(gapped.values()),
            'removals': sum(removed.values()), 'silent': len(silent),
            'nonregular_rows': len(rows)}

result = {'axes': ['disposition correctness', 'receipt completeness', 'expectation reproducibility'],
          'law_model': new, 'carriers': {}}
for cid in ('c6430', 'c6490', 'g7581', 'g7582'):
    base = ROOT / 'corpus/evidence/round-50/c1' / cid
    run = json.loads((base / 'run.json').read_text())
    raw = (base / 'after.json').read_bytes()
    env = json.loads(raw)
    assert hashlib.sha256(raw).hexdigest() == run['receipt']['sha256']
    table = ROOT / 'tools/round-50/oracle' / (cid + '.nonregular.tsv')
    rows = []
    for line in table.read_text().splitlines():
        fields = line.split('\t')
        if not line.strip() or fields[:2] == ['relative_path', 'kind']:
            continue
        rows.append((fields[0].strip(), fields[1].strip().lower(), fields[2] if len(fields) > 2 else None))
    roots = [d['child_path'].removeprefix('$output/') for d in env['normalized_result']['derivations'] if d['handler'] == 'squashfs_v4_le']
    assert len(roots) == 1
    root = roots[0]
    published = [f['relative_path'] for f in env['normalized_result']['files']]
    hits = sorted(set(relative(p, root) for p in published) & {p for p, _, _ in rows})
    carrier = {'run_receipt_sha_verified': True, 'root': root,
               'run_gaps_total': run['receipt']['gaps'],
               'run_gaps_detail_length': len(run['receipt']['gaps_detail']),
               'nonregular_unpublished_ok': not hits,
               'nonregular_published': hits, 'census': dict(collections.Counter(k for _, k, _ in rows))}
    for label, rule in [('r50', old), ('law', new)]:
        value = derive(env, rows, rule, root)
        ok, why = counter.disposition_check(counter.gaps(env), counter.diagnostics(env), rows, rule, root, env['parameters']['output_directory'])
        assert ok == value['pass'], (cid, label, value, why)
        value['canonical_gaps_ok'] = ok
        value['canonical_reason'] = why
        value['disposition_verdict'] = value['pass'] and not hits
        carrier[label] = value
    result['carriers'][cid] = carrier
print(json.dumps(result, indent=2, sort_keys=True))
