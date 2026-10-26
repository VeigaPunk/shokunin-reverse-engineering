#!/usr/bin/env python3
"""MH-1 — one path helper, two domains: `same_rel` (suffix) is reused where the
frozen binding promises equality, so a regular file whose tail *is* a symlink's
path is read as a materialised symlink.

Frozen text (`tools/round-40/c1-counter.py:54`):
  `nonregular_unpublished_ok  no published regular file path equals a non-regular
   entry path`
Frozen code (`:606-607`, `:643-649`):
  `same_rel(candidate, rel) = candidate == rel or candidate.endswith('/' + rel)`
  `nonregular_published(files, nonreg)` tests every published `relative_path`
  against every non-regular `rel` with `same_rel`.

Why suffix is right for the oracle and wrong here: an oracle row is
squashfs-root-relative and the receipt path carries an extraction-root prefix, so
suffix is the only join.  `nonregular.tsv` rows are in the *same* space as the
receipt's published paths (both carry the extract root), so equality after
stripping that root is the promised test.

The same helper is reused a second time, in `gap_check` (`:660-676`): a gap is
accepted only when its `relative_path` resolves to exactly one non-regular entry,
and the resolution is `same_rel`.  There the defect points the other way: a gap
recorded on a *regular* file's path resolves to a symlink and is accepted, so the
counter can pass a bogus gap.

Usage:
  mh1-suffix-domain.py --root LANE [--rev REV] [--matcher frozen|exact]
                       [--control materialised|deeper|bogus-gap|none] [--oracle]
                       [--gaps]
Exit 0 = no hit; exit 1 = hits (printed); exit 2 = usage/missing input.
Red/green:
  --matcher frozen --control none        on L2 -> exit 1, hit usr/bin/busy  (the defect)
  --matcher exact  --control none        on L2 -> exit 0
  --matcher exact  --control materialised on L2 -> exit 1, hit bin/busy    (still catches)
  --gaps --matcher frozen --control bogus-gap      on L2 -> exit 1, gap on the
      regular file `usr/bin/busy` is accepted as a symlink gap (false pass)
  --gaps --matcher exact  --control bogus-gap      on L2 -> exit 0, refused
"""
import argparse
import json
import os
import subprocess
import sys

IDS = ('V1', 'V2', 'L1', 'L2')
AFTER = 'corpus/evidence/round-40/c1/%s/after.json'
NONREG = 'corpus/evidence/round-40/c1/%s/nonregular.tsv'
ORACLE = 'corpus/evidence/round-40/c1/%s/oracle.tsv'
ROOT_MARK = '_extract'


def show(root, rev, path):
    if rev:
        return subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                              check=True, stdout=subprocess.PIPE).stdout
    with open(os.path.join(root, path), 'rb') as fh:
        return fh.read()


def same_rel(candidate, rel):
    """Verbatim from tools/round-40/c1-counter.py:606-607."""
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))


def recorded_root(raw):
    """The receipt's own chunk extraction root: the basename of the task path
    unblob reported (`raw_result.report[*].task.path`, e.g. `firmware.bin_extract`).
    This is the *recorded* root, not a name pattern, so a publication moved under
    any other prefix cannot match."""
    try:
        doc = json.loads(raw.decode())
    except (ValueError, AttributeError):
        return None
    report = ((doc.get('raw_result') or {}).get('report') or [])
    for entry in report:
        task = (entry or {}).get('task') or {}
        path = task.get('path')
        if path:
            return path.rstrip('/').split('/')[-1]
    return None


def rel_after_root(path, root):
    if not path or not root:
        return None
    prefix = root + '/'
    return path[len(prefix):] if path.startswith(prefix) else None


def exact_after_root(candidate, rel, root):
    tail = rel_after_root(candidate, root)
    return tail is not None and tail == rel


def gap_resolution(gaps, nonreg, match):
    """The first test of `gap_check` (`c1-counter.py:660-676`), reproduced: a gap
    whose path resolves to exactly one non-regular entry is accepted."""
    rows = []
    for gap in gaps:
        rp = gap.get('relative_path')
        if rp is None:
            rows.append((gap.get('kind'), rp, 'structural', None))
            continue
        hits = [rel for rel, _kind in nonreg if match(rp, rel)]
        verdict = 'accepted' if len(hits) == 1 else (
            'refused(%d matches)' % len(hits))
        rows.append((gap.get('kind'), rp, verdict, hits))
    return rows


def receipt_gaps(raw):
    nr = (json.loads(raw.decode()).get('normalized_result') or {})
    return list(nr.get('extraction_gaps') or [])


def parse_nonregular(raw):
    rows = []
    for line in raw.decode().splitlines():
        if not line.strip():
            continue
        cells = line.split('\t')
        rows.append((cells[0], cells[1] if len(cells) > 1 else ''))
    return rows


def published(raw):
    nr = (json.loads(raw.decode()).get('normalized_result') or {})
    return [(f.get('relative_path') or '', f.get('sha256') or '')
            for f in (nr.get('files') or []) if isinstance(f, dict)]


def hits(files, nonreg, match):
    out = []
    for fp, _sha in files:
        for rel, _kind in nonreg:
            if match(fp, rel):
                out.append((fp, rel))
    return out


def oracle_check(oracle_raw, files, match):
    rows = []
    for line in oracle_raw.decode().splitlines():
        if not line.strip():
            continue
        cells = line.split('\t')
        rows.append((cells[0], cells[1]))
    missing = [rel for rel, sha in rows
               if not any(sha == fsha and match(fp, rel) for fp, fsha in files)]
    return len(rows), missing


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', default=None)
    ap.add_argument('--matcher', choices=('frozen', 'exact'), default='frozen')
    ap.add_argument('--control', choices=('none', 'materialised', 'deeper', 'bogus-gap',
                                          'wrong-root'), default='none')
    ap.add_argument('--gaps', action='store_true',
                    help='run the gap-resolution test instead of the publication test')
    ap.add_argument('--oracle', action='store_true',
                    help='also run the oracle-hit binding under the chosen matcher')
    ap.add_argument('--ids', default=','.join(IDS))
    args = ap.parse_args(argv)

    def match_for(raw):
        if args.matcher == 'frozen':
            return same_rel
        root = recorded_root(raw)
        return lambda candidate, rel: exact_after_root(candidate, rel, root)
    rev = args.rev or None
    rc = 0
    for cid in args.ids.split(','):
        try:
            raw_receipt = show(args.root, rev, AFTER % cid)
            files = published(raw_receipt)
            nonreg = parse_nonregular(show(args.root, rev, NONREG % cid))
        except FileNotFoundError:
            print('%s: absent' % cid)
            return 2
        match = match_for(raw_receipt)
        if args.control == 'materialised':
            # the symlink is published under its own path: a real materialisation
            files = files + [('firmware.bin_extract/' + rel, 'f' * 64) for rel, kind in nonreg
                             if kind == 'symlink']
        elif args.control == 'deeper':
            # published under a spurious subdirectory: same tail, different path
            files = files + [('firmware.bin_extract/sub/' + rel, 'e' * 64)
                             for rel, kind in nonreg if kind == 'symlink']
        elif args.control == 'wrong-root':
            # CTL-C1-14's overlay: every publication moved under another root
            files = [('nested/wrong-root/' + fp, sha) for fp, sha in files]
        if args.gaps:
            gaps = receipt_gaps(show(args.root, rev, AFTER % cid))
            if args.control == 'bogus-gap':
                # a gap recorded on the *regular* file that tails the symlink path
                gaps = gaps + [{'kind': 'unpublished-entry',
                                'relative_path': 'firmware.bin_extract/usr/bin/busy'}]
            rows = gap_resolution(gaps, nonreg, match)
            accepted = [r for r in rows if r[2] == 'accepted']
            print('%s gaps matcher=%s control=%s gaps=%d accepted=%d %s'
                  % (cid, args.matcher, args.control, len(rows), len(accepted),
                     ['%s<-%s' % (r[1], r[3]) for r in accepted
                      if r[1] == 'firmware.bin_extract/usr/bin/busy'][:2]))
            if args.control == 'bogus-gap':
                # the bogus gap must be refused: acceptance is the failure
                bogus = [r for r in accepted
                         if r[1] == 'firmware.bin_extract/usr/bin/busy']
                if bogus:
                    rc = 1
            continue
        h = hits(files, nonreg, match)
        line = ('%s matcher=%s control=%s published=%d nonregular=%d hits=%d %s'
                % (cid, args.matcher, args.control, len(files), len(nonreg), len(h),
                   ['%s<-%s' % (fp, rel) for fp, rel in h[:5]]))
        if args.oracle:
            n, missing = oracle_check(show(args.root, rev, ORACLE % cid), files, match)
            line += (' | oracle=%d/%d' % (n - len(missing), n))
            if args.control == 'none' and missing:
                rc = 1
                line += ' MISSING=%s' % missing[:3]
        print(line)
        if args.control == 'wrong-root':
            if args.oracle and not missing:
                rc = 1      # the binding accepted a wrong-root publication
        elif args.control == 'none':
            if h:
                rc = 1
        elif args.control == 'materialised':
            if not h:      # a real materialisation must be caught
                rc = 1
        elif args.control == 'deeper':
            if h:          # a foreign subpath is not the entry's path
                rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
