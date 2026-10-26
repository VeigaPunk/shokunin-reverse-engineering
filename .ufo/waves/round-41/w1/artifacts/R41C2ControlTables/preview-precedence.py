#!/usr/bin/env python3
"""preview-precedence.py - the `**Label precedence**` list, executed (PREVIEW ONLY).

This is NOT the frozen independent evaluator: R41C2Eval owns
`tools/round-41/indep-eval-v3.py` and writes it from the same numbered list without
reading any table.  This preview exists so the control tables can be scored before
that tool lands; it implements the twelve bullets of plans/round-41-claims.md
`**Label precedence**` literally, and takes the action cells from the round-40
manifest `label_actions` map plus `raise-depth` for the new depth-limited-nested label
(the draft names the pair in R41-C2).

Usage: preview-precedence.py [--json] ENVELOPE...
Output: `path<TAB>label<TAB>action` per envelope, or a JSON object with `results`.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_features():
    """Reuse the envelope reader of the replica interpreter (one implementation)."""
    import importlib.util
    path = os.path.join(HERE, 'v3-check-interp.py')
    spec = importlib.util.spec_from_file_location('v3checkinterp', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FEAT = load_features()

ACTIONS = {
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
    'depth-limited-nested': 'raise-depth',
    'unclassified': 'none',
}


def expected(feat):
    """Return (label, action, step) for one feature tuple, per the numbered list."""
    G = set(feat['G'])
    D = set(feat['D'])
    if feat['OP'] != 'extract_firmware' or feat['PV'] != 'unblob':
        return 'unclassified', 'none', 1
    if not any(h.startswith('squashfs_v4_') for h in feat['H']):
        return 'no-squashfs-chunk', ACTIONS['no-squashfs-chunk'], 2
    if 'missing-extractor-dependency' in G:
        if 'sasquatch-v4be' in D:
            return 'dep-missing-be', ACTIONS['dep-missing-be'], 3
        if 'sasquatch' in D:
            return 'dep-missing-le', ACTIONS['dep-missing-le'], 3
        # step 3 names no label for a dependency gap that names neither binary; the
        # list continues to the next applicable step.
    if 'extractor-failure' in G and feat['P'] > 0:
        return 'partial-body-failure', ACTIONS['partial-body-failure'], 4
    if 'extractor-failure' in G and feat['P'] == 0 and feat['BE'] == 'no' \
            and 'squashfs_v4_be' in feat['H']:
        return 'avm-marker-be-dropped', ACTIONS['avm-marker-be-dropped'], 5
    if 'extractor-failure' in G and feat['P'] == 0:
        return 'body-extractor-failure', ACTIONS['body-extractor-failure'], 6
    if 'depth-limited' in G:
        return 'depth-limited-nested', ACTIONS['depth-limited-nested'], 7
    if feat['SR'] == 'yes' and 'unpublished-entry' in G:
        return 'mixed-symlinks', ACTIONS['mixed-symlinks'], 8
    if feat['SR'] == 'yes' and not G:
        return 'escaping-symlink-removed', ACTIONS['escaping-symlink-removed'], 9
    if G == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', ACTIONS['in-tree-symlink-metadata'], 10
    if not G:
        if feat['P'] > 0:
            return 'clean', ACTIONS['clean'], 11
        return 'clean-empty', ACTIONS['clean-empty'], 11
    return 'unclassified', 'none', 12


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('envelopes', nargs='+')
    ns = ap.parse_args(argv)
    results = []
    for path in ns.envelopes:
        feat = FEAT.load_envelope(path)
        label, action, step = expected(feat)
        results.append({'path': path, 'label': label, 'action': action, 'step': step,
                        'features': feat})
    if ns.json:
        json.dump({'evaluator': 'preview-precedence.py', 'results': results},
                  sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write('\n')
        return 0
    for row in results:
        print('%s\t%s\t%s' % (row['path'], row['label'], row['action']))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
