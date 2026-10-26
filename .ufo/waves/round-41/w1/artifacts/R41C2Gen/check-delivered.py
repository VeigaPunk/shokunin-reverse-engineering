#!/usr/bin/env python3
"""R41C2Gen — re-read a delivered held-out set and check declared == observed.

Independent of the generator: it parses only `manifest.json` and each
`<id>/envelope.json` (plus `run.json` for the digest binding), so it can be run
on the frozen set before scoring.  Exit 0 = every carrier's observed tuple equals
its declared tuple; 1 = at least one MISS; 2 = setup error.

    python3 -I -B check-delivered.py <set-dir>

The six bound fields and their derivation (L1 amendment,
`observed_features_match_declared`):
  handler_set      sorted {chunks[].handler}
  gap_kinds        sorted {extraction_gaps[].kind}
  gap_dependencies sorted union of extraction_gaps[].dependencies
  be_argv          'yes' if a recorded sasquatch/unsquashfs child argv carries -be,
                   'no' if such an argv exists without it, 'n/a' when no argv is
                   recorded at all (a successful run records none)
  symlink_removed  any MaliciousSymlinkRemoved diagnostic
  published        'nonzero' if any regular file was published, else 'zero'
"""
import json
import os
import sys

FIELDS = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
          'symlink_removed', 'published')


def observed(envelope, run):
    data = envelope.get('data', envelope)
    nr = data.get('normalized_result') or {}
    reports = [(d.get('report') or {}) for d in nr.get('diagnostics') or []]
    be = 'n/a'
    for report in reports:
        command = report.get('command')
        if not command:
            continue
        tokens = command.split()
        if not tokens:
            continue
        if os.path.basename(tokens[0]).startswith(('sasquatch', 'unsquashfs')):
            be = 'yes' if '-be' in tokens[1:] else 'no'
            if be == 'yes':
                break
    return {
        'handler_set': sorted({c['handler'] for c in nr.get('chunks') or []
                               if c.get('handler')}),
        'gap_kinds': sorted({g['kind'] for g in nr.get('extraction_gaps') or []
                             if g.get('kind')}),
        'gap_dependencies': sorted({dep for g in nr.get('extraction_gaps') or []
                                    for dep in (g.get('dependencies') or [])}),
        'be_argv': be,
        'symlink_removed': any((r.get('__typename__') == 'MaliciousSymlinkRemoved')
                               for r in reports),
        'published': 'nonzero' if (nr.get('files') or []) else 'zero',
    }


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = os.path.abspath(argv[1])
    manifest_path = os.path.join(root, 'manifest.json')
    if not os.path.isfile(manifest_path):
        print('no manifest.json under %s' % root)
        return 2
    with open(manifest_path, encoding='utf-8') as handle:
        manifest = json.load(handle)
    carriers = manifest.get('carriers') or []
    if not carriers:
        print('manifest declares no carriers')
        return 2
    bad = 0
    for entry in carriers:
        cid = entry['id']
        declared = entry.get('declared') or {}
        missing = [f for f in FIELDS if f not in declared]
        if missing:
            print('FAIL %s %s: declared is missing %s' % (cid, entry.get('class'), missing))
            bad += 1
            continue
        paths = {stem: os.path.join(root, cid, stem + '.json')
                 for stem in ('envelope', 'run')}
        absent = [p for p in paths.values() if not os.path.isfile(p)]
        if absent:
            print('FAIL %s: missing %s' % (cid, [os.path.basename(p) for p in absent]))
            bad += 1
            continue
        with open(paths['envelope'], encoding='utf-8') as handle:
            envelope = json.load(handle)
        with open(paths['run'], encoding='utf-8') as handle:
            run = json.load(handle)
        obs = observed(envelope, run)
        diff = {k: {'declared': declared[k], 'observed': obs[k]}
                for k in FIELDS if declared[k] != obs[k]}
        digest_ok = run.get('digest_matches_carrier')
        if diff or digest_ok is False:
            bad += 1
            print('MISS %s %-26s %s%s' % (cid, entry.get('class'), diff,
                                          '' if digest_ok is not False
                                          else ' digest-mismatch'))
    print('%d/%d carriers: observed == declared%s'
          % (len(carriers) - bad, len(carriers),
             '' if not bad else '  (%d MISS)' % bad))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
