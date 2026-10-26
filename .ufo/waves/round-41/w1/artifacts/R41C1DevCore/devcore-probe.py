#!/usr/bin/env python3
"""devcore-probe.py -- round-41 wave-1 recon over one REA after-receipt.

Reads an REA 6.5.0 `extract-firmware` after-receipt (the evidence envelope,
`--format json --full-output`) plus an independent SquashFS oracle
(`sqfs-list.py --files/--nonregular` TSVs) and reports, without trusting any
suffix match:

  * chunk handlers and whether any chunk carries `extraction_failed`;
  * every distinct extract-root named by a published or unpublished path, i.e.
    whether the publication sits under exactly one `<staged name>_extract/`;
  * oracle coverage by EXACT path relative to the chunk extract root (the
    R40-CL1 fix): hits, sha mismatches, rows published at another depth;
  * non-regular entries that a published regular file collides with exactly
    (a materialised symlink/device);
  * gap histogram: path-resolved gaps by entry kind against the oracle's
    non-regular table, structural gaps (null path), gaps that resolve to no
    table row or to several;
  * `unpublished_entries` by kind, and which non-regular table rows are invisible
    to the extractor (no gap, no unpublished entry) -- devices in particular;
  * the staged entry/byte budget: counted from the extraction tree on disk when
    `--outdir` is given (REA's default budget is 10 000 entries and 256 MiB).

Exit 0 when every oracle row is published exactly with the same sha256 and no
published path collides with a non-regular entry; exit 1 otherwise; exit 2 on an
unreadable input.  This is a recon tool: it does not score a claim.
"""

import argparse
import collections
import json
import os
import sys

BUDGET_ENTRIES = 10000          # REA 6.5.0 max_output_files default
BUDGET_BYTES = 256 * 1024 * 1024  # REA 6.5.0 max_output_bytes default


def extract_rel(path, roots=None):
    """Path relative to its chunk extract root, or None.

    unblob extracts a chunk into `<staged name>_extract/`; the leading component
    is dropped only when it ends in `_extract` (the same rule as the round-41
    counter port).  `$output/` is REA's marker for the extraction root."""
    if not isinstance(path, str):
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    parts = [x for x in p.split('/') if x not in ('', '.')]
    if parts and parts[0].endswith('_extract'):
        root = parts[0]
        if roots is not None:
            roots.add(root)
        parts = parts[1:]
    elif parts and roots is not None:
        roots.add('<none>:' + parts[0])
    return '/'.join(parts)


def read_tsv(path, width):
    rows = []
    with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            cells = line.split('\t')
            if len(cells) < width:
                cells += [''] * (width - len(cells))
            rows.append(tuple(cells[:width]))
    return rows


def count_tree(outdir):
    """Staged entries and bytes under the extraction root (unblob's own tree)."""
    entries = files = links = dirs = other = 0
    total = 0
    for base, dirnames, filenames in os.walk(outdir, followlinks=False):
        # Each directory entry is counted once: the walk yields every
        # subdirectory as a `base` later, so `dirnames` here are not pre-counted.
        for name in dirnames + filenames:
            full = os.path.join(base, name)
            try:
                st = os.lstat(full)
            except OSError:
                other += 1
                continue
            entries += 1
            if os.path.stat.S_ISLNK(st.st_mode):
                links += 1
            elif os.path.stat.S_ISREG(st.st_mode):
                files += 1
                total += st.st_size
            elif os.path.stat.S_ISDIR(st.st_mode):
                dirs += 1
            else:
                other += 1
    return {'entries': entries, 'files': files, 'dirs': dirs,
            'links': links, 'other': other, 'bytes': total}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--after', required=True, help='REA after-receipt JSON')
    ap.add_argument('--oracle', required=True, help='regular-file TSV')
    ap.add_argument('--nonregular', required=True, help='non-regular TSV')
    ap.add_argument('--outdir', help='extraction tree, for the staged budget')
    ap.add_argument('--max-rows', type=int, default=20,
                    help='cap each printed example list (default 20)')
    ap.add_argument('--json-out', help='write the full summary here')
    args = ap.parse_args(argv)

    try:
        with open(args.after, 'r', encoding='utf-8') as f:
            doc = json.load(f)
    except (OSError, ValueError) as exc:
        print('devcore-probe: %s' % exc, file=sys.stderr)
        return 2
    if isinstance(doc, dict) and 'ok' in doc and isinstance(doc.get('data'), dict):
        doc = doc['data']       # CLI wrapper: {"ok":true,"data":<envelope>}
    nr = doc.get('normalized_result') or {}
    oracle = read_tsv(args.oracle, 3)
    nonreg = read_tsv(args.nonregular, 3)

    roots = set()
    files = []
    for f in nr.get('files') or []:
        if not isinstance(f, dict):
            continue
        rel = extract_rel(f.get('relative_path'), roots)
        files.append((rel, f.get('sha256') or '', f.get('size'),
                      f.get('relative_path')))
    unpub = []
    for u in nr.get('unpublished_entries') or []:
        if not isinstance(u, dict):
            continue
        unpub.append((extract_rel(u.get('relative_path'), roots),
                      u.get('kind'), u.get('link_target')))

    pub_by_rel = collections.defaultdict(list)
    for rel, sha, size, raw in files:
        pub_by_rel[rel].append((sha, size, raw))
    unpub_by_rel = collections.defaultdict(list)
    for rel, kind, target in unpub:
        unpub_by_rel[rel].append((kind, target))
    nonreg_kind = {}
    for rel, kind, _detail in nonreg:
        nonreg_kind[rel] = kind

    # -- oracle coverage, exact ------------------------------------------
    hits, sha_mismatch, absent, depth_mismatch = [], [], [], []
    for rel, sha, size in oracle:
        cands = pub_by_rel.get(rel) or []
        good = [c for c in cands if c[0] == sha]
        if good:
            hits.append(rel)
            continue
        if cands:
            sha_mismatch.append({'rel': rel, 'oracle_sha256': sha,
                                 'published': [{'sha256': c[0], 'size': c[1]}
                                               for c in cands]})
            continue
        # published under another extract root only (nested extraction)?
        tail = [r for r in pub_by_rel
                if r and (r == rel or r.endswith('/' + rel))]
        if tail:
            depth_mismatch.append({'rel': rel, 'published_as': tail[:5]})
        else:
            absent.append(rel)

    # -- non-regular collisions ------------------------------------------
    materialised = [{'rel': rel, 'kind': nonreg_kind[rel],
                     'published': [c[2] for c in pub_by_rel[rel]]}
                    for rel in nonreg_kind if rel in pub_by_rel]
    invisible = [{'rel': rel, 'kind': kind}
                 for rel, kind in nonreg_kind.items()
                 if rel not in unpub_by_rel]
    unpublished_entries_seen = [{'rel': rel, 'kinds': sorted({k for k, _ in v})}
                                for rel, v in unpub_by_rel.items()]

    # -- gaps -------------------------------------------------------------
    gaps = [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)]
    structural = collections.Counter()
    by_entry_kind = collections.Counter()
    no_row, multi_row = [], []
    per_entry = collections.Counter()
    for g in gaps:
        kind, rp = g.get('kind'), g.get('relative_path')
        if rp is None:
            structural[kind] += 1
            continue
        rel = extract_rel(rp, roots)
        if rel in nonreg_kind:
            per_entry[rel] += 1
            by_entry_kind[nonreg_kind[rel]] += 1
        elif rel in pub_by_rel:
            no_row.append({'rel': rel, 'reason': 'published regular file'})
        else:
            # count table rows the gap could resolve to under any rule
            n = sum(1 for r in nonreg_kind if r == rel)
            (no_row if n == 0 else multi_row).append({'rel': rel})
    # entries that are neither published nor gapped nor listed unpublished
    silent = [{'rel': rel, 'kind': kind} for rel, kind in nonreg_kind.items()
              if rel not in unpub_by_rel and per_entry.get(rel, 0) == 0]

    chunks = [{'handler': c.get('handler'),
               'failed': bool(c.get('extraction_failed')),
               'relative_path': c.get('relative_path')}
              for c in (nr.get('chunks') or []) if isinstance(c, dict)]

    budget = None
    if args.outdir:
        budget = count_tree(args.outdir)
        budget['entry_budget'] = BUDGET_ENTRIES
        budget['byte_budget'] = BUDGET_BYTES
        budget['entries_over'] = budget['entries'] > BUDGET_ENTRIES
        budget['bytes_over'] = budget['bytes'] > BUDGET_BYTES

    summary = {
        'ok': doc.get('ok'),
        'provider': (doc.get('provider') or {}).get('id'),
        'operation': doc.get('operation'),
        'chunks': chunks,
        'handlers': sorted({c['handler'] for c in chunks if c['handler']}),
        'any_chunk_failed': any(c['failed'] for c in chunks),
        'extract_roots': sorted(roots),
        'published_files': len(files),
        'published_bytes': nr.get('published_bytes'),
        'oracle_rows': len(oracle),
        'oracle_hits': len(hits),
        'oracle_sha_mismatch': len(sha_mismatch),
        'oracle_absent': len(absent),
        'oracle_other_depth': len(depth_mismatch),
        'oracle_examples': {
            'sha_mismatch': sha_mismatch[:args.max_rows],
            'absent': absent[:args.max_rows],
            'other_depth': depth_mismatch[:args.max_rows]},
        'nonregular_rows': len(nonreg_kind),
        'nonregular_kinds': dict(collections.Counter(nonreg_kind.values())),
        'materialised_nonregular': materialised[:args.max_rows],
        'materialised_count': len(materialised),
        'unpublished_entries': len(unpub),
        'unpublished_kinds': dict(collections.Counter(k for _, k, _ in unpub)),
        'gaps_total': len(gaps),
        'gaps_structural': dict(structural),
        'gaps_by_entry_kind': dict(by_entry_kind),
        'gaps_without_row': no_row[:args.max_rows],
        'gaps_without_row_count': len(no_row),
        'invisible_nonregular_count': len(invisible),
        'invisible_nonregular_by_kind': dict(
            collections.Counter(x['kind'] for x in invisible)),
        'silent_nonregular_count': len(silent),
        'budget': budget,
        'depth_limited_paths': nr.get('depth_limited_paths'),
    }
    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=1, sort_keys=True)
            f.write('\n')
    json.dump(summary, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    clean = (summary['oracle_hits'] == summary['oracle_rows']
             and summary['materialised_count'] == 0
             and not summary['any_chunk_failed'])
    return 0 if clean else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
