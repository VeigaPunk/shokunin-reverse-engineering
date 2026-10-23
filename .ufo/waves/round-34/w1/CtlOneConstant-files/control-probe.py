#!/usr/bin/env python3
"""Bound one frozen counter invocation using only the constant --control-reader."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlOneConstant-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
CLAIMS = '.ufo/waves/round-34/claims.json'
COUNTER = 'tools/round-34/version-needs-counter.py'
CONTROL = OUT / 'constant-reader.py'
ENV = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
ENV.update({'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull})
contract = json.loads((ROOT / CLAIMS).read_bytes())
manifest = json.loads((ROOT / contract['manifest']).read_bytes())
selected = json.loads((OUT / 'selected-expected.json').read_bytes())
paths = sorted(set([CLAIMS, 'SKILL.md', 'corpus/SOURCES.md', COUNTER]
                   + list(contract['instruments']) + list(contract['frozen_inputs'])))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def snapshot():
    return {path: sha((ROOT / path).read_bytes()) for path in paths}

before = snapshot()
(OUT / 'before-sha256.json').write_text(json.dumps(before, sort_keys=True, indent=2) + '\n')
# Retain only text instrument/fixture bytes; never author or execute an ELF fixture.
for name, path in [('counter.py', COUNTER), ('claims.json', CLAIMS), ('expected.json', contract['manifest'])]:
    (OUT / ('frozen-' + name)).write_bytes((ROOT / path).read_bytes())
ARGV = ['/usr/bin/timeout', '--kill-after=5s', '160s', '/usr/bin/prlimit',
        '--as=536870912', '--nproc=8192', '--cpu=120', '--',
        '/usr/bin/python3', '-I', '-B', COUNTER,
        '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE,
        '--control-reader', str(CONTROL)]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
run = subprocess.run(ARGV, cwd=ROOT, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=170)
stop = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert len(run.stdout) <= 1048576 and len(run.stderr) <= 1048576
(OUT / 'control.stdout').write_bytes(run.stdout)
(OUT / 'control.stderr').write_bytes(run.stderr)
result = json.loads(run.stdout)
after = snapshot()
(OUT / 'after-sha256.json').write_text(json.dumps(after, sort_keys=True, indent=2) + '\n')
receipt = {'argv': ARGV, 'cwd': str(ROOT), 'observed_start_utc': start, 'observed_end_utc': stop,
           'exit': run.returncode, 'stdout_sha256': sha(run.stdout), 'stderr_sha256': sha(run.stderr),
           'freeze_revision': FREEZE, 'measured_revision': result.get('measured_revision'),
           'constant_reader_sha256': sha(CONTROL.read_bytes()),
           'selected_expected_carriers': [row['id'] for row in manifest['carriers'] if row['expected'] == selected],
           'source_bytes_unchanged': before == after,
           'changed_paths': [path for path in paths if before[path] != after[path]],
           'production_reader_executed': False,
           'control_source': CONTROL.read_text(),
           'predicate': contract['predicate']}
(OUT / 'control.receipt.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
schedules = [{'id': row['id'], 'row_matched': row['matched'], **attempt}
             for row in result.get('rows', []) for attempt in row['attempts']]
(OUT / 'all-schedules.json').write_text(json.dumps(schedules, sort_keys=True, indent=2) + '\n')
print(json.dumps(receipt, sort_keys=True))
print(json.dumps({key: value for key, value in result.items() if key not in ('rows', 'documents')}, sort_keys=True))
print(json.dumps({'schedules': [{'id': row['id'], 'row_matched': row['matched'],
                               'attempts': [{'schedule': a['schedule'], 'exit': a.get('exit'), 'matched': a['matched'],
                                             'string_translation_present': a.get('string_translation') is not None}
                                            for a in row['attempts']]} for row in result.get('rows', [])]}, sort_keys=True))
