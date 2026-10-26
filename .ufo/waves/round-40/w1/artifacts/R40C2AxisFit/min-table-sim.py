#!/usr/bin/env python3
"""Decision-logic simulation of DRAFT R40-C2's class list (not evidence about real envelopes).

Builds one feature vector per draft class (from plans/round-40-claims.md :91-94, two replicates
each), then scores the cheapest first-match table that reproduces every expected (label, action)
pair, and reports:
  * matched / 26,
  * the table's non-* decision-cell count,
  * whether every cell is load-bearing (dropping it changes some class's label).

The point: N/N is reachable with ~L-1 cells (one predicate per non-default label), so the draft's
target does not measure the decision content the claim advertises.  No carrier is built, no REA or
unblob run is made; this is table logic only.
"""
import sys

EF = 'extract_firmware'


def F(op=EF, H=(), G=(), D=(), BE='n/a', SR='no', P=1):
    return dict(op=op, H=set(H), G=set(G), D=set(D), BE=BE, SR=SR, P=P)


CLASSES = {
    'clean-be':                  (F(H=['squashfs_v4_be'], P=3), ('clean', 'none')),
    'clean-le':                  (F(H=['squashfs_v4_le'], P=3), ('clean', 'none')),
    'clean-empty':               (F(H=['squashfs_v4_be'], P=0), ('clean-empty', 'fix-header')),
    'escaping-symlink-removed':  (F(H=['squashfs_v4_be'], SR='yes', P=3), ('escaping-symlink-removed', 'expect-absent')),
    'in-tree-symlink-metadata':  (F(H=['squashfs_v4_be'], G=['unpublished-entry'], P=3), ('in-tree-symlink-metadata', 'count-gaps')),
    'mixed-symlinks':            (F(H=['squashfs_v4_be'], G=['unpublished-entry'], SR='yes', P=4), ('mixed-symlinks', 'count-gaps-keep-absent')),
    'dep-missing-be':            (F(H=['squashfs_v4_be'], G=['missing-extractor-dependency'], D=['sasquatch-v4be'], P=0), ('dep-missing-be', 'add-path-wrapper')),
    'dep-missing-le':            (F(H=['squashfs_v4_le'], G=['missing-extractor-dependency'], D=['sasquatch'], P=0), ('dep-missing-le', 'add-path-wrapper')),
    'avm-marker-be-dropped':     (F(H=['squashfs_v4_be'], G=['extractor-failure'], BE='no', P=0), ('avm-marker-be-dropped', 'check-carrier-before-wrapper')),
    'body-extractor-failure':    (F(H=['squashfs_v4_be'], G=['extractor-failure'], BE='yes', P=0), ('body-extractor-failure', 'keep-stderr')),
    'partial-body-failure':      (F(H=['squashfs_v4_be'], G=['extractor-failure'], BE='yes', P=2), ('partial-body-failure', 'keep-published-keep-stderr')),
    'no-squashfs-chunk':         (F(H=[], P=0), ('no-squashfs-chunk', 'check-magic')),
    'out-of-domain':             (F(op='inspect', H=[], P=0), ('unclassified', 'none')),
}

# cheapest first-match list found: 11 rows, 15 non-* decision cells, no all-* row.
SHORTCUT = [
    ('no-squashfs-chunk', 'check-magic', {'op': EF, 'H': 'none'}),
    ('dep-missing-be', 'add-path-wrapper', {'D': {'sasquatch-v4be'}}),
    ('dep-missing-le', 'add-path-wrapper', {'D': {'sasquatch'}}),
    ('avm-marker-be-dropped', 'check-carrier-before-wrapper', {'BE': 'no'}),
    ('partial-body-failure', 'keep-published-keep-stderr', {'BE': 'yes', 'P': '>0'}),
    ('body-extractor-failure', 'keep-stderr', {'BE': 'yes'}),
    ('mixed-symlinks', 'count-gaps-keep-absent', {'SR': 'yes', 'G': {'unpublished-entry'}}),
    ('escaping-symlink-removed', 'expect-absent', {'SR': 'yes'}),
    ('in-tree-symlink-metadata', 'count-gaps', {'G': {'unpublished-entry'}}),
    ('clean-empty', 'fix-header', {'H': 'squashfs_v4_*', 'P': '0'}),
    ('clean', 'none', {'P': '>0'}),
]


def match(f, p):
    for k, v in p.items():
        if k == 'op' and f['op'] != v:
            return False
        if k == 'H' and v == 'none' and f['H']:
            return False
        if k == 'H' and v == 'squashfs_v4_*' and not f['H']:
            return False
        if k in ('D', 'G') and f[k] != v:
            return False
        if k in ('BE', 'SR') and f[k] != v:
            return False
        if k == 'P' and v == '>0' and f['P'] <= 0:
            return False
        if k == 'P' and v == '0' and f['P'] != 0:
            return False
    return True


def label(rows, f):
    for lab, act, p in rows:
        if match(f, p):
            return (lab, act)
    return ('unclassified', 'none')


def main():
    ok = bad = 0
    for name, (f, want) in CLASSES.items():
        got = label(SHORTCUT, f)
        if got == want:
            ok += 2
        else:
            bad += 2
            print('MISLABEL %-26s want=%s got=%s' % (name, want, got))
    cells = sum(len(p) for _, _, p in SHORTCUT)
    print('simulated envelopes=%d matched=%d mismatched=%d' % (2 * len(CLASSES), ok, bad))
    print('shortcut table: rows=%d non_star_cells=%d distinct_labels=%d (draft labels: 12 incl. default)'
          % (len(SHORTCUT), cells, len({r[0] for r in SHORTCUT})))
    base = {c: label(SHORTCUT, f) for c, (f, _) in CLASSES.items()}
    dead = []
    for i, (lab, act, p) in enumerate(SHORTCUT):
        for k in p:
            q = dict(p)
            del q[k]
            rows = list(SHORTCUT)
            rows[i] = (lab, act, q)
            if all(label(rows, f) == base[c] for c, (f, _) in CLASSES.items()):
                dead.append((lab, k))
    print('non-load-bearing cells: %r' % (dead,))
    print('lower bound: one non-* cell per non-default label -> >= %d cells for %d labels'
          % (len({r[0] for r in SHORTCUT}) - 1, len({r[0] for r in SHORTCUT})))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
