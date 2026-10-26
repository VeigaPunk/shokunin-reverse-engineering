#!/usr/bin/env python3
"""removal-predict.py -- which symlinks of a SquashFS image are *at risk* of
unblob 26.6.4's silent removal, and how the receipt's removals partition the
image's link rows.

Measured mechanism (unblob/extractor.py `fix_symlink`, read at 26.6.4, and
reproduced by `symlink-order-probe.py`):

  * a link with an empty target is unlinked **silently** -- no report, so it is
    invisible in the receipt (neither a gap nor an unpublished entry);
  * a link whose target chain passes through an **absolute** symlink at hop 2 or
    later is unlinked with a `MaliciousSymlinkRemoved` report: the first hop of
    an absolute target is re-rooted at the extraction root, but `Path.resolve`
    follows any later absolute target from the *host* root, so the resolved path
    leaves the extraction root and `is_safe_path` is false.  That is static: it
    depends only on the image.
  * **whether** such a link is still removed is order-dependent: once the
    intermediate absolute link is itself rewritten to a portable relative link
    by an earlier `fix_symlink` call, the chain resolves inside the extraction
    root and the later link is kept.  The at-risk set is therefore a superset of
    the removals, and the removal set is not derivable from the image alone.

Inputs are the independent oracle's tables (`sqfs-list.py --files`,
`--nonregular`, whose symlink detail column is the image target) and a receipt.
No extractor input is read.

Checks (exit 0 iff all hold):
  1. every receipt removal diagnostic resolves to a symlink row of the oracle
     (an exact path relative to the chunk extract root);
  2. every receipt removal is in the statically at-risk set;
  3. every oracle symlink row is in exactly one of {removed, unpublished};
  4. every unpublished entry resolves to a symlink row.
"""

import argparse
import json
import sys


def read_tsv(path, width):
    rows = []
    with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            cells = line.split('\t')
            cells += [''] * (width - len(cells))
            rows.append(tuple(cells[:width]))
    return rows


def norm(parts):
    out = []
    for p in parts:
        if p in ('', '.'):
            continue
        if p == '..':
            if out:
                out.pop()
            continue
        out.append(p)
    return '/'.join(out)


def at_risk(links):
    """{link rel: reason} -- chains that leave the extraction root once the
    first hop is re-rooted and later hops are not rewritten yet."""
    out = {}
    for rel in links:
        cur, hops, seen = rel, 0, set()
        t = links[rel]
        while True:
            hops += 1
            if t == '':
                out[rel] = 'empty-target'
                break
            if cur in seen or hops > 40:
                break                       # loop: resolve() returns the path
            seen.add(cur)
            if t.startswith('/'):
                if hops >= 2:
                    out[rel] = 'absolute-hop'
                    break
                nxt = norm(t.split('/'))
            else:
                nxt = norm(cur.split('/')[:-1] + t.split('/'))
            if nxt not in links:
                break
            cur, t = nxt, links[nxt]
    return out


def rel_of(path):
    """Extract-root-relative path; `$output/` is REA's marker, and a removal
    diagnostic carries the host absolute path, so the first `<chunk>_extract`
    component is the baseline."""
    if not isinstance(path, str):
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    parts = [x for x in p.split('/') if x not in ('', '.')]
    for i, part in enumerate(parts):
        if part.endswith('_extract'):
            return '/'.join(parts[i + 1:])
    return '/'.join(parts)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--oracle', required=True, help='regular-file TSV')
    ap.add_argument('--nonregular', required=True, help='non-regular TSV')
    ap.add_argument('--after', required=True, help='REA after-receipt JSON')
    ap.add_argument('--json-out')
    args = ap.parse_args(argv)

    try:
        rows = read_tsv(args.nonregular, 3)
        with open(args.after, 'r', encoding='utf-8') as f:
            doc = json.load(f)
    except (OSError, ValueError) as exc:
        print('removal-predict: %s' % exc, file=sys.stderr)
        return 2
    if isinstance(doc, dict) and isinstance(doc.get('data'), dict):
        doc = doc['data']
    nr = doc.get('normalized_result') or {}

    links = {rel: detail for rel, kind, detail in rows if kind == 'symlink'}
    kinds = {rel: kind for rel, kind, _ in rows}
    unpublished = {rel_of(u.get('relative_path')) for u in
                   nr.get('unpublished_entries') or [] if isinstance(u, dict)}
    removed = {}
    for d in nr.get('diagnostics') or []:
        if not isinstance(d, dict):
            continue
        report = d.get('report') or {}
        if report.get('__typename__') == 'MaliciousSymlinkRemoved':
            removed[rel_of(report.get('link'))] = report.get('target')

    risk = at_risk(links)
    checks = []
    for rel in sorted(removed):
        if rel not in links:
            checks.append({'check': 'removal is a symlink row', 'rel': rel,
                           'kind': kinds.get(rel)})
        if rel not in risk:
            checks.append({'check': 'removal is statically at risk', 'rel': rel})
    for rel in sorted(links):
        n = (rel in removed) + (rel in unpublished)
        if n != 1:
            checks.append({'check': 'exactly one disposition', 'rel': rel,
                           'removed': rel in removed,
                           'unpublished': rel in unpublished})
    for rel in sorted(unpublished):
        if rel not in links:
            checks.append({'check': 'unpublished entry is a symlink row',
                           'rel': rel, 'kind': kinds.get(rel)})
    summary = {
        'symlink_rows': len(links),
        'statically_at_risk': len(risk),
        'at_risk_links': sorted(risk),
        'receipt_removed': len(removed),
        'removed_links': sorted(removed),
        'receipt_unpublished': len(unpublished),
        'kept_at_risk': sorted(set(risk) - set(removed)),
        'problems': checks,
        'problem_count': len(checks),
        'ok': not checks,
    }
    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=1, sort_keys=True)
            f.write('\n')
    json.dump(summary, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    return 0 if summary['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
