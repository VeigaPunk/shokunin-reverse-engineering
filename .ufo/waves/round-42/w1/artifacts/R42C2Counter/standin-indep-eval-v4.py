#!/usr/bin/env python3
"""STAND-IN v4 independent evaluator — dry-run scaffold for `tools/round-42/indep-eval-v4.py`.

NOT the frozen evaluator: the frozen one belongs to the `R42C2Eval` seat and is
written from the precedence text only. This stand-in is written from
`plans/round-42-claims.md` `## R42-C2` amendment A1 (15 steps) and reads no
table.

FEATURES (envelope field -> feature)
  OP  operation
  PR  provider.id
  H   {chunks[].handler} ∪ {extraction_gaps[].handler}, nulls dropped
  F   {h in H : h startswith `squashfs_`}
  L   {h in F : h matches squashfs_v1*, squashfs_v2* or squashfs_v3*}
  G   {extraction_gaps[].kind}
  D   union of extraction_gaps[].dependencies (exact names)
  HF  handlers of the `extractor-failure` gaps (nulls dropped); F when none
      carries a handler
  BE  `yes` if any recorded child argv (diagnostics[].report.command, plus
      raw_result commands) carries `-be`; `no` if argvs are recorded and none
      does; `n/a` if none is recorded
  SR  true iff a `MaliciousSymlinkRemoved` report is in diagnostics
  P   number of normalized_result.files (absent reads 0)

STEPS (first match wins)
   1 OP != extract_firmware or PR != unblob      -> unclassified/none
   2 F empty and depth-limited in G              -> container-depth-limited/raise-depth
   3 F empty                                     -> no-squashfs-chunk/inspect-input
   4 missing-extractor-dependency in G:
       sasquatch-v4be in D -> dep-missing-be/install-extractor-be
       sasquatch in D      -> dep-missing-le/install-extractor-le
       else continue
   5 extractor-failure in G and P > 0            -> partial-body-failure/salvage-partial
   6 extractor-failure in G, P == 0, BE == no,
     squashfs_v4_be in HF                         -> avm-marker-be-dropped/wrap-extractor-be
   7 extractor-failure in G, P == 0, HF ∩ L != ∅ -> legacy-body-failure/cross-read-legacy
   8 extractor-failure in G, P == 0              -> body-extractor-failure/preserve-failure
   9 unknown-chunk-handler in G                  -> unknown-residue/isolate-residue
  10 depth-limited in G                          -> depth-limited/raise-depth
  11 SR and unpublished-entry in G               -> mixed-symlinks/audit-symlinks
  12 SR and G empty                              -> escaping-symlink-removed/expect-link-absent
  13 G == {unpublished-entry}                    -> in-tree-symlink-metadata/count-gap
  14 G empty: P > 0 -> clean/none; P == 0 -> clean-empty/confirm-empty
  15 else                                        -> unclassified/none

Usage
  python3 -I -B indep-eval-v4.py --envelopes DIR [--out FILE] [--json]
  python3 -I -B indep-eval-v4.py ENVELOPE.json
  python3 -I -B indep-eval-v4.py --selftest
Exit 0 on success, 2 on an unreadable envelope or directory.
"""
import argparse
import fnmatch
import json
import os
import shlex
import sys

SYMLINK = 'MaliciousSymlinkRemoved'
LEGACY_GLOBS = ('squashfs_v1*', 'squashfs_v2*', 'squashfs_v3*')


def _list(v):
    return v if isinstance(v, list) else []


def _walk(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def _tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return []


def _commands(data):
    out = []
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for src in (nr.get('diagnostics'), data.get('diagnostics')):
        for d in _list(src):
            rep = d.get('report') if isinstance(d, dict) else None
            if isinstance(rep, dict) and 'command' in rep:
                cmd = rep['command']
                if any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in _tokens(cmd)):
                    if cmd not in out:
                        out.append(cmd)
    for found in _walk(data.get('raw_result')):
        cmd = found.get('command')
        if cmd is not None and any(t.rsplit('/', 1)[-1].startswith('sasquatch')
                                   for t in _tokens(cmd)):
            if cmd not in out:
                out.append(cmd)
    return out


def is_legacy(handler):
    if not isinstance(handler, str):
        return False
    return any(fnmatch.fnmatchcase(handler, g) for g in LEGACY_GLOBS)


def features(data):
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    handlers = set()
    for chunk in _list(nr.get('chunks')):
        if isinstance(chunk, dict) and isinstance(chunk.get('handler'), str) \
                and chunk['handler']:
            handlers.add(chunk['handler'])
    gaps, deps, hf = set(), set(), set()
    for gap in _list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        kind = gap.get('kind')
        if isinstance(kind, str):
            gaps.add(kind)
        gh = gap.get('handler')
        if isinstance(gh, str) and gh:
            handlers.add(gh)
            if kind == 'extractor-failure':
                hf.add(gh)
        for d in _list(gap.get('dependencies')):
            if isinstance(d, str):
                deps.add(d)
    F = {h for h in handlers if h.startswith('squashfs_')}
    L = {h for h in F if is_legacy(h)}
    cmds = _commands(data)
    if not cmds:
        be = 'n/a'
    else:
        be = 'no'
        for c in cmds:
            if '-be' in _tokens(c):
                be = 'yes'
                break
    sr = False
    for d in _list(nr.get('diagnostics')):
        rep = d.get('report') if isinstance(d, dict) else None
        if isinstance(rep, dict) and rep.get('__typename__') == SYMLINK:
            sr = True
    if not sr:
        for found in _walk(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK:
                sr = True
                break
    provider = data.get('provider')
    return {'OP': data.get('operation'),
            'PR': provider.get('id') if isinstance(provider, dict) else provider,
            'H': handlers, 'F': F, 'L': L, 'G': gaps, 'D': deps,
            'HF': hf or F, 'BE': be, 'SR': sr,
            'P': len(_list(nr.get('files')))}


def evaluate(data):
    f = features(data)
    F, G, D, HF, L = f['F'], f['G'], f['D'], f['HF'], f['L']
    BE, SR, P = f['BE'], f['SR'], f['P']
    if f['OP'] != 'extract_firmware' or f['PR'] != 'unblob':
        return ('unclassified', 'none')
    if not F and 'depth-limited' in G:
        return ('container-depth-limited', 'raise-depth')
    if not F:
        return ('no-squashfs-chunk', 'inspect-input')
    if 'missing-extractor-dependency' in G:
        if 'sasquatch-v4be' in D:
            return ('dep-missing-be', 'install-extractor-be')
        if 'sasquatch' in D:
            return ('dep-missing-le', 'install-extractor-le')
    if 'extractor-failure' in G and P > 0:
        return ('partial-body-failure', 'salvage-partial')
    if 'extractor-failure' in G and P == 0:
        if BE == 'no' and 'squashfs_v4_be' in HF:
            return ('avm-marker-be-dropped', 'wrap-extractor-be')
        if HF & L:
            return ('legacy-body-failure', 'cross-read-legacy')
        return ('body-extractor-failure', 'preserve-failure')
    if 'unknown-chunk-handler' in G:
        return ('unknown-residue', 'isolate-residue')
    if 'depth-limited' in G:
        return ('depth-limited', 'raise-depth')
    if SR and 'unpublished-entry' in G:
        return ('mixed-symlinks', 'audit-symlinks')
    if SR and not G:
        return ('escaping-symlink-removed', 'expect-link-absent')
    if G == {'unpublished-entry'}:
        return ('in-tree-symlink-metadata', 'count-gap')
    if not G:
        return ('clean', 'none') if P > 0 else ('clean-empty', 'confirm-empty')
    return ('unclassified', 'none')


def envelope_data(obj):
    if isinstance(obj, dict) and 'subject' not in obj \
            and isinstance(obj.get('data'), dict):
        return obj['data']
    return obj


def run_dir(path):
    out = {}
    for name in sorted(os.listdir(path)):
        if not name.endswith('.json') or name == 'manifest.json':
            continue
        with open(os.path.join(path, name)) as fh:
            obj = json.load(fh)
        lab, act = evaluate(envelope_data(obj))
        out[name[:-5]] = {'label': lab, 'action': act}
    return out


def envelope(op='extract_firmware', prov='unblob', chunks=(), gaps=(), files=2,
             be=None, symlink=False):
    """Build a synthetic envelope from (handler, failed) chunks and gaps."""
    nr = {'chunks': [{'handler': h, 'extraction_failed': bool(failed)}
                     for h, failed in chunks],
          'extraction_gaps': [dict(kind=k[0], dependencies=list(k[2]),
                                   **({'handler': k[1]} if k[1] else {}))
                              for k in gaps],
          'files': [{'path': 'f%d' % i} for i in range(files)],
          'diagnostics': []}
    if be in ('yes', 'no'):
        nr['diagnostics'].append({'report': {
            'command': ['sasquatch'] + (['-be'] if be == 'yes' else [])
            + ['-d', 'out', 'in.sqsh']}})
    if symlink:
        nr['diagnostics'].append({'report': {'__typename__': SYMLINK}})
    return {'operation': op, 'provider': {'id': prov}, 'normalized_result': nr}


SELFTEST = [
    # (envelope, expected)
    (envelope(chunks=[('squashfs_v3', False)], be='no'),
     ('clean', 'none')),
    (envelope(chunks=[('squashfs_v3', False)], be='no', files=0),
     ('clean-empty', 'confirm-empty')),
    (envelope(files=0), ('no-squashfs-chunk', 'inspect-input')),
    (envelope(chunks=[('trx_v1', False)],
              gaps=[('depth-limited', None, [])], files=0),
     ('container-depth-limited', 'raise-depth')),
    (envelope(chunks=[('squashfs_v3', False)],
              gaps=[('missing-extractor-dependency', None, ['sasquatch'])],
              files=0), ('dep-missing-le', 'install-extractor-le')),
    (envelope(chunks=[('squashfs_v4_be', False)],
              gaps=[('missing-extractor-dependency', None, ['sasquatch-v4be'])],
              files=0), ('dep-missing-be', 'install-extractor-be')),
    (envelope(chunks=[('squashfs_v3', False)],
              gaps=[('extractor-failure', 'squashfs_v3', [])],
              be='no', files=0), ('legacy-body-failure', 'cross-read-legacy')),
    (envelope(chunks=[('squashfs_v4_be', False)],
              gaps=[('extractor-failure', 'squashfs_v4_be', [])],
              be='no', files=0),
     ('avm-marker-be-dropped', 'wrap-extractor-be')),
    (envelope(chunks=[('squashfs_v4_le', False)],
              gaps=[('extractor-failure', 'squashfs_v4_le', [])],
              be='no', files=0),
     ('body-extractor-failure', 'preserve-failure')),
    (envelope(chunks=[('squashfs_v3', False)],
              gaps=[('extractor-failure', 'squashfs_v3', [])], be='no'),
     ('partial-body-failure', 'salvage-partial')),
    (envelope(chunks=[('squashfs_v4_be', False)],
              gaps=[('unknown-chunk-handler', None, [])]),
     ('unknown-residue', 'isolate-residue')),
    (envelope(chunks=[('squashfs_v3', False)],
              gaps=[('depth-limited', None, [])], be='no'),
     ('depth-limited', 'raise-depth')),
    (envelope(chunks=[('squashfs_v4_be', False)],
              gaps=[('unpublished-entry', None, [])], symlink=True),
     ('mixed-symlinks', 'audit-symlinks')),
    (envelope(chunks=[('squashfs_v4_be', False)], symlink=True),
     ('escaping-symlink-removed', 'expect-link-absent')),
    (envelope(chunks=[('squashfs_v4_be', False)],
              gaps=[('unpublished-entry', None, [])]),
     ('in-tree-symlink-metadata', 'count-gap')),
    (envelope(op='analyze', chunks=[('squashfs_v3', False)], be='no'),
     ('unclassified', 'none')),
    (envelope(chunks=[('squashfs_v3', False)],
              gaps=[('extractor-failure', 'squashfs_v3', []),
                    ('depth-limited', None, [])], be='yes', files=0),
     ('legacy-body-failure', 'cross-read-legacy')),
    (envelope(chunks=[('squashfs_v4_be', False)],
              gaps=[('extractor-failure', 'squashfs_v4_be', []),
                    ('unknown-chunk-handler', None, [])], be='yes'),
     ('partial-body-failure', 'salvage-partial')),
]


def selftest():
    bad = []
    for env, want in SELFTEST:
        got = evaluate(env)
        if got != want:
            bad.append({'want': want, 'got': got,
                        'features': sorted(features(env))})
    print(json.dumps({'selftest': 'indep-eval-v4 (standin, A1)', 'cases':
                      len(SELFTEST), 'failures': bad}, sort_keys=True))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('envelopes', nargs='*')
    ap.add_argument('--envelopes', dest='envelopes_dir')
    ap.add_argument('--out')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.envelopes_dir:
            out = run_dir(a.envelopes_dir)
        elif a.envelopes:
            out = {}
            for p in a.envelopes:
                with open(p) as fh:
                    obj = json.load(fh)
                lab, act = evaluate(envelope_data(obj))
                out[os.path.basename(p)[:-5]] = {'label': lab, 'action': act}
        else:
            ap.error('an envelope, --envelopes DIR, or --selftest is required')
    except (OSError, ValueError) as e:
        sys.stderr.write('indep-eval-v4(standin): %s\n' % e)
        return 2
    text = json.dumps(out, indent=1, sort_keys=True)
    if a.out:
        with open(a.out, 'w') as fh:
            fh.write(text + '\n')
        return 0
    print(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
