#!/usr/bin/env python3
"""R23 cumulative T1 counter; original R22 binding policy is reused unchanged.

Two fixed evidence roots, one frozen six-verb denominator. New witnesses also
need an S058+ mined A/B row opened2026-10-21 with the exact entry in used-by.
Historical witnesses are measured at the frozen baseline, never extended by
new files under the old root. New entries are scanned explicitly and use the
reviewed original-envelope binder. Source relevance/admission remain manual.
0=clean6/6;1=failed/incomplete;2=could-not-evaluate. No authentication claim.
"""
import argparse
import hashlib
import types
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

LEGACY = '.ufo/waves/round-22/tools/count-c1.py'
LEGACY_SHA256 = 'c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879'
ROOTS = ('.ufo/waves/round-22/evidence/c1/', '.ufo/waves/round-23/evidence/c1/')
SELFTEST_MANIFEST_SHA256 = 'c0701915d7129a9b5078899c080cbe8be01cfe8b7381a33819e3866dc220b75f'
BASELINE = 'aa1450b82f9ede35aada63efe8a34e01c6e02f72'
CATALOG = '.ufo/waves/round-20/verify/round20/verb-coverage.json'

def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if p.returncode:
        raise ValueError('git_input_unreadable')
    return p.stdout


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

def bind_new(r22, r21, text, verb, evidence_id):
    # Keep refusal ancestry in metadata/sibling containers as well as data.
    try:
        pending = [r21.decode(text)]
        while pending:
            node = pending.pop()
            if isinstance(node, list):
                pending.extend(node)
            elif isinstance(node, dict):
                if ('ok' in node and node['ok'] is not True) or r21.refused(node):
                    return 1
                pending.extend(node.values())
        return r22.bind_cli(r21, text, verb, evidence_id)
    except (ValueError, RecursionError):
        return 2


def measure(root, revision):
    rev = git(root, 'rev-parse', '--verify', '--end-of-options', revision+'^{commit}').decode().strip()
    legacy = git(root, 'show', rev+':'+LEGACY)
    if hashlib.sha256(legacy).hexdigest() != LEGACY_SHA256:
        raise ValueError('legacy_source_untrusted')
    if git(root, 'show', rev+':'+CATALOG) != git(root, 'show', BASELINE+':'+CATALOG):
        raise ValueError('catalog_changed')
    old_root = ROOTS[0].rstrip('/')
    if git(root, 'rev-parse', rev+':'+old_root) != git(root, 'rev-parse', BASELINE+':'+old_root):
        raise ValueError('historical_evidence_changed')
    old_sources = git(root, 'show', BASELINE+':corpus/SOURCES.md').decode('utf-8')
    new_sources = git(root, 'show', rev+':corpus/SOURCES.md').decode('utf-8')
    source_rows = lambda text: [line for line in text.splitlines() if re.match(r'^\| S[0-9]+ \|', line)]
    if source_rows(new_sources)[:len(source_rows(old_sources))] != source_rows(old_sources):
        raise ValueError('historical_sources_changed')
    def knowledge_blobs(ref):
        entries = git(root, 'ls-tree', '-r', '-z', ref, '--', 'corpus/knowledge/')
        return {entry.partition(b'\t')[2]: (entry.partition(b'\t')[0].split()[0],
                                           entry.partition(b'\t')[0].split()[2])
                for entry in entries.split(b'\0') if entry}
    current_knowledge = knowledge_blobs(rev)
    if any(current_knowledge.get(path) != digest
           for path, digest in knowledge_blobs(BASELINE).items()):
        raise ValueError('historical_knowledge_changed')
    runtime = root / '.ufo/waves/round-23/runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(runtime)
    with tempfile.TemporaryDirectory(prefix='counter-') as directory:
        path = Path(directory) / 'r22.py'
        path.write_bytes(legacy)
        r22 = load(path, 'reviewed_r22_counter')
        historical = r22.measure(root, BASELINE)
        if historical['t1_exercised'] != ['identify-flutter-build']:
            raise ValueError('historical_baseline_changed')
        r21, r20 = r22.revision_helpers(root, rev)
    rows = {}
    for line in git(root, 'show', rev+':corpus/SOURCES.md').decode('utf-8').splitlines():
        cells = [c.strip() for c in line.split('|')]
        if len(cells) == 13 and re.fullmatch(r'S[0-9]{3,}', cells[1]):
            if cells[1] in rows:
                raise ValueError('duplicate_source_id')
            rows[cells[1]] = cells
    targets = {verb: {'historical': historical['targets'][verb]['bound_evidence'], 'new': []}
               for verb in r22.T1}
    try:
        regular_blobs = dict(r20.tree_entries(root, rev))
    except r20.Refusal as error:
        raise ValueError(str(error)) from error
    files = [path for path in regular_blobs if path.startswith('corpus/knowledge/')]
    catalog = r21.decode(git(root, 'show', rev+':'+CATALOG).decode('utf-8'))['cli_commands']
    mentioned = set()
    cited_pattern = re.compile(r'(?<![/A-Za-z0-9_.-])'+re.escape(ROOTS[1])+r'[A-Za-z0-9._/-]+')
    for entry in files:
        text = git(root, 'show', rev+':'+entry).decode('utf-8')
        mentioned.update(verb for verb in catalog if r20.command_pattern(verb).search(text))
        first = text.partition('\n')[0]
        if not first.startswith('source:'):
            continue
        eligible = False
        for sid in re.findall(r'\bS[0-9]{3,}\b', first):
            row = rows.get(sid)
            if row and int(sid[1:]) >= 58 and row[4] in ('A', 'B') and row[8] == 'mined' and row[9] == '2026-10-21' and entry in [x.strip() for x in row[11].split(',')]:
                eligible = True
        if not eligible:
            continue
        ids = sorted(set(r20.HEX64.findall(text)))
        for evidence_path in sorted(set(cited_pattern.findall(text))):
            if not evidence_path.endswith('.json'):
                continue  # Carrier bytes are cited provenance, not JSON Evidence.
            if evidence_path not in regular_blobs:
                continue  # Symlink target text is not an Evidence file.
            # Git fails closed on missing/absolute/traversal citations; no live path reads.
            if '..' in evidence_path.split('/'):
                raise ValueError('evidence_path_invalid')
            blob = git(root, 'show', rev+':'+evidence_path).decode('utf-8')
            for verb in r22.T1:
                if not r20.command_pattern(verb).search(text):
                    continue
                for eid in ids:
                    if eid in blob and bind_new(r22, r21, blob, verb, eid) == 0:
                        targets[verb]['new'].append({'entry': entry, 'evidence_id': eid, 'path': evidence_path})
    for target in targets.values():
        target['exercised'] = bool(target['historical'] or target['new'])
    held = [verb for verb in r22.T1 if targets[verb]['exercised']]
    return {'rev': rev, 'historical_rev': BASELINE, 'claim': 'R23-C1',
            'finding': 'c1_complete' if len(held)==6 else 'c1_incomplete',
            't1': list(r22.T1), 't1_exercised': held, 't1_exercised_count': len(held), 't1_total': 6,
            'targets': targets, 'catalog_mentioned_count': len(mentioned),
            'catalog_total': len(catalog), 'catalog_zero_count': len(catalog)-len(mentioned),
            'limit': 'local original-envelope/source linkage; run stdout checked separately; manual source relevance; no authentication'}


def selftest(root):
    frozen = root / '.ufo/waves/round-23/frozen'
    raw = (frozen/'expected-v3.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != SELFTEST_MANIFEST_SHA256:
        raise ValueError('snapshot_tampered: manifest')
    manifest = json.loads(raw)
    for rel, digest in manifest['inputs'].items():
        if hashlib.sha256((root/rel).read_bytes()).hexdigest() != digest:
            raise ValueError('snapshot_tampered: '+rel)
    fixtures = load(root / '.ufo/waves/round-23/tools/counter-fixtures.py', 'r23_independent_fixtures')
    return fixtures.run(root, Path(__file__).resolve(), manifest)


def main():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
    os.environ.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
                      GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.hooksPath',
                      GIT_CONFIG_VALUE_0='/dev/null')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev')
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    try:
        if a.selftest:
            result, code = selftest(a.root.resolve())
        else:
            if not a.rev:
                raise ValueError('revision_required')
            result = measure(a.root.resolve(), a.rev)
            code = 0 if result['t1_exercised_count'] == 6 else 1
    except (OSError, ValueError, UnicodeError, RecursionError, KeyError, RuntimeError) as error:
        result, code = {'finding': 'unevaluable', 'error': str(error)}, 2
    print(json.dumps(result, sort_keys=True))
    return code

if __name__ == '__main__':
    raise SystemExit(main())
