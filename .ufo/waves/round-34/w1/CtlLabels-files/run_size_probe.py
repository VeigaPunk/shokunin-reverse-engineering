#!/usr/bin/env python3
"""Record the same frozen --control-reader score for size replay bytes in three states."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlLabels')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlLabels-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
COUNTER = ROOT / 'tools/round-34/version-needs-counter.py'
CONTROL = OUT / 'size_lookup.py'
phase = sys.argv[1]
if phase not in ('pristine', 'mutated', 'restored'):
    raise SystemExit('unknown_phase')
env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C')


def digest(data):
    return hashlib.sha256(data).hexdigest()


claims = json.loads((OUT / 'claims.freeze.json').read_bytes())
expected_counter = claims['instruments']['tools/round-34/version-needs-counter.py']
control_bytes = CONTROL.read_bytes()
if len(control_bytes) > 131072 or digest(COUNTER.read_bytes()) != expected_counter:
    raise RuntimeError('source_bound_or_counter_pin')
(OUT / ('size_lookup.' + phase + '.py')).write_bytes(control_bytes)
argv = ['timeout', '--signal=TERM', '--kill-after=2s', '35s',
        '/usr/bin/prlimit', '--as=536870912', '--nproc=4096', '--nofile=128',
        '--fsize=4194304', '--cpu=30', '--', '/usr/bin/python3', '-I', '-B',
        str(COUNTER), '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE,
        '--control-reader', str(CONTROL)]
started = datetime.now(timezone.utc).isoformat()
start = time.monotonic()
process = subprocess.Popen(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
expired = False
try:
    stdout, stderr = process.communicate(timeout=40)
except subprocess.TimeoutExpired:
    expired = True
    os.killpg(process.pid, signal.SIGKILL)
    stdout, stderr = process.communicate(timeout=3)
finally:
    try:
        os.killpg(process.pid, signal.SIGKILL)
        cleanup = 'remaining_owned_group_killed'
    except ProcessLookupError:
        cleanup = 'owned_process_group_absent'
receipt = {'kind': 'frozen_size_replay_control_probe', 'phase': phase, 'argv': argv,
           'cwd': str(ROOT), 'observed_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
           'elapsed_seconds': time.monotonic() - start, 'exit': process.returncode,
           'outer_timeout': expired, 'process_group_cleanup': cleanup,
           'stdout': stdout.decode('utf-8', errors='replace'), 'stderr': stderr.decode('utf-8', errors='replace'),
           'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr),
           'predicate': claims['predicate'], 'expected_measured_revision': FREEZE, 'freeze_revision': FREEZE,
           'control_sha256': digest(control_bytes), 'control_sha256_after': digest(CONTROL.read_bytes()),
           'counter_sha256_before': expected_counter, 'counter_sha256_after': digest(COUNTER.read_bytes()),
           'resource_bounds': {'wall_seconds': 35, 'memory_bytes_per_process': 536870912,
                               'process_limit': 4096, 'own_child_trees_at_a_time': 1, 'open_files': 128,
                               'output_file_bytes': 4194304, 'cpu_seconds_per_process': 30}}
(OUT / ('size-' + phase + '.stdout.json')).write_bytes(stdout)
(OUT / ('size-' + phase + '.stderr.txt')).write_bytes(stderr)
try:
    result = json.loads(stdout)
    summary = {key: result.get(key) for key in ['matched', 'target', 'met_target', 'finding', 'documents_ok',
                                               'mode', 'measured_revision', 'freeze_revision']}
    summary.update(phase=phase, exit=process.returncode, schedules={})
    for schedule in (0, 1):
        attempts = [dict(id=row['id'], **attempt) for row in result.get('rows', [])
                    for attempt in row['attempts'] if attempt['schedule'] == schedule]
        diagnostics = [json.loads(attempt['stderr']) for attempt in attempts if 'stderr' in attempt]
        summary['schedules'][str(schedule)] = {
            'attempt_count': len(attempts), 'matched': sum(a['matched'] for a in attempts),
            'matched_ids': [a['id'] for a in attempts if a['matched']],
            'reader_exits': [a.get('exit') for a in attempts],
            'translated_inputs': sum(a.get('string_translation') is not None for a in attempts),
            'fixed_slice_reads': sum(d['fixed_slice_reads'] for d in diagnostics),
            'fixed_slice_bytes': sum(d['fixed_slice_bytes'] for d in diagnostics),
            'diagnostics': diagnostics}
    receipt['schedule_inspection'] = summary
except (ValueError, KeyError, TypeError) as error:
    summary = {'phase': phase, 'exit': process.returncode, 'inspection_error': str(error)}
    receipt['inspection_error'] = str(error)
(OUT / ('size-' + phase + '.receipt.json')).write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
compact = {key: value for key, value in summary.items() if key != 'schedules'}
compact['schedules'] = {schedule: {key: value for key, value in item.items() if key != 'diagnostics'}
                        for schedule, item in summary.get('schedules', {}).items()}
print(json.dumps(compact, sort_keys=True))
