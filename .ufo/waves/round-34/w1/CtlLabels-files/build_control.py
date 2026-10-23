#!/usr/bin/env python3
"""Build a text-only label lookup from the frozen manifest; never open a carrier."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlLabels')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlLabels-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
COUNTER = 'tools/round-34/version-needs-counter.py'
CLAIMS = '.ufo/waves/round-34/claims.json'
MANIFEST = '.ufo/waves/round-34/expected.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    argv = ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false', '-C', str(ROOT), *args]
    started = datetime.now(timezone.utc).isoformat()
    run = subprocess.run(argv, env=ENV, capture_output=True, timeout=10)
    evidence.append({'argv': argv, 'observed_utc': started, 'exit': run.returncode,
                     'stdout_sha256': digest(run.stdout), 'stdout_size': len(run.stdout),
                     'stderr': run.stderr.decode('utf-8', errors='replace')})
    run.check_returncode()
    return run.stdout


evidence = []
revision = git('rev-parse', 'HEAD').decode().strip()
if revision != FREEZE:
    raise RuntimeError('unexpected_sandbox_revision:' + revision)
claims_bytes = git('show', FREEZE + ':' + CLAIMS)
claims = json.loads(claims_bytes)
manifest_bytes = git('show', FREEZE + ':' + MANIFEST)
counter_bytes = git('show', FREEZE + ':' + COUNTER)
if digest(manifest_bytes) != claims['manifest_sha256']:
    raise RuntimeError('frozen_manifest_digest')
if digest(counter_bytes) != claims['instruments'][COUNTER]:
    raise RuntimeError('frozen_counter_digest')
manifest = json.loads(manifest_bytes)
if len(manifest['carriers']) != 12:
    raise RuntimeError('record_count')
records = {}
aliases = {}
inventory = []
for row in manifest['carriers']:
    record_id = row['id']
    records[record_id] = row['expected']
    names = [record_id, row['path'].rsplit('/', 1)[-1], row['path'],
             row['source_path'], row['source_path'].rsplit('/', 1)[-1]]
    for alias in names:
        if alias in aliases and aliases[alias] != record_id:
            raise RuntimeError('alias_collision:' + alias)
        aliases[alias] = record_id
    inventory.append({'id': record_id, 'aliases': names,
                      'expected_sha256': digest(json.dumps(row['expected'], sort_keys=True).encode()),
                      'needed': len(row['expected']['needed']),
                      'versions': sum(len(x['versions']) for x in row['expected']['needed'])})
source = ('#!/usr/bin/env python3\n'
          '"""Adversarial label-only control: no carrier-content or filesystem lookup."""\n'
          'import json\nimport sys\n\n'
          'RECORDS = ' + repr(records) + '\n\n'
          'ALIASES = ' + repr(aliases) + '\n\n'
          'label = sys.argv[1]\n'
          'record_id = ALIASES.get(label, ALIASES.get(label.rsplit("/", 1)[-1], "e12"))\n'
          'sys.stderr.write(json.dumps({"argv": sys.argv, "label_hit": label in ALIASES or label.rsplit("/", 1)[-1] in ALIASES, "record_id": record_id}, sort_keys=True) + "\\n")\n'
          'print(json.dumps(RECORDS[record_id], sort_keys=True))\n')
if len(source.encode()) > 131072:
    raise RuntimeError('control_source_bound')
OUT.mkdir(parents=True, exist_ok=True)
for name, data in [('claims.freeze.json', claims_bytes), ('manifest.freeze.json', manifest_bytes),
                   ('counter.freeze.py', counter_bytes), ('label_lookup.py', source.encode()),
                   ('label_lookup.pristine.py', source.encode())]:
    (OUT / name).write_bytes(data)
calls = sorted({ast.unparse(node.func) for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call)})
receipt = {'kind': 'label_lookup_control_build', 'axes': ['depth (frozen claim)', 'control discrimination', 'no carrier-content reads', 'bounded cost', 'exact restoration'],
           'observed_utc': datetime.now(timezone.utc).isoformat(), 'root': str(ROOT),
           'freeze_revision': FREEZE, 'measured_revision': revision, 'predicate': claims['predicate'],
           'manifest_sha256': digest(manifest_bytes), 'counter_sha256': digest(counter_bytes),
           'control_sha256': digest(source.encode()), 'record_count': len(records),
           'alias_count': len(aliases), 'inventory': inventory,
           'control_imports': ['json', 'sys'], 'control_calls': calls,
           'carrier_content_reads_by_builder': 0, 'git_reads': evidence,
           'runtime': sys.version, 'tools_installed_or_updated': []}
(OUT / 'build-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({k: receipt[k] for k in ['measured_revision', 'record_count', 'alias_count', 'control_sha256', 'counter_sha256', 'control_calls']}, sort_keys=True))
