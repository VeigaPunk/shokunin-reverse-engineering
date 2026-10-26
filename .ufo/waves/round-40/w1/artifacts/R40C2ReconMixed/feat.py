#!/usr/bin/env python3
"""feat.py -- dump the v1/spec feature set of an REA extract-firmware envelope.

Independent re-implementation of tools/round-39/sqfs-triage.py features() plus the
v2 extras (operation, provider id/name, chunk detail, gap detail, unpublished
entries, diagnostic typenames and commands).  Reads a bare ``data`` object or a
full ``{ok,data,meta}`` CLI envelope.

Usage:
  python3 -I -B feat.py ENVELOPE.json...          one JSON object per envelope
  python3 -I -B feat.py --json ENVELOPE...        one JSON array
"""
import argparse
import json
import shlex
import sys

SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'


def as_list(v):
    return v if isinstance(v, list) else []


def iter_dicts(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def command_tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def names_sasquatch(tokens):
    return any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens)


def extractor_commands(data):
    found = []

    def take(cmd):
        toks = command_tokens(cmd)
        if toks and names_sasquatch(toks) and cmd not in found:
            found.append(cmd)

    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in as_list(source):
            report = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(report, dict) and 'command' in report:
                take(report['command'])
    for d in iter_dicts(data.get('raw_result')):
        if 'command' in d:
            take(d['command'])
    return found


def envelope_data(obj):
    if not isinstance(obj, dict):
        raise SystemExit('not a JSON object')
    if isinstance(obj.get('normalized_result'), dict):
        return obj
    inner = obj.get('data')
    if isinstance(inner, dict) and isinstance(inner.get('normalized_result'), dict):
        return inner
    raise SystemExit('no normalized_result (bare data nor full envelope)')


def features(data):
    nr = data['normalized_result']
    handlers, gap_kinds, dependencies = set(), set(), set()
    chunk_detail, gap_detail = [], []
    for chunk in as_list(nr.get('chunks')):
        if not isinstance(chunk, dict):
            continue
        h = chunk.get('handler')
        if isinstance(h, str) and h.startswith('squashfs'):
            handlers.add(h)
        chunk_detail.append({'handler': h,
                             'extraction_failed': chunk.get('extraction_failed'),
                             'range': chunk.get('range')})
    for gap in as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        kind = gap.get('kind')
        if isinstance(kind, str):
            gap_kinds.add(kind)
        deps = [d for d in as_list(gap.get('dependencies')) if isinstance(d, str)]
        dependencies.update(deps)
        gap_detail.append({'kind': kind, 'dependencies': deps,
                           'handler': gap.get('handler'),
                           'relative_path': gap.get('relative_path')})
    cmds = extractor_commands(data)
    if not cmds:
        be = 'n/a'
    else:
        be = 'no'
        for cmd in cmds:
            if '-be' in (command_tokens(cmd) or []):
                be = 'yes'
                break
    sr = 'no'
    diag_detail = []
    for diag in as_list(nr.get('diagnostics')):
        report = diag.get('report') if isinstance(diag, dict) else None
        typename = report.get('__typename__') if isinstance(report, dict) else None
        command = report.get('command') if isinstance(report, dict) else None
        diag_detail.append({'__typename__': typename,
                            'stage': diag.get('stage') if isinstance(diag, dict) else None,
                            'has_command': command is not None,
                            'command': command})
        if typename == SYMLINK_TYPENAME:
            sr = 'yes'
    if sr == 'no':
        for d in iter_dicts(data.get('raw_result')):
            if d.get('__typename__') == SYMLINK_TYPENAME:
                sr = 'yes'
                break
    provider = data.get('provider') if isinstance(data.get('provider'), dict) else {}
    return {
        'operation': data.get('operation'),
        'provider_id': provider.get('id'),
        'provider_name': provider.get('name'),
        'H': sorted(handlers),
        'G': sorted(gap_kinds),
        'D': sorted(dependencies),
        'BE': be,
        'SR': sr,
        'P': len(as_list(nr.get('files'))),
        'commands': cmds,
        'chunks': chunk_detail,
        'gaps': gap_detail,
        'diagnostics': diag_detail,
        'unpublished_entries': [
            {'kind': u.get('kind'), 'relative_path': u.get('relative_path'),
             'link_target': u.get('link_target')}
            for u in as_list(nr.get('unpublished_entries')) if isinstance(u, dict)],
    }


def load(path):
    with open(path, 'r', encoding='utf-8') as fh:
        return envelope_data(json.load(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('paths', nargs='+')
    ns = ap.parse_args()
    out = []
    for p in ns.paths:
        fe = features(load(p))
        fe['path'] = p
        out.append(fe)
    if ns.json:
        json.dump(out, sys.stdout, indent=1, sort_keys=True)
        print()
    else:
        for fe in out:
            print(json.dumps(fe, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
