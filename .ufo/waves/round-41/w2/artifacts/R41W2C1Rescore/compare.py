#!/usr/bin/env python3
"""Independent re-scoring of one R41-C1 carrier, from scratch.

Does not import or call tools/round-41/c1-counter.py; the rules below are
re-implemented from the frozen predicate text (plans/round-41-claims.md):
exact-path rule = strip one '$output/' prefix, root = child_path of the
derivation edge whose handler starts 'squashfs_v4', rel only if
P.startswith(root + '/'), comparisons are equality on (root, rel).
"""
import hashlib, json, sys, collections

def load(p):
    return json.load(open(p))

def root_of(nr):
    for e in nr.get('derivations') or []:
        h = e.get('handler') or ''
        if h.startswith('squashfs_v4'):
            cp = e.get('child_path') or ''
            if cp.startswith('$output/'):
                cp = cp[len('$output/'):]
            return cp
    return None

def relof(path, root):
    """rel under the chunk extract root; bare or $output/-prefixed paths only."""
    if not isinstance(path, str) or not path:
        return None
    if path.startswith('$output/'):
        path = path[len('$output/'):]
    elif path.startswith('/'):
        return None          # absolute: not a receipt namespace path
    if root is None or not path.startswith(root + '/'):
        return None
    return path[len(root) + 1:]

def abs_relof(link, root):
    """unblob removal diagnostics carry an absolute link; find the root run."""
    if not isinstance(link, str) or root is None:
        return None
    segs = [x for x in link.split('/') if x not in ('', '.')]
    rsegs = root.split('/')
    for i in range(len(segs) - len(rsegs), -1, -1):
        if segs[i:i + len(rsegs)] == rsegs:
            return '/'.join(segs[i + len(rsegs):])
    return None

def summarize(env, which):
    if 'normalized_result' not in env and isinstance(env.get('data'), dict):
        env = env['data']
    nr = env['normalized_result']
    root = root_of(nr)
    files = {}
    outside = []
    for f in nr.get('files') or []:
        r = relof(f.get('relative_path'), root)
        if r is None:
            outside.append(f.get('relative_path'))
            continue
        files[r] = (f.get('sha256'), f.get('size'))
    gaps = collections.Counter()
    gpaths = collections.Counter()
    gdeps = collections.Counter()
    for g in nr.get('extraction_gaps') or []:
        k = g.get('kind')
        gaps[k] += 1
        r = relof(g.get('relative_path'), root)
        gpaths[(k, r)] += 1
        for d in g.get('dependencies') or []:
            gdeps[(k, r, d)] += 1
    removals = collections.Counter()
    for d in nr.get('diagnostics') or []:
        rep = d.get('report') or {}
        if rep.get('__typename__') == 'MaliciousSymlinkRemoved':
            removals[abs_relof(rep.get('link'), root)] += 1
    return dict(which=which, root=root, files=files, outside=outside,
                gaps=gaps, gpaths=gpaths, gdeps=gdeps, removals=removals,
                chunks=[(c.get('handler'), bool(c.get('extraction_failed')))
                        for c in nr.get('chunks') or []],
                operation=env.get('operation'), provider=(env.get('provider') or {}).get('id'),
                subject=((env.get('subject') or {}).get('digest') or {}).get('sha256'),
                coverage=nr.get('coverage'), published_bytes=nr.get('published_bytes'),
                depth_limited_paths=nr.get('depth_limited_paths'),
                engine=json.dumps(nr.get('engine'), sort_keys=True)[:200],
                params=env.get('parameters'))

def main(cid, receipt, fresh, oracle, nonreg, carrier):
    R = summarize(load(receipt), 'receipt')
    F = summarize(load(fresh), 'fresh')
    out = {'id': cid, 'problems': []}
    P = out['problems']
    for k in ('root', 'operation', 'provider', 'coverage', 'published_bytes', 'engine'):
        out[k] = {R['which']: R[k], F['which']: F[k]}
        if R[k] != F[k]:
            P.append('mismatch %s: receipt=%r fresh=%r' % (k, R[k], F[k]))
    if R['outside'] or F['outside']:
        P.append('files outside root: receipt=%d fresh=%d' % (len(R['outside']), len(F['outside'])))
    if R['subject'] != F['subject']:
        P.append('subject digest differs')
    # carrier identity
    raw = open(carrier, 'rb').read()
    out['carrier'] = {'sha256': hashlib.sha256(raw).hexdigest(), 'size': len(raw)}
    if R['subject'] != out['carrier']['sha256']:
        P.append('receipt subject != carrier sha256')
    # file sets
    rf, ff = R['files'], F['files']
    miss = sorted(set(rf) - set(ff)); extra = sorted(set(ff) - set(rf))
    diff = sorted(k for k in set(rf) & set(ff) if rf[k] != ff[k])
    out['files'] = {'receipt': len(rf), 'fresh': len(ff), 'only_receipt': miss[:20],
                    'only_fresh': extra[:20], 'hash_or_size_differ': diff[:20]}
    if miss or extra or diff:
        P.append('file set mismatch: -%d +%d ~%d' % (len(miss), len(extra), len(diff)))
    # gaps / removals
    out['gaps'] = {R['which']: dict(R['gaps']), F['which']: dict(F['gaps'])}
    if R['gpaths'] != F['gpaths']:
        a = set(R['gpaths']) - set(F['gpaths']); b = set(F['gpaths']) - set(R['gpaths'])
        out['gap_path_diff'] = {'only_receipt': sorted(map(str, list(a)[:10])),
                                'only_fresh': sorted(map(str, list(b)[:10]))}
        P.append('gap (kind,rel) multisets differ: -%d +%d' % (len(a), len(b)))
    if R['gdeps'] != F['gdeps']:
        a = set(R['gdeps']) - set(F['gdeps']); b = set(F['gdeps']) - set(R['gdeps'])
        out['gap_dep_diff'] = {'only_receipt': sorted(map(str, list(a)[:10])),
                               'only_fresh': sorted(map(str, list(b)[:10]))}
        P.append('gap dependencies differ: -%d +%d' % (len(a), len(b)))
    out['removals'] = {R['which']: sorted(k for k in R['removals']),
                       F['which']: sorted(k for k in F['removals'])}
    if R['removals'] != F['removals']:
        P.append('removal diagnostics differ')
    if any(f for _, f in R['chunks']) or any(f for _, f in F['chunks']):
        P.append('a chunk carries extraction_failed')
    out['chunks'] = {'receipt': R['chunks'], 'fresh': F['chunks']}
    # oracle (frozen independent reader) vs both runs
    orows = []
    for line in open(oracle, encoding='utf-8'):
        if not line.strip():
            continue
        p, h, s = line.rstrip('\n').split('\t')
        orows.append((p, h, int(s)))
    om = {p: (h, s) for p, h, s in orows}
    out['oracle'] = {'rows': len(orows), 'unique': len(om)}
    if len(om) != len(orows):
        P.append('oracle lists a path twice')
    for tag, m in (('receipt', rf), ('fresh', ff)):
        m2 = set(om) - set(m); m3 = set(m) - set(om)
        bad = [p for p in set(om) & set(m) if om[p] != m[p]]
        out['oracle'][tag] = {'oracle_only': len(m2), 'run_only': len(m3),
                              'value_differ': len(bad),
                              'oracle_only_sample': sorted(m2)[:10],
                              'run_only_sample': sorted(m3)[:10]}
        if m2 or m3 or bad:
            P.append('oracle vs %s: -%d +%d ~%d' % (tag, len(m2), len(m3), len(bad)))
    # non-regular accounting, independently of the counter
    nrows = []
    for line in open(nonreg, encoding='utf-8'):
        if not line.strip():
            continue
        parts = line.rstrip('\n').split('\t')
        nrows.append((parts[0], parts[1]))
    kinds = collections.Counter(k for _, k in nrows)
    symlinks = {p for p, k in nrows if k == 'symlink'}
    dirs = {p for p, k in nrows if k == 'dir'}
    devs = {p for p, k in nrows if k not in ('symlink', 'dir')}
    acct = collections.Counter()
    for (k, r) in R['gpaths']:
        if k == 'unpublished-entry':
            acct[r] += 1
    for r in R['removals']:
        acct[r] += 1
    unresolved = sorted(p for p in symlinks if acct[p] != 1)
    bogus = sorted(p for p in acct if p not in symlinks)
    published_as_file = sorted(p for p in (symlinks | dirs | devs) if p in rf)
    structural = [k for k in R['gaps'] if k not in ('unpublished-entry',)]
    out['nonregular'] = {'rows': len(nrows), 'kinds': dict(kinds),
                         'symlinks': len(symlinks), 'Dirs': len(dirs), 'devices': len(devs),
                         'unpublished_entries': R['gaps'].get('unpublished-entry', 0),
                         'removals': sum(R['removals'].values()),
                         'unresolved_symlinks': unresolved[:10],
                         'non_symlink_accounted': bogus[:10],
                         'nonregular_published_as_file': published_as_file[:10],
                         'non_unpublished_gap_kinds': structural}
    if unresolved: P.append('%d symlinks not accounted exactly once' % len(unresolved))
    if bogus: P.append('%d accounted paths are not symlink rows' % len(bogus))
    if published_as_file: P.append('%d non-regular rows published as files' % len(published_as_file))
    if sum(R['removals'].values()) > len(symlinks): P.append('more removals than symlinks')
    out['pass'] = not P
    return out

if __name__ == '__main__':
    cid, receipt, fresh, oracle, nonreg, carrier = sys.argv[1:7]
    o = main(cid, receipt, fresh, oracle, nonreg, carrier)
    print(json.dumps(o, indent=1, sort_keys=True))
    sys.exit(0 if o['pass'] else 1)
