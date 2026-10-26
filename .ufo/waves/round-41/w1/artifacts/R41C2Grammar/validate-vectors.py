#!/usr/bin/env python3
"""validate-vectors.py - mechanical check of R41C2Grammar/grammar-vectors.json.

Re-derives every vector's expected (label, action) from a direct transcription of
the **Label precedence** steps 1-12 in plans/round-41-claims.md (draft, lines 72-88)
and asserts the JSON's structure.  This is the reviewer's own third implementation:
it proves the vectors' labels follow the precedence text mechanically, not by eye.

Usage: python3 -I -B validate-vectors.py [PATH_TO_JSON]
Exit: 0 all checks pass; 1 assertion failed; 2 usage/IO.
"""

import json
import os
import sys

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'grammar-vectors.json')

LABELS = {
    'unclassified', 'no-squashfs-chunk', 'dep-missing-be', 'dep-missing-le',
    'partial-body-failure', 'avm-marker-be-dropped', 'body-extractor-failure',
    'depth-limited-nested', 'mixed-symlinks', 'escaping-symlink-removed',
    'in-tree-symlink-metadata', 'clean', 'clean-empty',
}
ACTIONS = {
    'none', 'inspect-input', 'install-extractor-be', 'install-extractor-le',
    'wrap-extractor-be', 'preserve-failure', 'salvage-partial',
    'audit-symlinks', 'expect-link-absent', 'count-gap', 'confirm-empty',
    'raise-depth',
}
ORIGINS = {'rea-observed', 'rea-reachable', 'synthetic-only',
           'unreachable-by-construction'}
GRAMMAR = {'encodable', 'needs-amendment'}
BE_VALUES = {'yes', 'no', 'n/a'}
SR_VALUES = {'yes', 'no'}
GAP_KINDS = {
    'missing-extractor-dependency', 'unknown-chunk-handler', 'encrypted-chunk',
    'depth-limited', 'extractor-failure', 'unpublished-entry',
}


def classify(op, pr, h, g, d, be, sr, p):
    """Direct transcription of the **Label precedence** steps 1-12.

    Documented resolutions (see the JSON's `resolutions` object):
      - step 2 read literally over the collected handler set (glob squashfs_v4_*);
      - step 3 'D names X' is exact element membership; when D names both
        executables the first-listed branch (be) wins; when D names neither the
        step falls through to step 4.
    """
    # 1. domain guard
    if op != 'extract_firmware' or pr != 'unblob':
        return 'unclassified', 'none'
    # 2. no squashfs_v4_* handler in H
    if not any(isinstance(h, str) and h.startswith('squashfs_v4_') for h in h):
        return 'no-squashfs-chunk', 'inspect-input'
    # 3. dependency gap branch
    if 'missing-extractor-dependency' in g:
        if 'sasquatch-v4be' in d:
            return 'dep-missing-be', 'install-extractor-be'
        if 'sasquatch' in d:
            return 'dep-missing-le', 'install-extractor-le'
        # neither named -> fall through to step 4
    # 4. partial body failure
    if 'extractor-failure' in g and p > 0:
        return 'partial-body-failure', 'salvage-partial'
    # 5./6. zero-file failure split by BE and handler
    if 'extractor-failure' in g and p == 0:
        if be == 'no' and 'squashfs_v4_be' in h:
            return 'avm-marker-be-dropped', 'wrap-extractor-be'
        return 'body-extractor-failure', 'preserve-failure'
    # 7. depth-limited (new)
    if 'depth-limited' in g:
        return 'depth-limited-nested', 'raise-depth'
    # 8. mixed symlinks
    if sr == 'yes' and 'unpublished-entry' in g:
        return 'mixed-symlinks', 'audit-symlinks'
    # 9. escaping symlink removed
    if sr == 'yes' and not g:
        return 'escaping-symlink-removed', 'expect-link-absent'
    # 10. in-tree symlink metadata (exact singleton)
    if set(g) == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', 'count-gap'
    # 11. clean / clean-empty
    if not g and p > 0:
        return 'clean', 'none'
    if not g and p == 0:
        return 'clean-empty', 'confirm-empty'
    # 12. anything else
    return 'unclassified', 'none'


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_PATH
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            doc = json.load(handle)
    except (OSError, ValueError) as exc:
        print('cannot read %s: %s' % (path, exc), file=sys.stderr)
        return 2

    errors = []

    def check(cond, message):
        if not cond:
            errors.append(message)

    check(doc.get('schema') == 'kaidoku-r41-c2-grammar-vectors-v1',
          'schema field missing or wrong')
    vectors = doc.get('vectors')
    check(isinstance(vectors, list) and len(vectors) >= 20,
          'fewer than 20 vectors (got %r)' % (len(vectors) if isinstance(vectors, list) else None))
    if not isinstance(vectors, list):
        print('vectors is not a list', file=sys.stderr)
        return 1

    ids = set()
    steps_seen = set()
    amap = doc.get('action_map', {})
    for vec in vectors:
        vid = vec.get('id')
        check(isinstance(vid, str) and vid not in ids, 'bad or duplicate id %r' % (vid,))
        ids.add(vid)
        feat = vec.get('features')
        check(isinstance(feat, dict), '%s: features is not an object' % vid)
        if not isinstance(feat, dict):
            continue
        op, pr = feat.get('OP'), feat.get('PR')
        h, g, d = feat.get('H'), feat.get('G'), feat.get('D')
        be, sr, p = feat.get('BE'), feat.get('SR'), feat.get('P')
        check(isinstance(op, str) and isinstance(pr, str), '%s: OP/PR not strings' % vid)
        check(isinstance(h, list) and all(isinstance(x, str) for x in h),
              '%s: H not a list of strings' % vid)
        check(isinstance(g, list) and all(isinstance(x, str) for x in g),
              '%s: G not a list of strings' % vid)
        check(all(x in GAP_KINDS for x in g),
              '%s: G holds a kind outside the REA 6.5.0 enum: %r' % (vid, g))
        check(isinstance(d, list) and all(isinstance(x, str) for x in d),
              '%s: D not a list of strings' % vid)
        check(be in BE_VALUES, '%s: BE %r not in %s' % (vid, be, sorted(BE_VALUES)))
        check(sr in SR_VALUES, '%s: SR %r not in %s' % (vid, sr, sorted(SR_VALUES)))
        check(isinstance(p, int) and p >= 0, '%s: P %r not a natural number' % (vid, p))
        check(h == sorted(h) and len(set(h)) == len(h), '%s: H not a sorted set' % vid)
        check(g == sorted(g) and len(set(g)) == len(g), '%s: G not a sorted set' % vid)
        check(d == sorted(d) and len(set(d)) == len(d), '%s: D not a sorted set' % vid)
        exp = vec.get('expected')
        check(isinstance(exp, dict) and exp.get('label') in LABELS,
              '%s: expected label %r outside the label set' % (vid, exp))
        check(isinstance(exp, dict) and exp.get('action') in ACTIONS,
              '%s: expected action %r outside the vocabulary' % (vid, exp))
        if isinstance(exp, dict) and exp.get('label') in amap:
            check(amap[exp.get('label')] == exp.get('action'),
                  '%s: action disagrees with the JSON action_map' % vid)
        step = vec.get('decided_by_step')
        check(step in range(1, 13), '%s: decided_by_step %r outside 1-12' % (vid, step))
        steps_seen.add(step)
        origin = vec.get('origin') or ''
        check(any(origin == o or origin.startswith(o + ' ') or origin.startswith(o + ' (')
                  for o in ORIGINS),
              '%s: origin %r unknown' % (vid, origin))
        check(vec.get('draft_grammar') in GRAMMAR,
              '%s: draft_grammar %r unknown' % (vid, vec.get('draft_grammar')))
        if vec.get('draft_grammar') == 'needs-amendment':
            note = vec.get('note', '')
            check('amendment' in note or 'Recommended amendment' in note or 'F1' in note or 'F2' in note or 'F3' in note,
                  '%s: needs-amendment without an amendment note' % vid)
        # mechanical re-derivation from the precedence text
        want = classify(op, pr, h, g, d, be, sr, p)
        got = (exp.get('label'), exp.get('action')) if isinstance(exp, dict) else None
        check(got == want,
              '%s: precedence re-derivation gives %r, JSON says %r' % (vid, want, got))

    missing_steps = sorted(set(range(1, 13)) - steps_seen)
    check(not missing_steps, 'no vector decides by step(s) %r' % missing_steps)

    if errors:
        for message in errors:
            print('FAIL %s' % message)
        print('checked %d vectors, %d error(s)' % (len(vectors), len(errors)))
        return 1
    print('ok: %d vectors, %d unique ids, steps covered %r'
          % (len(vectors), len(ids), sorted(steps_seen)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
