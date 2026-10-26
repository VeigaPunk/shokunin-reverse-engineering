#!/usr/bin/env python3
"""R39-C2 recon: envelope feature extraction exactly as the L1 triage grammar
defines it, plus a candidate-row evaluator used only to test separability on
development carriers.

    python3 features.py ENVDIR MANIFEST OUTSTEM

Features (per the contract):
  H  = {chunks[].handler that start with "squashfs"}
  G  = {extraction_gaps[].kind}
  D  = union(extraction_gaps[].dependencies)
  BE = yes | no | n/a from diagnostics[].report.command naming sasquatch
  SR = yes | no  (MaliciousSymlinkRemoved anywhere in diagnostics or raw_result.report)
  P  = len(normalized_result.files)
Accepts a bare `data` object or a full CLI envelope {ok,data,meta}.
"""
import fnmatch
import json
import os
import shlex
import sys


def unwrap(doc):
    if isinstance(doc, dict) and isinstance(doc.get('data'), dict):
        return doc['data'], doc
    return doc, {'ok': None, 'data': doc}


def argv_of(command):
    if isinstance(command, list):
        return [str(t) for t in command]
    if isinstance(command, str):
        try:
            return shlex.split(command)
        except ValueError:
            return command.split()
    return []


def names_sasquatch(argv):
    return any(os.path.basename(tok).startswith('sasquatch') for tok in argv)


def walk_typenames(node, out):
    if isinstance(node, dict):
        tn = node.get('__typename__')
        if isinstance(tn, str):
            out.append(tn)
        for v in node.values():
            walk_typenames(v, out)
    elif isinstance(node, list):
        for v in node:
            walk_typenames(v, out)
    return out


def features(doc):
    data, env = unwrap(doc)
    nr = data.get('normalized_result') or {}
    chunks = [c for c in (nr.get('chunks') or []) if isinstance(c, dict)]
    gaps = [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)]
    H = sorted({c['handler'] for c in chunks
                if isinstance(c.get('handler'), str) and c['handler'].startswith('squashfs')})
    G = sorted({g.get('kind') for g in gaps if isinstance(g.get('kind'), str)})
    D = sorted({d for g in gaps for d in (g.get('dependencies') or [])})
    sas_cmds, be = [], 'n/a'
    for diag in (nr.get('diagnostics') or []):
        rep = (diag or {}).get('report') or {}
        argv = argv_of(rep.get('command'))
        if argv and names_sasquatch(argv):
            sas_cmds.append(argv)
    if sas_cmds:
        be = 'yes' if any('-be' in a for a in sas_cmds) else 'no'
    diag_types = [(d.get('report') or {}).get('__typename__') for d in (nr.get('diagnostics') or [])]
    sr = 'yes' if 'MaliciousSymlinkRemoved' in diag_types else 'no'
    if sr == 'no':
        sr = 'yes' if 'MaliciousSymlinkRemoved' in walk_typenames(data.get('raw_result'), []) else 'no'
    files = nr.get('files') or []
    return {
        'ok': env.get('ok'),
        'H': H, 'G': G, 'D': D, 'BE': be, 'SR': sr, 'P': len(files),
        'coverage': nr.get('coverage'),
        'published_bytes': nr.get('published_bytes'),
        'chunks': [{'handler': c.get('handler'),
                    'offset': (c.get('range') or {}).get('offset'),
                    'length': (c.get('range') or {}).get('length'),
                    'extraction_failed': c.get('extraction_failed'),
                    'encrypted': c.get('encrypted')} for c in chunks],
        'gaps': [{'kind': g.get('kind'), 'dependencies': g.get('dependencies'),
                  'handler': g.get('handler'),
                  'range': g.get('range')} for g in gaps],
        'unpublished': [{'kind': u.get('kind'), 'relative_path': u.get('relative_path')}
                        for u in (nr.get('unpublished_entries') or [])],
        'diagnostics': [{'typename': t,
                         'command': ((d.get('report') or {}).get('command'))}
                        for t, d in zip(diag_types, (nr.get('diagnostics') or []))],
        'sasquatch_argv': sas_cmds,
        'files': [f.get('relative_path') for f in files],
        'subject_sha256': ((data.get('subject') or {}).get('digest') or {}).get('sha256'),
        'selection': nr.get('selection'),
        'evidence_id': data.get('evidence_id'),
    }


# ---- candidate triage rows (development only; the frozen table belongs to L1) --
# cell grammar: handler: `none` | fnmatch pattern over H;
#               gap kinds / dependencies: `none` | `a+b` exact set;
#               BE/SR: yes|no|n/a; P: `0` | `>0` | `*`.
CANDIDATE_ROWS = [
    ('clean',                    'squashfs_v4*', 'none', 'none', 'n/a', 'no', '>0'),
    ('escaping-symlink-removed', 'squashfs_v4*', 'none', 'none', 'n/a', 'yes', '>0'),
    ('in-tree-symlink-metadata', 'squashfs_v4*', 'unpublished-entry', 'none', 'n/a', 'no', '>0'),
    ('dep-missing',              'squashfs_v4*', 'missing-extractor-dependency', '*', 'n/a', 'no', '0'),
    ('avm-marker-be-dropped',    'squashfs_v4_be', 'extractor-failure', 'none', 'no', 'no', '0'),
    ('body-extractor-failure',   '*', 'extractor-failure', 'none', 'yes', 'no', '0'),
    ('garbage-prefix-or-tail',   'squashfs_v4*', 'unknown-chunk-handler', 'none', 'n/a', 'no', '>0'),
    ('no-squashfs-chunk',        'none', 'none', 'none', 'n/a', 'no', '0'),
]


def gap_cell(value):
    if value == 'none':
        return set()
    if value == '*':
        return '*'
    return set(value.split('+'))


def row_matches(row, f):
    _, h, g, d, be, sr, p = row
    if h == 'none':
        if f['H']:
            return False
    elif h != '*' and not any(fnmatch.fnmatchcase(x, h) for x in f['H']):
        return False
    for cell, got in ((g, set(f['G'])), (d, set(f['D']))):
        want = gap_cell(cell)
        if want != '*' and want != got:
            return False
    if be != '*' and be != f['BE']:
        return False
    if sr != '*' and sr != f['SR']:
        return False
    if p == '0' and f['P'] != 0:
        return False
    if p.startswith('>') and not f['P'] > int(p[1:]):
        return False
    return True


def label(f):
    for row in CANDIDATE_ROWS:
        if row_matches(row, f):
            return row[0]
    return 'unclassified'


def main(argv=None):
    argv = argv or sys.argv[1:]
    envdir, manifest_path, outstem = argv
    manifest = json.load(open(manifest_path))['carriers']
    feats = {}
    for cid in sorted(manifest):
        ep = os.path.join(envdir, cid + '.json')
        if not os.path.exists(ep):
            continue
        f = features(json.load(open(ep)))
        f['carrier'] = {k: manifest[cid].get(k) for k in
                        ('sha256', 'size', 'endian', 'comp', 'recipe',
                         'base_bytes_used', 'declared_bytes_used', 'chunk_offset')}
        f['carrier_sha256_matches_subject'] = f['subject_sha256'] == manifest[cid].get('sha256')
        f['label'] = label(f)
        feats[cid] = f
    with open(outstem + '.json', 'w') as fh:
        json.dump(feats, fh, indent=1, sort_keys=True)
    lines = ['| carrier | recipe | H | G | D | BE | SR | P | coverage | bytes_used vs size | chunk@ | label |',
             '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for cid, f in feats.items():
        c = f['carrier']
        extent = (f"{c.get('declared_bytes_used')} vs {c.get('size')}"
                  if c.get('declared_bytes_used') is not None else '-')
        lines.append('| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |'.format(
            cid, c.get('recipe'),
            '{' + ','.join(f['H']) + '}' if f['H'] else '{}',
            '{' + ','.join(f['G']) + '}' if f['G'] else '{}',
            '{' + ','.join(f['D']) + '}' if f['D'] else '{}',
            f['BE'], f['SR'], f['P'], f['coverage'], extent,
            ','.join(f"{x['offset']}:{x['handler']}" for x in f['chunks']) or '-',
            f['label']))
    md = '\n'.join(lines) + '\n'
    with open(outstem + '.md', 'w') as fh:
        fh.write(md)
    print(md)
    return 0


if __name__ == '__main__':
    sys.exit(main())
