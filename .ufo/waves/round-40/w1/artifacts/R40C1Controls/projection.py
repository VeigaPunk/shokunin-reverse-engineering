#!/usr/bin/env python3
"""projection.py -- what the P40-C1 rerun binding must compare, measured against the
strongest fabrication a committed-bytes forger can build.

Two projections of one REA `extract_firmware` envelope:

  --draft  the fields P40-C1 (draft) names: subject digest, chunk handler(s),
           extraction_failed, and the publication map (relpath suffix, sha256).
  --run    --draft plus the fields a run produces and an oracle cannot:
           per-file mime_type/analysis_depth/size, the derivations table, the
           diagnostics sequence, the gap list, chunk ranges, published_bytes,
           coverage, confidence.

`--synthesize ORACLE.tsv [SYMLINKS.tsv]` builds the envelope a forger writes when it
holds only the committed oracle (relpath, sha256, size) and the committed symlink
table -- i.e. the CTL-C1-2 class, whose evidence id it can re-mint at will. Comparing
`--draft` of the synthesized envelope with the real one is the measurement: equal
means a bytes-only counter cannot refuse the class.

Volatile fields dropped from every projection (measured across two honest runs of one
carrier, see measurements.txt): evidence_id, parameters.output_directory,
normalized_result.output_directory, files[].path, chunks[].provider_id, raw_result
(REA's own temp dir name carries randomness and its unblob.log is deleted).

Usage:
  python3 -I -B projection.py --envelope ENV.json [--draft|--run] [--json]
  python3 -I -B projection.py --envelope ENV.json --synthesize ORACLE.tsv [--symlinks S.tsv] --compare
Exit 0 always unless an input is unreadable (2).
"""
import hashlib
import json
import os
import sys


def load(path):
    with open(path, 'rb') as f:
        raw = f.read()
    doc = json.loads(raw)
    if isinstance(doc, dict) and 'data' in doc and 'evidence_id' not in doc:
        doc = doc['data']
    return doc


def env_of(doc):
    for key in ('normalized_result',):
        if key not in doc:
            raise SystemExit('not an REA envelope: %s' % key)
    return doc['normalized_result']


def published(nr):
    out = []
    for f in nr.get('files') or []:
        out.append((f.get('relative_path'), f.get('sha256')))
    return sorted(out)


def draft_projection(env):
    nr = env_of(env)
    return {
        'subject_sha256': (env.get('subject') or {}).get('digest', {}).get('sha256'),
        'handlers': [c.get('handler') for c in nr.get('chunks') or []],
        'extraction_failed': [bool(c.get('extraction_failed')) for c in nr.get('chunks') or []],
        'publication': published(nr),
    }


def run_projection(env):
    nr = env_of(env)
    proj = draft_projection(env)
    proj.update({
        'coverage': nr.get('coverage'),
        'confidence': env.get('confidence'),
        'published_bytes': nr.get('published_bytes'),
        'files': sorted((f.get('relative_path'), f.get('size'), f.get('sha256'),
                         f.get('mime_type'), f.get('analysis_depth'))
                        for f in nr.get('files') or []),
        'derivations': sorted((d.get('parent_path'), d.get('child_path'), d.get('handler'))
                              for d in nr.get('derivations') or []),
        'diagnostics': [(d.get('report') or {}).get('__typename__',
                                                    (d.get('report') or {}).get('severity'))
                        for d in nr.get('diagnostics') or []],
        'gaps': [(g.get('kind') or g.get('relative_path') or str(g))
                 for g in nr.get('extraction_gaps') or []],
        'unpublished': [u.get('relative_path') if isinstance(u, dict) else str(u)
                        for u in nr.get('unpublished_entries') or []],
        'chunks': [(c.get('range', {}).get('offset'), c.get('range', {}).get('length'),
                    c.get('handler'), bool(c.get('extraction_failed')),
                    bool(c.get('encrypted'))) for c in nr.get('chunks') or []],
    })
    return proj


def read_tsv(path):
    rows = []
    with open(path, 'rb') as f:
        for line in f:
            line = line.rstrip(b'\r\n')
            if not line:
                continue
            rows.append([c.decode('utf-8', 'surrogateescape') for c in line.split(b'\t')])
    return rows


def synthesize(oracle_path, symlink_path=None, subject_sha256=None, root='firmware.bin_extract'):
    """The CTL-C1-2 forgery: everything a holder of the committed TSVs can assert.

    It asserts, for each oracle row, the publication path REA uses
    (`<root>/<relpath>`), the oracle's own sha256 and size; a single
    `squashfs_v4_be` chunk over the whole carrier with extraction_failed false;
    one `unpublished-entry` gap per in-tree symlink (the frozen gap rule); and the
    likely diagnostics. It does not invent mime_type, analysis_depth or the
    derivations table (it cannot: the oracle holds hashes, not content), because
    that is the honest limit of the class.
    """
    rows = read_tsv(oracle_path)
    files = []
    for rel, sha, size in rows:
        files.append({'relative_path': '%s/%s' % (root, rel), 'path': 'file://' + rel,
                      'size': int(size), 'sha256': sha, 'reported_sha256': sha,
                      'mime_type': None, 'analysis_depth': 1,
                      'runtime_address': None, 'original_file_range': None})
    gaps, diags = [], []
    if symlink_path and os.path.exists(symlink_path):
        for row in read_tsv(symlink_path):
            if len(row) < 3:
                continue
            rel, target, kind = row[0], row[1], row[2]
            if kind == 'in-tree':
                gaps.append({'kind': 'unpublished-entry', 'relative_path': '%s/%s' % (root, rel)})
            else:
                diags.append({'input_path': '$input', 'report': {
                    '__typename__': 'MaliciousSymlinkRemoved', 'severity': 'WARNING',
                    'link': 'file://' + rel, 'target': target}})
    return {
        'evidence_id': 'ev_' + '0' * 64,
        'subject': {'name': 'carrier', 'digest': {'sha256': subject_sha256},
                    'local_path': 'file://carrier', 'format': 'file', 'architecture': None},
        'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'},
        'predicate_type': 'rea.analysis', 'operation': 'extract_firmware',
        'parameters': {'path': 'file://carrier', 'output_directory': 'file://out'},
        'normalized_result': {
            'output_directory': 'file://out',
            'coverage': 'partial',
            'files': files,
            'unpublished_entries': [],
            'chunks': [{'input_path': '$input', 'provider_id': 'x',
                        'range': {'offset': 0, 'length': 0},
                        'root_file_range': {'offset': 0, 'length': 0},
                        'handler': 'squashfs_v4_be', 'encrypted': False,
                        'extraction_failed': False}],
            'derivations': [], 'diagnostics': diags,
            'extraction_gaps': gaps, 'depth_limited_paths': [],
            'extraction_continuations': [],
            'published_bytes': sum(f['size'] for f in files),
        },
        'confidence': 'observed',
    }


def diff(a, b, label_a, label_b):
    keys = sorted(set(a) | set(b))
    same, differ = [], []
    for k in keys:
        (same if a.get(k) == b.get(k) else differ).append(k)
    print('projection fields equal (%d): %s' % (len(same), ', '.join(same)))
    print('projection fields differing (%d): %s' % (len(differ), ', '.join(differ)))
    for k in differ:
        va, vb = a.get(k), b.get(k)
        print('  %s:\n    %s = %s\n    %s = %s'
              % (k, label_a, str(va)[:220], label_b, str(vb)[:220]))
    return same, differ


def main(argv):
    args = argv[1:]
    env_path = oracle = symlinks = None
    mode = 'run'
    as_json = compare = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--envelope':
            i += 1
            env_path = args[i]
        elif a == '--synthesize':
            i += 1
            oracle = args[i]
        elif a == '--symlinks':
            i += 1
            symlinks = args[i]
        elif a == '--draft':
            mode = 'draft'
        elif a == '--run':
            mode = 'run'
        elif a == '--json':
            as_json = True
        elif a == '--compare':
            compare = True
        else:
            print('unknown argument %r' % a, file=sys.stderr)
            return 2
        i += 1
    if not env_path:
        print('--envelope required', file=sys.stderr)
        return 2
    env = load(env_path)
    proj = draft_projection(env) if mode == 'draft' else run_projection(env)
    if as_json and not compare:
        print(json.dumps(proj, indent=1, sort_keys=True))
        return 0
    if oracle:
        synth = synthesize(oracle, symlinks,
                           (env.get('subject') or {}).get('digest', {}).get('sha256'))
        if compare:
            for name, fn in (('draft', draft_projection), ('run', run_projection)):
                print('=== %s projection, real vs CTL-C1-2 synthesis' % name)
                diff(fn(env), fn(synth), 'real', 'synthesized')
                print('')
            return 0
        proj = draft_projection(synth) if mode == 'draft' else run_projection(synth)
    print(json.dumps(proj, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
