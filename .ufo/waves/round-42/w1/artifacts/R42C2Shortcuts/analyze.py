#!/usr/bin/env python3
"""analyze.py -- shortcut-table analysis for R42-C2 (feeding the wave-1
report of seat R42C2Shortcuts).

Computes, over the universe (real held-out + predicted legacy + predicted
widened combo draws):

  1. minimal-table census: min row count for the full universe and for each
     one-class-deleted universe (class = planned round-41 class bucket, legacy
     family bucket, or the whole combo family);
  2. forced-order graph: for every unordered pair of groups, whether a valid
     13-row table exists with each order (one direction forced -> a genuine
     order dependency the table must encode);
  3. column essentiality: restrict one column to `*` on every row and re-run
     the search; if the minimum rises above 13 (or no table exists) the
     column is load-bearing;
  4. canonical shortcut tables: the first-found minimal table, a least-
     constrained-cell minimal table, and (when it exists) a minimal table
     that never uses the dependencies column;
  5. per-group drop fate: for each group, what happens to its tuples when its
     row is omitted from the canonical table (which other row mislabels them,
     or they fall to unclassified);
  6. deviation frontier: a factor-grid scan outside U over every canonical
     table, reporting the nearest planned class / combo draw whose natural
     variant the table mislabels.
"""
import json
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mintable import (prepare, search_min, load_universe, group_touched,
                      build_rows, row_matches, norm_sr, NOMATCH_PAIR,
                      HANDLER_PATTERNS)  # noqa: E402
from v4eval import classify as v4_classify  # noqa: E402

PLANNED_R41 = [
    'clean-be', 'clean-le', 'clean-empty', 'escaping-symlink-removed',
    'in-tree-symlink-metadata', 'mixed-symlinks', 'dep-missing-be',
    'dep-missing-le', 'avm-marker-be-dropped', 'body-extractor-failure',
    'body-extractor-failure-le', 'partial-body-failure',
    'no-squashfs-chunk', 'out-of-domain', 'partial-in-tree',
    'partial-mixed', 'depth-limited-alone', 'depth-limited-in-tree',
    'depth-limited-mixed', 'failure-depth-limited',
]
LEGACY_FAMILIES = ['legacy-clean', 'legacy-dep-missing', 'legacy-zero-file',
                   'legacy-partial', 'legacy-body-failure']

COLUMNS = ('op', 'pr', 'handler', 'fh', 'gaps', 'deps', 'be', 'sr',
           'files')


MANIFEST = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
            "corpus/evidence/round-41/c2/heldout/manifest.json")
_MAN = json.load(open(MANIFEST)) if os.path.isfile(MANIFEST) else {}
_ID_TO_CLASS = {}
for _c in _MAN.get("carriers") or []:
    if isinstance(_c, dict):
        _ID_TO_CLASS[str(_c.get("id", ""))] = str(_c.get("class", ""))


def bucket_of(m):
    c = m.get('class')
    if c == 'real-heldout':
        cid = m['id'][5:]
        cls = _ID_TO_CLASS.get(cid, cid)
        return 'planned:' + cls
    if c == 'combo':
        return 'combo'
    return 'legacy:' + c

def run_search(members, col_restrict=None, sort_key=None):
    g, rows = prepare(list(members))
    if col_restrict:
        rows = restrict_rows(rows, col_restrict)
    return search_min(g, rows, sort_key=sort_key)


def restrict_rows(rows, col):
    out = {}
    for key, pool in rows.items():
        out[key] = [(r, t) for r, t in pool if r[col] == '*']
    return out


def min_size(members):
    g, rows = prepare(list(members))
    best = search_min(g, rows)
    return len(best) if best is not None else None


def forced_order_pairs(g, rows):
    """For each unordered pair (a,b): 'a<b' possible iff some row of a avoids
    b entirely; 'b<a' iff some row of b avoids a.  Return pairs where exactly
    one direction is possible."""
    keys = [k for k in g if k != NOMATCH_PAIR]
    avoids = {}
    for key in keys:
        membership = [k for k in keys]
        avoids[key] = set()
        for r, touched in rows[key]:
            avoids[key] |= (set(membership) - touched)
    forced = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            a_before_b = b in avoids[a]
            b_before_a = a in avoids[b]
            if a_before_b and not b_before_a:
                forced.append((a, b, 'a-first'))
            elif b_before_a and not a_before_b:
                forced.append((b, a, 'b-first'))
            elif not a_before_b and not b_before_a:
                forced.append((a, b, 'INFEASIBLE'))
    return forced


def table_eval(rows, members):
    """(member -> (label, action)) under an ordered row list."""
    out = {}
    for m in members:
        hit = None
        for r in rows:
            if row_matches(r, m['features']):
                hit = (r['label'], r['action'])
                break
        out[m['id']] = hit or NOMATCH_PAIR
    return out


def constrained_cells(rows):
    return sum(1 for r in rows for c in COLUMNS if r[c] != '*')


def main():
    members = load_universe(os.environ.get("UNIVERSE_PATH")
                            or os.path.join(os.environ.get("TMPDIR") or HERE,
                                            "universe.json"))
    for m in members:
        m['features']['SR'] = norm_sr(m['features']['SR'])

    g, rows = prepare(list(members))
    keys = [k for k in g if k != NOMATCH_PAIR]
    print('== groups ==', len(keys))

    print('== forced order pairs ==')
    for a, b, how in forced_order_pairs(g, rows):
        print('  %s %s %s' % (a[0], how, b[0]))

    print('== column essentiality (restrict col to * everywhere) ==')
    ess = {}
    for col in COLUMNS:
        g2, rows2 = prepare(list(members))
        rows2 = restrict_rows(rows2, col)
        best = search_min(g2, rows2)
        sz = len(best) if best else None
        ess[col] = sz
        print('  %-8s min=%s' % (col, sz if sz is not None else 'infeasible'))

    print('== first-found minimal table ==')
    best0 = search_min(g, rows)
    print('  rows', len(best0), 'constrained cells', constrained_cells([r for _, r in best0]))

    print('== least-constrained minimal table ==')
    best_lc = search_min(g, rows, sort_key=lambda o: constrained_cells([r for _, r in o]))
    print('  rows', len(best_lc), 'constrained cells', constrained_cells([r for _, r in best_lc]))

    print('== minimal table without dependencies column ==')
    g2, rows2 = prepare(list(members))
    rows2 = restrict_rows(rows2, 'deps')
    best_nod = search_min(g2, rows2)
    if best_nod:
        print('  rows', len(best_nod), 'constrained cells',
              constrained_cells([r for _, r in best_nod]))
    else:
        print('  inFEASIBLE without deps column')

    print('== per-group drop fate under first-found table ==')
    rows_of = [r for _, r in best0]
    drop_fates = {}
    for gk in keys:
        label = gk[0]
        reduced = [r for r in rows_of if r['label'] != label]
        fates = {}
        for m in members:
            if tuple(m['expected']) == gk:
                hit = None
                for r in reduced:
                    if row_matches(r, m['features']):
                        hit = (r['label'], r['action'])
                        break
                fates.setdefault(hit or NOMATCH_PAIR, 0)
                fates[hit or NOMATCH_PAIR] += 1
        drop_fates[label] = sorted(fates.items())
        print('  drop %s -> %s' % (label, drop_fates[label]))

    # all-but-one-class min sizes
    print('== all-but-one-class min sizes ==')
    by_bucket = {}
    for m in members:
        by_bucket.setdefault(bucket_of(m), []).append(m)
    for bname in sorted(by_bucket):
        rest = [m for m in members if bucket_of(m) != bname]
        sz = min_size(rest)
        print('  remove %-42s n_remaining=%3d min=%s' % (bname, len(rest), sz))

    # deviation frontier for canonical tables
    print('== deviation frontier ==')
    for name, tbl in (('first-found', best0), ('least-constrained', best_lc),
                      ('no-deps', best_nod)):
        if not tbl:
            continue
        trows = [r for _, r in tbl]
        devs = scan_deviations(trows, members)
        print('  %-18s deviations=%d' % (name, len(devs)))

    res = {
        'forced_order': [[a[0], how, b[0]] for a, b, how in
                         forced_order_pairs(g, rows)],
        'column_essentiality': ess,
        'first_found': [[list(k), r] for k, r in best0],
        'least_constrained': [[list(k), r] for k, r in best_lc],
        'no_deps': [[list(k), r] for k, r in best_nod] if best_nod else None,
        'drop_fates': drop_fates,
    }
    out = os.environ.get("ANALYZE_OUT") or os.path.join(
        os.environ.get("TMPDIR") or HERE, "analyze.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print('wrote', out)


def scan_deviations(trows, members):
    """Grid scan: vary H family, G subset, D subset, BE, SR, P and compare the
    table to the v4 evaluator, returning ids of deviating tuples."""
    kinds = ["extractor-failure", "depth-limited", "unpublished-entry",
             "missing-extractor-dependency", "unknown-chunk-handler"]
    devs = []
    handlers = [["squashfs_v4_be"], ["squashfs_v4_le"],
                ["squashfs_v3"], ["squashfs_v1"], [],
                ["squashfs_v4_be", "squashfs_v3"],
                ["squashfs_v4_le", "squashfs_v3"]]
    hf_map = {"squashfs_v4_be": "squashfs_v4_be",
              "squashfs_v4_le": "squashfs_v4_le",
              "squashfs_v3": "squashfs_v3",
              "squashfs_v1": "squashfs_v1",
              "squashfs_v4_be,squashfs_v3": "squashfs_v3",
              "squashfs_v4_le,squashfs_v3": "squashfs_v4_le"}
    gap_opts = [set(x) for r in range(0, 3)
                for x in product(kinds, repeat=r)]
    gap_opts = list(dict.fromkeys(frozenset(x) for x in gap_opts))
    dep_opts = [set(), {"sasquatch"}, {"sasquatch-v4be"},
                {"sasquatch", "sasquatch-v4be"}]
    count = 0
    for h in handlers:
        for gset in gap_opts:
            for dset in dep_opts:
                for be in ("yes", "no", "n/a"):
                    for sr in ("yes", "no"):
                        for p in (0, 1):
                            hf = [] if not h else [hf_map[",".join(h)]]
                            f = {"OP": "extract_firmware", "PR": "unblob",
                                 "H": h, "HF": hf, "G": sorted(gset),
                                 "D": sorted(dset), "BE": be, "SR": sr,
                                 "P": p}
                            pair, _ = v4_classify(f)
                            exp = pair
                            hit = None
                            for r in trows:
                                if row_matches(r, f):
                                    hit = (r['label'], r['action'])
                                    break
                            got = hit or NOMATCH_PAIR
                            count += 1
                            if got != exp:
                                devs.append({
                                    "features": f, "expected": list(exp),
                                    "got": list(got),
                                })
    return devs


if __name__ == "__main__":
    sys.exit(main())
