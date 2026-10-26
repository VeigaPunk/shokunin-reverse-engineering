#!/usr/bin/env python3
"""Pre-freeze validator and predictor for the P39-C2 sqfs triage-table grammar.

This is NOT the frozen counter (`tools/round-39/sqfs-triage.py`, owned by the L1). It
implements the L1's stated grammar so the six shortcut controls can be checked for
well-formedness and scored against the seven draft classes before the freeze.

Usage:
  triage-eval.py <control.md> [--class-signatures class-signatures.json] [--json-out F]
  triage-eval.py --bounds [--class-signatures class-signatures.json]

Exit: 0 evaluated, 2 malformed table / envelope / grammar use.
"""
import argparse
import fnmatch
import json
import os
import shlex
import sys

MARKER = '<!-- sqfs-triage-table v1 -->'
SECTION = '## Queue-drain craft'
HEADER = [
    'label', 'handler', 'gap kinds', 'dependencies', '-be in child argv',
    'symlink removed', 'published files', 'cause -> action', 'source',
]


class Malformed(Exception):
    pass


def cell(raw):
    return raw.strip().strip('`').strip()


def parse_table(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    start = None
    for i, line in enumerate(lines):
        if line.strip() == SECTION or line.startswith(SECTION + ' '):
            start = i
            break
    if start is None:
        raise Malformed(f'{path}: no {SECTION!r} heading')
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    mark = None
    for i in range(start, end):
        if MARKER in lines[i]:
            mark = i
            break
    if mark is None:
        raise Malformed(f'{path}: no marker {MARKER!r} in {SECTION!r}')
    first = None
    for i in range(mark + 1, end):
        if lines[i].lstrip().startswith('|'):
            first = i
            break
    if first is None:
        raise Malformed(f'{path}: no table after marker')
    block = []
    i = first
    while i < end and lines[i].lstrip().startswith('|'):
        block.append(lines[i])
        i += 1
    rows = [[cell(c) for c in ln.strip().strip('|').split('|')] for ln in block]
    if len(rows) < 2:
        raise Malformed(f'{path}: table needs a header and a separator')
    if rows[0] != HEADER:
        raise Malformed(f'{path}: header {rows[0]!r} != {HEADER!r}')
    sep = rows[1]
    if len(sep) != len(HEADER) or not all(
            c.replace(':', '').replace('-', '') == '' and '-' in c for c in sep):
        raise Malformed(f'{path}: bad separator row {sep!r}')
    rules = []
    for r in rows[2:]:
        if len(r) != len(HEADER):
            raise Malformed(f'{path}: row has {len(r)} cells, want {len(HEADER)}: {r!r}')
        rules.append(r)
    if not rules:
        raise Malformed(f'{path}: no data rows')
    return rules


def unwrap(obj):
    if isinstance(obj, dict) and isinstance(obj.get('data'), dict):
        return obj['data']
    if isinstance(obj, dict):
        return obj
    raise Malformed('envelope is not an object')


def scan_typename(node, name):
    if isinstance(node, dict):
        if node.get('__typename__') == name:
            return True
        return any(scan_typename(v, name) for v in node.values())
    if isinstance(node, list):
        return any(scan_typename(v, name) for v in node)
    return False


def features(obj):
    data = unwrap(obj)
    nr = data.get('normalized_result') or {}
    H = {c.get('handler') for c in (nr.get('chunks') or [])
         if isinstance(c.get('handler'), str) and c['handler'].startswith('squashfs')}
    G = {g.get('kind') for g in (nr.get('extraction_gaps') or []) if g.get('kind')}
    D = set()
    for g in nr.get('extraction_gaps') or []:
        for d in g.get('dependencies') or []:
            D.add(d)
    be_hits = []
    for diag in nr.get('diagnostics') or []:
        rpt = diag.get('report') or {}
        cmd = rpt.get('command')
        if cmd is None:
            continue
        toks = shlex.split(cmd) if isinstance(cmd, str) else [str(t) for t in cmd]
        if not any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in toks):
            continue
        be_hits.append('-be' in toks)
    be = 'yes' if any(be_hits) else ('no' if be_hits else 'n/a')
    sr = 'no'
    for diag in nr.get('diagnostics') or []:
        if (diag.get('report') or {}).get('__typename__') == 'MaliciousSymlinkRemoved':
            sr = 'yes'
    if sr == 'no' and scan_typename((data.get('raw_result') or {}).get('report'),
                                    'MaliciousSymlinkRemoved'):
        sr = 'yes'
    return {'H': sorted(H), 'G': sorted(G), 'D': sorted(D), 'BE': be, 'SR': sr,
            'P': len(nr.get('files') or [])}


def match_rule(rule, f):
    label, handler, gaps, deps, be, sr, pub = rule[0], rule[1], rule[2], rule[3], rule[4], rule[5], rule[6]
    # handler
    if handler == '*':
        pass
    elif handler == 'none':
        if f['H']:
            return False
    elif not any(fnmatch.fnmatchcase(h, handler) for h in f['H']):
        return False
    # sets
    for raw, actual in ((gaps, set(f['G'])), (deps, set(f['D']))):
        if raw == '*':
            continue
        if raw == 'none':
            if actual:
                return False
            continue
        want = [x.strip() for x in raw.split('+')]
        if not want or not all(want):
            raise Malformed(f'bad set cell {raw!r}')
        if actual != set(want):
            return False
    if be not in ('*', 'yes', 'no', 'n/a'):
        raise Malformed(f'bad -be cell {be!r}')
    if be != '*' and f['BE'] != be:
        return False
    if sr not in ('*', 'yes', 'no', 'n/a'):
        raise Malformed(f'bad symlink-removed cell {sr!r}')
    if sr != '*' and f['SR'] != sr:
        return False
    if pub == '*':
        pass
    elif pub == '0':
        if f['P'] != 0:
            return False
    elif pub == '>0':
        if f['P'] <= 0:
            return False
    else:
        raise Malformed(f'bad published-files cell {pub!r}')
    return True


def label_for(rules, f):
    for rule in rules:
        if match_rule(rule, f):
            return rule[0]
    return 'unclassified'


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('control', nargs='?')
    ap.add_argument('--class-signatures', default='class-signatures.json')
    ap.add_argument('--json-out')
    ap.add_argument('--bounds', action='store_true')
    ap.add_argument('--envelope')
    a = ap.parse_args(argv)
    try:
        if a.envelope:
            print(json.dumps(features(json.load(open(a.envelope))), indent=2))
            return 0
        sigs = json.load(open(a.class_signatures))
        base = os.path.dirname(os.path.abspath(a.class_signatures))
        feats = {k: features(json.load(open(os.path.join(base, v))))
                 for k, v in sigs.items()}
        if a.bounds:
            # The grammar only reads P as 0 vs >0, so compare that bucket, not the count.
            bucket = {k: {**feats[k], 'P': '0' if feats[k]['P'] == 0 else '>0'} for k in feats}
            names = sorted(feats)
            out = []
            for i, x in enumerate(names):
                for y in names[i + 1:]:
                    diff = [k for k in ('H', 'G', 'D', 'BE', 'SR', 'P')
                            if bucket[x][k] != bucket[y][k]]
                    rec = {'pair': [x, y], 'differ_in': diff,
                           'separable': bool(diff)}
                    out.append(rec)
                    if len(diff) <= 1:
                        print(f'{x} vs {y}: differ only in {diff}')
            if any(not r['separable'] for r in out):
                print('NOT_SEPARABLE: ' + json.dumps(
                    [r['pair'] for r in out if not r['separable']]))
            if a.json_out:
                open(a.json_out, 'w').write(json.dumps(out, indent=2) + '\n')
            return 0
        rules = parse_table(a.control)
        per = {k: label_for(rules, feats[k]) for k in sorted(feats)}
        score = sum(1 for k, v in per.items() if v == k) * 2
        total = len(feats) * 2
        out = {'control': a.control, 'rules': len(rules), 'per_class_label': per,
               'score': f'{score}/{total}', 'score_n': score, 'n': total}
        print(json.dumps(out, indent=2))
        if a.json_out:
            open(a.json_out, 'w').write(json.dumps(out, indent=2) + '\n')
        return 0
    except Malformed as e:
        print(f'UNEVALUABLE: {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
