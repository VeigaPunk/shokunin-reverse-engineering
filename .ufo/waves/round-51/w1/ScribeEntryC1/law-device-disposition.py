#!/usr/bin/env python3
"""Per-carrier device-row disposition census for the R51-C1 law (ScribeEntryC1).

Read-only over COMMITTED bytes: the four round-50 envelopes
(`corpus/evidence/round-50/c1/<id>/after.json`) and the four frozen non-regular
oracle tables (`tools/round-50/oracle/<id>.nonregular.tsv`).

For each carrier it reports, for the char-device rows of the independent census:
  * the number of device rows,
  * whether any of them carries an extraction gap (a path-resolved gap),
  * whether any of them is published as a regular file,
  * the gap kinds that do occur at all.

That is the measurement the device-accounting law rests on: a device row carries
no disposition at all. No REA run, no download, no lane write.

Usage: python3 -I -B law-device-disposition.py --lane <LANE>
Exit: 0 the census ran, 1 usage error, 2 an input could not be read.
"""
import argparse
import json
import os
import sys

CARRIERS = ('c6430', 'c6490', 'g7581', 'g7582')


def device_rows(path):
    rows = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            c = line.rstrip('\n').split('\t')
            if len(c) >= 2 and c[1] == 'char-device':
                rows.append((c[0], c[2] if len(c) > 2 else ''))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    args = ap.parse_args()
    for cid in CARRIERS:
        env_path = os.path.join(args.lane, 'corpus', 'evidence', 'round-50', 'c1',
                                cid, 'after.json')
        tab_path = os.path.join(args.lane, 'tools', 'round-50', 'oracle',
                                '%s.nonregular.tsv' % cid)
        try:
            with open(env_path, encoding='utf-8') as fh:
                env = json.load(fh)
            devs = device_rows(tab_path)
        except Exception as exc:                              # noqa: BLE001
            print('carrier %s unreadable: %s' % (cid, exc), file=sys.stderr)
            return 2
        nr = env['normalized_result']
        gaps = list(nr.get('unpublished_entries') or [])
        gap_paths = [g.get('relative_path') or '' for g in gaps]
        gap_kinds = sorted({g.get('kind') for g in gaps if g.get('kind')})
        pub_paths = [f.get('relative_path') or '' for f in nr.get('files') or []]

        def hits(rel, paths):
            return [p for p in paths
                    if p == rel or p.endswith('/' + rel)]

        with_gap = [rel for rel, _d in devs if hits(rel, gap_paths)]
        published = [rel for rel, _d in devs if hits(rel, pub_paths)]
        print('%s device_rows %d gap_kinds %r devices_with_gap %r '
              'devices_published %r gaps_total %d files %d'
              % (cid, len(devs), gap_kinds, with_gap, published,
                 len(gaps), len(nr.get('files') or [])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
