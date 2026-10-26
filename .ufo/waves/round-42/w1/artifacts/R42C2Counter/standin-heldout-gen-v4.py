#!/usr/bin/env python3
"""STAND-IN v4 held-out generator — dry-run scaffold for `tools/round-42/heldout-gen-v4.py`.

NOT the frozen generator (owned by the `R42C2Gen` seat, which builds carriers
from real unblob fixtures through REA). This stand-in exists so the round-42 C2
counter can be dry-run end to end before the owning drafts land: it writes
carriers, envelopes and a manifest with the round-42 A1 shape, deterministically
from `--seed`, so every binding of the counter is exercised.

Manifest shape (round-42 A1)
  seed             the freeze commit hash (or the dev seed with --arm dev)
  generator        {name, version, sha256 of this file}
  classes          named class list (no `combo`)
  combo_count      number of `combo` carriers
  combo_factors    {combo id: [decision factor, ...]} (>= 2 per combo)
  carriers[]       id, class, arm, carrier, envelope, sha256,
                   declared_features  <- THE ONLY declared-tuple key (R41-CL1)
  fixtures         absent: the stand-in fetches no fixture

Envelope shape: a bare data object with subject/operation/provider/
normalized_result (chunks, extraction_gaps, files, diagnostics), as the
round-41 committed envelopes carry, plus nothing else.  Extractor-failure gaps
carry their `handler` (A1's HF).

Usage
  heldout-gen-v4.py --seed SEED --out DIR [--arm heldout|dev] [--verify]
  heldout-gen-v4.py --selftest
Exit 0 on success, 1 when --verify finds a byte difference, 2 on bad usage.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile

H_V4_BE = 'squashfs_v4_be'
H_V4_LE = 'squashfs_v4_le'
H_V1 = 'squashfs_v1'
H_V2 = 'squashfs_v2'
H_V3 = 'squashfs_v3'
H_V3_BE = 'squashfs_v3_be'
H_V3_DD = 'squashfs_v3_ddwrt'
H_V3_BC = 'squashfs_v3_broadcom'
H_TRX = 'trx_v1'
H_GZIP = 'gzip'

LEGACY_PREFIXES = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3')


def rec(H=(), G=(), D=(), BE='n/a', SR=False, P=2, OP='extract_firmware',
        PR='unblob', HF=None):
    return {'H': list(H), 'G': list(G), 'D': list(D), 'BE': BE, 'SR': SR,
            'P': P, 'OP': OP, 'PR': PR, 'HF': HF}


def squashfs(H):
    return [h for h in H if h.startswith('squashfs_')]


def legacy(H):
    return [h for h in squashfs(H) if h.startswith(LEGACY_PREFIXES)]


# The round-41 named classes, the round-42 legacy family (A1) and the two A1
# decision classes.  The pair is NOT declared here (the evaluator derives it).
NAMED = [
    ('clean-be', rec(H=[H_V4_BE], BE='no')),
    ('clean-le', rec(H=[H_V4_LE], BE='no')),
    ('clean-empty', rec(H=[H_V4_BE], P=0)),
    ('escaping-symlink-removed', rec(H=[H_V4_BE], SR=True)),
    ('in-tree-symlink-metadata', rec(H=[H_V4_BE], G=['unpublished-entry'])),
    ('mixed-symlinks', rec(H=[H_V4_BE], G=['unpublished-entry'], SR=True)),
    ('dep-missing-be', rec(H=[H_V4_BE], G=['missing-extractor-dependency'],
                           D=['sasquatch-v4be'], P=0)),
    ('dep-missing-le', rec(H=[H_V4_LE], G=['missing-extractor-dependency'],
                           D=['sasquatch'], P=0)),
    ('avm-marker-be-dropped', rec(H=[H_V4_BE], G=['extractor-failure'],
                                  HF=H_V4_BE, BE='no', P=0)),
    ('body-extractor-failure', rec(H=[H_V4_BE], G=['extractor-failure'],
                                   HF=H_V4_BE, BE='yes', P=0)),
    ('body-extractor-failure-le', rec(H=[H_V4_LE], G=['extractor-failure'],
                                      HF=H_V4_LE, BE='no', P=0)),
    ('partial-body-failure', rec(H=[H_V4_BE], G=['extractor-failure'],
                                 HF=H_V4_BE, BE='yes', P=3)),
    ('no-squashfs-chunk', rec(P=0)),
    ('out-of-domain', rec(H=[H_V4_BE], OP='analyze')),
    ('partial-in-tree', rec(H=[H_V4_BE], G=['extractor-failure',
                                            'unpublished-entry'], P=2)),
    ('partial-mixed', rec(H=[H_V4_BE], G=['extractor-failure',
                                          'unpublished-entry'], SR=True, P=2)),
    ('depth-limited-alone', rec(H=[H_V4_BE], G=['depth-limited'], P=2)),
    ('depth-limited-in-tree', rec(H=[H_V4_BE], G=['depth-limited',
                                                  'unpublished-entry'], P=2)),
    ('depth-limited-mixed', rec(H=[H_V4_BE], G=['depth-limited',
                                                'unpublished-entry'], SR=True,
                                P=2)),
    ('failure-depth-limited', rec(H=[H_V4_BE], G=['extractor-failure',
                                                  'depth-limited'],
                                  HF=H_V4_BE, BE='yes', P=0)),
    # ---- A1 decision classes
    ('container-depth-limited', rec(H=[H_TRX], G=['depth-limited'], P=0)),
    ('unknown-residue', rec(H=[H_V4_BE], G=['unknown-chunk-handler'], P=2)),
    # ---- legacy family (round-42 widening)
    ('legacy-clean-v1', rec(H=[H_V1], BE='no')),
    ('legacy-clean-v2', rec(H=[H_V2], BE='no')),
    ('legacy-clean-v3-le', rec(H=[H_V3], BE='no')),
    ('legacy-clean-v3-be', rec(H=[H_V3_BE], BE='no')),
    ('legacy-clean-v3-ddwrt', rec(H=[H_V3_DD], BE='no')),
    ('legacy-clean-v3-broadcom', rec(H=[H_V3_BC], BE='no')),
    ('legacy-clean-empty', rec(H=[H_V3], P=0)),
    ('legacy-dep-missing-be', rec(H=[H_V3_BE],
                                  G=['missing-extractor-dependency'],
                                  D=['sasquatch'], P=0)),
    ('legacy-dep-missing-le', rec(H=[H_V3],
                                  G=['missing-extractor-dependency'],
                                  D=['sasquatch'], P=0)),
    ('legacy-body-failure-v1', rec(H=[H_V1], G=['extractor-failure'],
                                   HF=H_V1, BE='no', P=0)),
    ('legacy-body-failure-v3', rec(H=[H_V3], G=['extractor-failure'],
                                   HF=H_V3, BE='no', P=0)),
    ('legacy-partial-v3', rec(H=[H_V3], G=['extractor-failure'], HF=H_V3,
                              BE='no', P=2)),
    ('legacy-depth-limited-v3', rec(H=[H_V3], G=['depth-limited'], BE='no', P=2)),
    ('legacy-in-tree-v3', rec(H=[H_V3], G=['unpublished-entry'], BE='no', P=2)),
]

DEV = [
    ('legacy-clean-v1', rec(H=[H_V1], BE='no')),
    ('legacy-clean-v2', rec(H=[H_V2], BE='no')),
    ('legacy-clean-v3-le', rec(H=[H_V3], BE='no')),
    ('legacy-clean-v3-be', rec(H=[H_V3_BE], BE='no')),
    ('legacy-body-failure-v3', rec(H=[H_V3], G=['extractor-failure'],
                                   HF=H_V3, BE='no', P=0)),
    ('legacy-dep-missing-le', rec(H=[H_V3], G=['missing-extractor-dependency'],
                                  D=['sasquatch'], P=0)),
    ('legacy-partial-v3', rec(H=[H_V3], G=['extractor-failure'], HF=H_V3,
                              BE='no', P=3)),
]

FAMILIES = ([H_V4_BE], [H_V4_LE], [H_V3], [H_V3_BE], [H_V1], [H_V2],
            [H_V3, H_V4_LE], [H_V1, H_V4_BE], [H_V2, H_V3],
            [H_TRX], [H_GZIP, H_TRX], [H_TRX, H_V3], [H_V3, H_V4_BE])
GAPSETS = ([], ['unpublished-entry'], ['depth-limited'],
           ['depth-limited', 'unpublished-entry'], ['extractor-failure'],
           ['extractor-failure', 'depth-limited'],
           ['extractor-failure', 'unpublished-entry'],
           ['missing-extractor-dependency'],
           ['missing-extractor-dependency', 'depth-limited'],
           ['unknown-chunk-handler'],
           ['unknown-chunk-handler', 'depth-limited'],
           ['extractor-failure', 'unknown-chunk-handler'])

COMBO_COUNT = 24


def factors(f):
    """The A1 decision factors one carrier draws (report + wellformedness)."""
    H, G = set(f['H']), set(f['G'])
    F = {h for h in H if h.startswith('squashfs_')}
    L = {h for h in F if h.startswith(LEGACY_PREFIXES)}
    out = []
    if L:
        out.append('legacy_chunk')
    if len(F) >= 2 and any(h.startswith('squashfs_v4') for h in F):
        out.append('second_v4_chunk')
    if 'unknown-chunk-handler' in G:
        out.append('residue')
    if not F and 'depth-limited' in G:
        out.append('container_wrap')
    if 'extractor-failure' in G:
        out.append('damage')
    if 'missing-extractor-dependency' in G:
        out.append('dependency_unreachable')
    if 'depth-limited' in G:
        out.append('max_depth')
    if f['SR'] or 'unpublished-entry' in G:
        out.append('links')
    return out


def features_declared(f):
    return {'handler_set': sorted(f['H']),
            'gap_kinds': sorted(f['G']),
            'gap_dependencies': sorted(f['D']),
            'be_argv': f['BE'],
            'symlink_removed': bool(f['SR']),
            'published': '>0' if f['P'] else '0',
            'extraction_failed': 'yes' if 'extractor-failure' in f['G'] else 'no'}


def tuple_key(f):
    return (tuple(sorted(f['H'])), tuple(sorted(f['G'])), tuple(sorted(f['D'])),
            f['BE'], bool(f['SR']), bool(f['P']))


def build_envelope(f, digest):
    failing = 'extractor-failure' in f['G']
    fail_h = f['HF'] or (squashfs(f['H']) or f['H'] or [None])[0]
    chunks = []
    for h in f['H']:
        chunks.append({'handler': h,
                       'extraction_failed': bool(failing and h == fail_h)})
    gaps = []
    for k in f['G']:
        gap = {'kind': k, 'paths': [],
               'dependencies': list(f['D'])
               if k == 'missing-extractor-dependency' else []}
        if k == 'extractor-failure' and fail_h:
            gap['handler'] = fail_h
        gaps.append(gap)
    diags = []
    if f['BE'] in ('yes', 'no') and f['H']:
        diags.append({'report': {'__typename__': 'CommandReport',
                                 'command': ['sasquatch']
                                 + (['-be'] if f['BE'] == 'yes' else [])
                                 + ['-no-exit-code', '-d', 'out', 'carrier.sqsh']}})
    if f['SR']:
        diags.append({'report': {'__typename__': 'MaliciousSymlinkRemoved',
                                 'path': 'etc/escape', 'target': '../../etc/passwd'}})
    return {'subject': {'name': 'carrier.sqsh',
                        'digest': {'sha256': digest},
                        'format': 'file',
                        'architecture': None,
                        'local_path': '/dev/null'},
            'operation': f['OP'],
            'provider': {'id': f['PR'], 'name': 'Unblob', 'version': '26.6.4'},
            'normalized_result': {
                'chunks': chunks,
                'extraction_gaps': gaps,
                'files': [{'path': 'file%d' % i} for i in range(f['P'])],
                'diagnostics': diags}}


def combos_for(seed):
    """24 combos, each drawing >= 2 decision factors, tuples no class carries."""
    named = {tuple_key(f) for _, f in NAMED}
    pool = []
    for fam in FAMILIES:
        for gaps in GAPSETS:
            for sr in (False, True):
                for be in ('yes', 'no', 'n/a'):
                    for pub in (0, 2):
                        deps = ['sasquatch'] if 'missing-extractor-dependency' in gaps \
                            else []
                        f = rec(H=fam, G=gaps, D=deps, BE=be, SR=sr, P=pub)
                        if len(factors(f)) < 2:
                            continue
                        if tuple_key(f) in named:
                            continue
                        pool.append(f)
    digest = hashlib.sha256(('combos:' + seed).encode()).hexdigest()
    order = sorted(range(len(pool)),
                   key=lambda i: hashlib.sha256(
                       (digest + ':%d' % i).encode()).hexdigest())
    out, seen = [], set()
    for i in order:
        k = tuple_key(pool[i])
        if k in seen:
            continue
        seen.add(k)
        out.append(pool[i])
        if len(out) == COMBO_COUNT:
            break
    return out


def carrier_bytes(seed, ident):
    h = hashlib.sha256(('%s:%s' % (seed, ident)).encode()).hexdigest()
    return h.encode() + b'\n' + bytes.fromhex(h) * 4


def write_tree(out, seed, arm):
    """Write carriers, envelopes and the manifest; return the manifest."""
    os.makedirs(out, exist_ok=True)
    classes = [c for c, _ in (DEV if arm == 'dev' else NAMED)]
    carriers = []
    combo_factors = {}

    def emit(ident, cls, f, arm_name):
        body = carrier_bytes(seed, ident)
        sha = hashlib.sha256(body).hexdigest()
        d = os.path.join(out, ident)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'carrier.sqsh'), 'wb') as fh:
            fh.write(body)
        with open(os.path.join(d, 'envelope.json'), 'w') as fh:
            json.dump(build_envelope(f, sha), fh, indent=1, sort_keys=True)
            fh.write('\n')
        carriers.append({'id': ident, 'class': cls, 'arm': arm_name,
                         'carrier': ident + '/carrier.sqsh',
                         'envelope': ident + '/envelope.json',
                         'sha256': sha,
                         'declared_features': features_declared(f)})
        return factors(f)

    if arm == 'dev':
        for i, (cls, f) in enumerate(DEV):
            emit('D%02d' % (i + 1), cls, f, 'after')
    else:
        for i, (cls, f) in enumerate(NAMED):
            for k in range(2):
                emit('H%02d' % (i * 2 + k + 1), cls, f,
                     'ood' if f['OP'] != 'extract_firmware' else 'after')
        for j, f in enumerate(combos_for(seed)):
            combo_factors['C%02d' % (j + 1)] = emit('C%02d' % (j + 1), 'combo',
                                                   f, 'after')
    man = {'seed': seed,
           'generator': {'name': 'heldout-gen-v4.py',
                         'version': 'r42-c2-standin-a1',
                         'sha256': hashlib.sha256(
                             open(os.path.abspath(__file__), 'rb').read()).hexdigest()},
           'classes': classes,
           'combo_count': COMBO_COUNT if arm != 'dev' else 0,
           'carriers': carriers}
    if combo_factors:
        man['combo_factors'] = combo_factors
    with open(os.path.join(out, 'manifest.json'), 'w') as fh:
        json.dump(man, fh, indent=1, sort_keys=True)
        fh.write('\n')
    return man


def selftest():
    fails = []
    tmp = tempfile.mkdtemp(prefix='genv4.')
    try:
        a = write_tree(os.path.join(tmp, 'a'), 'a' * 64, 'heldout')
        b = write_tree(os.path.join(tmp, 'b'), 'a' * 64, 'heldout')
        if a != b:
            fails.append('regeneration not byte-identical')
        if len(a['carriers']) != 2 * len(NAMED) + COMBO_COUNT:
            fails.append('carrier count %d' % len(a['carriers']))
        for c in a['carriers']:
            if set(c) & {'declared', 'features', 'class_expected'}:
                fails.append('%s carries a non-`declared_features` tuple key' % c['id'])
            if 'declared_features' not in c:
                fails.append('%s carries no declared_features' % c['id'])
        combos = [c for c in a['carriers'] if c['class'] == 'combo']
        if len(combos) != COMBO_COUNT:
            fails.append('combos %d' % len(combos))
        for cid, fs in (a.get('combo_factors') or {}).items():
            if len(fs) < 2:
                fails.append('%s draws only %r' % (cid, fs))
        named = {tuple_key(f) for _, f in NAMED}
        for f in combos_for('a' * 64):
            if tuple_key(f) in named:
                fails.append('combo tuple coincides with a named class')
                break
        dev = write_tree(os.path.join(tmp, 'd'), 'b' * 40, 'dev')
        if len(dev['carriers']) != len(DEV):
            fails.append('dev carriers %d' % len(dev['carriers']))
        joined = json.dumps(a) + json.dumps(dev)
        for key in ('"declared"', '"class_expected"', '"features":'):
            if key in joined:
                fails.append('manifest carries forbidden key %s' % key)
        labels = {c['class'] for c in a['carriers']}
        for need in ('container-depth-limited', 'unknown-residue',
                     'legacy-body-failure-v3'):
            if need not in labels:
                fails.append('missing named class %s' % need)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({'selftest': 'heldout-gen-v4 (standin, A1)',
                      'named_classes': len(NAMED), 'combos': COMBO_COUNT,
                      'dev_classes': len(DEV), 'failures': fails},
                     sort_keys=True))
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed')
    ap.add_argument('--out')
    ap.add_argument('--arm', default='heldout', choices=('heldout', 'dev'))
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.seed:
        ap.error('--seed is required')
    if a.verify:
        if not a.out:
            ap.error('--verify needs --out to compare against')
        tmp = tempfile.mkdtemp(prefix='genv4v.')
        try:
            write_tree(os.path.join(tmp, 'regen'), a.seed, a.arm)
            diffs = []
            for root, _, files in os.walk(os.path.join(tmp, 'regen')):
                for n in files:
                    rel = os.path.relpath(os.path.join(root, n),
                                          os.path.join(tmp, 'regen'))
                    p = os.path.join(a.out, rel)
                    if not os.path.isfile(p):
                        diffs.append(rel + ' missing')
                    elif open(os.path.join(root, n), 'rb').read() != open(p, 'rb').read():
                        diffs.append(rel + ' differs')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        print(json.dumps({'verify': True, 'seed': a.seed, 'arm': a.arm,
                          'diffs': diffs[:20], 'n_diffs': len(diffs)},
                         sort_keys=True))
        return 0 if not diffs else 1
    if not a.out:
        ap.error('--out is required')
    man = write_tree(a.out, a.seed, a.arm)
    print(json.dumps({'out': a.out, 'arm': a.arm, 'seed': a.seed,
                      'classes': len(man['classes']),
                      'carriers': len(man['carriers']),
                      'combos': sum(1 for c in man['carriers']
                                    if c['class'] == 'combo')}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
