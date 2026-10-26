#!/usr/bin/env python3
"""R39C2ReconClean — feature extractor implementing the R39-C2 grammar exactly.

Accepts a bare `data` object or a full CLI envelope {ok,data,meta}.

  H  = {chunks[].handler that start with "squashfs"}
  G  = {extraction_gaps[].kind}
  D  = union(extraction_gaps[].dependencies)
  BE = yes  : some diagnostics[].report command naming sasquatch has a standalone "-be" token
       no   : such a command exists and none has it
       n/a  : no such command recorded
  SR = yes if any diagnostics[].report.__typename__ == "MaliciousSymlinkRemoved"
       (also accepted anywhere under raw_result.report), else no
  P  = len(normalized_result.files)
"""
import json
import shlex
import sys


def data_of(env):
    if isinstance(env, dict) and 'data' in env and isinstance(env['data'], dict):
        return env['data']
    return env


def reports(nr):
    for d in (nr.get('diagnostics') or []):
        if isinstance(d, dict) and isinstance(d.get('report'), dict):
            yield d['report']


def walk_reports(obj):
    """Every dict under a raw_result.report list, recursively."""
    if isinstance(obj, dict):
        if '__typename__' in obj:
            yield obj
        for v in obj.values():
            yield from walk_reports(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_reports(v)


def command_tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, list):
        return [str(t) for t in cmd]
    return []


def names_sasquatch(tokens):
    return any('sasquatch' in t for t in tokens)


def features(env):
    d = data_of(env)
    nr = d.get('normalized_result') or {}
    H = {c.get('handler') for c in (nr.get('chunks') or [])
         if isinstance(c, dict) and isinstance(c.get('handler'), str)
         and c['handler'].startswith('squashfs')}
    gaps = [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)]
    G = {g.get('kind') for g in gaps if g.get('kind') is not None}
    D = set()
    for g in gaps:
        for dep in (g.get('dependencies') or []):
            D.add(dep)
    be = 'n/a'
    seen = False
    for r in reports(nr):
        toks = command_tokens(r.get('command'))
        if names_sasquatch(toks):
            seen = True
            if '-be' in toks:
                be = 'yes'
    if seen and be != 'yes':
        be = 'no'
    sr = 'no'
    if any(r.get('__typename__') == 'MaliciousSymlinkRemoved' for r in reports(nr)):
        sr = 'yes'
    else:
        raw = d.get('raw_result') or {}
        if any(r.get('__typename__') == 'MaliciousSymlinkRemoved'
               for r in walk_reports(raw.get('report'))):
            sr = 'yes'
    return {
        'H': sorted(H), 'G': sorted(G), 'D': sorted(D), 'BE': be, 'SR': sr,
        'P': len(nr.get('files') or []),
    }


def detail(env):
    d = data_of(env)
    nr = d.get('normalized_result') or {}
    return {
        'ok': env.get('ok') if isinstance(env, dict) else None,
        'coverage': nr.get('coverage'),
        'published_bytes': nr.get('published_bytes'),
        'chunks': [{'handler': c.get('handler'),
                    'extraction_failed': c.get('extraction_failed'),
                    'range': c.get('range')}
                   for c in (nr.get('chunks') or []) if isinstance(c, dict)],
        'gaps': [{'kind': g.get('kind'), 'handler': g.get('handler'),
                  'dependencies': g.get('dependencies'),
                  'relative_path': g.get('relative_path')}
                 for g in (nr.get('extraction_gaps') or [])],
        'unpublished_entries': [{'kind': u.get('kind'),
                                 'relative_path': u.get('relative_path'),
                                 'link_target': u.get('link_target')}
                                for u in (nr.get('unpublished_entries') or [])],
        'diagnostics': [{'__typename__': r.get('__typename__'),
                         'command': r.get('command'),
                         'severity': r.get('severity')}
                        for r in reports(nr)],
        'files': [f.get('relative_path') for f in (nr.get('files') or [])],
        'evidence_id': d.get('evidence_id'),
    }


if __name__ == '__main__':
    out = {}
    for p in sys.argv[1:]:
        env = json.load(open(p))
        out[p.rsplit('/', 1)[-1][:-5]] = {'features': features(env),
                                          'detail': detail(env)}
    print(json.dumps(out, indent=1))
