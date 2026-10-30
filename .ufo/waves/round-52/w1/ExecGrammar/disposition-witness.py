#!/usr/bin/env python3
"""Offline three-family disposition comparison for committed round-50 envelopes."""
import json
from pathlib import Path

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
IDS = ('c6430', 'c6490', 'g7581', 'g7582')


def rel_under(path, root):
    if not isinstance(path, str):
        return None
    path = path.removeprefix('$output/')
    root = root.removeprefix('$output/').strip('/')
    marker = root + '/'
    position = path.find(marker)
    return path[position + len(marker):] if position >= 0 else None


def check(env, nonreg, rule):
    nr = env['normalized_result']
    root = 'firmware.bin_extract'
    rows_at, by_rel = {}, {}
    for rel, kind, detail in nonreg:
        rel = rel.removeprefix('./').lstrip('/')
        rows_at.setdefault(rel, []).append(rel)
        by_rel[rel] = (kind, detail)
    gaps_by_entry, structural_counts = {}, {}
    gaps = nr.get('extraction_gaps', [])
    for gap in gaps:
        kind, path = gap.get('kind'), gap.get('relative_path')
        if path is None:
            if kind not in rule.get('structural', {}):
                return False, len(gaps), 0, len(nonreg), 'structural-kind'
            structural_counts[kind] = structural_counts.get(kind, 0) + 1
            continue
        if kind in rule.get('structural', {}):
            return False, len(gaps), 0, len(nonreg), 'structural-has-path'
        rel = rel_under(path, root)
        hits = rows_at.get(rel, []) if rel else []
        if len(hits) != 1 or kind not in rule.get('allowed', {}).get(by_rel[hits[0]][0], []):
            return False, len(gaps), 0, len(nonreg), 'gap-invalid'
        gaps_by_entry.setdefault(hits[0], []).append(kind)
    if any(n > rule['structural'][kind] for kind, n in structural_counts.items()):
        return False, len(gaps), 0, len(nonreg), 'structural-over'
    removed_by_entry = {}
    removed = rule.get('removed', {})
    for diag in nr.get('diagnostics', []):
        if (diag.get('report') or {}).get('__typename__') != removed.get('diagnostic'):
            continue
        rel = rel_under((diag.get('report') or {}).get('link'), root)
        hits = rows_at.get(rel, []) if rel else []
        if (len(hits) != 1 or by_rel[hits[0]][0] not in removed.get('kinds', [])
                or gaps_by_entry.get(hits[0])):
            return False, len(gaps), sum(removed_by_entry.values()), len(nonreg), 'removal-invalid'
        removed_by_entry[hits[0]] = removed_by_entry.get(hits[0], 0) + 1
    missing = 0
    for rel, (kind, detail) in by_rel.items():
        required = rule.get('required', {}).get(kind, bool(rule.get('allowed', {}).get(kind)))
        if not required or gaps_by_entry.get(rel) or removed_by_entry.get(rel):
            continue
        allowed = removed.get('silent', {}).get(kind, [])
        if detail is not None and detail in allowed:
            continue
        missing += 1
    return missing == 0, len(gaps), sum(removed_by_entry.values()), len(nonreg), f'missing={missing}'


def main():
    old = json.loads((ROOT / 'tools/round-50/gap-rule.json').read_text())
    # Claims law: no disposition is expected for non-regular device/special nodes.
    new = {
        'allowed': old['allowed'], 'structural': old['structural'],
        'required': {**old['required'], 'char-device': False, 'block-device': False,
                     'fifo': False, 'socket': False},
        'removed': {**old['removed'], 'silent': {}},
    }
    print('carrier | R50 verdict gaps removals nonregular detail | law verdict gaps removals nonregular detail')
    for cid in IDS:
        env = json.loads((ROOT / f'corpus/evidence/round-50/c1/{cid}/after.json').read_text())
        rows = []
        for line in (ROOT / f'tools/round-50/oracle/{cid}.nonregular.tsv').read_text().splitlines():
            cols = line.split('\t')
            if len(cols) >= 2:
                rows.append((cols[0], cols[1], cols[2] if len(cols) > 2 else None))
        old_result, new_result = check(env, rows, old), check(env, rows, new)
        def fmt(result):
            ok, ng, nr, nn, detail = result
            return f'{"PASS" if ok else "FAIL"} {ng} {nr} {nn} {detail}'
        print(f'{cid} | {fmt(old_result)} | {fmt(new_result)}')


if __name__ == '__main__':
    main()
