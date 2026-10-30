#!/usr/bin/env python3
"""Read-only probe: over the committed round-50 envelopes and oracle tables,
report for every char-device census row whether it carries a disposition
(published file, unpublished entry, extraction gap or removal diagnostic).

Usage: python3 -I -B law-device-disposition.py --lane <LANE>
Exit 0: every device row has no disposition (the law's measured width).
Exit 1: some device row carries a disposition.
Exit 2: an input is missing (could-not-evaluate).
"""
import argparse, json, os, sys

KIND = 'char-device'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    a = ap.parse_args()
    lane = a.lane
    ids = ['c6430', 'c6490', 'g7581', 'g7582']
    total = 0
    with_disposition = 0
    problems = []
    for cid in ids:
        tsv = os.path.join(lane, 'tools/round-50/oracle', f'{cid}.nonregular.tsv')
        env = os.path.join(lane, 'corpus/evidence/round-50/c1', cid, 'after.json')
        if not os.path.exists(tsv) or not os.path.exists(env):
            problems.append(f'missing input for {cid}')
            continue
        dev = []
        with open(tsv, encoding='utf-8') as fh:
            for line in fh:
                line = line.rstrip('\n')
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 2 and parts[1] == KIND:
                    dev.append(parts[0])
        d = json.load(open(env, encoding='utf-8'))
        nr = d['normalized_result']
        pub = {f.get('relative_path', '') for f in nr.get('files') or []}
        unpub = {u.get('relative_path', '') for u in nr.get('unpublished_entries') or []}
        gaps = nr.get('extraction_gaps') or []
        gap_paths = {g.get('relative_path') for g in gaps if g.get('relative_path')}
        gap_kinds = {}
        for g in gaps:
            gap_kinds[g.get('kind')] = gap_kinds.get(g.get('kind'), 0) + 1
        diag_links = set()
        for diag in nr.get('diagnostics') or []:
            rep = diag.get('report') or {}
            if rep.get('__typename__') == 'MaliciousSymlinkRemoved':
                diag_links.add(rep.get('link', ''))
        for path in dev:
            total += 1
            hits = []
            for p in pub:
                if p == path or p.endswith('/' + path):
                    hits.append(f'published:{p}')
            for p in unpub:
                if p == path or p.endswith('/' + path):
                    hits.append(f'unpublished:{p}')
            for p in gap_paths:
                if p == path or p.endswith('/' + path):
                    hits.append(f'gap:{p}')
            for p in diag_links:
                if p.endswith('/' + path):
                    hits.append(f'removed:{p}')
            if hits:
                with_disposition += 1
                print(f'{cid}\t{path}\tDISPOSITION\t{hits}')
        dl = [g for g in gaps if g.get('kind') == 'depth-limited']
        for g in dl:
            print(f'{cid}\tdepth-limited\tinput_path={g.get("input_path")}\t'
                  f'relative_path={g.get("relative_path")}\t'
                  f'continuation_id={(g.get("continuation_id") or "")[:16]}')
        print(f'{cid}\tgap_kinds={json.dumps(gap_kinds, sort_keys=True)}')
    if problems:
        for p in problems:
            print('PROBLEM', p, file=sys.stderr)
        return 2
    print(f'TOTAL device rows={total} with_disposition={with_disposition}')
    return 0 if with_disposition == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
