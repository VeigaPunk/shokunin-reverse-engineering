#!/usr/bin/env python3
"""Extract the v1 feature vector plus the v2 domain/pubentry fields per envelope."""
import glob
import json
import os
import sys

S = os.environ.get('R40_WORK') or os.path.dirname(os.path.abspath(__file__))
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
        return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def names_sasquatch(tokens):
    return any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens)


def extractor_commands(data):
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and names_sasquatch(tokens) and cmd not in commands:
            commands.append(cmd)

    nr = data.get('normalized_result') or {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in as_list(source):
            report = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(report, dict) and 'command' in report:
                take(report['command'])
    for found in iter_dicts(data.get('raw_result')):
        if 'command' in found:
            take(found['command'])
    return commands


def envelope_data(obj):
    if isinstance(obj.get('normalized_result'), dict):
        return obj
    inner = obj.get('data')
    if isinstance(inner, dict) and isinstance(inner.get('normalized_result'), dict):
        return inner
    raise SystemExit('no normalized_result')


def features(data):
    nr = data['normalized_result']
    chunks = as_list(nr.get('chunks'))
    handlers = sorted({c.get('handler') for c in chunks
                       if isinstance(c, dict) and isinstance(c.get('handler'), str)
                       and c.get('handler', '').startswith('squashfs')})
    gaps = as_list(nr.get('extraction_gaps'))
    gap_kinds = sorted({g.get('kind') for g in gaps
                        if isinstance(g, dict) and isinstance(g.get('kind'), str)})
    deps = sorted({d for g in gaps if isinstance(g, dict)
                   for d in as_list(g.get('dependencies')) if isinstance(d, str)})
    commands = extractor_commands(data)
    if not commands:
        be = 'n/a'
    else:
        be = 'yes' if any('-be' in (command_tokens(c) or []) for c in commands) else 'no'
    sr = 'no'
    for diag in as_list(nr.get('diagnostics')):
        report = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:
            sr = 'yes'
            break
    if sr == 'no':
        for found in iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TYPENAME:
                sr = 'yes'
                break
    return {
        'OP': data.get('operation'),
        'PV': (data.get('provider') or {}).get('id'),
        'PROVIDER_KEYS': sorted((data.get('provider') or {}).keys()),
        'PROVIDER_NAME': (data.get('provider') or {}).get('name'),
        'H': handlers,
        'G': gap_kinds,
        'D': deps,
        'BE': be,
        'SR': sr,
        'P': len(as_list(nr.get('files'))),
        'chunks': [{'handler': c.get('handler'), 'extraction_failed': c.get('extraction_failed'),
                    'encrypted': c.get('encrypted')} for c in chunks if isinstance(c, dict)],
        'gaps': [{'kind': g.get('kind'), 'dependencies': as_list(g.get('dependencies')),
                  'entry_kind': g.get('entry_kind'), 'path': g.get('path'),
                  'input_path': g.get('input_path')} for g in gaps if isinstance(g, dict)],
        'unpublished_entries': [{'kind': u.get('kind'), 'relative_path': u.get('relative_path'),
                                 'link_target': u.get('link_target')}
                                for u in as_list(nr.get('unpublished_entries'))
                                if isinstance(u, dict)],
        'derivations': [{'child_path': d.get('child_path'), 'handler': d.get('handler')}
                        for d in as_list(nr.get('derivations')) if isinstance(d, dict)],
        'diagnostics': [{'typename': (d.get('report') or {}).get('__typename__'),
                         'command': (d.get('report') or {}).get('command'),
                         'exit_code': (d.get('report') or {}).get('exit_code')}
                        for d in as_list(nr.get('diagnostics')) if isinstance(d, dict)],
        'coverage': nr.get('coverage'),
        'files_sample': [{'path': f.get('path'), 'kind': f.get('kind')}
                         for f in as_list(nr.get('files'))[:5] if isinstance(f, dict)],
        'commands': [c if isinstance(c, str) else list(c) for c in commands],
        'output_directory': nr.get('output_directory'),
        'published_bytes': nr.get('published_bytes'),
    }


def main():
    out = {}
    for path in sorted(glob.glob(os.path.join(S, 'envelopes', '*.full.json'))):
        run_id = os.path.basename(path)[:-len('.full.json')]
        obj = json.load(open(path, encoding='utf-8'))
        entry = {'features': features(envelope_data(obj))}
        if os.path.exists(os.path.join(S, 'envelopes', run_id + '.run.json')):
            entry['run'] = json.load(open(os.path.join(S, 'envelopes',
                                                       run_id + '.run.json'), encoding='utf-8'))
        entry['full_keys'] = sorted(obj.keys()) if isinstance(obj, dict) else None
        out[run_id] = entry
    with open(os.path.join(S, 'features.json'), 'w', encoding='utf-8') as h:
        json.dump(out, h, indent=1, sort_keys=True)
        h.write('\n')
    hdr = ['run', 'OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P', 'failed', 'unpub', 'diag']
    print('\t'.join(hdr))
    for run_id in sorted(out):
        f = out[run_id]['features']
        print('\t'.join([
            run_id, str(f['OP']), str(f['PV']), ','.join(f['H']) or '-',
            '+'.join(f['G']) or '-', '+'.join(f['D']) or '-', f['BE'], f['SR'],
            str(f['P']),
            ','.join('%s:%s' % (c['handler'], c['extraction_failed']) for c in f['chunks']) or '-',
            ','.join('%s:%s' % (u['kind'], u['relative_path']) for u in f['unpublished_entries']) or '-',
            ','.join('%s:%s' % (d['typename'], d['exit_code']) for d in f['diagnostics']) or '-']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
