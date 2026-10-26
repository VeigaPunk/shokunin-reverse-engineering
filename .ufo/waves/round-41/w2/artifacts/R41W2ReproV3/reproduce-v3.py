#!/usr/bin/env python3
"""R41W2ReproV3 — independent reproduction check for the R41-C1 V3 receipt.

Written from the P41-C1 predicate, the exact-path rule of
`.ufo/waves/round-41/w1/R41C1Revenger.md` §1 and the gap rule
`.ufo/waves/round-41/c1/gap-rule.json`. It does not import or run the frozen
counter; the counter's own projection is compared separately.

    python3 -I -B reproduce-v3.py --committed <lane>/corpus/evidence/round-41/c1/V3/after.json \
        --fresh <fresh after.json> --oracle <oracle.tsv> --nonregular <nonregular.tsv> \
        --pin <carrier sha256> --json-out <out.json>
"""
import argparse
import json
import sys


def strip_output(path):
    """One optional `$output/` prefix removed (both namespaces name the same tree)."""
    if isinstance(path, str) and path.startswith('$output/'):
        return path[len('$output/'):]
    return path


def parts(path):
    if not isinstance(path, str) or not path:
        return None
    return [x for x in strip_output(path).split('/') if x not in ('', '.')]


def chunk_root(env):
    """The chunk extract root CR: child path of the squashfs_v4 derivation edge."""
    nr = env.get('normalized_result') or {}
    roots = set()
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        h = d.get('handler')
        if isinstance(h, str) and h.startswith('squashfs_v4'):
            child = strip_output(d.get('child_path'))
            if isinstance(child, str) and child:
                roots.add(child.rstrip('/'))
    return roots


def rel_of(path, root):
    """rel(P) by whole-segment prefix equality against one root, else None."""
    pp = parts(path)
    if pp is None or root is None:
        return None
    rp = [x for x in root.split('/') if x not in ('', '.')]
    if pp[:len(rp)] != rp:
        return None
    rest = pp[len(rp):]
    return '/'.join(rest) if rest else ''


def table(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh.read().splitlines():
            if line:
                rows.append(line.split('\t'))
    return rows


def diag_rel(d, root):
    """Entry path of a removal diagnostic: the root run inside report.link."""
    report = d.get('report') if isinstance(d, dict) else None
    link = report.get('link') if isinstance(report, dict) else None
    if not isinstance(link, str) or not link or root is None:
        return None
    segs = [x for x in link.split('/') if x not in ('', '.')]
    rsegs = [x for x in root.split('/') if x not in ('', '.')]
    for i in range(len(segs) - len(rsegs), -1, -1):
        if segs[i:i + len(rsegs)] == rsegs:
            return '/'.join(segs[i + len(rsegs):])
    return None


def examine(env, oracle, nonreg, pin, label):
    """Per-receipt verdict with the counter's clause names."""
    nr = env.get('normalized_result') or {}
    out = {'label': label}
    roots = chunk_root(env)
    out['chunk_roots'] = sorted(roots)
    # exactly one squashfs_v4 root is the V3 shape
    if len(roots) != 1:
        out['error'] = 'expected one squashfs_v4 derivation root, saw %r' % (sorted(roots),)
        return out
    root = sorted(roots)[0]
    out['root'] = root

    subject = ((env.get('subject') or {}).get('digest') or {}).get('sha256')
    out['subject_sha256'] = subject
    out['subject_pin_ok'] = subject == pin

    handlers = [c.get('handler') for c in nr.get('chunks') or [] if isinstance(c, dict)]
    out['chunk_handlers'] = handlers
    out['handler_ok'] = handlers == ['squashfs_v4_be']
    out['failed_chunks'] = [c for c in nr.get('chunks') or []
                            if isinstance(c, dict) and c.get('extraction_failed')]
    out['chunks_ok'] = bool(handlers) and not out['failed_chunks']

    # ---- regular files vs oracle (exact rel + sha256 + size, both directions)
    published = {}
    for f in nr.get('files') or []:
        if not isinstance(f, dict):
            continue
        rel = rel_of(f.get('relative_path'), root)
        if rel is None:
            continue
        published.setdefault(rel, []).append(
            (f.get('sha256'), f.get('size'), f.get('relative_path')))
    out['published_files'] = len(published)
    out['published_outside_root'] = [f.get('relative_path') for f in nr.get('files') or []
                                     if isinstance(f, dict)
                                     and rel_of(f.get('relative_path'), root) is None]
    hits, mismatches, extra = [], [], []
    for row in oracle:
        rel, sha = row[0], row[1]
        size = int(row[2]) if len(row) > 2 else None
        got = published.get(rel)
        if got is None:
            mismatches.append({'rel': rel, 'why': 'not published at this rel'})
            continue
        if len(got) != 1:
            mismatches.append({'rel': rel, 'why': 'published %d times' % len(got)})
            continue
        gsha, gsize, gpath = got[0]
        if gsha != sha:
            mismatches.append({'rel': rel, 'why': 'sha256 %s != oracle %s' % (gsha, sha)})
            continue
        if size is not None and gsize != size:
            mismatches.append({'rel': rel, 'why': 'size %r != oracle %r' % (gsize, size)})
            continue
        hits.append(rel)
    for rel in published:
        if rel not in {r[0] for r in oracle}:
            extra.append(rel)
    out['oracle_files'] = len(oracle)
    out['oracle_hits'] = len(hits)
    out['oracle_hits_ok'] = len(hits) == len(oracle)
    out['file_mismatches'] = mismatches
    out['published_not_in_oracle'] = extra
    nonreg_rels = {r[0] for r in nonreg}
    out['nonregular_published'] = sorted(set(published) & nonreg_rels)
    out['nonregular_unpublished_ok'] = not out['nonregular_published']

    # ---- gaps by kind and path
    gaps = [g for g in nr.get('extraction_gaps') or [] if isinstance(g, dict)]
    out['gaps'] = [[g.get('kind'), rel_of(g.get('relative_path'), root)]
                   if g.get('relative_path') is not None
                   else [g.get('kind'), None] for g in gaps]
    out['gap_kinds'] = {}
    for kind, _rel in out['gaps']:
        out['gap_kinds'][kind] = out['gap_kinds'].get(kind, 0) + 1

    # ---- diagnostics
    diags = [d for d in nr.get('diagnostics') or [] if isinstance(d, dict)]
    out['diagnostics'] = [[((d.get('report') or {}).get('__typename__')),
                           diag_rel(d, root)] for d in diags]

    # ---- gap rule: one disposition per required non-regular row
    allowed = {'symlink': {'unpublished-entry'}, 'char-device': set(),
               'block-device': set(), 'fifo': {'unpublished-entry'},
               'socket': {'unpublished-entry'}, 'dir': set()}
    required = {'symlink': True}
    gapped = {}
    unresolved = []
    for g in gaps:
        if g.get('relative_path') is None:
            continue
        rel = rel_of(g.get('relative_path'), root)
        if rel is None:
            unresolved.append({'gap': g.get('kind'), 'path': g.get('relative_path'),
                               'why': 'outside root'})
            continue
        gapped.setdefault(rel, set()).add(g.get('kind'))
    removed = {}
    for d in diags:
        if ((d.get('report') or {}).get('__typename__')) != 'MaliciousSymlinkRemoved':
            continue
        rel = diag_rel(d, root)
        if rel is None:
            unresolved.append({'removal': 'no path under root'})
            continue
        removed.setdefault(rel, 0)
        removed[rel] += 1
    kinds = {r[0]: r[1] for r in nonreg}
    problems = []
    for rel, kind in kinds.items():
        dispo = []
        if rel in gapped:
            if gapped[rel] - allowed.get(kind, set()):
                problems.append({'rel': rel, 'kind': kind,
                                 'why': 'gap kind %r not allowed for %r'
                                        % (sorted(gapped[rel]), kind)})
            dispo.append('gap')
        if rel in removed:
            if kind != 'symlink':
                problems.append({'rel': rel, 'kind': kind, 'why': 'removal on non-symlink'})
            dispo.append('removal')
        if len(dispo) > 1:
            problems.append({'rel': rel, 'kind': kind, 'why': 'gapped and removed'})
        if required.get(kind) and len(dispo) != 1:
            problems.append({'rel': rel, 'kind': kind,
                             'why': '%d dispositions (need exactly 1)' % len(dispo)})
        if kind in ('dir', 'char-device', 'block-device') and dispo:
            problems.append({'rel': rel, 'kind': kind,
                             'why': 'invisible kind carries a disposition'})
    for rel in gapped:
        if rel not in kinds:
            problems.append({'rel': rel, 'why': 'gap resolves to no non-regular row'})
    for rel in removed:
        if rel not in kinds:
            problems.append({'rel': rel, 'why': 'removal resolves to no non-regular row'})
    out['nonregular_rows'] = len(nonreg)
    out['gaps_ok'] = not problems and not unresolved
    out['gap_problems'] = problems
    out['gap_unresolved'] = unresolved
    out['structural'] = {'depth-limited': out['gap_kinds'].get('depth-limited', 0),
                         'unknown-chunk-handler':
                             out['gap_kinds'].get('unknown-chunk-handler', 0)}
    out['structural_ok'] = (out['structural']['depth-limited'] <= 1
                            and out['structural']['unknown-chunk-handler'] == 0)

    # ---- plus-extractor projection (fresh fields; run-variant fields excluded)
    def norm(path):
        rel = rel_of(path, root)
        if rel is not None:
            return rel
        # run-invariant fallback for paths outside the subject root
        p = strip_output(path)
        segs = [x for x in (p or '').split('/') if x not in ('', '.')]
        for i, s in enumerate(segs):
            if s.endswith('_extract') and i + 1 < len(segs):
                return '/'.join(segs[i + 1:])
        return '/'.join(segs) if segs else None

    files = sorted([norm(f.get('relative_path')), f.get('sha256'), f.get('size'),
                    f.get('mime_type')] for f in nr.get('files') or [] if isinstance(f, dict))
    chunks = sorted([[c.get('handler'), (c.get('range') or {}).get('offset'),
                      (c.get('range') or {}).get('length'), bool(c.get('extraction_failed'))]
                     for c in nr.get('chunks') or [] if isinstance(c, dict)])
    gaps_p = sorted([[g.get('kind'), norm(g.get('relative_path'))]
                     for g in gaps])
    unpub = sorted([[u.get('kind'), norm(u.get('relative_path'))]
                    for u in nr.get('unpublished_entries') or [] if isinstance(u, dict)])
    diag_p = sorted([[(d.get('report') or {}).get('__typename__'),
                      diag_rel(d, root) or norm(d.get('input_path'))] for d in diags])
    derivs = sorted([[norm(d.get('parent_path')), norm(d.get('child_path')),
                      d.get('handler')] for d in nr.get('derivations') or []
                     if isinstance(d, dict)])
    engine = nr.get('engine') or {}
    out['projection'] = {
        'subject_sha256': subject, 'files': files, 'chunks': chunks,
        'extraction_gaps': gaps_p, 'unpublished_entries': unpub,
        'diagnostics': diag_p, 'derivations': derivs,
        'engine': [engine.get('name'), engine.get('version')],
        'published_bytes': nr.get('published_bytes'), 'coverage': nr.get('coverage'),
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--committed', required=True)
    ap.add_argument('--fresh', required=True)
    ap.add_argument('--oracle', required=True)
    ap.add_argument('--nonregular', required=True)
    ap.add_argument('--pin', required=True)
    ap.add_argument('--json-out')
    a = ap.parse_args()

    oracle = table(a.oracle)
    nonreg = [(r[0], r[1]) for r in table(a.nonregular)]
    committed = json.load(open(a.committed))
    fresh = json.load(open(a.fresh))

    res = {'pin': a.pin,
           'committed': examine(committed, oracle, nonreg, a.pin, 'committed'),
           'fresh': examine(fresh, oracle, nonreg, a.pin, 'fresh')}

    diffs = {}
    cp, fp = res['committed']['projection'], res['fresh']['projection']
    for key in cp:
        if cp[key] != fp[key]:
            if isinstance(cp[key], list):
                onlyc = [x for x in cp[key] if x not in fp[key]]
                onlyf = [x for x in fp[key] if x not in cp[key]]
                diffs[key] = {'committed_only': onlyc[:5], 'fresh_only': onlyf[:5],
                              'counts': [len(cp[key]), len(fp[key])]}
            else:
                diffs[key] = {'committed': cp[key], 'fresh': fp[key]}
    res['projection_ok'] = not diffs
    res['projection_diff'] = diffs
    res['committed_only'] = {k: v for k, v in res['committed'].items()
                             if k not in ('projection',)}
    text = json.dumps(res, indent=1, sort_keys=True)
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            fh.write(text + '\n')
    print(json.dumps({'projection_ok': res['projection_ok'],
                      'projection_diff_keys': sorted(diffs),
                      'committed': {k: res['committed'].get(k) for k in
                                    ('subject_pin_ok', 'handler_ok', 'chunks_ok',
                                     'oracle_hits', 'oracle_files', 'oracle_hits_ok',
                                     'gaps_ok', 'nonregular_unpublished_ok',
                                     'structural_ok', 'gap_kinds', 'nonregular_rows')},
                      'fresh': {k: res['fresh'].get(k) for k in
                                ('subject_pin_ok', 'handler_ok', 'chunks_ok',
                                 'oracle_hits', 'oracle_files', 'oracle_hits_ok',
                                 'gaps_ok', 'nonregular_unpublished_ok',
                                 'structural_ok', 'gap_kinds', 'nonregular_rows')}},
                     indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
