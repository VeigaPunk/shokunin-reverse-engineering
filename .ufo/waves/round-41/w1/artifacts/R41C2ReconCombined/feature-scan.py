#!/usr/bin/env python3
"""Independent feature read of an REA extract-firmware envelope + v2 label.

The features are recomputed here from the *published envelope JSON*, with no
import of the v2 interpreter, so the interpreter's own feature line is a second
opinion rather than the source.  Definitions mirror SKILL.md table-v2 grammar:

  OP  data.operation
  PR  data.provider.id (or the bare string provider, or '')
  H   set of normalized_result.chunks[].handler starting with 'squashfs'
  G   set of normalized_result.extraction_gaps[].kind
  D   union of normalized_result.extraction_gaps[].dependencies
  BE  'yes' if a recorded child command naming sasquatch carries a standalone
      '-be' token, 'no' if such a command exists without it, 'n/a' if no
      sasquatch command is recorded (sources: normalized_result.diagnostics[]
      .report.command, data.diagnostics[].report.command, any 'command' member
      under raw_result)
  SR  'yes' if a MaliciousSymlinkRemoved report typename appears in
      diagnostics or anywhere under raw_result
  P   len(normalized_result.files)

Usage: feature-scan.py --skill SKILL.md RUN_DIR [RUN_DIR ...]
Prints one JSON line per run and a markdown table on stderr.
"""

import argparse
import json
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRIAGE = os.path.join(HERE, 'sqfs-triage-v2.py')


def walk_commands(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == 'command':
                if isinstance(value, str):
                    out.append(value)
                elif isinstance(value, list):
                    out.append(' '.join(str(v) for v in value))
            else:
                walk_commands(value, out)
    elif isinstance(node, list):
        for value in node:
            walk_commands(value, out)


def find_typename(node, want):
    if isinstance(node, dict):
        if node.get('__typename__') == want:
            return True
        return any(find_typename(v, want) for v in node.values())
    if isinstance(node, list):
        return any(find_typename(v, want) for v in node)
    return False


def features(full):
    if not isinstance(full, dict):
        raise SystemExit('no data object')
    data = full.get('data') if isinstance(full.get('data'), dict) else (
        full if ('normalized_result' in full or 'operation' in full) else None)
    if not isinstance(data, dict):
        raise SystemExit('no data object')
    normalized = data.get('normalized_result') or {}
    provider = data.get('provider')
    pr = provider.get('id') if isinstance(provider, dict) else (
        provider if isinstance(provider, str) else '')
    handlers = sorted({c.get('handler') for c in normalized.get('chunks') or []
                       if c.get('handler') and c['handler'].startswith('squashfs')})
    failed = sorted({c.get('handler') for c in normalized.get('chunks') or []
                     if c.get('extraction_failed') and c.get('handler')})
    gaps = normalized.get('extraction_gaps') or []
    kinds = sorted({g.get('kind') for g in gaps if g.get('kind')})
    deps = sorted({d for g in gaps for d in (g.get('dependencies') or [])})

    commands = []
    for diag in normalized.get('diagnostics') or []:
        report = diag.get('report') or {}
        if isinstance(report.get('command'), str):
            commands.append(report['command'])
    for diag in data.get('diagnostics') or []:
        report = diag.get('report') or {}
        if isinstance(report.get('command'), str):
            commands.append(report['command'])
    walk_commands(data.get('raw_result'), commands)
    sasq = [c for c in commands if 'sasquatch' in c]
    if not sasq:
        be = 'n/a'
    elif any('-be' in shlex.split(c) for c in sasq):
        be = 'yes'
    else:
        be = 'no'

    sr = 'yes' if (find_typename(normalized.get('diagnostics'), 'MaliciousSymlinkRemoved')
                   or find_typename(data.get('raw_result'), 'MaliciousSymlinkRemoved')
                   or find_typename(data.get('diagnostics'), 'MaliciousSymlinkRemoved')) else 'no'

    files = [f.get('relative_path') for f in normalized.get('files') or []]
    unpublished = [(u.get('relative_path'), u.get('kind'), u.get('link_target'))
                   for u in normalized.get('unpublished_entries') or []]
    return {
        'OP': data.get('operation'),
        'PR': pr,
        'H': handlers,
        'G': kinds,
        'D': deps,
        'BE': be,
        'SR': sr,
        'P': len(files),
        'failed_chunks': failed,
        'files': files,
        'unpublished': unpublished,
        'depth_limited_paths': normalized.get('depth_limited_paths'),
        'coverage': normalized.get('coverage'),
        'sasquatch_commands': sasq,
    }


def v2_label(skill, envelope_path):
    proc = subprocess.run([sys.executable, '-I', '-B', TRIAGE, '--skill', skill,
                           '--json', envelope_path],
                          capture_output=True, text=True)
    out = (proc.stdout or '').strip()
    rows = []
    try:
        document = json.loads(out) if out else {}
    except json.JSONDecodeError:
        document = {}
    if isinstance(document, dict):
        rows = document.get('results') or []
    return proc.returncode, rows, (proc.stderr or '').strip()[-300:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skill', required=True)
    parser.add_argument('runs', nargs='+')
    args = parser.parse_args()
    table = []
    for run in args.runs:
        path = os.path.join(run, 'stdout.json')
        with open(path, encoding='utf-8') as handle:
            full = json.load(handle)
        feats = features(full)
        code, rows, err = v2_label(args.skill, path)
        row = dict(feats)
        row['run'] = os.path.basename(run.rstrip('/'))
        row['v2_exit'] = code
        row['v2_label'] = rows[0].get('label') if rows else None
        row['v2_action'] = rows[0].get('action') if rows else None
        row['v2_rule'] = rows[0].get('rule') if rows else None
        row['v2_features'] = {k: rows[0].get('features', {}).get(k)
                              for k in ('OP', 'PR', 'H', 'G', 'D', 'BE', 'SR', 'P')} if rows else None
        row['v2_stderr'] = err
        print(json.dumps(row, sort_keys=True))
        table.append(row)
    sys.stderr.write('| run | H | G | D | BE | SR | P | v2 (label, action) |\n')
    sys.stderr.write('| --- | --- | --- | --- | --- | --- | --- | --- |\n')
    for row in table:
        sys.stderr.write('| %s | %s | %s | %s | %s | %s | %s | %s |\n' % (
            row['run'], ','.join(row['H']) or '-', ','.join(row['G']) or '{}',
            ','.join(row['D']) or '{}', row['BE'], row['SR'], row['P'],
            '(%s, %s)' % (row['v2_label'], row['v2_action'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
