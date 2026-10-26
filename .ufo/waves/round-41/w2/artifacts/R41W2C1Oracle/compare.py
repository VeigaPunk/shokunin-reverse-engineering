#!/usr/bin/env python3
"""Compare regenerated oracle/nonregular/extract tables against committed tables.

For each carrier:
  committed oracle.tsv (lane)            vs  regenerated reader avm oracle.tsv
  committed nonregular.tsv (lane)        vs  regenerated reader avm nonregular.tsv
  regenerated reader avm oracle.tsv      vs  regenerated reader auto oracle.tsv
  regenerated reader avm nonregular.tsv  vs  regenerated reader auto nonregular.tsv
  regenerated sasquatch extract-files.tsv vs regenerated reader avm oracle.tsv
Counts by kind, every path, every sha, every detail.
"""
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
ORACLE = '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/oracle'
IDS = ['V3', 'V4', 'L3', 'L4']


def load_tsv(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh.read().splitlines():
            if not line:
                continue
            rows.append(tuple(line.split('\t')))
    return rows


def rowsets(rows):
    s = {}
    for r in rows:
        s[r[0]] = r
    return s, len(rows)


def report(label, committed, regen):
    co, cn = rowsets(committed)
    ro, rn = rowsets(regen)
    out = {'label': label, 'committed_rows': cn, 'regen_rows': rn,
           'match': co == ro}
    if co != ro:
        missing = sorted(set(co) - set(ro))
        extra = sorted(set(ro) - set(co))
        changed = sorted(k for k in set(co) & set(ro) if co[k] != ro[k])
        out['missing_count'] = len(missing)
        out['extra_count'] = len(extra)
        out['changed_count'] = len(changed)
        out['missing'] = missing[:20]
        out['extra'] = extra[:20]
        out['changed'] = {k: (co[k], ro[k]) for k in changed[:20]}
    return out


def kind_counts(rows):
    counts = {}
    for r in rows:
        counts[r[1]] = counts.get(r[1], 0) + 1
    return counts


def main():
    results = {}
    for cid in IDS:
        d = os.path.join(ORACLE, cid)
        lane = os.path.join(LANE, 'corpus/evidence/round-41/c1', cid)
        res = {'carrier': cid}
        res['committed_oracle'] = report(
            'committed vs regen avm oracle',
            load_tsv(os.path.join(lane, 'oracle.tsv')),
            load_tsv(os.path.join(d, 'oracle.tsv')))
        res['committed_nonregular'] = report(
            'committed vs regen avm nonregular',
            load_tsv(os.path.join(lane, 'nonregular.tsv')),
            load_tsv(os.path.join(d, 'nonregular.tsv')))
        res['avm_vs_auto_oracle'] = report(
            'avm vs auto oracle',
            load_tsv(os.path.join(d, 'oracle.tsv')),
            load_tsv(os.path.join(d, 'oracle-auto.tsv')))
        res['avm_vs_auto_nonregular'] = report(
            'avm vs auto nonregular',
            load_tsv(os.path.join(d, 'nonregular.tsv')),
            load_tsv(os.path.join(d, 'nonregular-auto.tsv')))
        res['sasquatch_vs_reader'] = report(
            'sasquatch extract vs reader avm oracle',
            load_tsv(os.path.join(d, 'oracle.tsv')),
            load_tsv(os.path.join(d, 'extract-files.tsv')))
        # kind counts of committed nonregular
        res['committed_nonregular_kinds'] = kind_counts(
            load_tsv(os.path.join(lane, 'nonregular.tsv')))
        res['regen_nonregular_kinds'] = kind_counts(
            load_tsv(os.path.join(d, 'nonregular.tsv')))
        res['extract_symlinks'] = None
        with open(os.path.join(d, 'rec.json')) as fh:
            rec = json.load(fh)
        res['reader_avm_inspect'] = rec.get('reader_avm_inspect')
        res['reader_auto_inspect'] = rec.get('reader_auto_inspect')
        res['sq_exit'] = rec.get('sq_exit')
        res['extract_symlinks'] = rec.get('extract_symlinks')
        res['carrier_pin_matches'] = rec.get('pin_matches')
        results[cid] = res
    with open(os.path.join(ORACLE, 'compare.json'), 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    for cid, res in results.items():
        print('== %s' % cid)
        for k in ('committed_oracle', 'committed_nonregular',
                  'avm_vs_auto_oracle', 'avm_vs_auto_nonregular',
                  'sasquatch_vs_reader'):
            r = res[k]
            print('  %-32s match=%s rows=%d/%d' % (
                r['label'], r['match'], r['committed_rows'], r['regen_rows']))
            if not r['match']:
                print('    missing=%d extra=%d changed=%d' % (
                    r.get('missing_count'), r.get('extra_count'),
                    r.get('changed_count')))
                for m in r.get('missing', []):
                    print('    MISSING', m)
                for e in r.get('extra', []):
                    print('    EXTRA', e)
                for k2, v in r.get('changed', {}).items():
                    print('    CHANGED', k2, 'committed=', v[0], 'regen=', v[1])
        print('  committed_nonregular_kinds=', res['committed_nonregular_kinds'])
        print('  regen_nonregular_kinds=', res['regen_nonregular_kinds'])
        print('  extract_symlinks=%s' % res['extract_symlinks'])
        ia = res['reader_avm_inspect']
        ib = res['reader_auto_inspect']
        if ia:
            print('  avm inspect: layout=%s header_endian=%s block_length_signal=%s '
                  'avm_marker=%s regular=%d dirs=%d links=%d special=%s' % (
                      ia.get('layout'), ia.get('header_endian'),
                      ia.get('block_length_signal'), ia.get('avm_marker'),
                      ia.get('regular_files'), ia.get('directories'),
                      ia.get('symlinks'), ia.get('special_kinds')))
            print('    header_length_candidates=', ia.get('header_length_candidates'))
            print('    data_block_length_evidence=', ia.get('data_block_length_evidence'))
            print('    fragment_entry_evidence=', ia.get('fragment_entry_evidence'))
            print('    warnings=', ia.get('warnings'))
        if ib:
            print('  auto inspect: layout=%s header_endian=%s block_length_signal=%s '
                  'regular=%d dirs=%d links=%d special=%s' % (
                      ib.get('layout'), ib.get('header_endian'),
                      ib.get('block_length_signal'), ib.get('regular_files'),
                      ib.get('directories'), ib.get('symlinks'),
                      ib.get('special_kinds')))
            print('    header_length_candidates=', ib.get('header_length_candidates'))
            print('    warnings=', ib.get('warnings'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
