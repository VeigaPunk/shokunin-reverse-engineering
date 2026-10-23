#!/usr/bin/env python3
"""Capture one assigned empty-reader control; never import or run the production reader."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlDoNothing')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlDoNothing-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
COUNTER = ROOT / 'tools/round-34/version-needs-counter.py'
CONTROL = OUT / 'empty-reader.py'
CLAIMS = ROOT / '.ufo/waves/round-34/claims.json'


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def store(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


contract = json.loads(CLAIMS.read_bytes())
pins = dict(contract['instruments'])
pins.update(contract['frozen_inputs'])
paths = sorted(set(pins) | {'.ufo/waves/round-34/claims.json', 'SKILL.md', 'corpus/SOURCES.md'})


def snapshot():
    result = {}
    for path in paths:
        data = (ROOT / path).read_bytes()
        result[path] = {'sha256': sha(data), 'size': len(data)}
    data = CONTROL.read_bytes()
    result[str(CONTROL.relative_to(ROOT))] = {'sha256': sha(data), 'size': len(data)}
    return result


before = snapshot()
store('before-hashes.json', {'utc': utc(), 'files': before})
if any(before[path]['sha256'] != expected for path, expected in pins.items()):
    raise RuntimeError('Frozen working-copy bytes do not match claims; detector not invoked')
for name, path in [('frozen-counter.py', COUNTER), ('frozen-claims.json', CLAIMS), ('frozen-expected.json', ROOT / contract['manifest'])]:
    (OUT / name).write_bytes(path.read_bytes())
argv = [
    '/usr/bin/timeout', '--signal=TERM', '--kill-after=5s', '150s',
    sys.executable, '-I', '-B', str(COUNTER),
    '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE,
    '--control-reader', str(CONTROL),
]
env = {key: value for key, value in os.environ.items() if not key.startswith(('GIT_', 'PYTHON'))}
env['GIT_CONFIG_NOSYSTEM'] = '1'
env['GIT_CONFIG_GLOBAL'] = os.devnull
env['LC_ALL'] = 'C'
started = utc()
proc = None
stdout = b''
stderr = b''
exit_code = None
capture_error = None
forced_group_cleanup = False
try:
    proc = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=160)
    except subprocess.TimeoutExpired:
        capture_error = 'capture_deadline_160s'
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate(timeout=5)
    exit_code = proc.returncode
except Exception as error:
    capture_error = type(error).__name__ + ': ' + str(error)
finally:
    if proc is not None:
        try:
            os.killpg(proc.pid, 0)
        except ProcessLookupError:
            pass
        else:
            forced_group_cleanup = True
            os.killpg(proc.pid, signal.SIGKILL)
            if proc.poll() is None:
                proc.wait(timeout=5)
    ended = utc()
    after = snapshot()
    store('after-hashes.json', {'utc': utc(), 'files': after})
    store('restoration.json', {
        'utc': utc(), 'frozen_files_modified': False if before == after else None,
        'all_before_after_equal': before == after,
        'pin_matches_before': all(before[path]['sha256'] == expected for path, expected in pins.items()),
        'pin_matches_after': all(after[path]['sha256'] == expected for path, expected in pins.items()),
        'restoration_action': 'None: control substitution uses --control-reader; no frozen file overwritten.',
        'before': before, 'after': after,
    })
    (OUT / 'counter.stdout.json').write_bytes(stdout)
    (OUT / 'counter.stderr.txt').write_bytes(stderr)
    (OUT / 'counter.exit.txt').write_text(str(exit_code) + '\n', encoding='utf-8')
    receipt = {
        'argv': argv, 'argv_shell': shlex.join(argv),
        'capture_orig_argv': sys.orig_argv, 'cwd': str(ROOT),
        'utc_start': started, 'utc_end': ended, 'exit': exit_code,
        'stdout': stdout.decode('utf-8', errors='replace'),
        'stderr': stderr.decode('utf-8', errors='replace'),
        'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr),
        'capture_error': capture_error, 'forced_group_cleanup': forced_group_cleanup,
        'measured_revision': FREEZE, 'freeze_revision': FREEZE,
        'reader_sha256': sha(CONTROL.read_bytes()), 'counter_sha256': sha(COUNTER.read_bytes()),
        'predicate': contract['predicate'], 'target': contract['target'],
        'limits': {'detector_wall_seconds': 150, 'capture_wall_seconds': 160, 'kill_after_seconds': 5,
                   'address_space_bytes': 536870912, 'cpu_seconds': 120,
                   'processes_per_uid': 4096, 'open_files': 128,
                   'child_process_trees': 1, 'reader_invocations': '24, sequential, each counter-bounded to 10s'},
        'scope': 'Assigned text-only empty control. Production reader, expected-author, targets and held items were not executed.',
    }
    store('run-receipt.json', receipt)

result = json.loads(stdout) if stdout else None
summary = {'exit': exit_code, 'capture_error': capture_error, 'utc_start': started, 'utc_end': ended,
           'all_before_after_equal': before == after, 'forced_group_cleanup': forced_group_cleanup}
if result is not None:
    summary.update({key: result.get(key) for key in ('predicate', 'finding', 'mode', 'matched', 'target', 'met_target', 'documents_ok', 'measured_revision', 'freeze_revision', 'reader_sha256')})
    summary['documents'] = result.get('documents')
    summary['carriers'] = [{'id': row['id'], 'matched': row['matched'], 'schedules': [{'schedule': attempt['schedule'], 'exit': attempt.get('exit'), 'matched': attempt['matched'], 'observed': attempt.get('observed'), 'stderr': attempt.get('stderr')} for attempt in row['attempts']]} for row in result.get('rows', [])]
store('summary.json', summary)
print(json.dumps(summary, sort_keys=True))
if capture_error is not None:
    sys.exit(2)
