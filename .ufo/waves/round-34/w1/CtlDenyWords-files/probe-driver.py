import asyncio
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import time
from datetime import datetime, timezone

SANDBOX = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlDenyWords')
EVIDENCE = SANDBOX / '.ufo/waves/round-34/w1/CtlDenyWords-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
ACTIVE = EVIDENCE / 'active-reader.py'
PINNED = [
    'tools/round-34/version-needs-counter.py',
    'tools/round-34/elf-version-needs.py',
    '.ufo/waves/round-34/claims.json',
    '.ufo/waves/round-34/expected.json',
]

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def input_hashes():
    return {path: sha256((SANDBOX / path).read_bytes()) for path in PINNED}

async def probe_control(phase, expected_stdout):
    argv = [shutil.which('timeout'), '--signal=TERM', '--kill-after=3s', '150s',
            shutil.which('prlimit'), '--as=1073741824', '--cpu=90',
            '--fsize=16777216', '--nofile=128', '--nproc=4096', '--core=0',
            shutil.which('python3'), '-I', '-B',
            'tools/round-34/version-needs-counter.py', '--root', str(SANDBOX),
            '--rev', FREEZE, '--freeze', FREEZE, '--control-reader', str(ACTIVE)]
    if any(value is None for value in argv):
        raise RuntimeError('missing_required_runtime_or_resource_limiter')
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_') and not key.startswith('PYTHON')}
    environment.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'LC_ALL': 'C'})
    before = input_hashes()
    active_before = sha256(ACTIVE.read_bytes())
    started = datetime.now(timezone.utc).isoformat()
    monotonic = time.monotonic()
    process = None
    timed_out = False
    try:
        process = subprocess.Popen(argv, cwd=SANDBOX, env=environment,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=160)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate(timeout=5)
    finally:
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    finished = datetime.now(timezone.utc).isoformat()
    duration = time.monotonic() - monotonic
    result = None
    decode_error = None
    try:
        result = json.loads(stdout)
    except (UnicodeError, ValueError) as error:
        decode_error = repr(error)
    rows = result.get('rows', []) if isinstance(result, dict) else []
    attempts = [attempt for row in rows for attempt in row.get('attempts', [])]
    stdout_expected_hash = sha256(expected_stdout.encode())
    summary = {
        'matched': result.get('matched') if isinstance(result, dict) else None,
        'target': result.get('target') if isinstance(result, dict) else None,
        'met_target': result.get('met_target') if isinstance(result, dict) else None,
        'documents_ok': result.get('documents_ok') if isinstance(result, dict) else None,
        'mode': result.get('mode') if isinstance(result, dict) else None,
        'finding': result.get('finding') if isinstance(result, dict) else None,
        'measured_revision': result.get('measured_revision') if isinstance(result, dict) else None,
        'freeze_revision': result.get('freeze_revision') if isinstance(result, dict) else None,
        'carrier_count': len(rows), 'attempt_count': len(attempts),
        'attempts_matched': sum(attempt.get('matched') is True for attempt in attempts),
        'attempts_exit_zero': sum(attempt.get('exit') == 0 for attempt in attempts),
        'attempts_valid_json_strings': sum(isinstance(attempt.get('observed'), str) for attempt in attempts),
        'attempts_stdout_exact': sum(attempt.get('stdout_sha256') == stdout_expected_hash for attempt in attempts),
        'attempts_empty_stderr': sum(attempt.get('stderr') == '' for attempt in attempts),
        'renamed_attempts': sum(attempt.get('string_translation') is not None for attempt in attempts),
    }
    receipt = {
        'phase': phase, 'observed_start_utc': started, 'observed_end_utc': finished,
        'duration_seconds': duration, 'argv': argv, 'shell_rendering': shlex.join(argv),
        'cwd': str(SANDBOX), 'exit': process.returncode, 'harness_timeout': timed_out,
        'environment_policy': 'Remove all GIT_* and PYTHON* variables, then GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, LC_ALL=C; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE absent.',
        'stdout': {'file': phase + '.stdout', 'bytes': len(stdout), 'sha256': sha256(stdout)},
        'stderr': {'file': phase + '.stderr', 'bytes': len(stderr), 'sha256': sha256(stderr)},
        'expected_reader_stdout_sha256': stdout_expected_hash,
        'active_reader_before_sha256': active_before,
        'active_reader_after_sha256': sha256(ACTIVE.read_bytes()),
        'pinned_before_sha256': before, 'pinned_after_sha256': input_hashes(),
        'json_decode_error': decode_error, 'observed': summary,
        'child_process_group_cleanup': 'SIGKILL attempted in finally; no background child retained.'
    }
    if len(stdout) > 2097152 or len(stderr) > 1048576:
        raise RuntimeError('bounded_control_receipt_size_exceeded')
    await asyncio.gather(
        tool.write({'i': 'Retaining detector stdout bytes', 'path': str(EVIDENCE / (phase + '.stdout')), 'content': stdout.decode('utf-8')}),
        tool.write({'i': 'Retaining detector stderr bytes', 'path': str(EVIDENCE / (phase + '.stderr')), 'content': stderr.decode('utf-8')}),
        tool.write({'i': 'Retaining bounded detector receipt', 'path': str(EVIDENCE / (phase + '.receipt.json')), 'content': json.dumps(receipt, indent=2) + '\n'}),
    )
    return receipt
