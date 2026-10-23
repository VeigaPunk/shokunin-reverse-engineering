#!/usr/bin/env python3
"""Run only the frozen comparator with an explicit text control; preserve receipts."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlAllFalse')
HERE = Path(__file__).resolve().parent
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
READER = HERE / 'control-reader.py'
PHASE = sys.argv[1]
if PHASE not in ('pristine', 'mutated', 'restored'):
    raise SystemExit('invalid phase')
if (HERE / (PHASE + '.receipt.json')).exists():
    raise SystemExit('refusing to replace a receipt')
ENV = {key: value for key, value in os.environ.items()
       if not key.startswith(('GIT_', 'PYTHON'))}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C',
           TMPDIR=str(HERE))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def hashes():
    paths = [
        'tools/round-34/version-needs-counter.py',
        'tools/round-34/elf-version-needs.py',
        'tools/round-34/freeze-integrity.py',
        '.ufo/waves/round-34/claims.json',
        '.ufo/waves/round-34/expected.json',
    ]
    return {path: sha((ROOT / path).read_bytes()) for path in paths}

reader_bytes = READER.read_bytes()
(HERE / (PHASE + '.reader.py')).write_bytes(reader_bytes)
revision_command = ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false',
                    '-C', str(ROOT), 'rev-parse', 'HEAD']
revision = subprocess.run(revision_command, env=ENV, capture_output=True,
                          timeout=10, check=True)
argv = ['/usr/bin/python3', '-I', '-B',
        str(ROOT / 'tools/round-34/version-needs-counter.py'),
        '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE,
        '--control-reader', str(READER)]
receipt = {
    'phase': PHASE, 'utc_start': utc(), 'argv': argv, 'cwd': str(ROOT),
    'measured_revision_command': revision_command,
    'measured_revision_stdout': revision.stdout.decode(),
    'measured_revision_stderr': revision.stderr.decode(),
    'measured_revision_exit': revision.returncode,
    'freeze_revision': FREEZE, 'reader_before_sha256': sha(reader_bytes),
    'source_before_sha256': hashes(), 'counter_timeout_seconds': 145,
    'resource_limits': {name: list(resource.getrlimit(getattr(resource, name)))
                        for name in ('RLIMIT_AS', 'RLIMIT_NPROC', 'RLIMIT_NOFILE',
                                     'RLIMIT_FSIZE', 'RLIMIT_CPU')},
    'launch_argv': [
        'env', '-u', 'GIT_DIR', '-u', 'GIT_WORK_TREE', '-u', 'GIT_INDEX_FILE',
        '/usr/bin/timeout', '--signal=TERM', '--kill-after=5s', '160s',
        '/usr/bin/prlimit', '--as=536870912', '--nproc=2048', '--nofile=128',
        '--fsize=16777216', '--cpu=120', '/usr/bin/python3', '-I', '-B',
        str(Path(__file__).resolve()), PHASE],
}
process = subprocess.Popen(argv, cwd=ROOT, env=ENV, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, start_new_session=True)
def terminate_group(signum=None, frame=None):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    if signum is not None:
        raise SystemExit(128 + signum)

signal.signal(signal.SIGTERM, terminate_group)
signal.signal(signal.SIGINT, terminate_group)
try:
    stdout, stderr = process.communicate(timeout=145)
    receipt['timed_out'] = False
except subprocess.TimeoutExpired:
    terminate_group()
    stdout, stderr = process.communicate()
    receipt['timed_out'] = True
finally:
    terminate_group()
    process.wait()
receipt.update(utc_end=utc(), exit=process.returncode,
               stdout_sha256=sha(stdout), stderr_sha256=sha(stderr),
               stdout_bytes=len(stdout), stderr_bytes=len(stderr),
               reader_after_sha256=sha(READER.read_bytes()),
               source_after_sha256=hashes())
(HERE / (PHASE + '.stdout.json')).write_bytes(stdout)
(HERE / (PHASE + '.stderr.txt')).write_bytes(stderr)
try:
    result = json.loads(stdout)
    receipt['summary'] = {key: result.get(key) for key in
                          ('predicate', 'mode', 'measured_revision', 'freeze_revision',
                           'reader_sha256', 'matched', 'target', 'met_target',
                           'documents_ok', 'finding')}
    receipt['rows'] = [
        {'id': row['id'], 'matched': row['matched'],
         'attempts': [{'schedule': attempt['schedule'],
                       'exit': attempt.get('exit'), 'matched': attempt['matched'],
                       'observed': attempt.get('observed'),
                       'stderr': attempt.get('stderr', '')}
                      for attempt in row['attempts']]}
        for row in result.get('rows', [])]
except (ValueError, KeyError, TypeError) as error:
    receipt['receipt_parse_error'] = str(error)
(HERE / (PHASE + '.receipt.json')).write_text(
    json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({key: receipt.get(key) for key in
                  ('phase', 'utc_start', 'utc_end', 'exit', 'timed_out', 'summary',
                   'reader_before_sha256', 'reader_after_sha256',
                   'stdout_sha256', 'stderr_sha256')}, sort_keys=True))
