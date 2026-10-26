#!/usr/bin/env python3
"""R41CritC2Draft — the DRAFT precedence text of R41-C2, implemented literally.

Purpose (critique instrument, not a lane table): apply `plans/round-41-claims.md`
lines 72-88 verbatim to real and probe envelopes and count what it decides.

Two things it measures:
 1. how many DISTINCT (label, action) pairs the precedence can produce, and
    whether the draft's five "combined classes" produce pairs of their own;
 2. which clauses are actionless — the precedence names an action in clause 1
    only, so the action half of every other pair has to be borrowed from the
    round-40 v2 table's `<!-- sqfs-triage-actions: ... -->` line, and the one
    genuinely new label has no token there at all.

Usage: precedence-probe.py <envelope.json>...   (prints TSV + a summary)
"""
import json
import sys

# The round-40 v2 vocabulary (SKILL.md:362 at lane HEAD). Nothing in the round-41
# precedence text supplies these; the mapping label->action is *not* in the text.
V2_ACTIONS = {
    'clean': 'none',
    'clean-empty': 'confirm-empty',
    'escaping-symlink-removed': 'expect-link-absent',
    'in-tree-symlink-metadata': 'count-gap',
    'mixed-symlinks': 'audit-symlinks',
    'dep-missing-be': 'install-extractor-be',
    'dep-missing-le': 'install-extractor-le',
    'avm-marker-be-dropped': 'wrap-extractor-be',
    'body-extractor-failure': 'preserve-failure',
    'partial-body-failure': 'salvage-partial',
    'no-squashfs-chunk': 'inspect-input',
    'unclassified': 'none',
}
# `depth-limited-nested` is new in v3: no v2 token exists for it.
NEW_LABELS = ('depth-limited-nested',)


def features(data):
    nr = data.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    gaps = nr.get('extraction_gaps') or []
    diags = nr.get('diagnostics') or []
    be = 'n/a'
    for d in diags:
        cmd = (d.get('report') or {}).get('command')
        if isinstance(cmd, str) and cmd:
            be = 'yes' if ' -be ' in ' ' + cmd + ' ' else 'no'
    sr = any((d.get('report') or {}).get('kind') == 'MaliciousSymlinkRemoved'
             for d in diags)
    return {
        'OP': data.get('operation'),
        'PR': (data.get('provider') or {}).get('id'),
        'H': {c.get('handler') for c in chunks if c.get('handler')},
        'G': {g.get('kind') for g in gaps},
        'D': {x for g in gaps for x in (g.get('dependencies') or [])},
        'BE': be,
        'SR': sr,
        'P': len(nr.get('files') or []),
        '_gap_count': len(gaps),
        '_unpublished': len(nr.get('unpublished_entries') or []),
        '_depth_limited': nr.get('depth_limited_paths') or [],
        '_max_depth': (data.get('parameters') or {}).get('max_depth'),
        '_coverage': nr.get('coverage'),
    }


def label(f):
    """plans/round-41-claims.md:75-88, first match wins."""
    G, D, P, SR, BE, H = f['G'], f['D'], f['P'], f['SR'], f['BE'], f['H']
    if f['OP'] != 'extract_firmware' or f['PR'] != 'unblob':
        return 'unclassified', 'clause 1'
    if not any(h.startswith('squashfs_v4_') for h in H):
        return 'no-squashfs-chunk', 'clause 2'
    if 'missing-extractor-dependency' in G:
        if 'sasquatch-v4be' in D:
            return 'dep-missing-be', 'clause 3'
        if 'sasquatch' in D:
            return 'dep-missing-le', 'clause 3'
        # clause 3 states no branch for an UNNAMED dependency; fall through.
    if 'extractor-failure' in G and P > 0:
        return 'partial-body-failure', 'clause 4'
    if 'extractor-failure' in G and P == 0 and BE == 'no' and 'squashfs_v4_be' in H:
        return 'avm-marker-be-dropped', 'clause 5'
    if 'extractor-failure' in G and P == 0:
        return 'body-extractor-failure', 'clause 6'
    if 'depth-limited' in G:
        return 'depth-limited-nested', 'clause 7'
    if SR and 'unpublished-entry' in G:
        return 'mixed-symlinks', 'clause 8'
    if SR and not G:
        return 'escaping-symlink-removed', 'clause 9'
    if G == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', 'clause 10'
    if not G and P > 0:
        return 'clean', 'clause 11'
    if not G and P == 0:
        return 'clean-empty', 'clause 11'
    return 'unclassified', 'clause 12'


def main(paths):
    rows = []
    for path in paths:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        f = features(data)
        lab, clause = label(f)
        act = V2_ACTIONS.get(lab)
        rows.append((path, f, lab, act, clause))
    hdr = ['envelope', 'OP', 'PR', 'H', 'G', 'D', 'BE', 'SR', 'P', 'gaps',
           'unpub', 'depth_limited', 'clause', 'label', 'action_from_v2']
    print('\t'.join(hdr))
    for path, f, lab, act, clause in rows:
        print('\t'.join([
            path.rsplit('/', 2)[-2] if path.endswith('envelope.json') else path.split('/')[-1],
            str(f['OP']), str(f['PR']), ','.join(sorted(f['H'])) or '-',
            ','.join(sorted(f['G'])) or '-', ','.join(sorted(f['D'])) or '-',
            f['BE'], str(f['SR']), str(f['P']), str(f['_gap_count']),
            str(f['_unpublished']), ','.join(f['_depth_limited']) or '-',
            clause, lab, str(act)]))
    pairs = sorted({(r[2], r[3]) for r in rows}, key=str)
    print('\n# distinct (label, action) pairs the precedence decides on this set: %d'
          % len(pairs))
    for p in pairs:
        print('#   %s' % (p,))
    holes = sorted({r[2] for r in rows if r[3] is None})
    print('# labels with no action token in the v2 vocabulary: %s' % (holes or 'none'))
    print('# distinct labels: %d' % len({r[2] for r in rows}))


if __name__ == '__main__':
    main(sys.argv[1:])
