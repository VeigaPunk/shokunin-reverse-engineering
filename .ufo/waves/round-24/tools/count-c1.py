#!/usr/bin/env python3
"""R24-C1 packet-capture family counter (frozen before the claim).

Denominator: the four REA6.5.0 catalog verbs that need TShark/capinfos and
read saved captures or the installed dissector registry (T2 below). A verb is
held at REV only when ALL of these hold, read from Git objects of REV:

  * a corpus/knowledge/*.md entry whose first line is `source:` and cites an
    S064+ SOURCES row with tier A/B, status mined, opened >= 2026-10-21 and the
    exact entry path in used-by;
  * the entry text names the verb (round-20 mention pattern) and cites an
    original envelope `.ufo/waves/round-24/evidence/c1/<name>.envelope.json`
    plus an `ev_<64 hex>` id that the envelope carries;
  * the envelope binds through the reviewed round-22 binder (ok:true,
    meta.command == verb, data.operation == verb with underscores, the cited
    evidence id, no refusal anywhere in the tree);
  * the adjacent `<name>.run.json` producer record exists, has exit 0, an argv
    naming rea-agents@6.5.0 and the verb, and stdout byte-identical to the
    envelope blob.

No-harm guards (exit 2 if violated): REA catalog, prior knowledge blobs,
prior SOURCES rows and the round-22/23 evidence trees equal BASE.
Exit 0 = 4/4 held; 1 = incomplete; 2 = could not evaluate.
Also reports the lexical catalog zero-mention set over corpus/knowledge.
Limits: no authentication of producer records; source relevance is manual.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import types

BASE = 'fe10219ec6e92c32b7eb40d83fbcac888756c6c1'
T2 = ('inspect-pcap-client', 'inspect-pcap-capture',
      'inspect-packet-fields', 'inspect-packet-capture')
ROOT = '.ufo/waves/round-24/evidence/c1/'
LEGACY = '.ufo/waves/round-22/tools/count-c1.py'
LEGACY_SHA256 = 'c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879'
CATALOG = '.ufo/waves/round-20/verify/round20/verb-coverage.json'
FROZEN_TREES = ('.ufo/waves/round-22/evidence', '.ufo/waves/round-23/evidence')
MIN_SOURCE = 64
MIN_OPENED = '2026-10-21'
PACKAGE = 'rea-agents@6.5.0'


def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if p.returncode:
        raise ValueError('git_input_unreadable: ' + ' '.join(args[:2]))
    return p.stdout


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def source_rows(text):
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.split('|')]
        if len(cells) == 13 and re.fullmatch(r'S[0-9]{3,}', cells[1]):
            if cells[1] in rows:
                raise ValueError('duplicate_source_id: ' + cells[1])
            rows[cells[1]] = cells
    return rows


def knowledge_blobs(root, ref):
    out = git(root, 'ls-tree', '-r', '-z', '--full-tree', ref, '--', 'corpus/knowledge/')
    blobs = {}
    for entry in out.split(b'\0'):
        if entry:
            meta, _, path = entry.partition(b'\t')
            mode, kind, digest = meta.split()
            blobs[path.decode('utf-8')] = (mode, kind, digest)
    return blobs


def no_refusal(r21, node):
    pending = [node]
    while pending:
        node = pending.pop()
        if isinstance(node, list):
            pending.extend(node)
        elif isinstance(node, dict):
            if ('ok' in node and node['ok'] is not True) or r21.refused(node):
                return False
            pending.extend(node.values())
    return True


def producer_ok(root, rev, run_path, envelope_blob, verb, regular):
    if run_path not in regular:
        return 'run_record_missing'
    try:
        run = json.loads(git(root, 'show', rev + ':' + run_path).decode('utf-8'))
    except (ValueError, UnicodeError):
        return 'run_record_invalid'
    if not isinstance(run, dict) or run.get('exit') != 0 or type(run.get('exit')) is not int:
        return 'run_exit_nonzero'
    argv = run.get('argv')
    if not isinstance(argv, list) or PACKAGE not in argv or verb not in argv:
        return 'run_argv_mismatch'
    stdout = run.get('stdout')
    if not isinstance(stdout, str) or stdout.encode('utf-8') != envelope_blob:
        return 'run_stdout_differs'
    return None


def measure(root, revision):
    if git(root, 'rev-parse', '--show-prefix').strip():
        raise ValueError('root_not_repository_top')
    rev = git(root, 'rev-parse', '--verify', '--end-of-options', revision + '^{commit}').decode().strip()
    legacy = git(root, 'show', rev + ':' + LEGACY)
    if hashlib.sha256(legacy).hexdigest() != LEGACY_SHA256:
        raise ValueError('legacy_source_untrusted')
    if git(root, 'show', rev + ':' + CATALOG) != git(root, 'show', BASE + ':' + CATALOG):
        raise ValueError('catalog_changed')
    for tree in FROZEN_TREES:
        if git(root, 'rev-parse', rev + ':' + tree) != git(root, 'rev-parse', BASE + ':' + tree):
            raise ValueError('historical_evidence_changed: ' + tree)
    old_rows = list(source_rows(git(root, 'show', BASE + ':corpus/SOURCES.md').decode('utf-8')).values())
    rows = source_rows(git(root, 'show', rev + ':corpus/SOURCES.md').decode('utf-8'))
    if list(rows.values())[:len(old_rows)] != old_rows:
        raise ValueError('historical_sources_changed')
    current = knowledge_blobs(root, rev)
    if any(current.get(path) != meta for path, meta in knowledge_blobs(root, BASE).items()):
        raise ValueError('historical_knowledge_changed')
    with tempfile.TemporaryDirectory(prefix='kaidoku-r24-c1-') as directory:
        path = Path(directory) / 'r22.py'
        path.write_bytes(legacy)
        r22 = load(path, 'reviewed_r22_counter')
        r21, r20 = r22.revision_helpers(root, rev)
    try:
        regular = dict(r20.tree_entries(root, rev))
    except r20.Refusal as error:
        raise ValueError(str(error)) from error
    catalog = r21.decode(git(root, 'show', rev + ':' + CATALOG).decode('utf-8'))['cli_commands']
    if any(verb not in catalog for verb in T2):
        raise ValueError('denominator_not_in_catalog')
    cited = re.compile(r'(?<![/A-Za-z0-9_.-])' + re.escape(ROOT) + r'[A-Za-z0-9._/-]+')
    targets = {verb: {'held': [], 'rejected': []} for verb in T2}
    mentioned = set()
    for entry in sorted(p for p in regular if p.startswith('corpus/knowledge/')):
        text = git(root, 'show', rev + ':' + entry).decode('utf-8')
        mentioned.update(v for v in catalog if r20.command_pattern(v).search(text))
        first = text.partition('\n')[0]
        if not first.startswith('source:'):
            continue
        eligible = any(
            sid in rows and int(sid[1:]) >= MIN_SOURCE and rows[sid][4] in ('A', 'B')
            and rows[sid][8] == 'mined' and rows[sid][9] >= MIN_OPENED
            and entry in [x.strip() for x in rows[sid][11].split(',')]
            for sid in re.findall(r'\bS[0-9]{3,}\b', first))
        if not eligible:
            continue
        ids = sorted(set(r20.HEX64.findall(text)))
        for evidence_path in sorted(set(cited.findall(text))):
            if not evidence_path.endswith('.envelope.json'):
                continue
            if '..' in evidence_path.split('/'):
                raise ValueError('evidence_path_invalid')
            if evidence_path not in regular:
                continue
            blob = git(root, 'show', rev + ':' + evidence_path)
            decoded = blob.decode('utf-8')
            run_path = evidence_path[:-len('.envelope.json')] + '.run.json'
            for verb in T2:
                if not r20.command_pattern(verb).search(text):
                    continue
                for eid in ids:
                    if eid not in decoded:
                        continue
                    record = {'entry': entry, 'evidence_id': eid, 'path': evidence_path}
                    try:
                        envelope = r21.decode(decoded)
                    except ValueError:
                        targets[verb]['rejected'].append(dict(record, reason='envelope_unparseable'))
                        continue
                    if not no_refusal(r21, envelope):
                        targets[verb]['rejected'].append(dict(record, reason='refusal_in_tree'))
                        continue
                    if r22.bind_cli(r21, decoded, verb, eid) != 0:
                        targets[verb]['rejected'].append(dict(record, reason='unbound'))
                        continue
                    problem = producer_ok(root, rev, run_path, blob, verb, regular)
                    if problem:
                        targets[verb]['rejected'].append(dict(record, reason=problem))
                        continue
                    targets[verb]['held'].append(record)
    held = [verb for verb in T2 if targets[verb]['held']]
    zero = [verb for verb in catalog if verb not in mentioned]
    return {'claim': 'R24-C1', 'rev': rev, 'base': BASE, 't2': list(T2),
            't2_held': held, 't2_held_count': len(held), 't2_total': len(T2),
            'finding': 'c1_complete' if len(held) == len(T2) else 'c1_incomplete',
            'targets': targets, 'catalog_total': len(catalog),
            'catalog_zero_count': len(zero), 'catalog_zero': zero,
            'limit': 'Git-object reads only; producer records unauthenticated; source relevance manual'}


def main():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_NOSYSTEM='1',
                      GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_COUNT='2',
                      GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
                      GIT_CONFIG_KEY_1='core.attributesFile', GIT_CONFIG_VALUE_1='/dev/null')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev', required=True)
    a = p.parse_args()
    try:
        result = measure(a.root.resolve(), a.rev)
        code = 0 if result['t2_held_count'] == len(T2) else 1
    except (OSError, ValueError, UnicodeError, RecursionError, KeyError, RuntimeError) as error:
        result, code = {'claim': 'R24-C1', 'finding': 'unevaluable', 'error': str(error)}, 2
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
