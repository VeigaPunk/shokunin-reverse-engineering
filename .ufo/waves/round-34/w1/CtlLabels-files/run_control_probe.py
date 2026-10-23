#!/usr/bin/env python3
"""Run only frozen --control-reader, preserving exact streams and both schedules."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlLabels')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlLabels-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
COUNTER = ROOT / 'tools/round-34/version-needs-counter.py'
CONTROL = OUT / 'label_lookup.py'
phase = sys.argv[1]
if phase not in ('pristine', 'mutated', 'restored'):
    raise SystemExit('unknown_phase')
env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def capture(argv, seconds):
    before = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    process = subprocess.Popen(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    expired = False
    try:
        stdout, stderr = process.communicate(timeout=seconds)
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
    return {'argv': argv, 'cwd': str(ROOT), 'observed_utc': before,
            'finished_utc': datetime.now(timezone.utc).isoformat(),
            'elapsed_seconds': time.monotonic() - start,
            'exit': process.returncode, 'outer_timeout': expired,
            'process_group_cleanup': cleanup,
            'stdout': stdout.decode('utf-8', errors='replace'),
            'stderr': stderr.decode('utf-8', errors='replace'),
            'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr)}


build = json.loads((OUT / 'build-receipt.json').read_bytes())
control_bytes = CONTROL.read_bytes()
if len(control_bytes) > 131072:
    raise RuntimeError('control_source_bound')
if digest(COUNTER.read_bytes()) != build['counter_sha256']:
    raise RuntimeError('running_counter_differs')
(OUT / ('label_lookup.' + phase + '.py')).write_bytes(control_bytes)
argv = ['timeout', '--signal=TERM', '--kill-after=2s', '35s',
        '/usr/bin/prlimit', '--as=536870912', '--nproc=4096', '--nofile=128',
        '--fsize=4194304', '--cpu=30', '--', '/usr/bin/python3', '-I', '-B',
        str(COUNTER), '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE,
        '--control-reader', str(CONTROL)]
receipt = capture(argv, 40)
receipt.update(kind='frozen_label_control_probe', phase=phase, freeze_revision=FREEZE,
               expected_measured_revision=FREEZE, predicate=build['predicate'],
               reader_mode='control', control_sha256=digest(control_bytes),
               counter_sha256_before=build['counter_sha256'],
               counter_sha256_after=digest(COUNTER.read_bytes()),
               control_sha256_after=digest(CONTROL.read_bytes()),
               resource_bounds={'wall_seconds': 35, 'memory_bytes_per_process': 536870912,
                                'process_limit': 4096, 'own_child_trees_at_a_time': 1,
                                'open_files': 128, 'output_file_bytes': 4194304,
                                'cpu_seconds_per_process': 30})
(OUT / (phase + '.stdout.json')).write_text(receipt['stdout'])
(OUT / (phase + '.stderr.txt')).write_text(receipt['stderr'])
try:
    result = json.loads(receipt['stdout'])
    summary = {'phase': phase, 'exit': receipt['exit'],
               'matched': result.get('matched'), 'target': result.get('target'),
               'met_target': result.get('met_target'), 'finding': result.get('finding'),
               'mode': result.get('mode'), 'documents_ok': result.get('documents_ok'),
               'measured_revision': result.get('measured_revision'),
               'freeze_revision': result.get('freeze_revision'), 'schedules': {}}
    for schedule in (0, 1):
        attempts = [dict(id=row['id'], **attempt)
                    for row in result.get('rows', [])
                    for attempt in row['attempts'] if attempt['schedule'] == schedule]
        diagnostics = [json.loads(attempt['stderr']) for attempt in attempts if 'stderr' in attempt]
        summary['schedules'][str(schedule)] = {
            'attempt_count': len(attempts),
            'matched': sum(attempt['matched'] for attempt in attempts),
            'matched_ids': [a['id'] for a in attempts if a['matched']],
            'reader_exits': [a.get('exit') for a in attempts],
            'label_hits': sum(d['label_hit'] for d in diagnostics),
            'selected_record_ids': sorted({d['record_id'] for d in diagnostics}),
            'translated_inputs': sum(a.get('string_translation') is not None for a in attempts),
            'carrier_argv': [d['argv'] for d in diagnostics]}
    receipt['schedule_inspection'] = summary
except (ValueError, KeyError, TypeError) as error:
    summary = {'phase': phase, 'exit': receipt['exit'], 'inspection_error': str(error)}
    receipt['inspection_error'] = str(error)
(OUT / (phase + '.receipt.json')).write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps(summary, sort_keys=True))
