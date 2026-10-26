#!/usr/bin/env python3
"""Compare the extract-root-relative projection of several REA `after.json` receipts.

Each receipt embeds the scratch extraction root in `parameters.output_directory`
and in every normalized path. This tool strips that root, keeps the fields the
C1 counter scores (operation, provider, engine, selection/subject digests,
coverage, handler set, per-file relative path + sha256 + size, extraction gaps,
unpublished entries, published bytes) and prints a digest per receipt.

Exit 0 when every receipt has the same projection, 1 otherwise.
"""
import hashlib
import json
import sys


def rel(path, root):
    if not isinstance(path, str):
        return path
    return path[len(root):].lstrip('/') if path.startswith(root) else path


def projection(doc):
    root = (doc.get('parameters') or {}).get('output_directory') or ''
    norm = doc.get('normalized_result') or {}
    chunks = []
    for chunk in norm.get('chunks') or []:
        chunks.append({
            'handler': chunk.get('handler'),
            'range': [chunk.get('range', {}).get('offset'), chunk.get('range', {}).get('length')],
            'extraction_failed': chunk.get('extraction_failed'),
        })
    files = []
    for f in norm.get('files') or []:
        files.append({'path': rel(f.get('path'), root),
                      'sha256': f.get('sha256'), 'size': f.get('size')})
    files.sort(key=lambda r: (r['path'] or ''))
    gaps = []
    for g in norm.get('extraction_gaps') or []:
        gaps.append({'kind': g.get('kind'),
                     'relative_path': rel(g.get('relative_path'), root),
                     'dependencies': g.get('dependencies') or []})
    gaps.sort(key=lambda r: (r['kind'] or '', r['relative_path'] or ''))
    unpublished = []
    for u in norm.get('unpublished_entries') or []:
        unpublished.append({'relative_path': rel(u.get('relative_path'), root),
                            'kind': u.get('kind'), 'link_target': u.get('link_target')})
    unpublished.sort(key=lambda r: (r['relative_path'] or ''))
    engine = norm.get('engine') or {}
    return {
        'operation': doc.get('operation'),
        'provider': (doc.get('provider') or {}).get('id'),
        'engine': {'name': engine.get('name'), 'version': engine.get('version'),
                   'sha256': engine.get('executable_sha256')},
        'selection_sha256': (norm.get('selection') or {}).get('sha256'),
        'subject_sha256': ((doc.get('subject') or {}).get('digest') or {}).get('sha256'),
        'coverage': norm.get('coverage'),
        'chunks': chunks,
        'files': files,
        'gaps': gaps,
        'unpublished': unpublished,
        'published_bytes': norm.get('published_bytes'),
        'depth_limited_paths': [rel(p, root) for p in norm.get('depth_limited_paths') or []],
    }


def main(argv):
    if len(argv) < 2:
        sys.stderr.write('usage: projection-compare.py AFTER.json [AFTER.json ...]\n')
        return 2
    digests = []
    for path in argv[1:]:
        with open(path, encoding='utf-8') as fh:
            doc = json.load(fh)
        proj = projection(doc)
        digest = hashlib.sha256(
            json.dumps(proj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        digests.append(digest)
        print('%s  %s\n    files=%d gaps=%d unpublished=%d coverage=%s handlers=%s published_bytes=%s'
              % (digest, path, len(proj['files']), len(proj['gaps']), len(proj['unpublished']),
                 proj['coverage'], [c['handler'] for c in proj['chunks']], proj['published_bytes']))
    ok = len(set(digests)) == 1
    print('PROJECTIONS_%s' % ('EQUAL' if ok else 'DIFFER'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
