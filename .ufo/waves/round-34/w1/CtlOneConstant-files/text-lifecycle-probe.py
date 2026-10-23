#!/usr/bin/env python3
"""Record one stage of a bounded fake-TEXT mutation probe; never imports ELF reader."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlOneConstant-files'
stage = sys.argv[1]
if stage not in ('pristine', 'mutated', 'restored'):
    raise SystemExit('unknown lifecycle stage')
reader = OUT / 'text-reader.py'
reader_bytes = reader.read_bytes()
sha = lambda data: hashlib.sha256(data).hexdigest()
if stage == 'pristine':
    (OUT / 'text-reader.pristine.py').write_bytes(reader_bytes)
env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
env.update({'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull})
argv = ['/usr/bin/timeout', '--kill-after=5s', '30s', '/usr/bin/prlimit',
        '--as=536870912', '--nproc=8192', '--cpu=25', '--', '/usr/bin/python3', '-I', '-B',
        'tools/round-34/version-needs-counter.py', '--fixture-spec', str(OUT / 'text-spec.json'),
        '--fixture-reader', str(reader)]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
run = subprocess.run(argv, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=40)
stop = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert len(run.stdout) <= 1048576 and len(run.stderr) <= 1048576
(OUT / ('text-' + stage + '.stdout')).write_bytes(run.stdout)
(OUT / ('text-' + stage + '.stderr')).write_bytes(run.stderr)
(OUT / ('text-reader.' + stage + '.py')).write_bytes(reader_bytes)
receipt = {'stage': stage, 'argv': argv, 'cwd': str(ROOT), 'observed_start_utc': start,
           'observed_end_utc': stop, 'exit': run.returncode, 'stdout_sha256': sha(run.stdout),
           'stderr_sha256': sha(run.stderr), 'reader_before_sha256': sha(reader_bytes),
           'reader_after_sha256': sha(reader.read_bytes()),
           'counter_sha256': sha((ROOT / 'tools/round-34/version-needs-counter.py').read_bytes()),
           'fixture_sha256': sha((OUT / 'text-fixture.txt').read_bytes()),
           'spec_sha256': sha((OUT / 'text-spec.json').read_bytes()),
           'measured_revision': '54a87a51a865ab931fd355e767303337b05cccf4',
           'source_restored_exactly': (reader.read_bytes() == (OUT / 'text-reader.pristine.py').read_bytes())}
(OUT / ('text-' + stage + '.receipt.json')).write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps(receipt, sort_keys=True))
print(run.stdout.decode(), end='')
if run.stderr:
    print(run.stderr.decode(), file=sys.stderr, end='')
